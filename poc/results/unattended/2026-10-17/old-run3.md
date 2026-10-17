# IFC questions answered through the MCP tools

- Date: 2026-10-17 18:26:19 -04:00
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

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:19:58.2739963Z"}

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
  "propertySet": "NRC"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":20,"skip":0,"count":20,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"An…

Now let me convert the model to BOS format and query for the total operational carbon:

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
  "sql": "SELECT SUM(CAST(Value AS DOUBLE)) as TotalOperationalCarbon_kgCO2e_per_year\nFROM ParameterText\nWHERE Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\nAND ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\nAND ValueType = \u0027Number\u0027"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["TotalOperationalCarbon_kgCO2e_per_year"],"rows":[[111588.59999999996]]}

**Answer:** The total operational carbon for the building is approximately 111,589 kgCO2e per year. This comes from ifc_sql summing the OperationalCarbon_kgCO2e_per_year property (from the Pset_NRCOperationalCarbon property set) across all 223 elements in the model that carry this metric.

Turns 6; input tokens 79835; output tokens 1537.

### Which storey has the higher mean energy intensity, Level 1 or Level 2?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:19:58.2739963Z"}

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
  "sql": "SELECT \n  s.StoreyName,\n  AVG(CAST(p.Value AS DOUBLE)) as MeanEnergyIntensity\nFROM StoreyOfElement s\nJOIN ParameterText p ON s.EntityIndex = p.EntityIndex\nWHERE p.Name = \u0027EnergyUseIntensity_kWh_per_m2_year\u0027\nGROUP BY s.StoreyName\nORDER BY s.StoreyName"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StoreyName","MeanEnergyIntensity"],"rows":[["Level 1",40.4990291262136],["Level 2",40.55698924731183],["Roof",62.03750…

**Answer:** From ifc_sql, Level 2 has the higher mean energy intensity: 40.56 kWh/m²/year compared to Level 1's 40.50 kWh/m²/year. The difference is small—just 0.06 kWh/m²/year.

Turns 6; input tokens 64013; output tokens 1379.

### Which five elements have the highest operational carbon?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:19:58.2739963Z"}

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
  "sql": "SELECT \n  et.GlobalId, \n  et.Name, \n  et.Category,\n  pt.Value AS OperationalCarbon_kgCO2e_per_year\nFROM EntityText et\nJOIN ParameterText pt ON et.EntityIndex = pt.EntityIndex\nWHERE pt.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027 \n  AND pt.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\nORDER BY CAST(pt.Value AS DOUBLE) DESC\nLIMIT 5"
}
```

**Result** {"total":5,"skip":0,"count":5,"columns":["GlobalId","Name","Category","OperationalCarbon_kgCO2e_per_year"],"rows":[["1xS3BCk291UvhgP2a6eflK",null,"IFCBUILDING",…

**Answer:** From ifc_sql, 5 rows show the five elements with the highest operational carbon: the Building (37,196.2 kgCO2e per year), Level 1 (17,457.0), Level 2 (13,970.2), T/FDN (4,001.7), and Roof (1,767.3), all from the Pset_NRCOperationalCarbon property set. These values represent annual operational carbon emissions measured in kilograms of CO2 equivalent.

Turns 5; input tokens 59081; output tokens 1216.

### What is the operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z?

I'll help you find the operational carbon of that door. Let me start by opening the IFC file and then locating the specific door.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:19:58.2739963Z"}

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

**Answer:** The operational carbon of the door with GlobalId 1hOSvn6df7F8_7GcBWlS8Z is 54 kgCO2e per year, from ifc_properties which returned 74 properties including those in the Pset_NRCOperationalCarbon property set. The analysis was run under the "Baseline" scenario with a grid emission factor of 0.11 kgCO2e per kWh.

Turns 4; input tokens 39265; output tokens 837.

### How much operational carbon is stored per IFC class?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:19:58.2739963Z"}

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
  "sql": "\nSELECT \n  e.Category,\n  COUNT(DISTINCT e.EntityIndex) as ElementCount,\n  SUM(CAST(p.Value AS DOUBLE)) as TotalOperationalCarbon_kgCO2e_per_year,\n  AVG(CAST(p.Value AS DOUBLE)) as AvgOperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\n  AND p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\nGROUP BY e.Category\nORDER BY TotalOperationalCarbon_kgCO2e_per_year DESC\n"
}
```

**Result** {"total":16,"skip":0,"count":16,"columns":["Category","ElementCount","TotalOperationalCarbon_kgCO2e_per_year","AvgOperationalCarbon_kgCO2e_per_year"],"rows":[["…

**Answer:** From ifc_sql, 16 rows show operational carbon (OperationalCarbon_kgCO2e_per_year from Pset_NRCOperationalCarbon) per IFC class. Building storeys carry the most at 37,196 kg CO₂e per year total across 4 storeys (9,299 kg CO₂e per year average), followed by wall standard cases at 17,547 kg CO₂e per year across 56 elements. Slabs contribute 5,817 kg CO₂e per year (277 per element average), furnishing elements 5,766 kg CO₂e per year across 61 items, footings 2,087 kg CO₂e per year across 7 items, doors 1,325 kg CO₂e per year across 14 items, and smaller amounts from coverings, windows, beams, members, stairs, roofs and railings, down to railings at 165 kg CO₂e per year across 4 items.

Turns 5; input tokens 59549; output tokens 1289.

### Which analysis run produced these values, and when?

I need to explore the model to find analytics run information. Let me start by opening the file and checking for analytics metadata.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:19:58.2739963Z"}

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
  "name": "provenance"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "propertySet": "NRC_"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "NRC"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":0,"skip":0,"count":0,"items":[]}}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "take": 50
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":342,"skip":0,"count":50,"items":[{"propertySet":"GSA Space Areas","name":"GSA BIM Area"…

**Answer:** Perfect! I found the analytics provenance information. The analysis values in this model were produced by **run-2026-09-17-01**, computed on **September 17, 2026 at 00:00:00 UTC**. From ifc_parameters, the Pset_NRCAnalyticsProvenance property set shows the analysis was performed by Ara 3D using the source tool nrc-ifc-llm/poc/generate_synthetic_analytics.py, based on the NRC-metrics-0.1 metric dictionary version. The methodology is noted as synthetic and illustrative, not conforming to EN 15978 standard.

Turns 7; input tokens 65895; output tokens 1383.

### Which analysed elements carry no embodied-carbon property set?

I'll help you find which analyzed elements lack an embodied-carbon property set. Let me start by opening the file and exploring the available property sets.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:19:58.2739963Z"}

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
  "name": "carbon",
  "take": 100
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT DISTINCT e.GlobalId, e.Name, e.Category\nFROM EntityText e\nWHERE e.EntityIndex IN (\n  SELECT DISTINCT EntityIndex FROM ParameterText \n  WHERE ParameterGroup LIKE \u0027NRC_%\u0027\n)\nORDER BY e.Category, e.Name",
  "take": 500
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["GlobalId","Name","Category"],"rows":[]}

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT DISTINCT ParameterGroup \nFROM ParameterText \nWHERE ParameterGroup LIKE \u0027%Carbon%\u0027 OR ParameterGroup LIKE \u0027NRC_%\u0027\nORDER BY ParameterGroup"
}
```

**Result** {"total":2,"skip":0,"count":2,"columns":["ParameterGroup"],"rows":[["Pset_NRCEmbodiedCarbon"],["Pset_NRCOperationalCarbon"]]}

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT DISTINCT e.GlobalId, e.Name, e.Category\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\nAND e.EntityIndex NOT IN (\n  SELECT DISTINCT EntityIndex FROM ParameterText \n  WHERE ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\n)\nORDER BY e.Category, e.Name",
  "take": 500
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["GlobalId","Name","Category"],"rows":[["0jf0rYHfX3RAB3bSIRjmxl","Basic Roof:Live Roof over Wood Joist Flat Roof:184483"…

**Answer:** From ifc_sql, 1 row: One analyzed element carries no embodied-carbon property set. It is an IFCROOF element named "Basic Roof:Live Roof over Wood Joist Flat Roof:184483" (GlobalId 0jf0rYHfX3RAB3bSIRjmxl). This roof element has the Pset_NRCOperationalCarbon property set but lacks Pset_NRCEmbodiedCarbon.

Turns 7; input tokens 86001; output tokens 1813.

### What is the total embodied carbon (A1-A3) per storey?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:19:58.2739963Z"}

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

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "SELECT \n  StoreyName,\n  SUM(CAST(ParameterText.Value AS DOUBLE)) as Total_EmbodiedCarbon_A1A3_kgCO2e\nFROM StoreyOfElement\nJOIN ParameterText ON StoreyOfElement.EntityIndex = ParameterText.EntityIndex\nWHERE ParameterText.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027\n  AND ParameterText.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\nGROUP BY StoreyName\nORDER BY StoreyName"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StoreyName","Total_EmbodiedCarbon_A1A3_kgCO2e"],"rows":[["Level 1",49451.2],["Level 2",48696.79999999999],["Roof",5821…

**Answer:** From ifc_sql, 4 rows: The total embodied carbon (A1-A3) per storey, from Pset_NRCEmbodiedCarbon.EmbodiedCarbon_A1A3_kgCO2e, is Level 1 at 49,451.2 kgCO2e, Level 2 at 48,696.8 kgCO2e, T/FDN at 11,761.3 kgCO2e, and Roof at 5,821 kgCO2e.

Turns 6; input tokens 51892; output tokens 1366.

### Which zone has the highest energy use intensity?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-17T22:19:58.2739963Z"}

**Agent calls** `ifc_type_counts` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"total":103,"skip":0,"count":100,"items":[{"type":"IFCCARTESIANPOINT","count":8520},{"type":"IFCPROPERTYSINGLEVALUE","count":7651},{"type":"IFCPOLYLOOP","count…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "energy"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":271,"parameters":{"total":1,"skip":0,"count":1,"items":[{"propertySet":"Pset_NRCEnergyPerformance","name":"Energy…

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
  "sql": "SELECT \n  e.GlobalId,\n  e.Name AS ZoneName,\n  e.Category,\n  p.Value AS EnergyUseIntensity\nFROM EntityText e\nLEFT JOIN ParameterText p ON e.EntityIndex = p.EntityIndex \n  AND p.Name = \u0027EnergyUseIntensity_kWh_per_m2_year\u0027\nWHERE e.Category = \u0027IFCZONE\u0027\nORDER BY CAST(COALESCE(p.Value, \u00270\u0027) AS DOUBLE) DESC"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["GlobalId","ZoneName","Category","EnergyUseIntensity"],"rows":[]}

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "SELECT \n  e.GlobalId,\n  e.Name,\n  e.Category,\n  p.Value AS EnergyUseIntensity\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex \n  AND p.Name = \u0027EnergyUseIntensity_kWh_per_m2_year\u0027\nORDER BY CAST(p.Value AS DOUBLE) DESC\nLIMIT 20"
}
```

**Result** {"total":20,"skip":0,"count":20,"columns":["GlobalId","Name","Category","EnergyUseIntensity"],"rows":[["0dxE1Sy6nDqfpDb5vIMN_Z","Basic Wall:Interior - Furring (…

**Agent calls** `ifc_spatial_tree` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","roots":[{"id":34,"type":"IFCPROJECT","name":"0001","elementCount":0,"children":[{"…

**Agent calls** `bos_sql` with

```json
{
  "bosPath": "C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp\\bos\\fa7c72e02fc41b10\\duplex-enriched.bos",
  "sql": "SELECT DISTINCT Category FROM EntityText WHERE Category LIKE \u0027%ZONE%\u0027 OR Category LIKE \u0027%zone%\u0027"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["Category"],"rows":[]}

**Answer:** The model does not contain any zones. The spatial structure includes building storeys and spaces (rooms), but no IFCZONE entities. The energy use intensity values are stored at the element level (walls, slabs, furnishing elements), not aggregated to zones or spaces. The highest energy use intensity among individual elements is 90.9 kWh/m²/year, from ifc_sql showing 218 elements with the EnergyUseIntensity_kWh_per_m2_year property.

Turns 9; input tokens 123589; output tokens 2130.
