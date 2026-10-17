# IFC questions answered through the MCP tools

- Date: 2026-10-17 18:19:30 -04:00
- Language model: claude-haiku-4-5-20251001 (claude-cli, effort medium)
- IFC model: `C:\Users\cdigg\git\nrc-ifc-llm\bim-open-toolkit\samples\nrc\duplex-enriched.ifc`
- Toolkit commit: `bf1e4a92`

### What is the total operational carbon for the building?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":10,"skip":0,"count":10,"items":[{"propertySet":"NRC_BuildingSummary","name":"TotalEmbod…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT Value FROM ParameterText WHERE ParameterGroup = \u0027NRC_BuildingSummary\u0027 AND Name = \u0027TotalOperationalCarbon_kgCO2e_per_year\u0027"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["Value"],"rows":[["37196.2"]]}

**Answer:** From ifc_sql, 1 row: the total operational carbon for the building is 37,196.2 kgCO2e per year, stored in the NRC_BuildingSummary property set as TotalOperationalCarbon_kgCO2e_per_year.

Turns 4; input tokens 47941; output tokens 749.

### Which storey has the higher mean energy intensity, Level 1 or Level 2?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "energy"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":5,"skip":0,"count":5,"items":[{"propertySet":"NRC_BuildingSummary","name":"MeanEnergyUs…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT e.Name, e.StepId, p.Value\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE e.Category = \u0027IFCBUILDINGSTOREY\u0027\nAND p.ParameterGroup = \u0027NRC_StoreySummary\u0027\nAND p.Name = \u0027MeanEnergyUseIntensity_kWh_per_m2_year\u0027\nORDER BY e.Name"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["Name","StepId","Value"],"rows":[["Level 1",39,"40.5"],["Level 2",43,"40.56"],["Roof",51,"62.04"],["T/FDN",47,"61.76"]]…

**Answer:** From ifc_sql, 4 rows: Level 2 has the higher mean energy intensity at 40.56 kWh/m²/year compared to Level 1's 40.5 kWh/m²/year, though the difference is minimal. The values come from the NRC_StoreySummary property set's MeanEnergyUseIntensity_kWh_per_m2_year property.

Turns 4; input tokens 46896; output tokens 996.

### Which five elements have the highest operational carbon?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "operational carbon"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":10,"skip":0,"count":10,"items":[{"propertySet":"NRC_BuildingSummary","name":"TotalEmbod…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  e.GlobalId,\n  e.Name,\n  e.Category,\n  CAST(p.Value AS DOUBLE) AS OperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\n  AND p.ParameterGroup = \u0027NRC_OperationalCarbon\u0027\nORDER BY CAST(p.Value AS DOUBLE) DESC\nLIMIT 5\n"
}
```

**Result** {"total":5,"skip":0,"count":5,"columns":["GlobalId","Name","Category","OperationalCarbon_kgCO2e_per_year"],"rows":[["0iEHWY1$XA8eQeeULq4jpl","Basic Wall:Interio…

**Answer:** From ifc_sql, the five elements with the highest operational carbon (in the NRC_OperationalCarbon property set) are:

1. Basic Wall: Interior - Partition (92mm Stud) at 412 kgCO2e per year
2. Basic Wall: Exterior - Brick on Block at 410.8 kgCO2e per year
3. M_Upper Cabinet-Double Door-Wall (1000mm x 1000mm) at 402 kgCO2e per year
4. Basic Wall: Interior - Furring (38 mm Stud) at 399.7 kgCO2e per year
5. Basic Wall: Interior - Furring (38 mm Stud) at 398.6 kgCO2e per year

The walls dominate this list, with four of the five top elements being wall types, and the single furnishing element ranks third.

Turns 6; input tokens 74740; output tokens 1380.

### What is the operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z?

I'll help you find the operational carbon for that door. Let me start by opening the file and locating the door with that GlobalId.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_search` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "text": "1hOSvn6df7F8_7GcBWlS8Z"
}
```

**Result** {"total":1,"skip":0,"count":1,"items":[{"id":8066,"type":"IFCDOOR","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173","globalId":"1hOSvn6df7F8_7GcBWlS8Z…

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "id": 8066
}
```

**Result** {"entity":{"id":8066,"type":"IFCDOOR","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173","globalId":"1hOSvn6df7F8_7GcBWlS8Z"},"properties":{"total":74,"…

**Answer:** The operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z is 54 kgCO2e per year (from the NRC_OperationalCarbon property set). This value was calculated as part of analysis run "run-2026-09-17-01" using a grid emission factor of 0.11 kgCO2e per kWh in the Baseline scenario.

Turns 4; input tokens 39271; output tokens 827.

### How much operational carbon is stored per IFC class?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":10,"skip":0,"count":10,"items":[{"propertySet":"NRC_BuildingSummary","name":"TotalEmbod…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  e.Category,\n  COUNT(e.EntityIndex) as ElementCount,\n  SUM(CAST(p.Value AS DOUBLE)) as TotalOperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.ParameterGroup = \u0027NRC_OperationalCarbon\u0027\n  AND p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\nGROUP BY e.Category\nORDER BY TotalOperationalCarbon_kgCO2e_per_year DESC\n"
}
```

**Result** {"total":14,"skip":0,"count":14,"columns":["Category","ElementCount","TotalOperationalCarbon_kgCO2e_per_year"],"rows":[["IFCWALLSTANDARDCASE",56,17547.399999999…

**Answer:** From ifc_sql, 14 rows show operational carbon stored per IFC class in the model. The totals in kgCO2e per year are: IFCWALLSTANDARDCASE 17,547.4 (56 elements), IFCSLAB 5,816.9 (21 elements), IFCFURNISHINGELEMENT 5,766.3 (61 elements), IFCFOOTING 2,086.9 (7 elements), IFCDOOR 1,324.7 (14 elements), IFCCOVERING 985.7 (13 elements), IFCWINDOW 978.9 (24 elements), IFCBEAM 771.6 (8 elements), IFCMEMBER 560 (4 elements), IFCWALL 357.5 (1 element), IFCSTAIRFLIGHT 311.5 (2 elements), IFCSTAIR 272.7 (2 elements), IFCROOF 251.3 (1 element), and IFCRAILING 164.8 (4 elements). Wall standard cases carry the largest annual operational carbon burden, followed by slabs and furnishing elements.

Turns 5; input tokens 62679; output tokens 1789.

### Which analysis run produced these values, and when?

I need to understand which analysis values you're referring to. Let me first open the model and look for analysis metadata.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "Provenance"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "NRC_",
  "take": 20
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":44,"skip":0,"count":20,"items":[{"propertySet":"NRC_AnalyticsProvenance","name":"Analys…

**Answer:** From ifc_parameters, 20 rows, the analysis run is identified in the NRC_AnalyticsProvenance property set: the run ID is "run-2026-09-17-01", computed on 2026-09-17 at 00:00:00 UTC by Ara 3D using the tool nrc-ifc-llm/poc/generate_synthetic_analytics.py. The analysis produced synthetic, illustrative results using methodology that is not based on EN 15978, with metric definitions from the file nrc-metrics.csv (version NRC-metrics-0.2).

Turns 4; input tokens 35847; output tokens 851.

### Which analysed elements carry no embodied-carbon property set?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "embodied"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":6,"skip":0,"count":6,"items":[{"propertySet":"NRC_BuildingSummary","name":"TotalEmbodie…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":10,"skip":0,"count":10,"items":[{"propertySet":"NRC_BuildingSummary","name":"TotalEmbod…

I need to convert the model to BOS format first, then run a query to find analysed elements without the embodied-carbon property set.

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\…

Now let me query to find elements with operational carbon analysis but no embodied carbon property:

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\475a2d0b72c21b3c\\duplex-enriched.bos",
  "sql": "\nSELECT DISTINCT e.StepId, e.GlobalId, e.Name, e.Category\nFROM EntityText e\nWHERE e.EntityIndex IN (\n  SELECT DISTINCT EntityIndex FROM ParameterText \n  WHERE ParameterGroup = \u0027NRC_OperationalCarbon\u0027\n)\nAND e.EntityIndex NOT IN (\n  SELECT DISTINCT EntityIndex FROM ParameterText \n  WHERE ParameterGroup = \u0027NRC_EmbodiedCarbon\u0027\n)\nORDER BY e.StepId\n"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["StepId","GlobalId","Name","Category"],"rows":[[22475,"0jf0rYHfX3RAB3bSIRjmxl","Basic Roof:Live Roof over Wood Joist Fl…

**Answer:** From ifc_sql, 1 row: One analysed element carries no embodied-carbon property set. It is a roof (IFCROOF) named "Basic Roof:Live Roof over Wood Joist Flat Roof:184483" with GlobalId 0jf0rYHfX3RAB3bSIRjmxl. This element has the NRC_OperationalCarbon property set but lacks the NRC_EmbodiedCarbon property set.

Turns 6; input tokens 66019; output tokens 1477.

### What is the total embodied carbon (A1-A3) per storey?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":10,"skip":0,"count":10,"items":[{"propertySet":"NRC_BuildingSummary","name":"TotalEmbod…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT DISTINCT \n  e.Name,\n  p.Value\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE e.Category = \u0027IFCBUILDINGSTOREY\u0027\n  AND p.ParameterGroup = \u0027NRC_StoreySummary\u0027\n  AND p.Name = \u0027TotalEmbodiedCarbon_A1A3_kgCO2e\u0027\nORDER BY e.Name"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["Name","Value"],"rows":[["Level 1","49451.2"],["Level 2","48696.8"],["Roof","5821.0"],["T/FDN","11761.3"]]}

**Answer:** From ifc_sql, 4 rows show the embodied carbon (A1-A3) per storey from the NRC_StoreySummary property set:

Level 1: 49,451.2 kgCO2e
Level 2: 48,696.8 kgCO2e
Roof: 5,821.0 kgCO2e
T/FDN: 11,761.3 kgCO2e

The total embodied carbon (A1-A3) across all storeys is 115,730.3 kgCO2e, as recorded in the NRC_BuildingSummary property set.

Turns 4; input tokens 48489; output tokens 1192.

### Which zone has the highest energy use intensity?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "energy"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":5,"skip":0,"count":5,"items":[{"propertySet":"NRC_BuildingSummary","name":"MeanEnergyUs…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT \n  et.Name,\n  pt.Value AS ZoneEnergyUseIntensity\nFROM EntityText et\nJOIN ParameterText pt ON et.EntityIndex = pt.EntityIndex\nWHERE et.Category = \u0027IFCZONE\u0027\n  AND pt.ParameterGroup = \u0027NRC_ZoneSummary\u0027\n  AND pt.Name = \u0027ZoneEnergyUseIntensity_kWh_per_m2_year\u0027\nORDER BY CAST(pt.Value AS DOUBLE) DESC\nLIMIT 1"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["Name","ZoneEnergyUseIntensity"],"rows":[["Unit B Level 1","78.04"]]}

**Answer:** From ifc_sql, 1 row: the zone "Unit B Level 1" has the highest energy use intensity at 78.04 kWh/m²/year, measured from the NRC_ZoneSummary property set.

Turns 5; input tokens 59964; output tokens 1123.
