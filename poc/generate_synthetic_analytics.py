"""Generate a synthetic analytics dataset for duplex.ifc following the paper's
three-layer storage recommendation (paper/03-storage-options.md, Appendix A).

Reads:  IFC-Test-Kit/duplex.ifc, IFC-Test-Kit/analytics_dataset_with_levels.csv
Writes: poc/data/nrc_analytics_elements.csv   Layer 1 values, one row per element (wide)
        poc/data/nrc_analytics_long.csv       Layer 2 table, one row per (run, element, metric)
        poc/data/nrc_analytics_storeys.csv    storey and building aggregates
        poc/data/psets_to_write.csv           rows for the byte-exact writer (entityId, psetName, paramName, valueType, paramValue)

Values are deterministic: each element's embodied carbon is a type-based base value
jittered by a hash of its GlobalId. Operational carbon and energy intensity are taken
from the existing test-kit dataset so the two stay consistent. The roof deliberately
receives no embodied-carbon set (question Q7 in paper section 6.2 tests absence).
"""
from __future__ import annotations

import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IFC = ROOT / "IFC-Test-Kit" / "duplex.ifc"
TESTKIT_CSV = ROOT / "IFC-Test-Kit" / "analytics_dataset_with_levels.csv"
OUT = ROOT / "poc" / "data"

RUN_ID = "run-2026-09-17-01"
SCENARIO = "Baseline"
GRID_FACTOR = 0.11  # kgCO2e per kWh, illustrative

# Embodied carbon A1-A3 base value per element in kgCO2e, by IFC type. Illustrative.
BASE_A1A3 = {
    "IFCWALLSTANDARDCASE": 820.0,
    "IFCWALL": 820.0,
    "IFCSLAB": 2400.0,
    "IFCFOOTING": 950.0,
    "IFCBEAM": 310.0,
    "IFCMEMBER": 120.0,
    "IFCWINDOW": 160.0,
    "IFCDOOR": 95.0,
    "IFCCOVERING": 65.0,
    "IFCRAILING": 70.0,
    "IFCSTAIR": 640.0,
    "IFCSTAIRFLIGHT": 320.0,
    "IFCFURNISHINGELEMENT": 45.0,
    "IFCROOF": 3100.0,
}
SKIP_TYPES = {"IFCOPENINGELEMENT"}  # voids, not physical elements
NO_EMBODIED_TYPES = {"IFCROOF"}  # deliberate absence for Q7


def jitter(global_id: str, spread: float = 0.30) -> float:
    """Deterministic multiplier in [1-spread, 1+spread] from the GlobalId."""
    h = int(hashlib.sha256(global_id.encode()).hexdigest()[:8], 16)
    return 1.0 + spread * ((h / 0xFFFFFFFF) * 2.0 - 1.0)


def parse_ifc(path: Path):
    """Return (guid->step id, guid->type, step id->name, element step id->storey step id).

    Storey is found by walking up containment (element in space or storey) and aggregation
    (stair flight part of stair, space part of storey) until an IFCBUILDINGSTOREY is reached.
    """
    ids, types, names, type_of = {}, {}, {}, {}
    parent = {}
    entity = re.compile(r"#(\d+)=(IFC\w+)\('([^']+)',#\d+,(?:'([^']*)'|\$)")
    contained = re.compile(r"#\d+=IFCRELCONTAINEDINSPATIALSTRUCTURE\('[^']+',#\d+,[^,]*,[^,]*,\(([^)]*)\),#(\d+)\)")
    aggregates = re.compile(r"#\d+=IFCRELAGGREGATES\('[^']+',#\d+,[^,]*,[^,]*,#(\d+),\(([^)]*)\)\)")
    with open(path, encoding="latin-1") as f:
        for line in f:
            m = entity.match(line)
            if m:
                sid, typ, guid, name = int(m.group(1)), m.group(2), m.group(3), m.group(4)
                ids[guid], types[guid], names[sid], type_of[sid] = sid, typ, name or "", typ
            m = contained.match(line)
            if m:
                for ref in m.group(1).split(","):
                    parent[int(ref.strip().lstrip("#"))] = int(m.group(2))
            m = aggregates.match(line)
            if m:
                for ref in m.group(2).split(","):
                    parent[int(ref.strip().lstrip("#"))] = int(m.group(1))

    def storey_of(sid: int):
        seen = set()
        while sid in parent and sid not in seen:
            seen.add(sid)
            sid = parent[sid]
            if type_of.get(sid) == "IFCBUILDINGSTOREY":
                return sid
        return None

    storey = {sid: s for sid in list(parent) if (s := storey_of(sid)) is not None}
    return ids, types, names, storey


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ids, types, names, contained = parse_ifc(IFC)
    testkit = {r["GlobalId"]: r for r in csv.DictReader(open(TESTKIT_CSV, encoding="utf-8-sig"))}

    elements = []
    for guid, row in testkit.items():
        typ = types[guid]
        if typ in SKIP_TYPES:
            continue
        sid = ids[guid]
        storey_id = contained.get(sid)
        storey = names.get(storey_id, "") if storey_id else ""
        a1a3 = None if typ in NO_EMBODIED_TYPES else round(BASE_A1A3[typ] * jitter(guid), 1)
        elements.append({
            "GlobalId": guid,
            "EntityId": sid,
            "IfcType": typ,
            "Name": row["Name"],
            "Storey": storey,
            "StoreyEntityId": storey_id or "",
            "Category": row["category"],
            "EmbodiedCarbon_A1A3_kgCO2e": a1a3,
            "EmbodiedCarbon_A1A5_kgCO2e": None if a1a3 is None else round(a1a3 * 1.12, 1),
            "OperationalCarbon_kgCO2e_per_year": float(row["operational_carbon"]),
            "EnergyUseIntensity_kWh_per_m2_year": float(row["energy_intensity"]),
            "ScenarioName": SCENARIO,
            "AnalysisRunId": RUN_ID,
        })
    elements.sort(key=lambda e: e["EntityId"])

    wide_cols = list(elements[0].keys())
    with open(OUT / "nrc_analytics_elements.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, wide_cols)
        w.writeheader()
        w.writerows(elements)

    # Layer 2: long format
    metrics = [
        ("NRC.EC.A1A3.TOTAL", "EmbodiedCarbon_A1A3_kgCO2e", "kgCO2e", "A1-A3"),
        ("NRC.EC.A1A5.TOTAL", "EmbodiedCarbon_A1A5_kgCO2e", "kgCO2e", "A1-A5"),
        ("NRC.OC.ANNUAL", "OperationalCarbon_kgCO2e_per_year", "kgCO2e/yr", "B6"),
        ("NRC.EUI.ANNUAL", "EnergyUseIntensity_kWh_per_m2_year", "kWh/m2/yr", "B6"),
    ]
    with open(OUT / "nrc_analytics_long.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["AnalysisRunId", "GlobalId", "IfcClass", "MetricId", "MetricName", "Value", "Unit",
                    "LifecycleStage", "Scenario", "Source", "Confidence", "ComputationMethod"])
        for e in elements:
            for metric_id, col, unit, stage in metrics:
                if e[col] is None:
                    continue
                w.writerow([RUN_ID, e["GlobalId"], e["IfcType"], metric_id, col, e[col], unit, stage,
                            SCENARIO, "synthetic-generator-v1", 0.5, "type-base-x-hash-jitter"])

    # Aggregates per storey and for the building
    agg = defaultdict(lambda: {"a1a3": 0.0, "a1a5": 0.0, "oc": 0.0, "eui_sum": 0.0, "n": 0, "n_ec": 0})
    for e in elements:
        for key in (e["Storey"], "__building__"):
            a = agg[key]
            a["n"] += 1
            a["oc"] += e["OperationalCarbon_kgCO2e_per_year"]
            a["eui_sum"] += e["EnergyUseIntensity_kWh_per_m2_year"]
            if e["EmbodiedCarbon_A1A3_kgCO2e"] is not None:
                a["a1a3"] += e["EmbodiedCarbon_A1A3_kgCO2e"]
                a["a1a5"] += e["EmbodiedCarbon_A1A5_kgCO2e"]
                a["n_ec"] += 1
    storey_ids = {names[sid]: sid for sid in set(contained.values())}
    building_id = next(ids[g] for g, t in types.items() if t == "IFCBUILDING")
    project_id = next(ids[g] for g, t in types.items() if t == "IFCPROJECT")

    with open(OUT / "nrc_analytics_storeys.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Container", "EntityId", "Elements", "EmbodiedCarbon_A1A3_kgCO2e", "EmbodiedCarbon_A1A5_kgCO2e",
                    "OperationalCarbon_kgCO2e_per_year", "MeanEnergyUseIntensity_kWh_per_m2_year"])
        for key, a in sorted(agg.items(), key=lambda kv: (kv[0] == "__building__", kv[0])):
            label = "Building" if key == "__building__" else key
            eid = building_id if key == "__building__" else storey_ids[key]
            w.writerow([label, eid, a["n"], round(a["a1a3"], 1), round(a["a1a5"], 1), round(a["oc"], 1),
                        round(a["eui_sum"] / a["n"], 2)])

    # Rows for the byte-exact writer
    rows = []

    def pset(eid, name, props):
        for pname, vtype, value in props:
            rows.append([eid, name, pname, vtype, value])

    for e in elements:
        if e["EmbodiedCarbon_A1A3_kgCO2e"] is not None:
            pset(e["EntityId"], "Pset_NRCEmbodiedCarbon", [
                ("EmbodiedCarbon_A1A3_kgCO2e", "Real", e["EmbodiedCarbon_A1A3_kgCO2e"]),
                ("EmbodiedCarbon_A1A5_kgCO2e", "Real", e["EmbodiedCarbon_A1A5_kgCO2e"]),
                ("ScenarioName", "Label", SCENARIO),
                ("AnalysisRunId", "Identifier", RUN_ID),
            ])
        pset(e["EntityId"], "Pset_NRCOperationalCarbon", [
            ("OperationalCarbon_kgCO2e_per_year", "Real", e["OperationalCarbon_kgCO2e_per_year"]),
            ("GridEmissionFactor_kgCO2e_per_kWh", "Real", GRID_FACTOR),
            ("ScenarioName", "Label", SCENARIO),
            ("AnalysisRunId", "Identifier", RUN_ID),
        ])
        pset(e["EntityId"], "Pset_NRCEnergyPerformance", [
            ("EnergyUseIntensity_kWh_per_m2_year", "Real", e["EnergyUseIntensity_kWh_per_m2_year"]),
            ("ScenarioName", "Label", SCENARIO),
            ("AnalysisRunId", "Identifier", RUN_ID),
        ])
    for key, a in agg.items():
        eid = building_id if key == "__building__" else storey_ids[key]
        pset(eid, "Pset_NRCEmbodiedCarbon", [
            ("EmbodiedCarbon_A1A3_kgCO2e", "Real", round(a["a1a3"], 1)),
            ("EmbodiedCarbon_A1A5_kgCO2e", "Real", round(a["a1a5"], 1)),
            ("ScenarioName", "Label", SCENARIO),
            ("AnalysisRunId", "Identifier", RUN_ID),
        ])
        pset(eid, "Pset_NRCOperationalCarbon", [
            ("OperationalCarbon_kgCO2e_per_year", "Real", round(a["oc"], 1)),
            ("ScenarioName", "Label", SCENARIO),
            ("AnalysisRunId", "Identifier", RUN_ID),
        ])
    pset(project_id, "Pset_NRCAnalyticsProvenance", [
        ("AnalysisRunId", "Identifier", RUN_ID),
        ("SourceTool", "Label", "nrc-ifc-llm/poc/generate_synthetic_analytics.py"),
        ("Methodology", "Label", "Synthetic, illustrative; not EN 15978"),
        ("ComputedAt", "Label", "2026-09-17T00:00:00Z"),
        ("ComputedBy", "Label", "Ara 3D"),
        ("MetricDictionaryVersion", "Label", "NRC-metrics-0.1"),
        ("ResultDatasetURI", "Text", "poc/data/nrc_analytics_long.csv"),
        ("ResultDatasetFormat", "Label", "CSV"),
        ("JoinKey", "Label", "GlobalId"),
    ])
    with open(OUT / "psets_to_write.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["entityId", "psetName", "paramName", "valueType", "paramValue"])
        w.writerows(rows)

    n_ec = sum(1 for e in elements if e["EmbodiedCarbon_A1A3_kgCO2e"] is not None)
    print(f"{len(elements)} elements ({n_ec} with embodied carbon), {len(agg) - 1} storeys, "
          f"{len(rows)} property values to write")
    for key, a in sorted(agg.items()):
        print(f"  {key:14s} n={a['n']:3d}  A1A3={a['a1a3']:9.1f}  OC/yr={a['oc']:8.1f}")


if __name__ == "__main__":
    main()
