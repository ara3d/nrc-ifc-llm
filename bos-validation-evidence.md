# BOS Toolchain — Validation Evidence Inventory (What Exists Today)

_Compiled 2026-08-04. All links are pinned to specific commits so they remain stable as the
repositories evolve._

This document inventories the existing, verifiable evidence in the
[ara3d-sdk](https://github.com/ara3d/ara3d-sdk) and
[nrc-ifc-llm](https://github.com/ara3d/nrc-ifc-llm) repositories that addresses the TRL /
feasibility validation criteria for an integrated end-to-end demonstration of the IFC / BIM Open
Schema (BOS) toolchain. Each section states the claim, the evidence, and where it lives —
tests, commits, sample data, and documentation.

The work described here was implemented and committed between **2026-06-30 and 2026-07-28**, with
each unit of work verified by automated tests at the time of its commit. Commit dates and messages
are the primary record; the test source files are the executable specification of what was
verified.

---

## 1. Real IFC models, with element counts

**Claim:** Real (not synthetic) IFC models are on hand and processed by the toolchain, with
element counts asserted in automated tests.

**Evidence:**

- The **Duplex Apartment** model (`duplex.ifc`, a widely used buildingSMART sample) is the primary
  test model. The round-trip test suite asserts it parses to **more than 30,000 STEP entities**:
  [IfcRoundTripTests.cs (line 10)](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Tests/IfcRoundTripTests.cs#L10)
- A companion dataset of **268 building elements** extracted from the Duplex model, each keyed by
  IFC GlobalId with type, storey, and analytics values (operational carbon, energy intensity):
  - [IFC-Test-Kit/model_elements.csv](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/IFC-Test-Kit/model_elements.csv)
    — columns `GlobalId, Name, IFCType, Level`
  - [IFC-Test-Kit/analytics_dataset_with_levels.csv](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/IFC-Test-Kit/analytics_dataset_with_levels.csv)
    — columns `GlobalId, Name, Level, operational_carbon, energy_intensity, category`
- Additional real models available in the repositories for scaling the demonstration:
  - [data/AC20-FZK-Haus.ifc](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/data/AC20-FZK-Haus.ifc)
    (KIT / Karlsruhe Institute of Technology reference model — used as the fixture for the MCP
    analytics and geometry test suites)
  - [data/C20-Institute-Var-2.ifc](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/data/C20-Institute-Var-2.ifc)
  - [data/Office_A_20110811.ifc](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/data/Office_A_20110811.ifc)
  - [IFC-Test-Kit/large_test_model.ifc](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/IFC-Test-Kit/large_test_model.ifc)

**Commits:**

- [`7d8a898`](https://github.com/ara3d/nrc-ifc-llm/commit/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b)
  (2026-07-23) — Add IFC-Test-Kit sample data folder
- [`d92dbeb`](https://github.com/ara3d/nrc-ifc-llm/commit/d92dbebbf40e0be1de43da18b6e457df9a3dbd29)
  (2026-07-20) — sample IFC data files added

---

## 2. The BOS toolchain, exercised end to end

**Claim:** A complete pipeline — IFC parse → BIM Open Schema conversion → columnar storage →
SQL query → export — exists and is exercised end to end by automated tests driven through the
same protocol surface (MCP `tools/call`) an external client would use.

**Evidence:**

- The pipeline: an IFC file is converted by `IfcToBosConverter` to a `.bos` file (a zip of
  Brotli-compressed Parquet tables), loaded into DuckDB, queried with read-only SQL, and exported
  to CSV/Parquet/JSON. The full tool surface (29 read-only tools) is documented in
  [wip/Ara3D.Ifc.Mcp/README.md](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/wip/Ara3D.Ifc.Mcp/README.md).
- [IfcAnalyticsToolTests.cs](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Mcp.Tests/IfcAnalyticsToolTests.cs)
  drives every stage through JSON-RPC against the FZK-Haus model and asserts:
  - `ToBos_WritesAZipAndCopiesItWhereAsked` — conversion produces a non-empty `.bos` zip at the
    requested path;
  - `Table_ListsTablesWithColumnsAndRowCounts` — the converted database reports its tables,
    columns, types, and row counts;
  - `Sql_PagesAndReportsTheUnpagedTotal`, `Sql_AggregatesAcrossTables` — arbitrary read-only SQL
    with correct paging and totals;
  - `Sql_RefusesAnythingButOneReadOnlyStatement` — `DROP`, `INSERT`, and statement-chaining are
    rejected (safety property of the query surface);
  - `Views_ResolveInternedIndexesToText` — BOS interns every string and enum; the
    `EntityText` / `ParameterText` / `RelationText` views resolve indexes back to readable text;
  - `SqlExport_WritesEveryRowToCsv` — full-result export with row-count verification against the
    written file;
  - `Bos_KeepsSpatialContainers` — **cross-tool consistency check**: the storey count obtained by
    SQL over the converted BOS database must equal the storey count reported by the entity-level
    IFC tools. This is a direct expected-versus-observed comparison between two independent code
    paths over the same model.
- [StdioEndToEndTests.cs](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Mcp.Tests/StdioEndToEndTests.cs)
  runs the server as a **live subprocess** over stdio — the toolchain is proven as a deployable
  process, not only as an in-process library.
- The BIM Open Schema implementation itself:
  [src/Ara3D.BimOpenSchema](https://github.com/ara3d/ara3d-sdk/tree/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/src/Ara3D.BimOpenSchema)
  with its own unit-test suites
  [tests/Ara3D.BimOpenSchema.Tests](https://github.com/ara3d/ara3d-sdk/tree/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.BimOpenSchema.Tests)
  and
  [tests/Ara3D.BimOpenSchema.Harmonizer.Tests](https://github.com/ara3d/ara3d-sdk/tree/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.BimOpenSchema.Harmonizer.Tests).

**Commits:**

- [`fc635ca`](https://github.com/ara3d/ara3d-sdk/commit/fc635ca698979138c3b0cf6e08fa0bdb23b2d901)
  (2026-07-27) — feat(ifc-mcp): add an IFC MCP server with the data tool surface
- [`393a9a2`](https://github.com/ara3d/ara3d-sdk/commit/393a9a24427e8c7b06d98083ecb588ae87fed6b0)
  (2026-07-28) — feat(ifc-mcp): add the analytics tool group over BOS and DuckDB
- [`91f12d6`](https://github.com/ara3d/ara3d-sdk/commit/91f12d6a0ff91d51235e99b7d03e77e9c1fc3609)
  (2026-07-28) — test(ifc-mcp): exercise the stdio server as a live subprocess
- [`944b378`](https://github.com/ara3d/ara3d-sdk/commit/944b3789aef35efed0b9c0b2f25f70d16efe09e5)
  (2026-07-06) — Add shared Ara3D.MCP library, move BOS data-table utilities
- [`e4a6edb`](https://github.com/ara3d/ara3d-sdk/commit/e4a6edb87fc11086b712c5045798d081c7e811ee)
  (2026-07-21) — fix: BimGeometry scale-column corruption on ToDataSet (defect found and fixed
  through this test discipline)

---

## 3. Determinism and repeated-execution identity

**Claim:** The toolchain's read, modify, and write operations are deterministic, and repeated
execution over the same input is verified to produce identical output — at a standard stronger
than an output hash: **byte-for-byte file identity**.

**Evidence:**

- `AppendThenRemoveIsByteIdentical`
  ([IfcRoundTripTests.cs, lines 32–56](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Tests/IfcRoundTripTests.cs#L32-L56)):
  a property set is appended to the Duplex model, the modification is verified by structural diff,
  the added entities are removed, and the result is asserted **equal byte for byte** to the
  original file (`File.ReadAllBytes` equality over the full ~30,000-entity file).
- `AddAnalyticsPropertiesDiffAndRestore`
  ([AnalyticsPropertyTests.cs, lines 22–53](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Tests/AnalyticsPropertyTests.cs#L22-L53)):
  the same byte-identical restore property proven at scale — analytics property sets for all 268
  dataset rows (6 STEP entities per row, count asserted exactly) are written into the model and
  removed again, restoring the original file byte for byte.
- `DiffOfFileWithItselfIsEmpty`
  ([IfcRoundTripTests.cs, lines 21–29](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Tests/IfcRoundTripTests.cs#L21-L29)):
  parsing is deterministic — two independent loads of the same file diff to empty.
- `SpansCoverEveryEntityAndReserializeExactly`
  ([IfcRoundTripTests.cs, lines 5–19](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Tests/IfcRoundTripTests.cs#L5-L19)):
  every one of the >30,000 entity spans re-serializes exactly from its source bytes.
- The supporting machinery is itself part of the evidence:
  [IfcDiff.cs](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Tests/IfcDiff.cs)
  (structural entity-level diff reporting added / deleted / changed ids),
  [IfcPatcher.cs](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Tests/IfcPatcher.cs)
  (append / remove that preserves untouched bytes), and
  [IfcPropertySetBuilder.cs](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Tests/IfcPropertySetBuilder.cs)
  (deterministic STEP-line generation for new property sets).

**Commits:**

- [`edb13c4`](https://github.com/ara3d/ara3d-sdk/commit/edb13c4d71e73953cf1e1fdf0ee4ec4622dff168)
  (2026-07-27) — feat(tests): IFC property append, entity diff, byte-identical round trip
- [`dd6227d`](https://github.com/ara3d/ara3d-sdk/commit/dd6227dc3c6aecc83c1a252e5e74e0528a2e9164)
  (2026-07-27) — chore(tests): write test output to a durable artifacts/ folder

---

## 4. Records bound to element identifiers

**Claim:** Per-element records (the shape a verdict record takes) are deterministically bound to
IFC element identifiers (GlobalIds), and the binding is verified against the model.

**Evidence:**

- `CsvRowsResolveToDuplexElements`
  ([AnalyticsPropertyTests.cs, lines 7–19](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Tests/AnalyticsPropertyTests.cs#L7-L19)):
  every one of the 268 dataset rows resolves by GlobalId to an element in the Duplex model, with
  a zero-missing assertion. This is the deterministic applicability-input binding: external
  per-element data joined to model elements by stable identifier, verified with no unmatched rows.
- `AddAnalyticsPropertiesDiffAndRestore` (linked in §3) then writes those records **into the IFC
  itself** as `Ara3D_Analytics` property sets — one property set and one relationship per element,
  four property values per row — and proves via structural diff that exactly the expected entities
  (and nothing else) were added. This is the mechanism by which a verdict, a human confirmation,
  or an override can be recorded against an element identifier inside the model with a complete,
  reversible audit trail.
- The design options for this recording mechanism are analyzed in
  [storing-analytics-in-ifc.md](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/storing-analytics-in-ifc.md)
  ([commit `f753e5f`](https://github.com/ara3d/nrc-ifc-llm/commit/f753e5f4a1e43990440f39ca8549f584e298d18d), 2026-07-20).

---

## 5. Property-rule and geometric-rule primitives

**Claim:** The query primitives needed to evaluate machine-readable provisions — property tests
and geometric measurements over model elements — exist and are tested.

**Evidence — property rules:**

- `ifc_find_by_parameter` evaluates predicate operators (`eq`, `contains`, `gt`, …) over any
  parameter in the model and returns the matching elements;
  `ifc_parameters` / `ifc_parameter_values` / `ifc_parameter_table` enumerate the parameter space
  with element counts, ranges, and distinct values. Tested in
  [IfcParameterToolTests.cs](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Mcp.Tests/IfcParameterToolTests.cs),
  including failure-envelope tests for unknown parameters and unknown operators.
- Arbitrary joins and aggregate provisions can be expressed as read-only SQL over the converted
  BOS database (`ifc_sql`, §2) — a machine-readable, replayable encoding of a provision.

**Evidence — geometric rules:**

- `ifc_volume` (volume and surface area from geometry), `ifc_bounds` (per-element and whole-model
  bounding boxes), `ifc_mesh` (mesh statistics), and `ifc_meshing_diagnostics` (which elements
  failed to mesh, and why — the raw material for an "inconclusive" verdict category). Tested in
  [IfcGeometryToolTests.cs](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/tests/Ara3D.Ifc.Mcp.Tests/IfcGeometryToolTests.cs)
  against FZK-Haus (current assertions are non-degeneracy — nonzero volumes and non-empty boxes —
  not yet comparisons against independently known values; see the gap list at the end).
- `ifc_quantities` reads the model's own declared quantities (lengths, areas, volumes, counts,
  weights, times), enabling declared-versus-measured cross-checks.

**Commits:**

- [`d6c19b7`](https://github.com/ara3d/ara3d-sdk/commit/d6c19b7c165021ac5344d7f8ada83f162a6883bd)
  (2026-07-28) — feat(ifc-mcp): add cross-model parameter query tools
- [`7fb847e`](https://github.com/ara3d/ara3d-sdk/commit/7fb847e7c126b702e04ddd14ca6aca410c5fa20f)
  (2026-07-28) — feat(ifc-mcp): add geometry tool group

---

## 6. Feasibility evidence: real defects found by the toolchain

**Claim:** The toolchain is sensitive enough to catch real data-fidelity defects — three parser
defects in the underlying IFC loader were discovered by driving these tools against real models,
and all three were fixed upstream. Each is documented with its mechanism in
[wip/Ara3D.Ifc.Mcp/README.md, "Three upstream defects"](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/wip/Ara3D.Ifc.Mcp/README.md#three-upstream-defects-found-and-since-fixed-here).

1. **`IFCELEMENTQUANTITY` attributes read from the wrong positions** — every quantity set in every
   model read back empty and misnamed; 64 missing quantities on a single FZK-Haus wall. Fixed in
   [`35660a8`](https://github.com/ara3d/ara3d-sdk/commit/35660a80f6bd1efce37e48e6ca81329de441dfa0)
   (2026-07-27).
2. **Typed property values unreachable through the attribute list** — every property read back as
   the name of its own measure type until value payloads were unwrapped from the token stream.
   Fixed in the same commit,
   [`35660a8`](https://github.com/ara3d/ara3d-sdk/commit/35660a80f6bd1efce37e48e6ca81329de441dfa0).
3. **Property and set names left STEP-encoded** — non-ASCII names (FZK-Haus: `Höhe` read back as
   `H\X2\00F6\X0\he`) made search-by-name silently fail. Fixed in
   [`fefff9f`](https://github.com/ara3d/ara3d-sdk/commit/fefff9faa6c9885c6af5fdf78c692abbae7c2e46)
   (2026-07-28).

These matter for validation because they demonstrate the expected-versus-observed discipline
working: wrong values were detected against a real model, root-caused, fixed at the source, and
re-verified — all recorded in dated commits.

---

## 7. Dated record in repository commits

**Claim:** The demonstration components are documented in dated repository commits, as the
validation language requires ("documented in repository commits and logs").

**The IFC/BOS commit series (ara3d-sdk):**

| Date | Commit | Subject |
|---|---|---|
| 2026-07-27 | [`edb13c4`](https://github.com/ara3d/ara3d-sdk/commit/edb13c4d71e73953cf1e1fdf0ee4ec4622dff168) | feat(tests): IFC property append, entity diff, byte-identical round trip |
| 2026-07-27 | [`dd6227d`](https://github.com/ara3d/ara3d-sdk/commit/dd6227dc3c6aecc83c1a252e5e74e0528a2e9164) | chore(tests): write Ara3D.Ifc.Tests output to artifacts/ instead of bin/ |
| 2026-07-27 | [`e8f5a14`](https://github.com/ara3d/ara3d-sdk/commit/e8f5a145ac32fb7f57e75228b58e4ec235be36ab) | docs(wip): hand off the IFC MCP server plan |
| 2026-07-27 | [`fc635ca`](https://github.com/ara3d/ara3d-sdk/commit/fc635ca698979138c3b0cf6e08fa0bdb23b2d901) | feat(ifc-mcp): add an IFC MCP server with the data tool surface |
| 2026-07-27 | [`d432e3d`](https://github.com/ara3d/ara3d-sdk/commit/d432e3dfe1c5e37076ddfcb0ace9feb83e23d181) | docs(wip): record the shipped IFC MCP work in the handoff |
| 2026-07-27 | [`35660a8`](https://github.com/ara3d/ara3d-sdk/commit/35660a80f6bd1efce37e48e6ca81329de441dfa0) | fix(ifc): correct IFCELEMENTQUANTITY parsing and unwrap typed property values |
| 2026-07-28 | [`393a9a2`](https://github.com/ara3d/ara3d-sdk/commit/393a9a24427e8c7b06d98083ecb588ae87fed6b0) | feat(ifc-mcp): add the analytics tool group over BOS and DuckDB |
| 2026-07-28 | [`91f12d6`](https://github.com/ara3d/ara3d-sdk/commit/91f12d6a0ff91d51235e99b7d03e77e9c1fc3609) | test(ifc-mcp): exercise the stdio server as a live subprocess |
| 2026-07-28 | [`81f14c5`](https://github.com/ara3d/ara3d-sdk/commit/81f14c53d2d3afa19e06fe0d238058335bbed3c7) | docs(wip): record wave 1 and correct two wrong facts |
| 2026-07-28 | [`7fb847e`](https://github.com/ara3d/ara3d-sdk/commit/7fb847e7c126b702e04ddd14ca6aca410c5fa20f) | feat(ifc-mcp): add geometry tool group |
| 2026-07-28 | [`d6c19b7`](https://github.com/ara3d/ara3d-sdk/commit/d6c19b7c165021ac5344d7f8ada83f162a6883bd) | feat(ifc-mcp): add cross-model parameter query tools |
| 2026-07-28 | [`fefff9f`](https://github.com/ara3d/ara3d-sdk/commit/fefff9faa6c9885c6af5fdf78c692abbae7c2e46) | fix(ifc-loader): decode IFC-escaped property and set names |

**Earlier BOS foundation commits (ara3d-sdk):**

| Date | Commit | Subject |
|---|---|---|
| 2026-06-30 | [`4fdcc1c`](https://github.com/ara3d/ara3d-sdk/commit/4fdcc1cb79aaa1e4e798ce59dac4e7effdf00aaa) | Adding properties from IFC entity attributes |
| 2026-07-03 | [`9246afe`](https://github.com/ara3d/ara3d-sdk/commit/9246afe5f4ab34ef2f09aa942420172655b1c332) | Consolidate NuGet meta-packages and fix IFC converter regressions |
| 2026-07-06 | [`944b378`](https://github.com/ara3d/ara3d-sdk/commit/944b3789aef35efed0b9c0b2f25f70d16efe09e5) | Add shared Ara3D.MCP library, move BOS data-table utilities |
| 2026-07-21 | [`e4a6edb`](https://github.com/ara3d/ara3d-sdk/commit/e4a6edb87fc11086b712c5045798d081c7e811ee) | fix: BimGeometry scale-column corruption on ToDataSet |

**Project documentation commits (nrc-ifc-llm):**

| Date | Commit | Subject |
|---|---|---|
| 2026-07-15 | [`4c1f5de`](https://github.com/ara3d/nrc-ifc-llm/commit/4c1f5dee7c414487ebf3d50afcafa2974dabc9e7) | Create ids.md (IDS / machine-readable provisions overview) |
| 2026-07-20 | [`f60df35`](https://github.com/ara3d/nrc-ifc-llm/commit/f60df35b93f1255e6b1da4112c7d3a92b7513dcc) | docs: move statement of work out of README, link all docs |
| 2026-07-20 | [`f753e5f`](https://github.com/ara3d/nrc-ifc-llm/commit/f753e5f4a1e43990440f39ca8549f584e298d18d) | Create storing-analytics-in-ifc.md |
| 2026-07-20 | [`d92dbeb`](https://github.com/ara3d/nrc-ifc-llm/commit/d92dbebbf40e0be1de43da18b6e457df9a3dbd29) | Sample IFC data files |
| 2026-07-23 | [`7d8a898`](https://github.com/ara3d/nrc-ifc-llm/commit/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b) | Add IFC-Test-Kit sample data folder |

---

## 8. Supporting documentation

- [Statement of Work](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/statement-of-work.md)
  — background, objectives, scope, deliverables, acceptance criteria.
- [IDS Overview](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/ids.md)
  — the buildingSMART standard for machine-readable information requirements; the natural target
  format for "machine readable provisions."
- [Storing Analytics in IFC](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/storing-analytics-in-ifc.md)
  — design options for recording per-element data (and by extension, verdicts and overrides)
  in or alongside IFC.
- [Ara3D.Ifc.Mcp README](https://github.com/ara3d/ara3d-sdk/blob/fefff9faa6c9885c6af5fdf78c692abbae7c2e46/wip/Ara3D.Ifc.Mcp/README.md)
  — the full 29-tool surface, session/lifetime design, and the three upstream defect reports.
- [nrc-ifc-llm README](https://github.com/ara3d/nrc-ifc-llm/blob/7d8a898caeb9b7caf4271f78ed1eff0ddbb7b96b/README.md)
  — project overview and document index.

---

## 9. What does not exist yet (for completeness)

The inventory above covers model processing, toolchain integration, determinism, identifier
binding, rule primitives, and the dated commit record. The following validation items have **no
existing evidence** and require a demonstration harness to be built:

1. **A rule engine producing the four verdict categories** (pass / fail / not applicable /
   inconclusive) — the primitives exist (§5), the engine does not.
2. **An executable machine-readable provision format** — IDS is documented but not implemented;
   SQL-over-BOS is the nearest existing encoding.
3. **A recorded human confirmation and override** — the recording mechanism exists and is proven
   reversible (§4), but no confirmation/override workflow has been run.
4. **Geometric measurements compared against independently known values** — current geometry
   assertions are non-degeneracy checks; declared-quantity-versus-measured-geometry cross-checks
   (via `ifc_quantities`) and KIT's published FZK-Haus dimensions are the available ground truths.
5. **Persisted run logs with output hashes** — tests verify byte identity in-process; no run-log
   artifact with recorded hashes is retained yet.
