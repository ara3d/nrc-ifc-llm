# IFC questions answered through the MCP tools

- Date: 2026-09-18 18:03:58 -04:00
- Language model: gpt-5
- IFC model: `C:\Users\cdigg\git\bim-open-toolkit\samples\nrc\duplex-enriched.ifc`
- Toolkit commit: `66df499`

### What is the total operational carbon for the building?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-09-18T21:58:27.7170…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "Pset_NRC",
  "take": 100
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":20,"skip":0,"count":20,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT e.StepId, e.GlobalId, e.Name, e.Category, CAST(p.Value AS DOUBLE) AS OperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\n  AND p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\n  AND e.Category = \u0027IFCBUILDING\u0027"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["StepId","GlobalId","Name","Category","OperationalCarbon_kgCO2e_per_year"],"rows":[[36,"1xS3BCk291UvhgP2a6eflK","#36","…

**Answer:** 37,196.2 kgCO2e per year. From ifc_sql, 1 row: Pset_NRCOperationalCarbon.OperationalCarbon_kgCO2e_per_year on the IFCBUILDING.

Turns 4; input tokens 18633; output tokens 1842.

### Which storey has the higher mean energy intensity, Level 1 or Level 2?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-09-18T21:58:27.7170…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "Pset_NRC",
  "take": 1000
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":20,"skip":0,"count":20,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

**Agent calls** `ifc_spatial_tree` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","roots":[{"id":34,"type":"IFCPROJECT","name":"0001","elementCount":0,"child…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT s.StoreyName,\n       COUNT(*) AS n,\n       AVG(CAST(p.Value AS DOUBLE)) AS mean_eui\nFROM ParameterText p\nJOIN StoreyOfEntity s USING(EntityIndex)\nWHERE p.ParameterGroup = \u0027Pset_NRCEnergyPerformance\u0027\n  AND p.Name = \u0027EnergyUseIntensity_kWh_per_m2_year\u0027\n  AND p.ValueType = \u0027Number\u0027\n  AND s.StoreyName IN (\u0027Level 1\u0027,\u0027Level 2\u0027)\nGROUP BY s.StoreyName\nORDER BY s.StoreyName;"
}
```

**Result** {"total":2,"skip":0,"count":2,"columns":["StoreyName","n","mean_eui"],"rows":[["Level 1",103,40.499029126213586],["Level 2",93,40.55698924731185]]}

**Answer:** Level 2 has the higher mean energy intensity. From ifc_sql, 2 rows: for Pset_NRCEnergyPerformance.EnergyUseIntensity_kWh_per_m2_year, Level 1 averaged 40.499 kWh/m2/year and Level 2 averaged 40.557 kWh/m2/year.

Turns 5; input tokens 25609; output tokens 3029.

### Which five elements have the highest operational carbon?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-09-18T21:58:27.7170…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "Pset_NRC",
  "take": 100
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":20,"skip":0,"count":20,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT e.StepId, e.GlobalId, e.Name, e.Category, e.Type,\n       CAST(p.Value AS DOUBLE) AS OperationalCarbon_kgCO2e_per_year\nFROM ParameterText p\nJOIN EntityText e ON e.EntityIndex = p.EntityIndex\nWHERE p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\n  AND p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\n  AND TRY_CAST(p.Value AS DOUBLE) IS NOT NULL\nORDER BY OperationalCarbon_kgCO2e_per_year DESC, e.StepId ASC\nLIMIT 5;"
}
```

**Result** {"total":5,"skip":0,"count":5,"columns":["StepId","GlobalId","Name","Category","Type","OperationalCarbon_kgCO2e_per_year"],"rows":[[36,"1xS3BCk291UvhgP2a6eflK",…

**Answer:** Based on Pset_NRCOperationalCarbon.OperationalCarbon_kgCO2e_per_year, the top five are: “#36” (IFCBUILDING) at 37196.2 kgCO2e/year, “Level 1” (IFCBUILDINGSTOREY) at 17457, “Level 2” (IFCBUILDINGSTOREY) at 13970.2, “T/FDN” (IFCBUILDINGSTOREY) at 4001.7, and “Roof” (IFCBUILDINGSTOREY) at 1767.3. Source: ifc_sql, 5 rows, property set Pset_NRCOperationalCarbon, property OperationalCarbon_kgCO2e_per_year.

Turns 4; input tokens 18805; output tokens 2238.

### What is the operational carbon of the door named M_Single-Flush:0762 x 2032mm?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-09-18T21:58:27.7170…

**Agent calls** `ifc_search` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "text": "M_Single-Flush:0762 x 2032mm",
  "type": "IFCDOOR",
  "skip": 0,
  "take": 100
}
```

**Result** {"total":4,"skip":0,"count":4,"items":[{"id":8066,"type":"IFCDOOR","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173","globalId":"1hOSvn6df7F8_7GcBWlS8Z…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "Pset_NRC",
  "skip": 0,
  "take": 100
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":20,"skip":0,"count":20,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

**Agent calls** `ifc_parameter_table` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "names": "OperationalCarbon_kgCO2e_per_year",
  "propertySet": "Pset_NRCOperationalCarbon",
  "ids": "8066,8169,35318,35413",
  "skip": 0,
  "take": 100
}
```

**Result** {"columns":["OperationalCarbon_kgCO2e_per_year"],"rows":{"total":4,"skip":0,"count":4,"items":[{"entity":{"id":8066,"type":"IFCDOOR","name":"M_Single-Flush:0762…

**Answer:** There are four doors matching that name; from ifc_search, 4 rows. From ifc_parameter_table (property set Pset_NRCOperationalCarbon, property OperationalCarbon_kgCO2e_per_year), 4 rows: M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173 (#8066) = 54.0 kgCO2e/year; …:150257 (#8169) = 146.1 kgCO2e/year; …:203720 (#35318) = 117.3 kgCO2e/year; …:204034 (#35413) = 61.8 kgCO2e/year. Which specific instance do you mean?

Turns 4; input tokens 20384; output tokens 2886.

### How much operational carbon is in each category?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-09-18T21:58:27.7170…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT ParameterGroup, Name, Units, ValueType, COUNT(*) AS n, COUNT(DISTINCT EntityIndex) AS entities\nFROM ParameterText\nWHERE ParameterGroup LIKE \u0027Pset_NRC%\u0027\nGROUP BY ALL\nORDER BY ParameterGroup, Name"
}
```

**Result** {"total":20,"skip":0,"count":20,"columns":["ParameterGroup","Name","Units","ValueType","n","entities"],"rows":[["Pset_NRCAnalyticsProvenance","AnalysisRunId",""…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "WITH Op AS (\n  SELECT EntityIndex, CAST(Value AS DOUBLE) AS kg\n  FROM ParameterText\n  WHERE ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\n    AND Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\n    AND ValueType = \u0027Number\u0027\n)\nSELECT e.Category, COUNT(*) AS elements, SUM(o.kg) AS total_kgCO2e_per_year\nFROM Op o\nJOIN EntityText e USING (EntityIndex)\nGROUP BY e.Category\nORDER BY total_kgCO2e_per_year DESC NULLS LAST, elements DESC"
}
```

**Result** {"total":16,"skip":0,"count":16,"columns":["Category","elements","total_kgCO2e_per_year"],"rows":[["IFCBUILDINGSTOREY",4,37196.2],["IFCBUILDING",1,37196.2],["IF…

**Answer:** From ifc_sql, 16 rows: I summed Pset_NRCOperationalCarbon.OperationalCarbon_kgCO2e_per_year by EntityText.Category. 
Totals (kgCO2e/year) by category are: IFCBUILDINGSTOREY 37196.2; IFCBUILDING 37196.2; IFCWALLSTANDARDCASE 17547.4; IFCSLAB 5816.9; IFCFURNISHINGELEMENT 5766.3; IFCFOOTING 2086.9; IFCDOOR 1324.7; IFCCOVERING 985.7; IFCWINDOW 978.9; IFCBEAM 771.6; IFCMEMBER 560.0; IFCWALL 357.5; IFCSTAIRFLIGHT 311.5; IFCSTAIR 272.7; IFCROOF 251.3; IFCRAILING 164.8. 
Note that IFCBUILDING and IFCBUILDINGSTOREY are container categories that carry whole-building and per-storey totals, respectively.

Turns 4; input tokens 17250; output tokens 3757.

### Which analysis run produced these values, and when?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-09-18T21:58:27.7170…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "Pset_NRC",
  "skip": 0,
  "take": 100
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":20,"skip":0,"count":20,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

**Agent calls** `ifc_parameter_values` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "Pset_NRCAnalyticsProvenance.AnalysisRunId",
  "skip": 0,
  "take": 100
}
```

**Result** {"name":"Pset_NRCAnalyticsProvenance.AnalysisRunId","propertySets":["Pset_NRCAnalyticsProvenance"],"values":{"total":1,"skip":0,"count":1,"items":[{"value":"run…

**Agent calls** `ifc_parameter_values` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "Pset_NRCAnalyticsProvenance.ComputedAt",
  "skip": 0,
  "take": 100
}
```

**Result** {"name":"Pset_NRCAnalyticsProvenance.ComputedAt","propertySets":["Pset_NRCAnalyticsProvenance"],"values":{"total":1,"skip":0,"count":1,"items":[{"value":"2026-0…

**Answer:** The values came from analysis run run-2026-09-17-01, computed at 2026-09-17T00:00:00Z (UTC) as recorded in Pset_NRCAnalyticsProvenance.AnalysisRunId and .ComputedAt. From ifc_parameter_values, 1 row for AnalysisRunId and 1 row for ComputedAt, both in Pset_NRCAnalyticsProvenance.

Turns 4; input tokens 18775; output tokens 1644.

### What is the embodied carbon of the roof?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-09-18T21:58:27.7170…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "Pset_NRC",
  "skip": 0,
  "take": 100
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":20,"skip":0,"count":20,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "WITH roofs AS (\n  SELECT e.EntityIndex\n  FROM EntityText e\n  WHERE e.Category = \u0027IFCROOF\u0027\n  UNION\n  SELECT p.EntityIndex\n  FROM ParameterText p\n  JOIN EntityText e2 ON e2.EntityIndex = p.EntityIndex\n  WHERE e2.Category = \u0027IFCSLAB\u0027 AND p.Name = \u0027PredefinedType\u0027 AND UPPER(p.Value) = \u0027ROOF\u0027\n)\nSELECT \n  COUNT(*) AS RoofElementCount,\n  SUM(CAST(pA1A3.Value AS DOUBLE)) AS Sum_A1A3_kgCO2e,\n  SUM(CAST(pA1A5.Value AS DOUBLE)) AS Sum_A1A5_kgCO2e,\n  COUNT(DISTINCT r.EntityIndex) AS ElementsWithEC\nFROM roofs r\nLEFT JOIN ParameterText pA1A3 ON pA1A3.EntityIndex = r.EntityIndex AND pA1A3.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pA1A3.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027\nLEFT JOIN ParameterText pA1A5 ON pA1A5.EntityIndex = r.EntityIndex AND pA1A5.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pA1A5.Name = \u0027EmbodiedCarbon_A1A5_kgCO2e\u0027;"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["RoofElementCount","Sum_A1A3_kgCO2e","Sum_A1A5_kgCO2e","ElementsWithEC"],"rows":[[1,null,null,1]]}

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT e.StepId, e.Category, e.Type, e.Name, p.Value AS PredefinedType\nFROM ParameterText p\nJOIN EntityText e ON e.EntityIndex = p.EntityIndex\nWHERE p.Name = \u0027PredefinedType\u0027 AND (UPPER(p.Value) LIKE \u0027%ROOF%\u0027 OR UPPER(e.Type) LIKE \u0027%ROOF%\u0027)\nORDER BY e.Category, e.StepId;"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["StepId","Category","Type","Name","PredefinedType"],"rows":[]}

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT e.StepId, e.GlobalId, e.Name, e.Category, e.Type,\n       pa.Value AS A1A3_kgCO2e, pb.Value AS A1A5_kgCO2e\nFROM EntityText e\nLEFT JOIN ParameterText pa ON pa.EntityIndex = e.EntityIndex AND pa.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pa.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027\nLEFT JOIN ParameterText pb ON pb.EntityIndex = e.EntityIndex AND pb.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pb.Name = \u0027EmbodiedCarbon_A1A5_kgCO2e\u0027\nWHERE e.Category = \u0027IFCROOF\u0027\nORDER BY e.StepId;"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["StepId","GlobalId","Name","Category","Type","A1A3_kgCO2e","A1A5_kgCO2e"],"rows":[[22475,"0jf0rYHfX3RAB3bSIRjmxl","Basi…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT EntityIndex, StepId, GlobalId, Name, Category, Type FROM EntityText WHERE Category = \u0027IFCROOF\u0027 ORDER BY StepId;"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["EntityIndex","StepId","GlobalId","Name","Category","Type"],"rows":[[3405,22475,"0jf0rYHfX3RAB3bSIRjmxl","Basic Roof:Li…

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "id": 22475,
  "skip": 0,
  "take": 100
}
```

**Result** {"entity":{"id":22475,"type":"IFCROOF","name":"Basic Roof:Live Roof over Wood Joist Flat Roof:184483","globalId":"0jf0rYHfX3RAB3bSIRjmxl"},"properties":{"total"…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT EntityIndexA, NameA, EntityIndexB, NameB, RelationType\nFROM RelationText\nWHERE EntityIndexA = 3405 OR EntityIndexB = 3405\nORDER BY RelationType, EntityIndexA, EntityIndexB;"
}
```

**Result** {"total":10,"skip":0,"count":10,"columns":["EntityIndexA","NameA","EntityIndexB","NameB","RelationType"],"rows":[[3405,"Basic Roof:Live Roof over Wood Joist Fla…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "WITH roof AS (\n  SELECT 3405 AS EntityIndex\n), children AS (\n  SELECT r.EntityIndex AS RoofIndex, rel.EntityIndexA AS ChildIndex, rel.RelationType\n  FROM RelationText rel\n  JOIN roof r ON rel.EntityIndexB = r.EntityIndex\n)\nSELECT \n  e.EntityIndex, e.StepId, e.Category, e.Type, e.Name,\n  c.RelationType,\n  pa.Value AS A1A3_kgCO2e,\n  pb.Value AS A1A5_kgCO2e\nFROM (\n  SELECT EntityIndex, NULL AS RelationType FROM roof\n  UNION ALL\n  SELECT ChildIndex AS EntityIndex, RelationType FROM children\n) x\nJOIN EntityText e ON e.EntityIndex = x.EntityIndex\nLEFT JOIN ParameterText pa ON pa.EntityIndex = e.EntityIndex AND pa.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pa.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027\nLEFT JOIN ParameterText pb ON pb.EntityIndex = e.EntityIndex AND pb.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pb.Name = \u0027EmbodiedCarbon_A1A5_kgCO2e\u0027\nORDER BY x.RelationType NULLS FIRST, e.Category, e.StepId;"
}
```

**Result** failed: Binder Error: Referenced table "c" not found!
Candidate tables: "x"

LINE 10:   c.RelationType,
           ^

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "WITH roof AS (\n  SELECT 3405 AS EntityIndex\n), children AS (\n  SELECT r.EntityIndex AS RoofIndex, rel.EntityIndexA AS ChildIndex, rel.RelationType\n  FROM RelationText rel\n  JOIN roof r ON rel.EntityIndexB = r.EntityIndex\n)\nSELECT \n  e.EntityIndex, e.StepId, e.Category, e.Type, e.Name,\n  x.RelationType,\n  pa.Value AS A1A3_kgCO2e,\n  pb.Value AS A1A5_kgCO2e\nFROM (\n  SELECT EntityIndex, NULL AS RelationType FROM roof\n  UNION ALL\n  SELECT ChildIndex AS EntityIndex, RelationType FROM children\n) x\nJOIN EntityText e ON e.EntityIndex = x.EntityIndex\nLEFT JOIN ParameterText pa ON pa.EntityIndex = e.EntityIndex AND pa.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pa.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027\nLEFT JOIN ParameterText pb ON pb.EntityIndex = e.EntityIndex AND pb.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pb.Name = \u0027EmbodiedCarbon_A1A5_kgCO2e\u0027\nORDER BY x.RelationType NULLS FIRST, e.Category, e.StepId;"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["EntityIndex","StepId","Category","Type","Name","RelationType","A1A3_kgCO2e","A1A5_kgCO2e"],"rows":[[3405,22475,"IFCROO…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "WITH roof AS (\n  SELECT 3405 AS EntityIndex\n), children AS (\n  SELECT rel.EntityIndexA AS ChildIndex\n  FROM RelationText rel\n  JOIN roof r ON rel.EntityIndexB = r.EntityIndex\n)\nSELECT \n  COUNT(DISTINCT e.EntityIndex) AS ElementCount,\n  SUM(CAST(pa.Value AS DOUBLE)) AS Sum_A1A3_kgCO2e,\n  SUM(CAST(pb.Value AS DOUBLE)) AS Sum_A1A5_kgCO2e,\n  COUNT(DISTINCT CASE WHEN pa.Value IS NOT NULL OR pb.Value IS NOT NULL THEN e.EntityIndex END) AS ElementsWithEC\nFROM (\n  SELECT EntityIndex FROM roof\n  UNION ALL\n  SELECT ChildIndex AS EntityIndex FROM children\n) x\nJOIN EntityText e ON e.EntityIndex = x.EntityIndex\nLEFT JOIN ParameterText pa ON pa.EntityIndex = e.EntityIndex AND pa.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pa.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027\nLEFT JOIN ParameterText pb ON pb.EntityIndex = e.EntityIndex AND pb.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 AND pb.Name = \u0027EmbodiedCarbon_A1A5_kgCO2e\u0027;"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["ElementCount","Sum_A1A3_kgCO2e","Sum_A1A5_kgCO2e","ElementsWithEC"],"rows":[[4,1838.5,2059.1,1]]}

**Answer:** The roof’s embodied carbon is 1,838.5 kgCO2e (A1–A3) and 2,059.1 kgCO2e (A1–A5), taken from Pset_NRCEmbodiedCarbon (properties EmbodiedCarbon_A1A3_kgCO2e and EmbodiedCarbon_A1A5_kgCO2e) on its IFCSLAB member. From ifc_sql, 1 row (aggregation over the IFCROOF and its children); a breakdown shows the values are on the slab child while the IFCROOF itself holds none.

Turns 12; input tokens 85523; output tokens 11318.

### What is the total embodied carbon (A1-A3) per storey?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-09-18T21:58:27.7170…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT ParameterGroup, Name, ValueType, COUNT(*) AS Rows FROM ParameterText WHERE ParameterGroup LIKE \u0027Pset_NRC%\u0027 GROUP BY 1,2,3 ORDER BY ParameterGroup, Name LIMIT 500"
}
```

**Result** {"total":20,"skip":0,"count":20,"columns":["ParameterGroup","Name","ValueType","Rows"],"rows":[["Pset_NRCAnalyticsProvenance","AnalysisRunId","String",1],["Pset…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT so.StoreyIndex, so.StoreyName, SUM(CAST(pt.Value AS DOUBLE)) AS EmbodiedCarbon_A1A3_kgCO2e\nFROM ParameterText pt\nJOIN StoreyOfEntity so ON so.EntityIndex = pt.EntityIndex\nWHERE pt.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\n  AND pt.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027\n  AND pt.ValueType = \u0027Number\u0027\nGROUP BY 1,2\nORDER BY so.StoreyIndex"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StoreyIndex","StoreyName","EmbodiedCarbon_A1A3_kgCO2e"],"rows":[[133,"Level 1",98902.4],[134,"Level 2",97393.599999999…

**Answer:** Per storey total embodied carbon (A1–A3) is: Level 1 98902.4 kgCO2e, Level 2 97393.6 kgCO2e, T/FDN 23522.6 kgCO2e, and Roof 11642 kgCO2e.  
From ifc_sql, 4 rows, summing Pset_NRCEmbodiedCarbon.EmbodiedCarbon_A1A3_kgCO2e by storey via StoreyOfEntity.

Turns 4; input tokens 16989; output tokens 3430.
