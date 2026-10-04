# IFC questions answered through the MCP tools

- Date: 2026-10-04 17:12:28 -04:00
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

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:10:30.6196837Z"}

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

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\23f6caf79ae14a21…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT ParameterGroup, Name, Value FROM ParameterText WHERE ParameterGroup LIKE \u0027Pset_NRCBuilding%\u0027 AND Name LIKE \u0027%OperationalCarbon%\u0027"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["ParameterGroup","Name","Value"],"rows":[]}

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT SUM(CAST(Value AS DOUBLE)) AS TotalOperationalCarbon FROM ParameterText WHERE ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027 AND Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027"
}
```

**Result** {"total":1,"skip":0,"count":1,"columns":["TotalOperationalCarbon"],"rows":[[111588.59999999996]]}

**Answer:** From ifc_sql, the total operational carbon for the building is approximately 111,589 kgCO2e per year. This value was calculated by summing the OperationalCarbon_kgCO2e_per_year property from the Pset_NRCOperationalCarbon property set across all 223 building elements that carry this metric.

Turns 6; input tokens 55209; output tokens 1241.

### Which storey has the higher mean energy intensity, Level 1 or Level 2?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:10:30.6196837Z"}

**Agent calls** `ifc_to_bos` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\23f6caf79ae14a21…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "energy"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":1,"skip":0,"count":1,"items":[{"propertySet":"Pset_NRCEnergyPerformance","name":"Energy…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  e.Name as StoreyName,\n  AVG(CAST(p.Value AS DOUBLE)) as MeanEnergyIntensity\nFROM EntityText e\nJOIN StoreyOfElement soe ON e.EntityIndex = soe.EntityIndex\nJOIN ParameterText p ON soe.StoreyIndex = p.EntityIndex\nWHERE p.Name = \u0027EnergyUseIntensity_kWh_per_m2_year\u0027\n  AND p.ParameterGroup = \u0027Pset_NRCEnergyPerformance\u0027\n  AND e.Category = \u0027IFCBUILDINGSTOREY\u0027\nGROUP BY e.Name, soe.StoreyIndex\nORDER BY e.Name\n"
}
```

**Result** {"total":0,"skip":0,"count":0,"columns":["StoreyName","MeanEnergyIntensity"],"rows":[]}

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  soe.StoreyName,\n  AVG(CAST(p.Value AS DOUBLE)) as MeanEnergyIntensity\nFROM StoreyOfElement soe\nJOIN ParameterText p ON soe.EntityIndex = p.EntityIndex\nWHERE p.Name = \u0027EnergyUseIntensity_kWh_per_m2_year\u0027\n  AND p.ParameterGroup = \u0027Pset_NRCEnergyPerformance\u0027\nGROUP BY soe.StoreyName, soe.StoreyIndex\nORDER BY soe.StoreyName\n"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StoreyName","MeanEnergyIntensity"],"rows":[["Level 1",40.4990291262136],["Level 2",40.55698924731183],["Roof",62.03750…

**Answer:** Level 2 has the higher mean energy intensity. From ifc_sql, 4 rows showing the energy intensity per storey: Level 1 has a mean of 40.50 kWh/m²/year while Level 2 has a mean of 40.56 kWh/m²/year from the Pset_NRCEnergyPerformance property set.

Turns 6; input tokens 45369; output tokens 1417.

### Which five elements have the highest operational carbon?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:10:30.6196837Z"}

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

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\23f6caf79ae14a21…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "SELECT e.Name, e.StepId, e.Type, p.Value \nFROM ParameterText p\nJOIN EntityText e ON p.EntityIndex = e.EntityIndex\nWHERE p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027 \nAND p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\nORDER BY CAST(p.Value AS DOUBLE) DESC\nLIMIT 5"
}
```

**Result** {"total":5,"skip":0,"count":5,"columns":["Name","StepId","Type","Value"],"rows":[["#36",36,null,"37196.2"],["Level 1",39,null,"17457.0"],["Level 2",43,null,"139…

**Answer:** From ifc_sql, 5 rows: The five elements with the highest operational carbon are (1) element #36 at 37,196.2 kgCO2e per year, (2) "Level 1" at 17,457 kgCO2e per year, (3) "Level 2" at 13,970.2 kgCO2e per year, (4) "T/FDN" at 4,001.7 kgCO2e per year, and (5) "Roof" at 1,767.3 kgCO2e per year. These values come from the Pset_NRCOperationalCarbon.OperationalCarbon_kgCO2e_per_year property.

Turns 5; input tokens 36439; output tokens 1082.

### What is the operational carbon of the door named M_Single-Flush:0762 x 2032mm?

I'll help you find the operational carbon of that door. Let me start by opening the file and then search for the door by name.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:10:30.6196837Z"}

**Agent calls** `ifc_search` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "text": "M_Single-Flush:0762 x 2032mm"
}
```

**Result** {"total":10,"skip":0,"count":10,"items":[{"id":7989,"type":"IFCOPENINGELEMENT","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173:1","globalId":"1xS3BCk2…

Now let me check the properties of this door to find the operational carbon value:

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "id": 8066
}
```

**Result** {"entity":{"id":8066,"type":"IFCDOOR","name":"M_Single-Flush:0762 x 2032mm:0762 x 2032mm:150173","globalId":"1hOSvn6df7F8_7GcBWlS8Z"},"properties":{"total":74,"…

**Answer:** From ifc_properties with 74 properties returned, the door named M_Single-Flush:0762 x 2032mm has an operational carbon of 54 kg CO2e per year, found in the Pset_NRCOperationalCarbon property set as "OperationalCarbon_kgCO2e_per_year".

Turns 4; input tokens 32367; output tokens 730.

### How much operational carbon is in each category?

I'll help you find the operational carbon by category. Let me start by opening the file and exploring the data.

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:10:30.6196837Z"}

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

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\23f6caf79ae14a21…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n  e.Category,\n  COUNT(DISTINCT e.EntityIndex) as ElementCount,\n  SUM(CAST(p.Value AS DOUBLE)) as TotalOperationalCarbon_kgCO2e_per_year\nFROM EntityText e\nJOIN ParameterText p ON e.EntityIndex = p.EntityIndex\nWHERE p.Name = \u0027OperationalCarbon_kgCO2e_per_year\u0027\n  AND p.ParameterGroup = \u0027Pset_NRCOperationalCarbon\u0027\nGROUP BY e.Category\nORDER BY TotalOperationalCarbon_kgCO2e_per_year DESC\n"
}
```

**Result** {"total":16,"skip":0,"count":16,"columns":["Category","ElementCount","TotalOperationalCarbon_kgCO2e_per_year"],"rows":[["IFCBUILDINGSTOREY",4,37196.2],["IFCBUIL…

**Answer:** From ifc_sql, 16 rows show operational carbon by category. Here's the breakdown of operational carbon (kgCO2e per year) for each category:

**Top contributors:**
- IFCBUILDINGSTOREY: 37,196.2 kgCO2e/year (4 elements)
- IFCBUILDING: 37,196.2 kgCO2e/year (1 element)
- IFCWALLSTANDARDCASE: 17,547.4 kgCO2e/year (56 elements)
- IFCSLAB: 5,816.9 kgCO2e/year (21 elements)
- IFCFURNISHINGELEMENT: 5,766.3 kgCO2e/year (61 elements)
- IFCFOOTING: 2,086.9 kgCO2e/year (7 elements)
- IFCDOOR: 1,324.7 kgCO2e/year (14 elements)
- IFCCOVERING: 985.7 kgCO2e/year (13 elements)
- IFCWINDOW: 978.9 kgCO2e/year (24 elements)
- IFCBEAM: 771.6 kgCO2e/year (8 elements)
- IFCMEMBER: 560.0 kgCO2e/year (4 elements)
- IFCWALL: 357.5 kgCO2e/year (1 element)
- IFCSTAIRFLIGHT: 311.5 kgCO2e/year (2 elements)
- IFCSTAIR: 272.7 kgCO2e/year (2 elements)
- IFCROOF: 251.3 kgCO2e/year (1 element)
- IFCRAILING: 164.8 kgCO2e/year (4 elements)

Turns 5; input tokens 45173; output tokens 1534.

### Which analysis run produced these values, and when?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:10:30.6196837Z"}

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "propertySet": "Pset_NRCAnalyticsProvenance"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":9,"skip":0,"count":9,"items":[{"propertySet":"Pset_NRCAnalyticsProvenance","name":"Anal…

**Answer:** From ifc_parameters, the analytics values in this model were produced by analysis run **"run-2026-09-17-01"**, computed on **2026-09-17 at 00:00:00 UTC** by Ara 3D. The analysis was generated using the tool nrc-ifc-llm/poc/generate_synthetic_analytics.py with methodology described as "Synthetic, illustrative; not EN 15978".

Turns 3; input tokens 25876; output tokens 805.

### What is the embodied carbon of the roof?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:10:30.6196837Z"}

**Agent calls** `ifc_type_counts` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"total":103,"skip":0,"count":100,"items":[{"type":"IFCCARTESIANPOINT","count":8520},{"type":"IFCPROPERTYSINGLEVALUE","count":7651},{"type":"IFCPOLYLOOP","count…

**Agent calls** `ifc_search` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "text": "roof"
}
```

**Result** {"total":10,"skip":0,"count":10,"items":[{"id":51,"type":"IFCBUILDINGSTOREY","name":"Roof","globalId":"1xS3BCk291UvhgP2dvNtSE"},{"id":3707,"type":"IFCSPACE","na…

**Agent calls** `ifc_parameters` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "carbon"
}
```

**Result** {"parameterCount":342,"elementsWithParameters":259,"parameters":{"total":3,"skip":0,"count":3,"items":[{"propertySet":"Pset_NRCEmbodiedCarbon","name":"EmbodiedC…

**Agent calls** `ifc_properties` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "id": 22475
}
```

**Result** {"entity":{"id":22475,"type":"IFCROOF","name":"Basic Roof:Live Roof over Wood Joist Flat Roof:184483","globalId":"0jf0rYHfX3RAB3bSIRjmxl"},"properties":{"total"…

**Agent calls** `ifc_find_by_parameter` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "name": "EmbodiedCarbon_A1A3_kgCO2e",
  "propertySet": "Pset_NRCEmbodiedCarbon",
  "ids": "22475"
}
```

**Result** {"op":"exists","matches":{"total":222,"skip":0,"count":100,"items":[{"entity":{"id":36,"type":"IFCBUILDING","name":"#36","globalId":"1xS3BCk291UvhgP2a6eflK"},"p…

**Agent calls** `ifc_parameter_table` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "names": "EmbodiedCarbon_A1A3_kgCO2e,EmbodiedCarbon_A1A5_kgCO2e",
  "propertySet": "Pset_NRCEmbodiedCarbon",
  "ids": "22475"
}
```

**Result** {"columns":["EmbodiedCarbon_A1A3_kgCO2e","EmbodiedCarbon_A1A5_kgCO2e"],"rows":{"total":1,"skip":0,"count":1,"items":[{"entity":{"id":22475,"type":"IFCROOF","nam…

**Answer:** The IFCROOF element itself (id 22475) does not have embodied carbon values assigned. However, the Roof building storey, which contains the roof assembly, has an embodied carbon value from ifc_find_by_parameter: the embodied carbon A1A3 stage (cradle to gate) is 5821.0 kgCO2e, and from ifc_parameters, the model also carries EmbodiedCarbon_A1A5_kgCO2e values (cradle to end-of-life). This storey-level value likely represents a rollup of all elements in that storey.

Turns 8; input tokens 112857; output tokens 1907.

### What is the total embodied carbon (A1-A3) per storey?

**Agent calls** `ifc_open` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc"
}
```

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","schema":"IFC2X3","entityCount":42664,"openedUtc":"2026-10-04T21:10:30.6196837Z"}

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

**Result** {"path":"C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc","bosPath":"C:\\Users\\cdigg\\AppData\\Local\\Temp\\bimopenmcp-ifc\\23f6caf79ae14a21…

**Agent calls** `ifc_sql` with

```json
{
  "path": "C:\\Users\\cdigg\\git\\nrc-ifc-llm\\poc\\data\\duplex-enriched.ifc",
  "sql": "\nSELECT \n    s.StoreyName,\n    SUM(CAST(p.Value AS DOUBLE)) as TotalEmbodiedCarbon_A1A3_kgCO2e\nFROM ParameterText p\nJOIN StoreyOfElement s ON p.EntityIndex = s.EntityIndex\nWHERE p.Name = \u0027EmbodiedCarbon_A1A3_kgCO2e\u0027 \n    AND p.ParameterGroup = \u0027Pset_NRCEmbodiedCarbon\u0027\nGROUP BY s.StoreyName\nORDER BY s.StoreyName\n"
}
```

**Result** {"total":4,"skip":0,"count":4,"columns":["StoreyName","TotalEmbodiedCarbon_A1A3_kgCO2e"],"rows":[["Level 1",49451.200000000004],["Level 2",48696.8],["Roof",5821…

**Answer:** From ifc_sql, 4 rows: the total embodied carbon (A1-A3) per storey from the Pset_NRCEmbodiedCarbon property set is Level 1: 49,451.2 kgCO2e, Level 2: 48,696.8 kgCO2e, Roof: 5,821 kgCO2e, and T/FDN: 11,761.3 kgCO2e.

Turns 5; input tokens 45089; output tokens 1277.
