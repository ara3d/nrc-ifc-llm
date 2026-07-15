# IDS means **Information Delivery Specification**

In BIM, IDS is a buildingSMART standard for expressing **information requirements in a machine-readable form**, primarily so software can automatically check whether an IFC model contains the required data. The current published standard is **IDS 1.0**, approved as a final buildingSMART standard in June 2024. ([buildingSMART][1])

A useful way to think about IDS is:

> **IDS is an automated checklist or validation contract for an IFC delivery.**

For example, an IDS could state:

* Every `IfcSpace` must have a name and room number.
* Every `IfcDoor` must have a fire rating.
* All air-handling units must have a manufacturer, model number and asset identifier.
* Wall fire ratings must use a particular property and permitted set of values.
* Elements classified as maintainable assets must contain warranty and installation information.

### How an IDS rule works

Each specification normally has two conceptual parts:

1. **Applicability** — which IFC objects the rule applies to
   For example: all `IfcDoor` entities classified as fire doors.

2. **Requirements** — what those objects must contain
   For example: a `FireRating` property with a value matching an allowed pattern.

IDS can define requirements involving IFC entities, classifications, properties, attributes, materials, relationships, values and units. The official format is XML, generally stored as a `.ids` file. ([buildingSMART Technical][2])

### Typical workflow

```text
Client or BIM manager authors an IDS
                  ↓
Design team produces or exports an IFC model
                  ↓
IDS validator checks the IFC against the requirements
                  ↓
Pass/fail results identify missing or incorrect information
                  ↓
The model is corrected and checked again
```

This makes requirements testable during design rather than discovering at handover that rooms, equipment or assets are missing important metadata.

### IDS versus IFC validation

These are related but different:

* **IFC schema validation:** Is this structurally valid IFC?
* **IDS validation:** Does this IFC contain the information required for this project or use case?

An IFC file can therefore be perfectly valid according to the IFC schema but still fail an IDS because, for example, its pumps lack serial numbers or its spaces lack occupancy classifications. buildingSMART describes IDS as the mechanism for project-, organization- and use-case-specific checks beyond general IFC validity. ([buildingSMART Technical][3])

### IDS is not

IDS is generally **not intended to define**:

* detailed geometric requirements, such as minimum clearance geometry;
* coordination clashes;
* construction processes or responsibilities;
* how authoring software should create the model;
* the complete IFC exchange implementation supported by software.

Its primary focus is checking **structured alphanumeric information associated with IFC objects**. More complex geometric validation normally requires a dedicated model-checking or geometry engine. ([buildingSMART][4])

For your NRC analytics work, IDS could be useful for specifying that particular IFC objects **must contain defined analytics property sets**, with required property names, units, data types and permitted values. It could validate that the analytics were delivered correctly, while the IFC itself would carry the actual analytics data.

[1]: https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/?utm_source=chatgpt.com "Information Delivery Specification (IDS)"
[2]: https://technical.buildingsmart.org/projects/information-delivery-specification-ids/?utm_source=chatgpt.com "Information Delivery Specification IDS"
[3]: https://technical.buildingsmart.org/services/validation-service/?utm_source=chatgpt.com "Validation Service - buildingSMART Technical"
[4]: https://www.buildingsmart.org/methods-to-specify-information-requirements-in-digital-construction-projects/?utm_source=chatgpt.com "Methods to specify information requirements in digital ..."
