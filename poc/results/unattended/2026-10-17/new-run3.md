# IFC questions answered through the MCP tools

- Date: 2026-10-17 18:25:36 -04:00
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

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "propertySet": "NRC_"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":44,"skip":0,"count":44,"items":[{"propertySet":"NRC_AnalyticsProvenance","name":"Analys…

**Answer:** The total operational carbon for the building is 37,196.2 kgCO2e per year, from the ifc_parameters search in the NRC_BuildingSummary property set. This figure includes 218 building elements and was computed in the "Baseline" scenario using an illustrative methodology with a grid emission factor of 0.11 kgCO2e per kWh.

Turns 5; input tokens 41161; output tokens 979.

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
  "sql": "\nSELECT \n  et.Name AS StoreyName,\n  pt.Value AS MeanEnergyUseIntensity\nFROM EntityText et\nJOIN ParameterText pt ON et.EntityIndex = pt.EntityIndex\nWHERE et.Category = \u0027IFCBUILDINGSTOREY\u0027\n  AND pt.ParameterGroup = \u0027NRC_StoreySummary\u0027\n  AND pt.Name = \u0027MeanEnergyUseIntensity_kWh_per_m2_year\u0027\n  AND et.Name IN (\u0027Level 1\u0027, \u0027Level 2\u0027)\nORDER BY et.Name\n"
}
```

**Result** {"total":2,"skip":0,"count":2,"columns":["StoreyName","MeanEnergyUseIntensity"],"rows":[["Level 1","40.5"],["Level 2","40.56"]]}

**Answer:** From ifc_sql, 2 rows show that Level 2 has the higher mean energy intensity at 40.56 kWh/m²/year, compared to Level 1's 40.5 kWh/m²/year. The values come from the NRC_StoreySummary property set.

Turns 5; input tokens 60117; output tokens 1230.

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

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\475a2d0b72c21b3c\\duplex-enriched.bos",
  "sql": "SELECT e.GlobalId, e.Name, e.Category, p.Value\nFROM ParameterText p\nJOIN EntityText e ON p.EntityIndex = e.EntityIndex\nWHERE p.ParameterGroup = \u0027NRC_OperationalCarbon\u0027 \n  AND p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\nORDER BY CAST(p.Value AS DOUBLE) DESC\nLIMIT 5"
}
```

**Result** {"total":5,"skip":0,"count":5,"columns":["GlobalId","Name","Category","Value"],"rows":[["0iEHWY1$XA8eQeeULq4jpl","Basic Wall:Interior - Partition (92mm Stud):19…

**Answer:** The five elements with the highest operational carbon, from ifc_sql (5 rows), are: a Basic Wall Interior Partition with 412 kgCO2e per year, a Basic Wall Exterior Brick on Block with 410.8 kgCO2e per year, an Upper Cabinet Double Door furnishing element with 402 kgCO2e per year, and two Basic Wall Interior Furring elements with 399.7 and 398.6 kgCO2e per year respectively. These operational carbon values come from the NRC_OperationalCarbon property set.

Turns 5; input tokens 62424; output tokens 1148.

### What is the operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z?

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

**Answer:** The operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z is 54.0 kgCO2e per year, from ifc_properties in the NRC_OperationalCarbon property set.

Turns 4; input tokens 39206; output tokens 707.

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
  "sql": "\nSELECT \n  e.Category,\n  COUNT(*) as ElementCount,\n  SUM(CAST(p.Value AS DOUBLE)) as TotalOperationalCarbon_kgCO2e_per_year,\n  AVG(CAST(p.Value AS DOUBLE)) as AvgOperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.ParameterGroup = \u0027NRC_OperationalCarbon\u0027 \n  AND p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\nGROUP BY e.Category\nORDER BY TotalOperationalCarbon_kgCO2e_per_year DESC\n"
}
```

**Result** {"total":14,"skip":0,"count":14,"columns":["Category","ElementCount","TotalOperationalCarbon_kgCO2e_per_year","AvgOperationalCarbon_kgCO2e_per_year"],"rows":[["…

**Answer:** From ifc_sql, 14 rows show operational carbon per IFC class in the model. The property set NRC_OperationalCarbon contains OperationalCarbon_kgCO2e_per_year values for 218 elements.

Operational carbon storage by IFC class (in kgCO2e per year):

IFCWALLSTANDARDCASE accounts for the largest share at 17,547 kgCO2e/year across 56 elements. IFCSLAB contributes 5,817 kgCO2e/year across 21 elements. IFCFURNISHINGELEMENT contributes 5,766 kgCO2e/year across 61 elements. The remaining 11 classes (IFCFOOTING, IFCDOOR, IFCCOVERING, IFCWINDOW, IFCBEAM, IFCMEMBER, IFCWALL, IFCSTAIRFLIGHT, IFCSTAIR, IFCROOF, IFCRAILING) collectively contribute 5,963 kgCO2e/year. The total operational carbon for the building is approximately 37,196 kgCO2e per year.

Turns 5; input tokens 62781; output tokens 1543.

### Which analysis run produced these values, and when?

I need to see what values you're referring to. Let me first open the model to look for analysis provenance information.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

**Agent calls** `ifc_entities_of_type` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "type": "IFCPROJECT"
}
```

**Result** {"total":1,"skip":0,"count":1,"items":[{"id":34,"type":"IFCPROJECT","name":"0001","globalId":"1xS3BCk291UvhgP2a6eflL"}]}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "name": "provenance"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc",
  "id": 34
}
```

**Result** {"entity":{"id":34,"type":"IFCPROJECT","name":"0001","globalId":"1xS3BCk291UvhgP2a6eflL"},"properties":{"total":12,"skip":0,"count":12,"items":[{"propertySet":"…

**Answer:** From ifc_properties on the IFCPROJECT entity, which returned 12 properties: the analysis run was produced by **Ara 3D** on **2026-09-17 at 00:00:00 UTC**, with the analysis run ID **run-2026-09-17-01**. This metadata is stored in the NRC_AnalyticsProvenance property set and indicates the analysis used the "Baseline" scenario with a methodology described as "Synthetic, illustrative; not EN 15978".

Turns 5; input tokens 46727; output tokens 978.

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
  "name": "analys"
}
```

**Result** {"parameterCount":366,"elementsWithParameters":275,"parameters":{"total":7,"skip":0,"count":7,"items":[{"propertySet":"NRC_AnalyticsProvenance","name":"Analysis…

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\…

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\475a2d0b72c21b3c\\duplex-enriched.bos",
  "sql": "WITH analysed_elements AS (\n  SELECT DISTINCT EntityIndex\n  FROM ParameterText\n  WHERE ParameterGroup LIKE \u0027NRC_%\u0027\n),\nelements_with_embodied_carbon AS (\n  SELECT DISTINCT EntityIndex\n  FROM ParameterText\n  WHERE ParameterGroup = \u0027NRC_EmbodiedCarbon\u0027\n)\nSELECT e.EntityIndex, e.GlobalId, e.Name, e.Type\nFROM EntityText e\nWHERE e.EntityIndex IN (SELECT EntityIndex FROM analysed_elements)\nAND e.EntityIndex NOT IN (SELECT EntityIndex FROM elements_with_embodied_carbon)\nORDER BY e.Name"
}
```

**Result** {"total":11,"skip":0,"count":11,"columns":["EntityIndex","GlobalId","Name","Type"],"rows":[[4723,"1xS3BCk291UvhgP2a6eflL","0001",null],[3408,"0jf0rYHfX3RAB3bSIR…

**Answer:** From ifc_sql, 11 analysed elements carry no embodied-carbon property set: the two storeys (Level 1, Level 2), the roof container (Roof), the foundation container (T/FDN), four unit-level spaces (Unit A Level 1, Unit A Level 2, Unit B Level 1, Unit B Level 2), one roof type definition (Basic Roof:Live Roof over Wood Joist Flat Roof:184483), the project element (0001), and one unnamed element. These are spatial containers and type definitions rather than building elements with materials.

Turns 6; input tokens 77040; output tokens 1717.

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
  "sql": "SELECT \n  e.Name as StoreyName,\n  p.Value as EmbodiedCarbon_A1A3_kgCO2e\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.ParameterGroup = \u0027NRC_StoreySummary\u0027\n  AND p.Name = \u0027TotalEmbodiedCarbon_A1A3_kgCO2e\u0027\nORDER BY e.Name"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StoreyName","EmbodiedCarbon_A1A3_kgCO2e"],"rows":[["Level 1","49451.2"],["Level 2","48696.8"],["Roof","5821.0"],["T/FD…

**Answer:** From ifc_sql, 4 rows: The embodied carbon (A1-A3) per storey is Level 1: 49,451.2 kgCO2e, Level 2: 48,696.8 kgCO2e, Roof: 5,821.0 kgCO2e, and T/FDN: 11,761.3 kgCO2e, from the NRC_StoreySummary property set.

Turns 5; input tokens 62353; output tokens 1233.

### Which zone has the highest energy use intensity?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\bim-open-toolkit\\samples\\nrc\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42704,"openedUtc":"2026-10-17T…

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
  "sql": "SELECT DISTINCT Type FROM EntityText WHERE Category = \u0027IFCZONE\u0027"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["Type"],"rows":[[null]]}

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
  "sql": "\nSELECT \n  e.Name AS ZoneName,\n  p.Value AS EnergyUseIntensity\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE e.Category = \u0027IFCZONE\u0027\n  AND p.ParameterGroup = \u0027NRC_ZoneSummary\u0027\n  AND p.Name = \u0027ZoneEnergyUseIntensity_kWh_per_m2_year\u0027\nORDER BY CAST(p.Value AS DOUBLE) DESC\n"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["ZoneName","EnergyUseIntensity"],"rows":[["Unit B Level 1","78.04"],["Unit A Level 1","72.93"],["Unit B Level 2","64.6"…

**Answer:** The zone with the highest energy use intensity is "Unit B Level 1" with 78.04 kWh per m² per year, from ifc_sql returning 4 zone rows sorted by their ZoneEnergyUseIntensity_kWh_per_m2_year property in the NRC_ZoneSummary property set.

Turns 6; input tokens 71860; output tokens 1233.
