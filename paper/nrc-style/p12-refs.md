# References

## Standards and specifications

[1] ISO 16739-1:2024. Industry Foundation Classes (IFC) for data sharing in the construction and facility management industries. buildingSMART IFC 4.3.2 documentation. https://ifc43-docs.standards.buildingsmart.org/

[2] buildingSMART International. Information Delivery Specification (IDS) 1.0, June 2024. https://technical.buildingsmart.org/projects/information-delivery-specification-ids/

[3] buildingSMART International. BIM Collaboration Format (BCF). https://technical.buildingsmart.org/standards/bcf/

[4] Rasmussen, M. H., et al. BOT: The Building Topology Ontology of the W3C Linked Building Data Group. Semantic Web 12(1), 2021.

[5] EN 15978:2011. Sustainability of construction works. Assessment of environmental performance of buildings. Calculation method.

[6] National Research Council of Canada. National Building Code of Canada 2020.

[7] Model Context Protocol specification. https://modelcontextprotocol.io/

## IFC entities cited

`IfcRelDefinesByProperties`, `IfcPropertySet`, `IfcPropertySingleValue` (ref. 1, sections 5.1.3.38, 8.16.3.12); `Pset_EnvironmentalImpactIndicators` (ref. 1, section 5.4.4.14); `IfcElementQuantity` (ref. 1, section 5.4.3.21); `IfcMaterialProperties` (ref. 1, section 8.10.3.16); `IfcDocumentReference`, `IfcRelAssociatesDocument` (ref. 1, section 5.1.3.31); `IfcLibraryInformation` (ref. 1, section 8.6.3.9); `IfcRelAssociatesClassification` (ref. 1, section 5.1.3.30); `IfcPerformanceHistory` (ref. 1, section 5.2.3.1); `IfcMetric`, `IfcRelAssociatesConstraint` (ref. 1, sections 8.3.3.2, 5.2.3.3).

## Software

[8] Ara 3D. BIM Open Toolkit. MIT licence. https://github.com/ara3d/bim-open-toolkit (cited at commit `71790a7`).

[9] Ara 3D. BIM Open Schema specification. https://github.com/ara3d/bim-open-schema

[10] IfcOpenShell. https://ifcopenshell.org/

[11] Bonsai, formerly BlenderBIM. https://bonsaibim.org/

[12] That Open Company. That Open Engine and Components. https://github.com/ThatOpen/engine_components

[13] web-ifc. https://github.com/ThatOpen/engine_web-ifc

[14] xBIM Toolkit and Xplorer. https://xbim.net/

[15] IFClite. https://github.com/ifclite

[16] DuckDB. https://duckdb.org/

[17] Apache Parquet. https://parquet.apache.org/

## Sample models

[18] buildingSMART. Duplex Apartment sample model, `duplex.ifc`, IFC2X3.

[19] Karlsruhe Institute of Technology. FZK-Haus and Institute reference models, `AC20-FZK-Haus.ifc` and `C20-Institute-Var-2.ifc`. https://www.ifcwiki.org/index.php/KIT_IFC_Examples

## Project documents

[20] Statement of Work. `statement-of-work.md`, this repository.

[21] Storing analytics in IFC: options brief. `storing-analytics-in-ifc.md`, this repository.

[22] Information Delivery Specification overview. `ids.md`, this repository.

[23] IFC viewer inventory and test kit. `ifc-viewers.md` and `IFC-Test-Kit/README.md`, this repository.

[24] MCP tools that are able to wrap an IFC. `mcp-ifc.md`, this repository.

[25] BOS toolchain validation evidence inventory. `bos-validation-evidence.md`, this repository.

[26] Door clearance demonstration. `door-clearance-demo.md`, this repository.

[27] Door ground-truth dataset. `IFC-Test-Kit/door_ground_truth.md`, this repository.

[28] AI-assisted architecture planning and design on Git. `ai_assisted_architecture_design_system.md`, this repository.

## Code cited

[29] `Ara3D.Ifc.Editing`: `IfcPropertySetBuilder`, `IfcPatcher`, `IfcDiff`, `IfcPropertyValue`. https://github.com/ara3d/bim-open-toolkit/tree/71790a7/src/Ara3D.Ifc.Editing

[30] `Ara3D.DoorClearance.Tests`: `ComplianceChecker`, `OverrideTests`, `rules/door-clearance-rules.json`. https://github.com/ara3d/bim-open-toolkit/tree/71790a7/tests/Ara3D.DoorClearance.Tests

[31] `Ara3D.Ifc.Mcp` README and `Ara3D.Ifc.Mcp.Tests`. https://github.com/ara3d/bim-open-toolkit/tree/71790a7/src/Ara3D.Ifc.Mcp

[32] `BimOpenFlow.Nodes.Compliance`: `CheckRuleNode`. https://github.com/ara3d/bim-open-toolkit/tree/71790a7/src/BimOpenFlow.Nodes.Compliance

[33] Building a DuckDB BIM Flow graph from natural language. https://github.com/ara3d/bim-open-toolkit/blob/71790a7/docs/bim-flow-mcp-demo.md

[34] AEC world-model terminology. https://github.com/ara3d/bim-open-toolkit/blob/71790a7/docs/aec-world-model-terminology.md
