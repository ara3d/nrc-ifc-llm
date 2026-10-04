# IFC questions answered through the MCP tools

- Date: 2026-10-04 17:03:36 -04:00
- Language model: claude-haiku-4-5-20251001 (claude-cli, effort medium)
- IFC model: `C:\Users\cdigg\git\nrc-ifc-llm\poc\data\duplex-enriched.ifc`
- Toolkit commit: `59aeb6d`

### What is the total operational carbon for the building?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:01:39.9527993Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "propertySet": "Pset_NRCBuildingSummary"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_spatial_tree` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","roots":[{"id":34,"type":"IFCPROJECT","name":"0001","elementCount":0,"children":[{"…

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "id": 36
}
```

**Result** {"entity":{"id":36,"type":"IFCBUILDING","name":"#36","globalId":"1xS3BCk291UvhgP2a6eflK"},"properties":{"total":16,"skip":0,"count":16,"items":[{"propertySet":"…

**Answer:** The total operational carbon for the building is 37,196.2 kgCO2e per year, from the Pset_NRCOperationalCarbon property set on the IFCBUILDING entity (id 36). This is a precomputed analytics result at the building level.

Turns 6; input tokens 58785; output tokens 1052.

### Which storey has the higher mean energy intensity, Level 1 or Level 2?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:01:39.9527993Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "energy"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":1,"skip":0,"count":1,"items":[{"propertySet":"Pset_NRCEnergyPerformance","name":"Energy…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\35eb484f3aa44203…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT \n  StoreyName,\n  AVG(CAST(p.Value AS DOUBLE)) as MeanEnergyIntensity\nFROM StoreyOfElement s\nJOIN ParameterText p ON s.EntityIndex = p.EntityIndex\nWHERE p.ParameterGroup = \u0027Pset_NRCEnergyPerformance\u0027\n  AND p.Name = \u0027EnergyUseIntensity_kWh_per_m2_year\u0027\n  AND StoreyName IN (\u0027Level 1\u0027, \u0027Level 2\u0027)\nGROUP BY StoreyName\nORDER BY StoreyName"
}
```

**Result** {"total":2,"skip":0,"count":2,"columns":["StoreyName","MeanEnergyIntensity"],"rows":[["Level 1",40.4990291262136],["Level 2",40.55698924731183]]}

**Answer:** From ifc_sql, 2 rows showed that Level 2 has the higher mean energy intensity at 40.56 kWh/m²/year, compared to Level 1 at 40.50 kWh/m²/year. The difference is small, with Level 2 exceeding Level 1 by approximately 0.07 kWh/m²/year based on the EnergyUseIntensity_kWh_per_m2_year property in the Pset_NRCEnergyPerformance property set.

Turns 5; input tokens 35757; output tokens 1139.

### Which five elements have the highest operational carbon?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:01:39.9527993Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\35eb484f3aa44203…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  e.Name,\n  e.Category,\n  e.StepId,\n  CAST(p.Value AS DOUBLE) AS OperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\n  AND p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\nORDER BY CAST(p.Value AS DOUBLE) DESC\nLIMIT 5\n"
}
```

**Result** {"total":5,"skip":0,"count":5,"columns":["Name","Category","StepId","OperationalCarbon_kgCO2e_per_year"],"rows":[["#36","IFCBUILDING",36,37196.2],["Level 1","IF…

**Answer:** From ifc_sql, 5 rows: the five elements with the highest operational carbon are (1) the building itself "#36" at 37,196.2 kgCO2e per year, (2) "Level 1" storey at 17,457 kgCO2e per year, (3) "Level 2" storey at 13,970.2 kgCO2e per year, (4) "T/FDN" storey at 4,001.7 kgCO2e per year, and (5) "Roof" storey at 1,767.3 kgCO2e per year. These values are from the Pset_NRCOperationalCarbon property set.

Turns 5; input tokens 36674; output tokens 1243.

### What is the operational carbon of the door named M_Single-Flush:0762 x 2032mm?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:01:39.9527993Z"}

**Agent calls** `ifc_search` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "text": "M_Single-Flush:0762 x 2032mm"
}
```

**Result** {"total":10,"skip":0,"count":10,"items":[{"id":7989,"type":"IFCOPENINGELEMENT","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173:1","globalId":"1xS3BCk2…

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "id": 8066
}
```

**Result** {"entity":{"id":8066,"type":"IFCDOOR","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173","globalId":"1hOSvn6df7F8_7GcBWlS8Z"},"properties":{"total":74,"…

**Answer:** The operational carbon of the door named M_Single-Flush:0762 x 2032mm is 54 kg CO2e per year, from the Pset_NRCOperationalCarbon property set returned by ifc_properties for that door entity.

Turns 4; input tokens 32389; output tokens 766.

### How much operational carbon is in each category?

I'll help you find the operational carbon data by category. Let me start by opening the file and exploring what's available.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:01:39.9527993Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `ifc_type_counts` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "take": 50
}
```

**Result** {"total":103,"skip":0,"count":50,"items":[{"type":"IFCCARTESIANPOINT","count":8520},{"type":"IFCPROPERTYSINGLEVALUE","count":7651},{"type":"IFCPOLYLOOP","count"…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\35eb484f3aa44203…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  et.Category,\n  COUNT(DISTINCT et.EntityIndex) as Element_Count,\n  SUM(CAST(pt.Value AS DOUBLE)) as Total_Operational_Carbon_kgCO2e_per_year\nFROM EntityText et\nJOIN ParameterText pt ON et.EntityIndex = pt.EntityIndex\nWHERE pt.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\n  AND pt.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\nGROUP BY et.Category\nORDER BY Total_Operational_Carbon_kgCO2e_per_year DESC\n"
}
```

**Result** {"total":16,"skip":0,"count":16,"columns":["Category","Element_Count","Total_Operational_Carbon_kgCO2e_per_year"],"rows":[["IFCBUILDINGSTOREY",4,37196.2],["IFCB…

**Answer:** From ifc_sql, 16 categories returned. The operational carbon per category (measured in kgCO2e per year) is: IFCBUILDINGSTOREY leads with 37,196.2 kgCO2e/year across 4 elements, followed by IFCBUILDING at 37,196.2 (1 element), IFCWALLSTANDARDCASE at 17,547.4 (56 elements), IFCSLAB at 5,816.9 (21 elements), IFCFURNISHINGELEMENT at 5,766.3 (61 elements), IFCFOOTING at 2,086.9 (7 elements), IFCDOOR at 1,324.7 (14 elements), IFCCOVERING at 985.7 (13 elements), IFCWINDOW at 978.9 (24 elements), IFCBEAM at 771.6 (8 elements), IFCMEMBER at 560.0 (4 elements), IFCWALL at 357.5 (1 element), IFCSTAIRFLIGHT at 311.5 (2 elements), IFCSTAIR at 272.7 (2 elements), IFCROOF at 251.3 (1 element), and IFCRAILING at 164.8 (4 elements).

Turns 6; input tokens 59344; output tokens 1407.

### Which analysis run produced these values, and when?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:01:39.9527993Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "Provenance"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "propertySet": "Pset_NRC"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":20,"skip":0,"count":20,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

**Answer:** The analysis run was **run-2026-09-17-01**, computed on **2026-09-17 at 00:00:00 UTC** by Ara 3D. From ifc_parameters, 20 rows showed that the Pset_NRCAnalyticsProvenance property set identifies the analysis run ID and timestamp, and the methodology is synthetic and illustrative (not EN 15978). All NRC property sets—EmbodiedCarbon, EnergyPerformance, and OperationalCarbon—carry the same AnalysisRunId, confirming they are outputs of the same run, created by the source tool nrc-ifc-llm/poc/generate_synthetic_analytics.py using metric dictionary version NRC-metrics-0.1.

Turns 4; input tokens 27773; output tokens 948.

### What is the embodied carbon of the roof?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:01:39.9527993Z"}

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\35eb484f3aa44203…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `ifc_search` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "text": "roof"
}
```

**Result** {"total":10,"skip":0,"count":10,"items":[{"id":51,"type":"IFCBUILDINGSTOREY","name":"Roof","globalId":"1xS3BCk291UvhgP2dvNtSE"},{"id":3707,"type":"IFCSPACE","na…

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "id": 22475
}
```

**Result** {"entity":{"id":22475,"type":"IFCROOF","name":"Basic Roof:Live Roof over Wood Joist Flat Roof:184483","globalId":"0jf0rYHfX3RAB3bSIRjmxl"},"properties":{"total"…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT DISTINCT e.Name, e.Type, e.StepId, p.Value \nFROM EntityText e \nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex \nWHERE (e.Type LIKE \u0027%ROOF%\u0027 OR e.Name LIKE \u0027%Roof%\u0027) \nAND (p.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027 OR p.Name = \u0027EmbodiedCarbon_A1A5_kgCO2e\u0027)\nORDER BY e.StepId"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["Name","Type","StepId","Value"],"rows":[["Roof",null,51,"6519.4"],["Roof",null,51,"5821.0"],["Basic Roof:Live Roof over…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT e.Name, e.Category, e.StepId, p.Name AS Property, p.Value \nFROM EntityText e \nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex \nWHERE e.Name = \u0027Basic Roof:Live Roof over Wood Joist Flat Roof:184483\u0027\nAND (p.Name LIKE \u0027EmbodiedCarbon%\u0027)\nORDER BY e.StepId, p.Name"
}
```

**Result** {"total":2,"skip":0,"count":2,"columns":["Name","Category","StepId","Property","Value"],"rows":[["Basic Roof:Live Roof over Wood Joist Flat Roof:184483","IFCSLA…

**Answer:** The embodied carbon of the roof is from ifc_sql, which returned 2 rows for the roof slab element (IFCSLAB category). The A1A3 embodied carbon (production, transport, and manufacturing) is 1838.5 kgCO2e and the A1A5 embodied carbon (which adds installation and initial transportation) is 2059.1 kgCO2e. The A1A5 value is more comprehensive as it includes the complete cradle-to-site assessment.

Turns 8; input tokens 82524; output tokens 1812.

### What is the total embodied carbon (A1-A3) per storey?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:01:39.9527993Z"}

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\35eb484f3aa44203…

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
  "name": "carbon"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

Perfect! I can see the model has embodied carbon data. Let me query the total embodied carbon (A1-A3) per storey using SQL.

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  soe.StoreyName,\n  ROUND(SUM(CAST(pt.Value AS DOUBLE)), 1) as TotalEmbodiedCarbon_A1A3_kgCO2e\nFROM ParameterText pt\nJOIN EntityText et ON pt.EntityIndex = et.EntityIndex\nJOIN StoreyOfElement soe ON et.EntityIndex = soe.EntityIndex\nWHERE pt.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\n  AND pt.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027\nGROUP BY soe.StoreyName\nORDER BY soe.StoreyName\n"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StoreyName","TotalEmbodiedCarbon_A1A3_kgCO2e"],"rows":[["Level 1",49451.2],["Level 2",48696.8],["Roof",5821],["T/FDN",…

**Answer:** From ifc_sql, 4 rows. The total embodied carbon (A1-A3) per storey is: Level 1 has 49,451.2 kgCO2e, Level 2 has 48,696.8 kgCO2e, T/FDN has 11,761.3 kgCO2e, and Roof has 5,821.0 kgCO2e. These values come from the Pset_NRCEmbodiedCarbon property set.

Turns 6; input tokens 39796; output tokens 1318.
