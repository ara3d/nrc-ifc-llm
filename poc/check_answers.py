"""Assert the paper's eight expected answers (section 6.2) against this repository's data.

Usage: python poc/check_answers.py [enriched.ifc]
       (default: poc/data/duplex-enriched.ifc)

Checks, one line each:
  1. poc/results/expected_answers.json equals what poc/expected_answers.py computes from
     poc/data/nrc_analytics_elements.csv, for all eight questions.
  2. The toolkit's copies of the analytics CSVs and of the source model (bim-open-toolkit/
     samples/nrc) are byte-identical to the ones here, so the toolkit's NrcWorkflows tests,
     which assert the eight answers over those copies, assert them over this data.
  3. Q2, Q4 and Q6 recomputed from the property sets inside the enriched IFC file, without
     the CSV, equal the expected answers. (The toolkit's CI comment names Q1, Q3, Q5, Q7 and
     Q8; its CsvGraphTests also assert Q2, Q4 and Q6, but over the CSV, not the IFC.)
  4. The recorded unattended language-model run (poc/results/results-unattended.json) states
     the expected values for Q2, Q4 and Q6, the three it answered correctly per paper
     section 6.2. No model is called.

Exit code 0 when every check passes, 1 otherwise. Standard library only.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from expected_answers import ELEMENTS, OUT as EXPECTED_JSON, compute  # noqa: E402
from ifc_step import property_sets, read_entities, storey_of  # noqa: E402

TOOLKIT_SAMPLES = ROOT / "bim-open-toolkit" / "samples" / "nrc"
SHARED_FILES = {
    "poc/data/nrc_analytics_elements.csv": "nrc_analytics_elements.csv",
    "poc/data/nrc_analytics_long.csv": "nrc_analytics_long.csv",
    "poc/data/nrc_analytics_storeys.csv": "nrc_analytics_storeys.csv",
    "IFC-Test-Kit/duplex.ifc": "duplex-base.ifc",
}
RECORDED_RUN = ROOT / "poc" / "results" / "results-unattended.json"

results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))


def check_expected_file(expected: dict) -> None:
    committed = json.loads(EXPECTED_JSON.read_text(encoding="utf-8"))
    for q in sorted(expected):
        check(f"{q} expected_answers.json matches the CSV", committed.get(q) == expected[q])


def check_toolkit_copies() -> None:
    for ours, theirs in SHARED_FILES.items():
        other = TOOLKIT_SAMPLES / theirs
        same = other.exists() and (ROOT / ours).read_bytes() == other.read_bytes()
        check(f"toolkit samples/nrc/{theirs} is byte-identical to {ours}", same)


def check_from_ifc(ifc: Path, expected: dict) -> None:
    entities = read_entities(ifc)
    psets = property_sets(entities)
    storeys = storey_of(entities)

    eui = "EnergyUseIntensity_kWh_per_m2_year"
    by_storey: dict[str, list[float]] = {}
    for eid, sets in psets.items():
        value = sets.get("Pset_NRCEnergyPerformance", {}).get(eui)
        if value is not None and entities[eid].type not in ("IFCBUILDING", "IFCBUILDINGSTOREY"):
            by_storey.setdefault(storeys.get(eid, "?"), []).append(value)
    means = {s: round(sum(v) / len(v), 2) for s, v in by_storey.items()}
    want = expected["Q2"]["answer"]
    check("Q2 mean energy intensity per storey, from the IFC", means == want, f"{means}")
    higher = max(("Level 1", "Level 2"), key=lambda s: means.get(s, float("-inf")))
    check("Q2 Level 2 is the higher, from the IFC", higher == "Level 2")

    doors = sorted(e.id for e in entities.values()
                   if e.type == "IFCDOOR" and str(e.args[2]).startswith("M_Single-Flush:0762 x 2032mm"))
    first = entities[doors[0]] if doors else None
    oc = psets.get(first.id, {}).get("Pset_NRCOperationalCarbon", {}).get(
        "OperationalCarbon_kgCO2e_per_year") if first else None
    want = expected["Q4"]["answer"]
    check("Q4 first door by STEP id and its operational carbon, from the IFC",
          first is not None and first.args[0] == want["GlobalId"] and first.args[2] == want["Name"]
          and oc == want["value"], f"{len(doors)} doors share the name; #{doors[0] if doors else '-'} = {oc}")

    provenance = [s["Pset_NRCAnalyticsProvenance"] for s in psets.values() if "Pset_NRCAnalyticsProvenance" in s]
    want = expected["Q6"]["answer"]
    got = {k: provenance[0].get(k) for k in want} if len(provenance) == 1 else None
    check("Q6 run id, time and source tool, from the IFC provenance set", got == want, f"{got}")
    run_ids = {v.get("AnalysisRunId") for s in psets.values() for name, v in s.items()
               if name.startswith("Pset_NRC")}
    check("Q6 every NRC set cites the same run", run_ids == {want["AnalysisRunId"]}, f"{run_ids}")


def check_recorded_run(expected: dict) -> None:
    answers = [r["answer"] for r in json.loads(RECORDED_RUN.read_text(encoding="utf-8"))]
    q2, q4, q6 = answers[1], answers[3], answers[5]
    levels = expected["Q2"]["answer"]
    numbers = [float(x) for x in re.findall(r"\d+\.\d+", q2)]
    check("Q2 recorded run names Level 2 and the two means",
          q2.startswith("Level 2 has the higher") and
          any(abs(n - levels["Level 1"]) < 0.01 for n in numbers) and
          any(abs(n - levels["Level 2"]) < 0.01 for n in numbers))
    door = expected["Q4"]["answer"]
    stated = re.escape(door["Name"]) + r" \(#\d+\) = " + re.escape(str(door["value"]))
    check("Q4 recorded run gives the first door's value", re.search(stated, q4) is not None)
    run = expected["Q6"]["answer"]
    check("Q6 recorded run gives the run id and time",
          run["AnalysisRunId"] in q6 and run["ComputedAt"] in q6)


def main() -> int:
    ifc = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "poc" / "data" / "duplex-enriched.ifc"
    with open(ELEMENTS, encoding="utf-8") as f:
        expected = compute(list(csv.DictReader(f)))
    check_expected_file(expected)
    check_toolkit_copies()
    check_from_ifc(ifc, expected)
    check_recorded_run(expected)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
    failed = sum(not ok for _, ok, _ in results)
    print(f"{len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
