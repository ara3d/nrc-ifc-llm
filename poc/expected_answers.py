"""Compute the expected answer to each question in paper section 6.2 directly from the
synthetic dataset, independently of the IFC file and the MCP server.

Reads:  poc/data/nrc_analytics_elements.csv and, for the zone question Q9, the toolkit's
        samples/nrc/nrc-zones.csv and nrc_analytics_spaces.csv (through the submodule)
Writes: poc/results/expected_answers.json
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ELEMENTS = ROOT / "poc" / "data" / "nrc_analytics_elements.csv"
OUT = ROOT / "poc" / "results" / "expected_answers.json"
TOOLKIT_SAMPLES = ROOT / "bim-open-toolkit" / "samples" / "nrc"
ZONES = TOOLKIT_SAMPLES / "nrc-zones.csv"
SPACES = TOOLKIT_SAMPLES / "nrc_analytics_spaces.csv"


def num(v: str):
    return None if v == "" else float(v)


def zone_intensities(zones: list[dict], space_rows: list[dict]) -> dict:
    """Energy use intensity of each zone: its spaces' annual energy over their floor area, rounded to
    0.01 kWh/m2/yr, as the question graph nrc-q9-zone-eui computes it. Highest first."""
    zone_of = {z["SpaceGlobalId"]: z["ZoneName"] for z in zones}
    energy, area = defaultdict(float), defaultdict(float)
    for r in space_rows:
        zone = zone_of.get(r["GlobalId"])
        if zone is None:
            continue
        if r["MetricId"] == "NRC.ENERGY.ANNUAL":
            energy[zone] += float(r["Value"])
        elif r["MetricId"] == "NRC.AREA.FLOOR":
            area[zone] += float(r["Value"])
    eui = {z: round(energy[z] / area[z], 2) for z in area}
    return dict(sorted(eui.items(), key=lambda kv: -kv[1]))


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def compute(rows: list[dict], zones: list[dict], space_rows: list[dict]) -> dict:
    """The expected answer to each question: the elements table for Q1 to Q8, the toolkit's zone and
    space tables for Q9."""
    oc = "OperationalCarbon_kgCO2e_per_year"
    eui = "EnergyUseIntensity_kWh_per_m2_year"
    ec = "EmbodiedCarbon_A1A3_kgCO2e"

    by_storey = defaultdict(list)
    for r in rows:
        by_storey[r["Storey"]].append(r)
    by_class = defaultdict(float)
    for r in rows:
        by_class[r["IfcType"]] += num(r[oc])

    top5 = sorted(rows, key=lambda r: -num(r[oc]))[:5]
    door = next(r for r in rows if r["GlobalId"] == "1hOSvn6df7F8_7GcBWlS8Z")
    no_embodied = [r for r in rows if r[ec] == ""]
    zone_eui = zone_intensities(zones, space_rows)
    top_zone = next(iter(zone_eui))

    expected = {
        "Q1": {
            "question": "What is the total operational carbon for the building?",
            "answer": round(sum(num(r[oc]) for r in rows), 1),
            "unit": "kgCO2e/yr",
        },
        "Q2": {
            "question": "Which storey has the higher mean energy intensity, Level 1 or Level 2?",
            "answer": {s: round(sum(num(r[eui]) for r in rs) / len(rs), 2) for s, rs in by_storey.items()},
            "unit": "kWh/m2/yr (mean per storey)",
        },
        "Q3": {
            "question": "Which five elements have the highest operational carbon?",
            "answer": [{"GlobalId": r["GlobalId"], "Name": r["Name"], "value": num(r[oc])} for r in top5],
            "unit": "kgCO2e/yr",
        },
        "Q4": {
            "question": "What is the operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z?",
            "answer": {"GlobalId": door["GlobalId"], "Name": door["Name"], "value": num(door[oc])},
            "unit": "kgCO2e/yr",
        },
        "Q5": {
            "question": "How much operational carbon is stored per IFC class?",
            "answer": {k: round(v, 1) for k, v in sorted(by_class.items(), key=lambda kv: -kv[1])},
            "unit": "kgCO2e/yr",
        },
        "Q6": {
            "question": "Which analysis run produced these values, and when?",
            "answer": {"AnalysisRunId": rows[0]["AnalysisRunId"], "ComputedAt": "2026-09-17T00:00:00Z",
                       "SourceTool": "nrc-ifc-llm/poc/generate_synthetic_analytics.py"},
        },
        "Q7": {
            "question": "Which analysed elements carry no embodied-carbon property set?",
            "answer": [{"GlobalId": r["GlobalId"], "IfcType": r["IfcType"], "Name": r["Name"]} for r in no_embodied],
            "note": "No NRC_EmbodiedCarbon set was written for these elements; the roof is the only one.",
        },
        "Q8": {
            "question": "What is the total embodied carbon (A1-A3) per storey?",
            "answer": {s: round(sum(num(r[ec]) for r in rs if r[ec] != ""), 1) for s, rs in by_storey.items()},
            "unit": "kgCO2e",
        },
        "Q9": {
            "question": "Which zone has the highest energy use intensity?",
            "answer": {"Zone": top_zone, "value": zone_eui[top_zone]},
            "all_zones": zone_eui,
            "unit": "kWh/m2/yr",
        },
    }
    return expected


def main() -> None:
    expected = compute(read_csv(ELEMENTS), read_csv(ZONES), read_csv(SPACES))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(expected, indent=2), encoding="utf-8")
    print(json.dumps(expected, indent=2))


if __name__ == "__main__":
    main()
