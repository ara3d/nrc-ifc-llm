# IFC MCP replay over C:/Users/cdigg/git/bim-open-toolkit/samples/nrc/duplex-enriched.ifc

Server ara3d-ifc 0.1.0 over stdio, 29 tools, 2026-09-18T21:57:09.806Z.
Every call and its result are recorded verbatim; the SQL is the recorded session's. No language model is involved.

### Setup: open the model and list the query views

**Agent calls** `ifc_open` with
```json
{
 "path": "C:/Users/cdigg/git/bim-open-toolkit/samples/nrc/duplex-enriched.ifc"
}
```
**Result** (299 ms)
```json
{
 "ok": true,
 "data": {
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "schema": "IFC2X3",
  "entityCount": 42664,
  "openedUtc": "2026-09-18T21:57:10.0852608Z"
 },
 "nextRecommendedTools": [
  "ifc_header",
  "ifc_type_counts",
  "ifc_spatial_tree"
 ]
}
```

**Agent calls** `ifc_table` with
```json
{
 "path": "C:/Users/cdigg/git/bim-open-toolkit/samples/nrc/duplex-enriched.ifc",
 "take": 50
}
```
**Result** (584 ms)
```json
{
 "ok": true,
 "data": {
  "total": 13,
  "skip": 0,
  "count": 13,
  "items": [
   {
    "table": "Descriptors",
    "rowCount": 437,
    "columns": [
     {
      "name": "Name",
      "type": "INTEGER"
     },
     {
      "name": "Units",
      "type": "INTEGER"
     },
     {
      "name": "Group",
      "type": "INTEGER"
     },
     {
      "name": "Type",
      "type": "INTEGER"
     }
    ]
   },
   {
    "table": "Diagnostics",
    "rowCount": 0,
    "columns": [
     {
      "name": "Type",
      "type": "INTEGER"
     },
     {
      "name": "Document",
      "type": "INTEGER"
     },
     {
      "name": "Entity",
      "type": "INTEGER"
     },
     {
      "name": "Message",
      "type": "INTEGER"
     }
    ]
   },
   {
    "table": "Documents",
    "rowCount": 1,
    "columns": [
     {
      "name": "Title",
      "type": "INTEGER"
     },
     {
      "name": "Path",
      "type": "INTEGER"
     }
    ]
   },
   {
    "table": "Entities",
    "rowCount": 4721,
    "columns": [
     {
      "name": "LocalId",
      "type": "BIGINT"
     },
     {
      "name": "GlobalId",
      "type": "INTEGER"
     },
     {
      "name": "Document",
      "type": "INTEGER"
     },
     {
      "name": "Name",
      "type": "INTEGER"
     },
     {
      "name": "Category",
      "type": "INTEGER"
     },
     {
      "name": "Type",
      "type": "INTEGER"
     }
    ]
   },
   {
    "table": "EntityText",
    "rowCount": 4721,
    "columns": [
     {
      "name": "EntityIndex",
      "type": "BIGINT"
     },
     {
      "name": "StepId",
      "type": "BIGINT"
     },
     {
      "name": "GlobalId",
      "type": "VARCHAR"
     },
     {
      "name": "Name",
      "type": "VARCHAR"
     },
     {
      "name": "Category",
      "type": "VARCHAR"
     },
     {
      "name": "Type",
      "type": "VARCHAR"
     }
    ]
   },
   {
    "table": "Numbers",
    "rowCount": 1142,
    "columns": [
     {
      "name": "Numbers",
      "type": "FLOAT"
     }
    ]
   },
   {
    "table": "ParameterText",
    "rowCount": 18094,
    "columns": [
     {
      "name": "EntityIndex",
      "type": "INTEGER"
     },
     {
      "name": "Name",
      "type": "VARCHAR"
     },
     {
      "name": "ParameterGroup",
      "type": "VARCHAR"
     },
     {
      "name": "Units",
      "type": "VARCHAR"
     },
     {
      "name": "ValueType",
      "type": "VARCHAR"
     },
     {
      "name": "Value",
      "type": "VARCHAR"
     }
    ]
   },
   {
    "table": "Parameters",
    "rowCount": 18094,
    "columns": [
     {
      "name": "Entity",
      "type": "INTEGER"
     },
     {
      "name": "Descriptor",
      "type": "INTEGER"
     },
     {
      "name": "Value",
      "type": "INTEGER"
     }
    ]
   },
   {
    "table": "Points",
    "rowCount": 0,
    "columns": [
     {
      "name": "X",
      "type": "FLOAT"
     },
     {
      "name": "Y",
      "type": "FLOAT"
     },
     {
      "name": "Z",
      "type": "FLOAT"
     }
    ]
   }
... (4234 chars total)
```

### Q1: What is the total operational carbon for the building?

**Agent calls** `ifc_sql` with
```json
{
 "path": "C:/Users/cdigg/git/bim-open-toolkit/samples/nrc/duplex-enriched.ifc",
 "sql": "SELECT round(sum(CAST(p.Value AS DOUBLE)),1) AS total_kgCO2e_per_year, count(*) AS elements FROM ParameterText p JOIN EntityText e ON e.EntityIndex = p.EntityIndex WHERE p.ParameterGroup='Pset_NRCOperationalCarbon' AND p.Name='OperationalCarbon_kgCO2e_per_year' AND e.Category NOT IN ('IFCBUILDING','IFCBUILDINGSTOREY','IFCPROJECT')",
 "take": 50
}
```
**Result** (38 ms)
```json
{
 "ok": true,
 "data": {
  "total": 1,
  "skip": 0,
  "count": 1,
  "columns": [
   "total_kgCO2e_per_year",
   "elements"
  ],
  "rows": [
   [
    37196.2,
    218
   ]
  ]
 }
}
```

**Expected:** 37,196.2 kgCO2e/yr over 218 elements

**Verdict:** match

### Q5: How much operational carbon is in each category?

**Agent calls** `ifc_sql` with
```json
{
 "path": "C:/Users/cdigg/git/bim-open-toolkit/samples/nrc/duplex-enriched.ifc",
 "sql": "SELECT e.Category, round(sum(CAST(p.Value AS DOUBLE)),1) AS oc, count(*) AS n FROM ParameterText p JOIN EntityText e ON e.EntityIndex = p.EntityIndex WHERE p.ParameterGroup='Pset_NRCOperationalCarbon' AND p.Name='OperationalCarbon_kgCO2e_per_year' AND e.Category NOT IN ('IFCBUILDING','IFCBUILDINGSTOREY','IFCPROJECT') GROUP BY e.Category ORDER BY oc DESC",
 "take": 50
}
```
**Result** (34 ms)
```json
{
 "ok": true,
 "data": {
  "total": 14,
  "skip": 0,
  "count": 14,
  "columns": [
   "Category",
   "oc",
   "n"
  ],
  "rows": [
   [
    "IFCWALLSTANDARDCASE",
    17547.4,
    56
   ],
   [
    "IFCSLAB",
    5816.9,
    21
   ],
   [
    "IFCFURNISHINGELEMENT",
    5766.3,
    61
   ],
   [
    "IFCFOOTING",
    2086.9,
    7
   ],
   [
    "IFCDOOR",
    1324.7,
    14
   ],
   [
    "IFCCOVERING",
    985.7,
    13
   ],
   [
    "IFCWINDOW",
    978.9,
    24
   ],
   [
    "IFCBEAM",
    771.6,
    8
   ],
   [
    "IFCMEMBER",
    560,
    4
   ],
   [
    "IFCWALL",
    357.5,
    1
   ],
   [
    "IFCSTAIRFLIGHT",
    311.5,
    2
   ],
   [
    "IFCSTAIR",
    272.7,
    2
   ],
   [
    "IFCROOF",
    251.3,
    1
   ],
   [
    "IFCRAILING",
    164.8,
    4
   ]
  ]
 }
}
```

**Expected:** walls first at 17,547.4 (IFCWALLSTANDARDCASE), 14 IFC classes

**Verdict:** match

### Q7: What is the embodied carbon of the roof?

**Agent calls** `ifc_sql` with
```json
{
 "path": "C:/Users/cdigg/git/bim-open-toolkit/samples/nrc/duplex-enriched.ifc",
 "sql": "SELECT e.GlobalId, p.ParameterGroup, p.Name AS prop, p.Value FROM EntityText e LEFT JOIN ParameterText p ON p.EntityIndex=e.EntityIndex AND p.ParameterGroup LIKE 'Pset_NRC%' WHERE e.Category='IFCROOF' ORDER BY p.ParameterGroup, prop",
 "take": 50
}
```
**Result** (37 ms)
```json
{
 "ok": true,
 "data": {
  "total": 7,
  "skip": 0,
  "count": 7,
  "columns": [
   "GlobalId",
   "ParameterGroup",
   "prop",
   "Value"
  ],
  "rows": [
   [
    "0jf0rYHfX3RAB3bSIRjmxl",
    "Pset_NRCEnergyPerformance",
    "AnalysisRunId",
    "run-2026-09-17-01"
   ],
   [
    "0jf0rYHfX3RAB3bSIRjmxl",
    "Pset_NRCEnergyPerformance",
    "EnergyUseIntensity_kWh_per_m2_year",
    "73.6"
   ],
   [
    "0jf0rYHfX3RAB3bSIRjmxl",
    "Pset_NRCEnergyPerformance",
    "ScenarioName",
    "Baseline"
   ],
   [
    "0jf0rYHfX3RAB3bSIRjmxl",
    "Pset_NRCOperationalCarbon",
    "AnalysisRunId",
    "run-2026-09-17-01"
   ],
   [
    "0jf0rYHfX3RAB3bSIRjmxl",
    "Pset_NRCOperationalCarbon",
    "GridEmissionFactor_kgCO2e_per_kWh",
    "0.11"
   ],
   [
    "0jf0rYHfX3RAB3bSIRjmxl",
    "Pset_NRCOperationalCarbon",
    "OperationalCarbon_kgCO2e_per_year",
    "251.3"
   ],
   [
    "0jf0rYHfX3RAB3bSIRjmxl",
    "Pset_NRCOperationalCarbon",
    "ScenarioName",
    "Baseline"
   ]
  ]
 }
}
```

**Expected:** not available: the roof carries no Pset_NRCEmbodiedCarbon set

**Verdict:** match

### Q8: What is the total embodied carbon (A1-A3) per storey?

**Agent calls** `ifc_sql` with
```json
{
 "path": "C:/Users/cdigg/git/bim-open-toolkit/samples/nrc/duplex-enriched.ifc",
 "sql": "SELECT e.Name AS storey, CAST(p.Value AS DOUBLE) AS a1a3 FROM ParameterText p JOIN EntityText e ON e.EntityIndex = p.EntityIndex WHERE e.Category='IFCBUILDINGSTOREY' AND p.ParameterGroup='Pset_NRCEmbodiedCarbon' AND p.Name='EmbodiedCarbon_A1A3_kgCO2e' ORDER BY a1a3 DESC",
 "take": 50
}
```
**Result** (25 ms)
```json
{
 "ok": true,
 "data": {
  "total": 4,
  "skip": 0,
  "count": 4,
  "columns": [
   "storey",
   "a1a3"
  ],
  "rows": [
   [
    "Level 1",
    49451.2
   ],
   [
    "Level 2",
    48696.8
   ],
   [
    "T/FDN",
    11761.3
   ],
   [
    "Roof",
    5821
   ]
  ]
 }
}
```

**Expected:** Level 1 49,451.2; Level 2 48,696.8; T/FDN 11,761.3; Roof 5,821.0

**Verdict:** match

## Summary

| Question | Rows | Verdict |
|---|---|---|
| Q1 | 1 | match |
| Q5 | 14 | match |
| Q7 | 7 | match |
| Q8 | 4 | match |
