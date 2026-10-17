# IFC questions answered through the MCP tools

- Date: 2026-10-17 18:13:33 -04:00
- Language model: claude-haiku-4-5-20251001 (claude-cli, effort medium)
- IFC model: `C:\Users\cdigg\git\nrc-ifc-llm\poc\data\duplex-enriched.ifc`
- Toolkit commit: `bf1e4a92`

### What is the total operational carbon for the building?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:08:37.8342846Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "operational"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":1,"skip":0,"count":1,"items":[{"propertySet":"Pset_NRCOperationalCarbon","name":"Operat…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT \n  SUM(CAST(Value AS DOUBLE)) as TotalOperationalCarbon_kgCO2e_per_year\nFROM ParameterText\nWHERE ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\n  AND Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\n  AND ValueType = \u0027Number\u0027"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["TotalOperationalCarbon_kgCO2e_per_year"],"rows":[[111588.59999999996]]}

**Answer:** The total operational carbon for the building is 111,589 kgCO2e per year (rounded), from ifc_sql summing the OperationalCarbon_kgCO2e_per_year property in the Pset_NRCOperationalCarbon property set across 223 elements. This represents the annual operational carbon emissions for the duplex building model.

Turns 4; input tokens 45347; output tokens 831.

### Which storey has the higher mean energy intensity, Level 1 or Level 2?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:08:37.8342846Z"}

**Agent calls** `ifc_spatial_tree` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","roots":[{"id":34,"type":"IFCPROJECT","name":"0001","elementCount":0,"children":[{"…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "energy"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":1,"skip":0,"count":1,"items":[{"propertySet":"Pset_NRCEnergyPerformance","name":"Energy…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "intensity"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":1,"skip":0,"count":1,"items":[{"propertySet":"Pset_NRCEnergyPerformance","name":"Energy…

Now let me query the mean energy intensity for each storey using ifc_sql:

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  soe.StoreyName,\n  AVG(CAST(p.Value AS DOUBLE)) as MeanEnergyIntensity\nFROM StoreyOfElement soe\nJOIN ParameterText p ON soe.EntityIndex = p.EntityIndex\nWHERE p.Name = \u0027EnergyUseIntensity_kWh_per_m2_year\u0027\n  AND p.ParameterGroup = \u0027Pset_NRCEnergyPerformance\u0027\n  AND soe.StoreyName IN (\u0027Level 1\u0027, \u0027Level 2\u0027)\nGROUP BY soe.StoreyName\nORDER BY soe.StoreyName\n"
}
```

**Result** {"total":2,"skip":0,"count":2,"columns":["StoreyName","MeanEnergyIntensity"],"rows":[["Level 1",40.4990291262136],["Level 2",40.55698924731183]]}

**Answer:** From ifc_sql, 2 rows: Level 2 has the higher mean energy intensity at 40.56 kWh/m²/year, compared to Level 1 at 40.50 kWh/m²/year. The difference is small, with Level 2 exceeding Level 1 by just 0.06 kWh/m²/year.

Turns 6; input tokens 63592; output tokens 1398.

### Which five elements have the highest operational carbon?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:08:37.8342846Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b1…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT \n  e.GlobalId,\n  e.Name,\n  e.Category,\n  p.Value as OperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\n  AND p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\nORDER BY CAST(p.Value AS DOUBLE) DESC\nLIMIT 5",
  "take": 5
}
```

**Result** {"total":5,"skip":0,"count":5,"columns":["GlobalId","Name","Category","OperationalCarbon_kgCO2e_per_year"],"rows":[["1xS3BCk291UvhgP2a6eflK",null,"IFCBUILDING",…

**Answer:** From ifc_sql, 5 rows: the five elements with the highest operational carbon (from the property Pset_NRCOperationalCarbon.OperationalCarbon_kgCO2e_per_year) are the building itself at 37,196.2 kgCO2e per year, followed by storey "Level 1" at 17,457.0, storey "Level 2" at 13,970.2, storey "T/FDN" at 4,001.7, and storey "Roof" at 1,767.3 kgCO2e per year.

Turns 5; input tokens 58944; output tokens 1197.

### What is the operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z?

I'll help you find the operational carbon of that door. Let me start by opening the file and then searching for the door with that GlobalId.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:08:37.8342846Z"}

**Agent calls** `ifc_search` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "text": "1hOSvn6df7F8_7GcBWlS8Z"
}
```

**Result** {"total":1,"skip":0,"count":1,"items":[{"id":8066,"type":"IFCDOOR","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173","globalId":"1hOSvn6df7F8_7GcBWlS8Z…

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "id": 8066
}
```

**Result** {"entity":{"id":8066,"type":"IFCDOOR","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173","globalId":"1hOSvn6df7F8_7GcBWlS8Z"},"properties":{"total":74,"…

**Answer:** The operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z is 54 kgCO2e per year, from ifc_properties (74 properties found). This value is stored in the Pset_NRCOperationalCarbon property set under "OperationalCarbon_kgCO2e_per_year". The door is a Single-Flush model at Level 1, and this operational carbon figure was calculated in the analysis run from September 17, 2026.

Turns 4; input tokens 39189; output tokens 744.

### How much operational carbon is stored per IFC class?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:08:37.8342846Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "propertySet": "NRC_",
  "take": 50
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b1…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  ET.Category,\n  COUNT(DISTINCT ET.EntityIndex) as ElementCount,\n  SUM(CAST(PT.Value AS DOUBLE)) as TotalOperationalCarbon_kgCO2e_per_year,\n  AVG(CAST(PT.Value AS DOUBLE)) as AvgOperationalCarbon_kgCO2e_per_year\nFROM EntityText ET\nJOIN ParameterText PT ON ET.EntityIndex = PT.EntityIndex\nWHERE PT.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\n  AND PT.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\nGROUP BY ET.Category\nORDER BY TotalOperationalCarbon_kgCO2e_per_year DESC\n"
}
```

**Result** {"total":16,"skip":0,"count":16,"columns":["Category","ElementCount","TotalOperationalCarbon_kgCO2e_per_year","AvgOperationalCarbon_kgCO2e_per_year"],"rows":[["…

**Answer:** From ifc_sql, 16 rows show operational carbon data from the Pset_NRCOperationalCarbon property set across 223 elements in 16 IFC classes. The largest operational carbon contributors are IFCBUILDINGSTOREY (37,196.2 kgCO2e per year total across 4 storeys, averaging 9,299.1 per storey), IFCWALLSTANDARDCASE (17,547.4 total across 56 walls, averaging 313.3 each), and IFCSLAB (5,816.9 total across 21 slabs, averaging 277 each). Other classes with significant operational carbon include IFCFURNISHINGELEMENT (5,766.3 total, 94.5 average), IFCFOOTING (2,086.9), IFCDOOR (1,324.7), and IFCCOVERING (985.7), with smaller amounts in the remaining nine classes like IFCWINDOW, IFCBEAM, IFCRAILING, and others.

Turns 6; input tokens 60454; output tokens 1515.

### Which analysis run produced these values, and when?

I'll help you find information about the analysis run. Let me start by opening the model and looking for provenance metadata.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:08:37.8342846Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "propertySet": "NRC_"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_entities_of_type` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "type": "IFCPROJECT"
}
```

**Result** {"total":1,"skip":0,"count":1,"items":[{"id":34,"type":"IFCPROJECT","name":"0001","globalId":"1xS3BCk291UvhgP2a6eflL"}]}

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "id": 34
}
```

**Result** {"entity":{"id":34,"type":"IFCPROJECT","name":"0001","globalId":"1xS3BCk291UvhgP2a6eflL"},"properties":{"total":9,"skip":0,"count":9,"items":[{"propertySet":"Ps…

**Answer:** From the project's Pset_NRCAnalyticsProvenance property set, the analysis run was identified as **run-2026-09-17-01** and was computed on **2026-09-17 at 00:00:00 UTC** by **Ara 3D** using the tool nrc-ifc-llm/poc/generate_synthetic_analytics.py. The values are synthetic and illustrative, not based on EN 15978, and follow the NRC-metrics-0.1 metric dictionary version.

Turns 5; input tokens 58375; output tokens 1198.

### Which analysed elements carry no embodied-carbon property set?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:08:37.8342846Z"}

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b1…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "propertySet": "NRC_",
  "take": 200
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "embodied",
  "take": 200
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":2,"skip":0,"count":2,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "\nWITH analyzed_elements AS (\n  SELECT DISTINCT EntityIndex\n  FROM ParameterText\n  WHERE ParameterGroup LIKE \u0027NRC_%\u0027\n)\nSELECT DISTINCT e.GlobalId, e.Name, e.Category\nFROM EntityText e\nWHERE e.EntityIndex IN (SELECT EntityIndex FROM analyzed_elements)\n  AND e.EntityIndex NOT IN (\n    SELECT DISTINCT EntityIndex\n    FROM ParameterText\n    WHERE ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\n  )\nORDER BY e.Category, e.Name\n",
  "take": 1000
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["GlobalId","Name","Category"],"rows":[]}

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "\nWITH analyzed_elements AS (\n  SELECT DISTINCT EntityIndex\n  FROM ParameterText\n  WHERE ParameterGroup LIKE \u0027NRC_%\u0027\n),\nwith_ec AS (\n  SELECT DISTINCT EntityIndex\n  FROM ParameterText\n  WHERE ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\n)\nSELECT \n  COUNT(DISTINCT a.EntityIndex) AS analyzed_count,\n  COUNT(DISTINCT ec.EntityIndex) AS with_embodied_carbon,\n  COUNT(DISTINCT a.EntityIndex) - COUNT(DISTINCT ec.EntityIndex) AS without_embodied_carbon\nFROM analyzed_elements a\nLEFT JOIN with_ec ec ON a.EntityIndex = ec.EntityIndex\n"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["analyzed_count","with_embodied_carbon","without_embodied_carbon"],"rows":[[0,0,0]]}

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "\nSELECT DISTINCT ParameterGroup\nFROM ParameterText\nWHERE ParameterGroup LIKE \u0027NRC_%\u0027\nORDER BY ParameterGroup\n"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["ParameterGroup"],"rows":[]}

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "\nSELECT DISTINCT ParameterGroup\nFROM ParameterText\nORDER BY ParameterGroup\nLIMIT 50\n"
}
```

**Result** {"total":50,"skip":0,"count":50,"columns":["ParameterGroup"],"rows":[["GSA Space Areas"],["IFCAPPLICATION"],["IFCARBITRARYPROFILEDEFWITHVOIDS"],["IFCBEAM"],["IF…

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "\nSELECT DISTINCT ParameterGroup\nFROM ParameterText\nWHERE ParameterGroup LIKE \u0027%NRC%\u0027 OR ParameterGroup LIKE \u0027Pset_NRC%\u0027\nORDER BY ParameterGroup\n"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["ParameterGroup"],"rows":[["Pset_NRCAnalyticsProvenance"],["Pset_NRCEmbodiedCarbon"],["Pset_NRCEnergyPerformance"],["Ps…

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "\nWITH analyzed_elements AS (\n  SELECT DISTINCT EntityIndex\n  FROM ParameterText\n  WHERE ParameterGroup LIKE \u0027Pset_NRC%\u0027\n)\nSELECT \n  COUNT(DISTINCT a.EntityIndex) AS analyzed_count,\n  COUNT(DISTINCT CASE WHEN ec.EntityIndex IS NOT NULL THEN a.EntityIndex END) AS with_embodied_carbon,\n  COUNT(DISTINCT CASE WHEN ec.EntityIndex IS NULL THEN a.EntityIndex END) AS without_embodied_carbon\nFROM analyzed_elements a\nLEFT JOIN (\n  SELECT DISTINCT EntityIndex\n  FROM ParameterText\n  WHERE ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\n) ec ON a.EntityIndex = ec.EntityIndex\n"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["analyzed_count","with_embodied_carbon","without_embodied_carbon"],"rows":[[224,222,2]]}

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "\nWITH analyzed_elements AS (\n  SELECT DISTINCT EntityIndex\n  FROM ParameterText\n  WHERE ParameterGroup LIKE \u0027Pset_NRC%\u0027\n)\nSELECT DISTINCT e.GlobalId, e.Name, e.Category\nFROM EntityText e\nWHERE e.EntityIndex IN (SELECT EntityIndex FROM analyzed_elements)\n  AND e.EntityIndex NOT IN (\n    SELECT DISTINCT EntityIndex\n    FROM ParameterText\n    WHERE ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\n  )\nORDER BY e.Category, e.Name\n",
  "take": 100
}
```

**Result** {"total":2,"skip":0,"count":2,"columns":["GlobalId","Name","Category"],"rows":[["1xS3BCk291UvhgP2a6eflL","0001","IFCPROJECT"],["0jf0rYHfX3RAB3bSIRjmxl","Basic R…

**Answer:** From ifc_sql, 2 rows: the IFCPROJECT named "0001" (GlobalId 1xS3BCk291UvhgP2a6eflL) and the IFCROOF named "Basic Roof:Live Roof over Wood Joist Flat Roof:184483" (GlobalId 0jf0rYHfX3RAB3bSIRjmxl). Of 224 analyzed elements (those carrying Pset_NRC* property sets), these two carry no Pset_NRCEmbodiedCarbon property set.

Turns 12; input tokens 137847; output tokens 3107.

### What is the total embodied carbon (A1-A3) per storey?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:08:37.8342846Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `ifc_spatial_tree` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","roots":[{"id":34,"type":"IFCPROJECT","name":"0001","elementCount":0,"children":[{"…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b1…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  StoreyOfElement.StoreyName,\n  CAST(SUM(CAST(ParameterText.Value AS DOUBLE)) AS DECIMAL(10,1)) AS TotalEmbodiedCarbon_A1A3_kgCO2e\nFROM StoreyOfElement\nJOIN ParameterText ON StoreyOfElement.EntityIndex = ParameterText.EntityIndex\nWHERE ParameterText.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\n  AND ParameterText.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027\nGROUP BY StoreyOfElement.StoreyName\nORDER BY StoreyOfElement.StoreyName\n"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StoreyName","TotalEmbodiedCarbon_A1A3_kgCO2e"],"rows":[["Level 1",49451.2],["Level 2",48696.8],["Roof",5821],["T/FDN",…

**Answer:** From ifc_sql, 4 rows. The total embodied carbon (A1-A3) per storey is: Level 1: 49,451.2 kgCO2e; Level 2: 48,696.8 kgCO2e; T/FDN: 11,761.3 kgCO2e; Roof: 5,821.0 kgCO2e. These values come from the Pset_NRCEmbodiedCarbon property set in the model.

Turns 6; input tokens 65206; output tokens 1494.

### Which zone has the highest energy use intensity?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:08:37.8342846Z"}

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b1…

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "SELECT DISTINCT Category FROM EntityText WHERE Category LIKE \u0027%ZONE%\u0027"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["Category"],"rows":[]}

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "SELECT DISTINCT ParameterGroup FROM ParameterText WHERE ParameterGroup LIKE \u0027NRC_%\u0027 ORDER BY ParameterGroup"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["ParameterGroup"],"rows":[]}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "energy"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":1,"skip":0,"count":1,"items":[{"propertySet":"Pset_NRCEnergyPerformance","name":"Energy…

**Agent calls** `ifc_type_counts` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "take": 50
}
```

**Result** {"total":103,"skip":0,"count":50,"items":[{"type":"IFCCARTESIANPOINT","count":8520},{"type":"IFCPROPERTYSINGLEVALUE","count":7651},{"type":"IFCPOLYLOOP","count"…

**Agent calls** `ifc_type_counts` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "skip": 50,
  "take": 100
}
```

**Result** {"total":103,"skip":50,"count":53,"items":[{"type":"IFCFILLAREASTYLEHATCHING","count":31},{"type":"IFCFURNITURETYPE","count":25},{"type":"IFCGEOMETRICSET","coun…

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "SELECT e.GlobalId, e.Name, e.Category, p.Value \nFROM EntityText e \nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex \nWHERE p.Name = \u0027EnergyUseIntensity_kWh_per_m2_year\u0027\nORDER BY CAST(p.Value AS DOUBLE) DESC\nLIMIT 10"
}
```

**Result** {"total":10,"skip":0,"count":10,"columns":["GlobalId","Name","Category","Value"],"rows":[["0dxE1Sy6nDqfpDb5vIMN_Z","Basic Wall:Interior - Furring (152 mm Stud):…

**Answer:** The model does not contain any zones. I searched the BOS database for IFCZONE entities and found none. The model has 21 IFCSPACE entities and 218 building elements (walls, furnishing elements, etc.) that carry EnergyUseIntensity_kWh_per_m2_year values ranging from 5.3 to 90.9 kWh/m²/year, but these are element-level properties, not zone-level metrics.

Turns 9; input tokens 117400; output tokens 1757.
