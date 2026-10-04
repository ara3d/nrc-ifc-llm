# IFC questions answered through the MCP tools

- Date: 2026-10-04 17:10:08 -04:00
- Language model: claude-haiku-4-5-20251001 (claude-cli, effort medium)
- IFC model: `C:\Users\cdigg\git\nrc-ifc-llm\bim-open-toolkit\samples\nrc\duplex-enriched.ifc`
- Toolkit commit: `59aeb6d`

### What is the total operational carbon for the building?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42657,"openedUtc":"2026-10-04T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":359,"elementsWithParameters":259,"parameters":{"total":9,"skip":0,"count":9,"items":[{"propertySet":"Pset_NRCBuildingSummary","name":"TotalEmb…

**Agent calls** `ifc_parameter_values` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "TotalOperationalCarbon_kgCO2e_per_year",
  "propertySet": "Pset_NRCBuildingSummary"
}
```

**Result** {"name":"TotalOperationalCarbon_kgCO2e_per_year","propertySets":["Pset_NRCBuildingSummary"],"values":{"total":1,"skip":0,"count":1,"items":[{"value":"37196.2","…

**Answer:** The total operational carbon for the building is 37,196.2 kgCO2e per year, from ifc_parameter_values returning 1 row. This value is stored in the Pset_NRCBuildingSummary property set as TotalOperationalCarbon_kgCO2e_per_year.

Turns 4; input tokens 36601; output tokens 791.

### Which storey has the higher mean energy intensity, Level 1 or Level 2?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42657,"openedUtc":"2026-10-04T…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "energy"
}
```

**Result** {"parameterCount":359,"elementsWithParameters":259,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCBuildingSummary","name":"MeanEner…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT \n  e.Name,\n  p.Value,\n  p.ParameterGroup\nFROM EntityText e\nLEFT JOIN ParameterText p ON e.EntityIndex = p.EntityIndex\n  AND p.ParameterGroup = \u0027Pset_NRCStoreySummary\u0027\n  AND p.Name = \u0027MeanEnergyUseIntensity_kWh_per_m2_year\u0027\nWHERE e.Category = \u0027IFCBUILDINGSTOREY\u0027\n  AND (e.Name = \u0027Level 1\u0027 OR e.Name = \u0027Level 2\u0027)\nORDER BY e.Name"
}
```

**Result** {"total":2,"skip":0,"count":2,"columns":["Name","Value","ParameterGroup"],"rows":[["Level 1","40.5","Pset_NRCStoreySummary"],["Level 2","40.56","Pset_NRCStoreyS…

**Answer:** From ifc_sql, 2 rows: Level 1 has a mean energy use intensity of 40.5 kWh per m² per year, while Level 2 has 40.56 kWh per m² per year (from Pset_NRCStoreySummary). Level 2 has the higher mean energy intensity, though the difference is minimal at 0.06 kWh per m² per year.

Turns 5; input tokens 45033; output tokens 1232.

### Which five elements have the highest operational carbon?

I'll help you find the five elements with the highest operational carbon. Let me start by opening the model and exploring the available data.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42657,"openedUtc":"2026-10-04T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "operational"
}
```

**Result** {"parameterCount":359,"elementsWithParameters":259,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCBuildingSummary","name":"TotalOpe…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT \n  e.Name, \n  e.Type,\n  CAST(p.Value AS DOUBLE) as OperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027 \n  AND p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\nORDER BY CAST(p.Value AS DOUBLE) DESC\nLIMIT 5"
}
```

**Result** {"total":5,"skip":0,"count":5,"columns":["Name","Type","OperationalCarbon_kgCO2e_per_year"],"rows":[["Basic Wall:Interior - Partition (92mm Stud):190140",null,4…

**Answer:** From ifc_sql, 5 rows: the five elements with the highest operational carbon are:

1. "Basic Wall:Interior - Partition (92mm Stud):190140" with 412 kgCO2e/year
2. "Basic Wall:Exterior - Brick on Block:185101" with 410.8 kgCO2e/year
3. "M_Upper Cabinet-Double Door-Wall:1000mm:1000mm:192610" with 402 kgCO2e/year
4. "Basic Wall:Interior - Furring (38 mm Stud):217415" with 399.7 kgCO2e/year
5. "Basic Wall:Interior - Furring (38 mm Stud):217414" with 398.6 kgCO2e/year

All five are primarily wall elements, with most being interior partition or furring walls, plus one exterior brick-on-block wall and one cabinet assembly.

Turns 5; input tokens 45250; output tokens 1252.

### What is the operational carbon of the door named M_Single-Flush:0762 x 2032mm?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42657,"openedUtc":"2026-10-04T…

**Agent calls** `ifc_search` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "text": "M_Single-Flush:0762 x 2032mm"
}
```

**Result** {"total":10,"skip":0,"count":10,"items":[{"id":7989,"type":"IFCOPENINGELEMENT","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173:1","globalId":"1xS3BCk2…

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "id": 8066
}
```

**Result** {"entity":{"id":8066,"type":"IFCDOOR","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173","globalId":"1hOSvn6df7F8_7GcBWlS8Z"},"properties":{"total":74,"…

**Answer:** From ifc_properties, the door named M_Single-Flush:0762 x 2032mm (entity id 8066) has an operational carbon value of 54 kgCO2e per year, found in the Pset_NRCOperationalCarbon property set under the property OperationalCarbon_kgCO2e_per_year.

Turns 4; input tokens 32406; output tokens 741.

### How much operational carbon is in each category?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42657,"openedUtc":"2026-10-04T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "operational"
}
```

**Result** {"parameterCount":359,"elementsWithParameters":259,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCBuildingSummary","name":"TotalOpe…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  e.Category,\n  COUNT(DISTINCT e.EntityIndex) as ElementCount,\n  SUM(CAST(p.Value AS DOUBLE)) as TotalOperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\n  AND p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\nGROUP BY e.Category\nORDER BY TotalOperationalCarbon_kgCO2e_per_year DESC\n"
}
```

**Result** {"total":14,"skip":0,"count":14,"columns":["Category","ElementCount","TotalOperationalCarbon_kgCO2e_per_year"],"rows":[["IFCWALLSTANDARDCASE",56,17547.399999999…

**Answer:** From ifc_sql, 14 rows show operational carbon per category. Walls (IFCWALLSTANDARDCASE) account for the largest share at 17,547 kgCO2e per year, followed by slabs at 5,817 kgCO2e per year and furnishing elements at 5,766 kgCO2e per year. The remaining categories each contribute less than 2,100 kgCO2e per year, with railings being the smallest at 165 kgCO2e per year. The total across all 218 elements is approximately 37,196 kgCO2e per year.

Turns 5; input tokens 45490; output tokens 1413.

### Which analysis run produced these values, and when?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42657,"openedUtc":"2026-10-04T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "Pset_NRCAnalyticsProvenance"
}
```

**Result** {"parameterCount":359,"elementsWithParameters":259,"parameters":{"total":12,"skip":0,"count":12,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

**Answer:** The analysis run was performed by Ara 3D on September 17, 2026 at 00:00:00 UTC, with analysis run ID "run-2026-09-17-01", according to the Pset_NRCAnalyticsProvenance property set found in the model. The methodology is noted as synthetic and illustrative, using metric dictionary version NRC-metrics-0.2 with a grid emission factor of 0.11 kgCO2e per kWh.

Turns 3; input tokens 17993; output tokens 749.

### What is the embodied carbon of the roof?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42657,"openedUtc":"2026-10-04T…

**Agent calls** `ifc_search` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "text": "roof"
}
```

**Result** {"total":10,"skip":0,"count":10,"items":[{"id":51,"type":"IFCBUILDINGSTOREY","name":"Roof","globalId":"1xS3BCk291UvhgP2dvNtSE"},{"id":3707,"type":"IFCSPACE","na…

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "id": 22475
}
```

**Result** {"entity":{"id":22475,"type":"IFCROOF","name":"Basic Roof:Live Roof over Wood Joist Flat Roof:184483","globalId":"0jf0rYHfX3RAB3bSIRjmxl"},"properties":{"total"…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "embodied carbon"
}
```

**Result** {"parameterCount":359,"elementsWithParameters":259,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

Let me search more specifically for embodied carbon parameters in the model:

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":359,"elementsWithParameters":259,"parameters":{"total":9,"skip":0,"count":9,"items":[{"propertySet":"Pset_NRCBuildingSummary","name":"TotalEmb…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "Pset_NRC"
}
```

**Result** {"parameterCount":359,"elementsWithParameters":259,"parameters":{"total":37,"skip":0,"count":37,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

Now let me check if the roof element has the embodied carbon properties:

**Agent calls** `ifc_find_by_parameter` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "Pset_NRCEmbodiedCarbon",
  "name": "EmbodiedCarbon_A1A3_kgCO2e",
  "ids": "22475"
}
```

**Result** {"op":"exists","matches":{"total":217,"skip":0,"count":100,"items":[{"entity":{"id":3797,"type":"IFCWALLSTANDARDCASE","name":"Basic Wall:Exterior - Brick on Blo…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT e.StepId, e.Name, e.Type, p.Name, p.Value FROM EntityText e LEFT JOIN ParameterText p ON e.EntityIndex = p.EntityIndex WHERE e.StepId = 22475 AND p.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["StepId","Name","Type","Name_1","Value"],"rows":[]}

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT e.StepId, e.Name, e.Type, p.Name, p.ParameterGroup, p.Value FROM EntityText e LEFT JOIN ParameterText p ON e.EntityIndex = p.EntityIndex WHERE e.StepId = 22475 AND p.ParameterGroup LIKE \u0027Pset_NRC%\u0027"
}
```

**Result** {"total":7,"skip":0,"count":7,"columns":["StepId","Name","Type","Name_1","ParameterGroup","Value"],"rows":[[22475,"Basic Roof:Live Roof over Wood Joist Flat Roo…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT e.Type, COUNT(*) as count FROM EntityText e JOIN ParameterText p ON e.EntityIndex = p.EntityIndex WHERE e.Category = \u0027IFCROOF\u0027 AND p.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 GROUP BY e.Type"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["Type","count"],"rows":[]}

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "SELECT e.StepId, e.Name, e.Type, p.Name, p.Value FROM EntityText e JOIN ParameterText p ON e.EntityIndex = p.EntityIndex WHERE e.Name LIKE \u0027%Roof%\u0027 AND p.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027 LIMIT 20"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StepId","Name","Type","Name_1","Value"],"rows":[[22492,"Basic Roof:Live Roof over Wood Joist Flat Roof:184483",null,"A…

Perfect! I found the embodied carbon data for the roof. Let me verify this is the correct element:

**Agent calls** `ifc_entity` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "id": 22492
}
```

**Result** {"entity":{"id":22492,"type":"IFCSLAB","name":"Basic Roof:Live Roof over Wood Joist Flat Roof:184483","globalId":"3ThA22djr8AQQ9eQMA5s7I"},"attributes":[{"index…

**Answer:** The embodied carbon of the roof is found in the model, from ifc_sql, 4 rows. The roof element (an IFCSLAB with type ".ROOF." named "Basic Roof:Live Roof over Wood Joist Flat Roof:184483") carries embodied carbon data in the Pset_NRCEmbodiedCarbon property set: **1838.5 kg CO2e (A1-A3, cradle to gate)** and **2059.1 kg CO2e (A1-A5, cradle to site)**. The A1-A3 figure represents production and transport, while the A1-A5 figure additionally includes installation impacts.

Turns 14; input tokens 292569; output tokens 3422.

### What is the total embodied carbon (A1-A3) per storey?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42657,"openedUtc":"2026-10-04T…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":359,"elementsWithParameters":259,"parameters":{"total":9,"skip":0,"count":9,"items":[{"propertySet":"Pset_NRCBuildingSummary","name":"TotalEmb…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  e.Name AS StoreyName,\n  p.Value AS EmbodiedCarbon_A1A3_kgCO2e\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE e.Category = \u0027IFCBUILDINGSTOREY\u0027\n  AND p.ParameterGroup = \u0027Pset_NRCStoreySummary\u0027\n  AND p.Name = \u0027TotalEmbodiedCarbon_A1A3_kgCO2e\u0027\nORDER BY e.Name\n"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StoreyName","EmbodiedCarbon_A1A3_kgCO2e"],"rows":[["Level 1","49451.2"],["Level 2","48696.8"],["Roof","5821.0"],["T/FD…

**Answer:** From ifc_sql, 4 rows: The model's Pset_NRCStoreySummary property set holds the total embodied carbon (A1-A3) per storey:

Level 1: 49,451.2 kgCO2e
Level 2: 48,696.8 kgCO2e
Roof: 5,821.0 kgCO2e
T/FDN: 11,761.3 kgCO2e

Turns 5; input tokens 48075; output tokens 1284.
