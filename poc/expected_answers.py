"""Compute the expected answer to each question in paper section 6.2 directly from the
synthetic dataset, independently of the IFC file and the MCP server.

Reads:  poc/data/nrc_analytics_elements.csv
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


def num(v: str):
    return None if v == "" else float(v)


def compute(rows: list[dict]) -> dict:
    """The expected answer to each question, from the rows of nrc_analytics_elements.csv."""
    oc = "OperationalCarbon_kgCO2e_per_year"
    eui = "EnergyUseIntensity_kWh_per_m2_year"
    ec = "EmbodiedCarbon_A1A3_kgCO2e"

    by_storey = defaultdict(list)
    for r in rows:
        by_storey[r["Storey"]].append(r)
    by_cat = defaultdict(float)
    for r in rows:
        by_cat[r["Category"]] += num(r[oc])

    top5 = sorted(rows, key=lambda r: -num(r[oc]))[:5]
    door = next(r for r in rows if r["Name"].startswith("M_Single-Flush:0762 x 2032mm"))
    roof = next(r for r in rows if r["IfcType"] == "IFCROOF")

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
            "question": "What is the operational carbon of the door named M_Single-Flush:0762 x 2032mm?",
            "note": "Several doors share this family name; the first by STEP id is used.",
            "answer": {"GlobalId": door["GlobalId"], "Name": door["Name"], "value": num(door[oc])},
            "unit": "kgCO2e/yr",
        },
        "Q5": {
            "question": "How much operational carbon is in each category?",
            "answer": {k: round(v, 1) for k, v in sorted(by_cat.items(), key=lambda kv: -kv[1])},
            "unit": "kgCO2e/yr",
        },
        "Q6": {
            "question": "Which analysis run produced these values, and when?",
            "answer": {"AnalysisRunId": rows[0]["AnalysisRunId"], "ComputedAt": "2026-09-17T00:00:00Z",
                       "SourceTool": "nrc-ifc-llm/poc/generate_synthetic_analytics.py"},
        },
        "Q7": {
            "question": "What is the embodied carbon of the roof?",
            "answer": None,
            "note": f"No Pset_NRCEmbodiedCarbon was written for the roof ({roof['GlobalId']}); "
                    "the correct answer is that the value is not available.",
        },
        "Q8": {
            "question": "What is the total embodied carbon (A1-A3) per storey?",
            "answer": {s: round(sum(num(r[ec]) for r in rs if r[ec] != ""), 1) for s, rs in by_storey.items()},
            "unit": "kgCO2e",
        },
    }
    return expected


def main() -> None:
    expected = compute(list(csv.DictReader(open(ELEMENTS, encoding="utf-8"))))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(expected, indent=2), encoding="utf-8")
    print(json.dumps(expected, indent=2))


if __name__ == "__main__":
    main()
