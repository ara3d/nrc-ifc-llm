<div class="coverpage" markdown="1">

**NRC Publications Archive / Archives des publications du CNRC**

Storing, displaying, and querying building analytics on IFC models with a large language model agent layer

Diggins, Christopher

This publication could be one of several versions: author's original, accepted manuscript or the publisher's version. / La version de cette publication peut être l'une des suivantes : la version prépublication de l'auteur, la version acceptée du manuscrit ou la version de l'éditeur.

For the publisher's version, please access the DOI link below. / Pour consulter la version de l'éditeur, utilisez le lien DOI ci-dessous.

Publisher's version / Version de l'éditeur: https://doi.org/[to be assigned]

**NRC Publications Record / Notice d'Archives des publications de CNRC:**
https://nrc-publications.canada.ca/eng/view/object/?id=[to be assigned]

Access and use of this website and the material on it are subject to the Terms and Conditions set forth at https://nrc-publications.canada.ca/eng/copyright

L'accès à ce site Web et l'utilisation de son contenu sont assujettis aux conditions présentées dans le site https://nrc-publications.canada.ca/fra/droits

Questions? Contact the NRC Publications Archive team at PublicationsArchive-ArchivesPublications@nrc-cnrc.gc.ca.

</div>

<div class="titlepage" markdown="1">

# Storing, displaying, and querying building analytics on IFC models with a large language model agent layer

**Christopher Diggins**

Ara 3D / Studio 2.5

Prepared for the National Research Council of Canada

**CONSTRUCTION**

Report No. A1-XXXXXX.X

Report Date: 2026-09-19

Contract No. [to be assigned]

Agreement date: [to be assigned]

Program: Construction Sector Digitalization and Productivity

</div>

<div class="signaturepage" markdown="1">

**Author**

_________________________
Christopher Diggins
Ara 3D / Studio 2.5

**Approved**

_________________________
[Approver name]
Program Leader

| | |
|---|---|
| Report No. | A1-XXXXXX.X |
| Report Date | 2026-09-19 |
| Contract No. | [to be assigned] |
| Agreement date | [to be assigned] |
| Program | Construction Sector Digitalization and Productivity |
| Pages | [to be completed] |

This report may not be reproduced in whole or in part without the written consent of the National Research Council of Canada and the Client.

</div>

<div class="blankpage" markdown="1">

(This page is intentionally left blank)

</div>

## Table of contents

Executive Summary

1 Background information
2 Scope
3 Who should use this report
4 Definitions and abbreviations
5 Storage of analytics within IFC
6 Display of analytics on IFC geometry
7 The large language model and agent layer
8 Proof of concept and results
9 Limitations
10 Future directions
11 Roadmap for an open bidirectional viewer
12 Conclusions
References
Annex A Property-set definitions
Annex B Rule file schema
Annex C Agent tool surface
Annex D Proof-of-concept gap report

## List of figures

Figure 1 Embodied and operational carbon per storey, drawn as a bar chart by a `chart.bar` node

Figure 2 The same storey aggregates rendered in the Table tab of the dataflow editor

Figure 3 The property values submitted to the byte-exact writer, one row per `IFCPROPERTYSINGLEVALUE`

Figure 4 `duplex-enriched.ifc` coloured by operational carbon through a viridis gradient

Figure 5 The same model coloured by embodied carbon, stages A1 to A3

Figure 6 The `Category` column rendered through a categorical palette, nine categories

Figure 7 Rule DC-W1 verdicts coloured on the 14 doors of the model

Figure 8 The verdict table produced by the `check.rule` node

Figure 9 The property sets of a picked wall, listed beneath the 3D view

Figure 10 Elements per storey obtained from the `StoreyOfEntity` view

Figure 11 Snowdon Towers, 456,598 instances, coloured by category

Figure 12 The Snowdon Towers door schedule, 142 doors, built from two `duck.query` nodes

Figure 13 The door-clearance pipeline: code provision, machine-readable rule, and verdict records

Figure 14 The 3D pane rejecting the Duplex model before the converter and loader were corrected

## List of tables

Table 1 Definitions used in this report

Table 2 Abbreviations used in this report

Table 3 Twelve mechanisms available within IFC 4.3 for carrying analytics

Table 4 Comparison of the twelve mechanisms on four properties

Table 5 Viewers and libraries considered, with the one row obtained from the test kit

Table 6 Model, data, and toolchain of the proof of concept

Table 7 Enrichment counts for case study A

Table 8 Case study A, hand-driven session of 2026-09-17: expected against returned

Table 9 Case study A, unattended `gpt-5` run of 2026-09-18: expected against returned

Table 10 The four door-clearance provisions modelled in case study B

Table 11 Verdict totals for case study B, 14 doors by 4 rules

Table 12 Operations a bidirectional viewer should expose

## Acknowledgments

This work was undertaken for the National Research Council of Canada under the Construction Sector Digitalization and Productivity program. The author thanks the NRC project team for the statement of work that framed the three objectives addressed here, and for the Information Delivery Specification framework that shaped the storage recommendation in Section 5.

The proof of concept is built on the open-source BIM Open Toolkit, released under the MIT licence by Ara 3D. The buildingSMART Duplex Apartment model and the Karlsruhe Institute of Technology reference models were used as public test data.

## DISCLAIMER

This report has been prepared under the Construction Sector Digitalization and Productivity program of the National Research Council of Canada. It is based on the best knowledge available at the time of publication. The analytics values reported in case study A are synthetic and are identified as such wherever they appear; they are not measured results and are not fit for any assessment purpose. The code citations in the rule file of case study B are illustrative paraphrases and are not reproductions of legal text; they have not been reviewed by a code authority. Neither the National Research Council of Canada nor the author accepts liability for any use made of the information contained in this report.

## Executive Summary

Building performance analytics such as embodied carbon, operational carbon, and energy use intensity are ordinarily computed by tools that sit outside the building information model, and the results are delivered as spreadsheets and reports that cannot be joined back to the geometry, cannot be validated against an information requirement, and cannot be interrogated in plain language. This report addresses three connected questions for openBIM workflows built on the Industry Foundation Classes (IFC) [1]: where analytics should be stored so that they travel with the model, how they should be displayed on the geometry, and how a large language model (LLM) can be placed in front of an enriched model so that it may be queried in natural language. The three questions correspond to the three objectives of the statement of work [20], and the report is organised around them.

Twelve storage mechanisms available within the IFC 4.3 schema were compared on portability, queryability, interoperability, and scalability, and a three-layer approach is recommended: scalar summary values held in custom property sets at element, space, storey, and building level; a reference from the IFC file to a richer external columnar dataset joined on `GlobalId`; and a metric dictionary that fixes names, units, and lifecycle stages so that queries resolve reliably. Display techniques and openly available viewers were surveyed, and colour mapping driven by the same tables in which the analytics are stored is recommended, with aggregated views alongside. For the query layer, it is recommended that the raw IFC file not be given to the language model, and that a small typed read-only tool surface be exposed over the Model Context Protocol (MCP) [7] instead. An implementation is described that converts IFC to the columnar BIM Open Schema, loads it into DuckDB, exposes 29 tools, and provides a dataflow graph in which the agent constructs queries, colourings, and rule checks with the same four editing operations a person uses.

The proof of concept was carried out on the buildingSMART Duplex Apartment model, 38,898 STEP entities, in two case studies. In case study B, executed 2026-08-04 and independently re-run 2026-08-05, a rule checker driven by a machine-readable provision file evaluated four accessible-door-clearance rules over 14 doors, produced 56 verdicts in all four verdict categories with per-element evidence, matched an independently derived ground truth door by door, produced byte-identical output across repeated runs, and recorded a human override inside the IFC file in a form that can be removed to restore the original byte for byte. In case study A, executed 2026-09-17, the same model was enriched with synthetic carbon and energy analytics, 664 property sets and 2,438 typed values written byte-exactly and reversibly, and eight natural-language questions were answered at building, storey, component, category, provenance, and absence level through the tool surface; seven of the eight matched the independently computed expectation in the hand-driven session, and four of the eight matched in the unattended `gpt-5` run of 2026-09-18. Three of the four unattended misses share a single cause, namely that the storey and building aggregates carry the same property names as the element values, which is a finding about the storage recommendation rather than about the agent, and which Annex A should accordingly be revised to correct.
