"""Assert the paper's nine expected answers (section 6.2) against this repository's data.

Usage: python poc/check_answers.py [control.ifc]
       (default: poc/data/duplex-enriched.ifc, the version 1 control file with Pset_NRC* names)

Checks, one line each:
  1. poc/results/expected_answers.json equals what poc/expected_answers.py computes from
     poc/data/nrc_analytics_elements.csv and, for Q9, the toolkit's zone and space tables, for
     all nine questions.
  2. The toolkit's copies of the analytics CSVs and of the source model (bim-open-toolkit/
     samples/nrc) are byte-identical to the ones here, so the toolkit's NrcWorkflows tests,
     which assert the eight answers over those copies, assert them over this data.
  3. Q2, Q4 and Q6 recomputed from the property sets inside the version 1 control file, without
     the CSV, equal the expected answers.
  3b. The same three from the toolkit's regenerated samples/nrc/duplex-enriched.ifc (NRC_*
     names), plus Q7 (the elements with no NRC_EmbodiedCarbon set) and Q9 (the zone with the
     highest NRC_ZoneSummary intensity). The toolkit's own tests assert the same values over
     the CSVs and the Run.
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
from expected_answers import ELEMENTS, OUT as EXPECTED_JSON, SPACES, ZONES, compute, read_csv  # noqa: E402
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
        same = other.exists() and _content(ROOT / ours) == _content(other)
        check(f"toolkit samples/nrc/{theirs} is byte-identical to {ours}", same)


def _content(path: Path) -> bytes:
    """File bytes; for a CSV, with line endings normalised, since a checkout may convert them."""
    data = path.read_bytes()
    return data.replace(b"\r\n", b"\n") if path.suffix == ".csv" else data


def check_from_ifc(ifc: Path, expected: dict, prefix: str = "Pset_NRC", label: str = "the IFC") -> None:
    """Q2, Q4 and Q6 from the property sets of one enriched file. `prefix` is the set-name prefix
    (Pset_NRC in the version 1 control file, NRC_ in the toolkit's file)."""
    entities = read_entities(ifc)
    psets = property_sets(entities)
    storeys = storey_of(entities)

    eui = "EnergyUseIntensity_kWh_per_m2_year"
    by_storey: dict[str, list[float]] = {}
    for eid, sets in psets.items():
        value = sets.get(prefix + "EnergyPerformance", {}).get(eui)
        if value is not None and entities[eid].type not in ("IFCBUILDING", "IFCBUILDINGSTOREY"):
            by_storey.setdefault(storeys.get(eid, "?"), []).append(value)
    means = {s: round(sum(v) / len(v), 2) for s, v in by_storey.items()}
    want = expected["Q2"]["answer"]
    check("Q2 mean energy intensity per storey, from " + label, means == want, f"{means}")
    higher = max(("Level 1", "Level 2"), key=lambda s: means.get(s, float("-inf")))
    check("Q2 Level 2 is the higher, from " + label, higher == "Level 2")

    want = expected["Q4"]["answer"]
    door = next((e for e in entities.values() if e.type == "IFCDOOR" and e.args[0] == want["GlobalId"]), None)
    oc = psets.get(door.id, {}).get(prefix + "OperationalCarbon", {}).get(
        "OperationalCarbon_kgCO2e_per_year") if door else None
    check("Q4 the door with the given GlobalId and its operational carbon, from " + label,
          door is not None and oc == want["value"], f"{oc}")

    provenance_set = prefix + "AnalyticsProvenance"
    provenance = [s[provenance_set] for s in psets.values() if provenance_set in s]
    want = expected["Q6"]["answer"]
    got = {k: provenance[0].get(k) for k in want} if len(provenance) == 1 else None
    check("Q6 run id, time and source tool, from the provenance set of " + label, got == want, f"{got}")
    run_ids = {v.get("AnalysisRunId") for s in psets.values() for name, v in s.items()
               if name.startswith(prefix)}
    check("Q6 every NRC set cites the same run, in " + label, run_ids == {want["AnalysisRunId"]}, f"{run_ids}")

    if prefix == "NRC_":
        check_zone_questions(entities, psets, expected, label)


def check_zone_questions(entities: dict, psets: dict, expected: dict, label: str) -> None:
    """Q7 and Q9 from the toolkit's file: the elements that carry operational carbon but no
    NRC_EmbodiedCarbon set, and the IfcZone whose NRC_ZoneSummary intensity is highest."""
    analysed = [eid for eid, sets in psets.items() if "NRC_OperationalCarbon" in sets]
    missing = sorted(entities[eid].args[0] for eid in analysed if "NRC_EmbodiedCarbon" not in psets[eid])
    want = sorted(row["GlobalId"] for row in expected["Q7"]["answer"])
    check("Q7 elements with no NRC_EmbodiedCarbon set, from " + label, missing == want, f"{missing}")

    key = "ZoneEnergyUseIntensity_kWh_per_m2_year"
    zones = {e.args[2]: psets.get(e.id, {}).get("NRC_ZoneSummary", {}).get(key)
             for e in entities.values() if e.type == "IFCZONE"}
    want = expected["Q9"]["all_zones"]
    check("Q9 intensity of each zone, from " + label, zones == want, f"{zones}")
    top = max(zones, key=lambda z: zones[z] if zones[z] is not None else float("-inf"))
    check("Q9 the highest is " + expected["Q9"]["answer"]["Zone"], top == expected["Q9"]["answer"]["Zone"], top)


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
    expected = compute(read_csv(ELEMENTS), read_csv(ZONES), read_csv(SPACES))
    check_expected_file(expected)
    check_toolkit_copies()
    check_from_ifc(ifc, expected, "Pset_NRC", "the version 1 control file")
    check_from_ifc(TOOLKIT_SAMPLES / "duplex-enriched.ifc", expected, "NRC_", "the toolkit's enriched file")
    check_recorded_run(expected)
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
    failed = sum(not ok for _, ok, _ in results)
    print(f"{len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
