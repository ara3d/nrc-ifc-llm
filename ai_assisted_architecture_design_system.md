---
title: "AI-Assisted Architecture Planning and Design on Git"
prompt_summary: "Explain how architecture and engineering firms might use a Git-based, AI-assisted design system, including the documents and artifacts they would track, the outcomes they would seek, and the features and user experience the platform should provide."
agent_model: "GPT-5.6 Thinking"
date: "2026-07-24"
---

# AI-Assisted Architecture Planning and Design on Git

## Product thesis

A design firm would not primarily want **Git with a friendlier interface**. It would want a **project memory, decision-management and controlled-change system**.

Git could provide the underlying mechanics:

| Git concept | Design-firm concept |
|---|---|
| Repository | Project workspace |
| Commit | Design checkpoint |
| Branch | Design option or workstream |
| Pull request | Proposed design change |
| Merge | Approved integration |
| Tag/release | Milestone or formal submission |
| Issue | Design question, risk or coordination item |
| CI pipeline | Automated design validation |
| Blame/history | Design provenance |

The important distinction is that a building project is not merely a collection of files. It is a network of:

- requirements;
- assumptions;
- design options;
- decisions;
- models;
- drawings;
- calculations;
- approvals;
- responsibilities;
- evidence;
- downstream consequences.

ISO 19650 explicitly treats building information management as a lifecycle process involving the exchange, recording, versioning and organisation of information. The RIBA Plan of Work similarly organises projects into stages with defined outcomes, tasks and information exchanges. Your system could make those ideas substantially more operational and machine-readable.

## What firms would want to track

### 1. Client requirements and project definition

These establish what the project is supposed to achieve:

- client brief;
- project objectives;
- functional programme;
- room and space schedule;
- occupancy assumptions;
- area targets;
- budget and cost limits;
- project programme;
- procurement strategy;
- performance targets;
- sustainability and carbon targets;
- accessibility requirements;
- planning constraints;
- site information;
- stakeholder requirements;
- owner information requirements;
- BIM execution plans;
- information exchange requirements.

Requirements should not exist only as paragraphs in a PDF. They should also be represented as individual, traceable objects:

> “The emergency department must accommodate 120 patients per hour.”

That requirement could be linked to the brief, circulation model, room programme, simulation results, cost plan and the eventual client approval.

### 2. Design intent and decisions

This may be the most valuable and least well-managed information in current projects.

A firm would want to record:

- the question being decided;
- alternatives considered;
- assumptions;
- evaluation criteria;
- supporting calculations;
- stakeholder comments;
- chosen option;
- reasons for the decision;
- person or group responsible;
- approval status;
- affected spaces, systems and documents;
- conditions under which the decision should be reconsidered.

Examples:

- Why was the structural grid changed from 8 m to 9 m?
- Why was Option B selected over Option C?
- Why was a particular façade system rejected?
- Why was a room moved to another floor?
- Why was a code interpretation accepted?
- Who approved the reduction in plant-room area?
- Was the decision based on cost, performance, constructability or preference?

This is analogous to an architecture decision record in software engineering, but connected directly to building objects, drawings and analysis results.

### 3. Design models and geometry

A project might contain:

- conceptual massing;
- site models;
- survey models;
- GIS data;
- Rhino and Grasshopper models;
- Revit or Archicad models;
- IFC models;
- structural analysis models;
- MEP calculation models;
- energy models;
- daylight models;
- computational fluid dynamics models;
- fabrication models;
- point clouds;
- meshes;
- parametric scripts;
- families, components and assemblies;
- federated coordination models.

IFC provides a standardised digital description of built assets and is therefore a logical neutral format for snapshots, model comparisons and long-term preservation.

However, the system should not treat a model as one opaque binary file. Where possible, it should understand:

- elements;
- spaces;
- systems;
- properties;
- relationships;
- classifications;
- geometry;
- quantities;
- element identity across versions.

That allows it to say:

> “This checkpoint added 14 doors, changed 27 room areas, increased façade area by 3.8%, and invalidated two previous daylight studies.”

### 4. Engineering analyses

Engineering firms would want to version both inputs and outputs for:

- structural loads and calculations;
- member sizing;
- foundation options;
- energy analysis;
- embodied and operational carbon;
- HVAC loads;
- ventilation;
- electrical demand;
- fire and smoke analysis;
- egress;
- acoustics;
- daylight and solar exposure;
- pedestrian circulation;
- transportation;
- drainage;
- wind;
- thermal comfort;
- life-cycle cost;
- constructability;
- quantity take-offs.

The important capability is reproducibility:

> “Which model version, assumptions, weather file and occupancy schedule produced this energy result?”

An analysis result without its inputs and assumptions is not a reliable project record.

### 5. Drawings, schedules and specifications

Traditional deliverables remain essential:

- plans, sections and elevations;
- detail drawings;
- sheet sets;
- door, room, equipment and finish schedules;
- specifications;
- quantity schedules;
- cost plans;
- reports;
- presentation boards;
- renderings;
- planning submissions;
- permit submissions;
- tender packages;
- construction packages;
- record drawings.

The system should connect a generated drawing or schedule to the exact source model checkpoint from which it was produced.

### 6. Coordination and issue records

These include:

- clash reports;
- coordination issues;
- markups;
- requests for information;
- action items;
- design queries;
- risk registers;
- meeting minutes;
- consultant comments;
- client comments;
- constructability reviews;
- unresolved interfaces between disciplines.

BCF is especially relevant because it allows an issue to contain contextual information, viewpoints, images, coordinates and references to IFC elements using GUIDs. Your internal issue system could support BCF import and export rather than inventing a closed coordination format.

### 7. Formal reviews and approvals

A firm needs evidence of what was reviewed, by whom and when:

- internal quality reviews;
- discipline lead reviews;
- code reviews;
- model audits;
- client approvals;
- authority comments;
- planning approvals;
- permit approvals;
- value-engineering approvals;
- design freezes;
- departures and waivers;
- signed transmittals;
- milestone acceptance.

A formal approval should apply to an immutable package, not merely to “the current model,” which may change immediately afterward.

### 8. Construction and handover information

During delivery, the project record expands to include:

- shop drawings;
- product submittals;
- contractor proposals;
- substitutions;
- RFIs;
- architect’s instructions;
- change notices;
- site observations;
- photographs;
- non-conformance reports;
- commissioning results;
- deficiency lists;
- warranties;
- operations manuals;
- as-built models;
- asset registers;
- training records.

These are natural candidates for structured, versioned workflows.

### 9. Post-occupancy evidence

For firms that care about actual outcomes:

- energy-use data;
- comfort surveys;
- maintenance records;
- operational issues;
- post-occupancy evaluations;
- measured versus predicted performance;
- lessons learned;
- client feedback;
- design defects;
- successful details or systems.

This closes the loop between design intent and real performance.

### 10. Firm-wide knowledge

The system could also manage reusable intellectual property:

- firm standards;
- design guides;
- typical details;
- approved products;
- specification clauses;
- code interpretations;
- room templates;
- calculation templates;
- QA checklists;
- project templates;
- previous decision records;
- lessons learned;
- AI prompts and skills;
- automation scripts;
- validation rules;
- approved agent workflows.

This may eventually become more commercially valuable than basic file versioning. It converts disconnected project experience into an institutional knowledge graph.

## What firms would want to achieve

### Preserve the reasoning behind the design

Conventional document systems answer:

> “What was issued?”

Your system should also answer:

> “Why did the design become this way?”

That is useful during staff turnover, consultant disputes, project restarts, value engineering, regulatory review and operation of the completed building.

### Explore alternatives without losing control

Early design is inherently divergent. Teams might investigate several:

- massing options;
- structural grids;
- circulation schemes;
- façade systems;
- servicing strategies;
- construction systems;
- phasing approaches.

Branches are a natural implementation, but users should see **Option A**, **Option B** and **Option C**, not Git branches.

Each option could have:

- its own models and reports;
- shared baseline requirements;
- comparison metrics;
- unresolved risks;
- associated comments;
- evaluation scores;
- a final disposition such as selected, rejected or retained for reconsideration.

### Understand the consequences of a change

A client might request:

> “Add 200 workstations while keeping the gross area unchanged.”

The system could identify likely consequences:

- affected floors and departments;
- reduced circulation;
- changed occupancy loads;
- toilet fixture requirements;
- egress implications;
- HVAC loads;
- energy consumption;
- furniture plans;
- cost plan;
- drawings and reports requiring regeneration;
- previous approvals that may no longer apply.

This is much more valuable than showing that a few files changed.

### Improve multidisciplinary coordination

Architects, structural engineers, MEP engineers, energy consultants and contractors operate in different tools and abstractions.

The system could expose a shared project layer containing:

- stable object identities;
- interface agreements;
- design responsibilities;
- coordination zones;
- discipline dependencies;
- shared milestones;
- questions and decisions;
- model exchanges.

A proposed structural change could become a review request to architecture and MEP rather than an emailed model with an ambiguous filename.

### Automate quality assurance

The equivalent of continuous integration could run whenever a meaningful design checkpoint is created:

- IFC validation;
- IDS information checks;
- naming and classification checks;
- model-coordinate validation;
- duplicated element detection;
- space enclosure checks;
- accessibility rules;
- egress tests;
- minimum clearance tests;
- clash detection;
- area and programme compliance;
- carbon budget checks;
- energy target checks;
- drawing completeness;
- broken references;
- missing approvals.

IDS is the buildingSMART-recommended mechanism for defining information requirements for IFC datasets, making it a strong basis for machine-executable delivery checks.

### Make AI work reviewable

The system should prevent an AI agent from silently changing the project.

Instead, an agent would create a structured proposal:

1. State its interpretation of the request.
2. Identify assumptions and missing information.
3. List the artefacts it inspected.
4. Produce proposed changes.
5. Show semantic differences.
6. Run applicable checks.
7. Identify risks and unresolved issues.
8. Request human review.
9. Record whether each change was accepted, modified or rejected.

This turns AI from an opaque chatbot into a supervised project participant.

### Reuse knowledge without blindly copying

On a new hospital project, an agent could retrieve:

- similar room programmes;
- previous circulation decisions;
- applicable firm standards;
- typical equipment requirements;
- past coordination problems;
- relevant details;
- previous post-occupancy findings.

But every reused item should preserve its source and be revalidated against the new project.

### Create defensible records

Architecture and engineering involve professional responsibility. Firms need to distinguish:

- an exploratory AI suggestion;
- an internal working decision;
- a reviewed design;
- an approved client direction;
- a formally issued deliverable.

The system could make these states explicit and difficult to confuse.

## Features the system should offer

### 1. A project-centric interface

The primary navigation should be:

- Project;
- Stage;
- Design options;
- Decisions;
- Models;
- Analyses;
- Reviews;
- Deliverables;
- Issues;
- Milestones.

The repository and file tree can remain available for advanced users, but should not be the main organising metaphor.

### 2. Automatic checkpoints

Architects should not have to write commit messages every ten minutes.

The system could:

- save continuous technical history;
- detect meaningful changes;
- suggest checkpoint descriptions;
- group related edits;
- ask for rationale only at important moments;
- create explicit checkpoints for reviews and submissions.

For example:

> **Suggested checkpoint:** Revised Level 2 clinical programme  
> 12 rooms moved, net area unchanged, circulation increased by 4.2%.

The user can accept or edit the description.

### 3. Semantic comparison

This is a foundational differentiator.

The comparison interface should support:

- 3D model differences;
- 2D drawing overlays;
- property changes;
- room and area changes;
- schedule differences;
- spreadsheet differences;
- specification changes;
- requirement changes;
- analysis-result changes;
- added and removed relationships;
- changes grouped by discipline or system.

A good model diff should answer both:

> “What changed?”

and:

> “What is likely to be affected?”

### 4. Design-option workspaces

A designer should be able to:

- duplicate the current scheme as an option;
- assign a team or agent;
- experiment independently;
- compare options against common criteria;
- bring selected changes back;
- archive rejected options without deleting them.

Merging will not always mean geometrically merging two models. It may mean:

- accepting a decision;
- importing selected rooms;
- adopting a façade strategy;
- applying a changed parameter set;
- updating a requirement;
- marking an option as the preferred basis of design.

### 5. First-class decision records

Creating a decision should be almost as easy as writing a comment.

A decision object could contain:

- title;
- question;
- status;
- decision owner;
- participants;
- alternatives;
- criteria;
- evidence;
- selected outcome;
- rationale;
- affected artefacts;
- affected building elements;
- assumptions;
- review date;
- approval;
- superseded decisions.

The system should also detect likely undocumented decisions:

> “The structural grid changed substantially between approved checkpoints, but no related decision has been recorded.”

### 6. In-context review

Comments should be attachable to:

- an IFC element;
- a group of elements;
- a room;
- a drawing region;
- a camera viewpoint;
- a specification paragraph;
- a calculation;
- a requirement;
- a design decision;
- a specific version of any of these.

A comment must remain anchored to the version on which it was made, even when the current design changes.

### 7. Stage and milestone packages

The system should let teams create immutable packages such as:

- concept review;
- planning submission;
- 60% design;
- 90% design;
- issued for tender;
- issued for construction;
- record information;
- handover package.

A package could include models, drawings, schedules, specifications, analysis results, open risks, approvals and validation reports.

It should be possible to reproduce the exact package later.

### 8. Agent workspaces and permissions

Agents should have identities and scoped capabilities:

- read project context;
- propose design alternatives;
- update a room schedule;
- run analysis;
- generate drawings;
- identify inconsistencies;
- draft reports;
- create issues;
- request information;
- perform code or standards checks.

Permissions should distinguish:

- read;
- analyse;
- create a proposal;
- modify working artefacts;
- approve;
- publish;
- issue externally.

An energy-analysis agent should not automatically be authorised to alter the approved architectural model.

### 9. AI provenance

Every material AI output should record:

- model and version;
- system instructions;
- user request;
- project context retrieved;
- tools called;
- input artefact versions;
- generated artefacts;
- automated tests;
- human reviewer;
- edits made after generation;
- final disposition.

In an AEC setting, this translates naturally into traceable agent actions, validation gates and explicit human responsibility.

### 10. Requirement-to-evidence traceability

A user should be able to select a requirement and see:

- which design elements address it;
- which decisions interpret it;
- which analyses verify it;
- which drawings communicate it;
- which approvals accepted it;
- whether later changes may have invalidated it.

Conversely, selecting a building element should reveal why it exists and which requirements it satisfies.

### 11. Open integration

The system should integrate with, rather than initially replace:

- BIM authoring systems;
- CAD systems;
- parametric modelling tools;
- analysis applications;
- spreadsheets;
- document editors;
- existing common data environments;
- email and collaboration platforms;
- issue-management systems;
- cost and scheduling systems.

Open exchange should include IFC, BCF, IDS, PDF, spreadsheets, images and common geometric formats.

For agent integration, the system could expose:

- project-query tools;
- artefact retrieval;
- structured change operations;
- validation tools;
- event subscriptions;
- agent proposal APIs;
- MCP-compatible interfaces.

### 12. Role-specific views

#### Architect

- design options;
- client requirements;
- spatial changes;
- design reviews;
- presentation packages;
- coordination issues.

#### Engineer

- input assumptions;
- analysis dependencies;
- calculation versions;
- interface changes;
- validation results;
- design approvals.

#### BIM or information manager

- model health;
- naming and classification;
- exchange requirements;
- federated model status;
- issue status;
- information-delivery compliance.

#### Project manager

- decisions awaiting approval;
- overdue reviews;
- stage readiness;
- risks;
- responsibilities;
- deliverable status.

#### Principal or quality reviewer

- major departures;
- unresolved risks;
- approval history;
- automated QA results;
- scope and liability exposure.

#### Client

- understandable design options;
- decisions requiring direction;
- milestone packages;
- budget and performance implications;
- approval history.

The client should not need access to every technical intermediate file.

## An example workflow

Suppose the client asks to reduce the project cost by 8%.

1. The project manager records the request as a requirement change.
2. An AI agent searches the current design, cost plan and previous value-engineering decisions.
3. It creates three value-engineering options.
4. Each option receives its own workspace.
5. The agents update selected artefacts and run area, energy, carbon and programme checks.
6. The system generates semantic comparisons.
7. Architects and engineers comment directly on affected objects.
8. The cost consultant updates estimates.
9. The system records trade-offs:
   - Option A saves 5% with little performance impact.
   - Option B saves 8% but increases operational energy.
   - Option C saves 10% but changes the planning submission.
10. The client approves Option A plus selected changes from Option B.
11. Those changes are integrated into the main design.
12. Superseded calculations and approvals are automatically flagged.
13. A new formal checkpoint is created with the decision rationale and evidence.

The resulting project history captures much more than a folder named `VE_FINAL_APPROVED_03`.

## Important product risks

### Git does not naturally understand BIM semantics

Git is excellent for immutable history and branching, but poor at merging large opaque binary files. You will need an AEC-aware object and identity layer above it.

### Too much documentation will fail

If every minor action requires a form, users will bypass the system. Most provenance should be captured automatically, with humans prompted only for meaningful rationale and approval.

### Firms already have document systems

The first version should probably be an intelligence and traceability layer over existing storage and authoring tools, not an immediate replacement for every common data environment.

### AI authority must be unmistakable

Users must always understand whether something is:

- AI-generated;
- human-authored;
- automatically validated;
- professionally reviewed;
- formally approved;
- formally issued.

### Design branches are not source-code branches

Two geometry options may not be mechanically mergeable. “Merge” must support selective adoption and semantic reconciliation, not merely file-level conflict resolution.

## A strong initial product

The most credible first release would combine five tightly connected capabilities:

1. **Design decision records** linked to models, drawings and requirements.
2. **Semantic IFC and document comparison** between meaningful checkpoints.
3. **Design-option workspaces** implemented using Git-like branching.
4. **AI change proposals** with assumptions, provenance, tests and human review.
5. **Milestone packages** containing immutable artefacts, approvals and validation results.

That would give you a clear position:

> **A collaborative design history and AI governance platform for architecture and engineering—not simply another file repository or BIM viewer.**

The deeper long-term opportunity is a machine-readable **design graph** in which every requirement, decision, artefact, model element, analysis, issue and approval is connected. Git provides the durable history, while the design graph gives that history architectural meaning.
