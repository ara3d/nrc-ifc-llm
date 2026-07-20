# LLM-Assisted Analytics Metadata on IFC Models

_A Studio 2.5 collaboration with the Canadian National Research Council_
  
## 1. Background

The client produces analytics on building models, including operational carbon, embodied carbon, energy, and other performance indicators, through workflows external to IFC. The client wishes to explore how these analytics can be:

1. Displayed on IFC geometry through methods such as color coding and text annotation.
2. Stored inside or linked to IFC so that the data is portable, reusable, and queryable.
3. Surfaced through AI- or LLM-based interfaces that allow users to ask natural-language questions about an enriched model.

Emerging approaches such as agentic AI, semantic building data, and LLM-based query interfaces offer new ways to make analytics accessible. This engagement explores their practical application to openBIM workflows, with a focus on the AI/LLM layer and the storage of analytics associated with IFC models.

The work will produce a technical paper and a minimal proof of concept.

## 2. Objectives

### 2.1 IFC storage

Investigate and recommend best-practice options for storing or associating analytics metadata with IFC models. Options may include:

- IFC property sets (`Pset`)
- Information Delivery Specification (IDS)
- IFC-LBD and related semantic representations
- External linked references

The analysis will consider component, zone, storey, and building levels, with reuse and export as priorities.

### 2.2 Visualization

Investigate and recommend approaches for displaying analytics on IFC models, including:

- Color coding
- Text annotation
- Aggregated views

### 2.3 Natural-language query

Prototype an LLM-based query layer that reads an IFC file enriched with analytics and answers natural-language questions about the model and its associated data.

### 2.4 Technical publication

Deliver a publication-ready technical paper describing the findings, recommendations, proof of concept, and possible future directions.

## 3. Scope of Work

### 3.1 IFC analytics-storage options

Analyze options for storing or linking analytics metadata in IFC, aligned with the client's existing IDS and openBIM framework.

### 3.2 Display and color-coding options

Analyze approaches for displaying analytics on IFC geometry. The investigation may include open-source or freely available IFC technologies such as:

- IfcOpenShell
- web-ifc
- xBIM
- BIMvision
- Speckle

### 3.3 Minimal proof of concept

Develop a minimal proof of concept demonstrating:

- An IFC model enriched with analytics using the recommended storage approach, such as a custom property set or equivalent mechanism.
- An LLM-based agent that ingests the enriched IFC model and answers natural-language questions about carbon, energy, and other stored analytics at component and building levels.
- A lightweight visualization showing color-coded analytics on the model. This may be a screenshot-level demonstration or a simple viewer built with an existing library; it is not intended to be a production viewer.

### 3.4 Technical paper

Prepare a technical paper covering:

- Storage options and recommendations
- Display options and recommendations
- The role of LLM and agentic layers in querying and reusing analytics
- Proof-of-concept results
- Complementary architectural patterns, such as knowledge graphs and world-model substrates, as possible future extensions beyond file-based IFC exchange
- A possible roadmap for a future open-source, bidirectional viewer

## 4. Deliverables

### D1. Options Analysis Brief

A concise analysis of storage and display options, including a comparison matrix and recommendations.

### D2. Proof-of-Concept Package

A package containing:

- An LLM-based query agent
- A sample enriched IFC model
- A lightweight visualization example
- Supporting source code and documentation

Licensing, ownership, repository visibility, and publication terms are intentionally omitted from this sanitized version.

### D3. Technical Paper

A publication-ready technical paper describing the research, recommendations, implementation, and results.

### D4. Final Presentation

A virtual presentation and handover to the client team.

## 5. Implementation Sequence

The work is expected to proceed through the following stages:

1. Analyze storage and display options.
2. Select and document a recommended approach.
3. Develop the minimal proof of concept.
4. Draft and revise the technical paper.
5. Present the results and hand over the deliverables.

Exact dates, durations, milestones, and payment-linked deadlines have been removed.

## 6. Acceptance Criteria

The work will be considered complete when:

- The options analysis covers storage and display approaches at component, zone, storey, and building levels and provides clear recommendations.
- The proof of concept demonstrates natural-language questions being answered against an IFC model enriched with analytics.
- The technical paper passes the client's editorial review.
- The final presentation and handover are completed.

## 7. Client Responsibilities

The client is expected to provide:

- Representative IFC models
- Representative analytics datasets, such as carbon and energy data
- Guidance on alignment with its existing IDS framework
- Timely review and feedback on deliverables

Named personnel, internal references, and detailed review-cycle limits have been removed.

## 8. Exclusions

The engagement does not include:

- A full production viewer
- A proprietary substrate or vendor-locked solution
- Portfolio-scale infrastructure
- Ongoing advisory or maintenance services

- Other commercially identifying details
