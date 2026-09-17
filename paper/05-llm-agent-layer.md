# 5. The LLM and agent layer

This section answers the third objective: how to build a layer in which a person asks a
question in plain language and receives a correct answer about an enriched model. The design
follows from one observation about what LLMs are and are not good at.

## 5.1 Why not give the model the file

An IFC file is a serialisation of an object graph. A question such as "what is the total
operational carbon on Level 2" requires finding the storey entity, following the containment
relationship to its elements, finding each element's property set relationship, finding the
set, finding the property, reading the value, and summing. In a 38,898-entity file the
relevant entities are scattered and the file is far larger than any model's context window.
Even where a file fits, a language model reading STEP text does arithmetic by pattern matching
and produces plausible rather than correct totals.

The alternative is to give the model tools. A tool is a function with a typed signature that
the model may call; the runtime executes it and returns the result. The model then reasons over
results that are small, structured, and correct. This is the design of every practical IFC MCP
server surveyed in [mcp-ifc.md](../mcp-ifc.md), and the design used here. The difference lies
in what the tools are.

## 5.2 Design principles

Four principles were applied. Each was learned from running varied questions against the
implementation and reading the transcripts; the toolkit's
[MCP demo notes](https://github.com/ara3d/bim-open-toolkit/blob/71790a7/docs/bim-flow-mcp-demo.md)
record the failures that motivated them.

**Few, typed, read-only tools.** A server that exposes the whole IFC API as 200 tools gives the
model too many ways to be wrong. The implementation exposes 29 tools grouped by question shape
(Appendix C). Every SQL tool accepts one read-only statement; `DROP`, `INSERT`, and statement
chaining are rejected, and the rejection is tested.

**Columnar copy, not the object graph.** The IFC file is converted once per session to BIM Open
Schema and loaded into DuckDB. Questions then become SQL over tables with text views, which a
model writes reliably. The conversion is the expensive step and happens once, not once per
question.

**Questions run the other way.** The per-element tools ("what does element N carry") are the
wrong shape for almost every real question ("which elements are load bearing", "`Height` for
all the windows"). An inverted parameter index, built once per session, answers those in one
call. Without it the model made one call per element.

**Answers carry their derivation.** Every list result reports its unpaged total, so the model
can tell a complete answer from a truncated one. In the dataflow surface, a question becomes a
graph, the graph is evaluated, and a run record pins the graph hash and every input by content
hash. A number comes with a way to recompute it.

## 5.3 The tool surface

The IFC MCP server has three groups of tools. The data tools answer questions about entities,
attributes, properties, quantities, relations, and the spatial tree directly from the parsed
file, without loading geometry. The geometry tools answer questions about meshes, bounds, and
volumes. The analytics tools convert the model to BOS, list the tables, run read-only SQL, and
export results.

A representative exchange, with the model's tool calls shown as they appear in a transcript:

```text
User:  Which storeys have the most operational carbon, and what is the total for each?

Agent: ifc_to_bos { path: "duplex.ifc" }
       -> { tables: 9, entities: 38898 }

Agent: ifc_sql { sql: "SELECT p.Value AS storey ... " }
       (reads the ContainedIn relations and the Pset_NRCOperationalCarbon values)

Agent: ifc_sql { sql:
         "SELECT storey, round(sum(oc), 1) AS total_kgCO2e_per_year, count(*) AS elements
            FROM element_carbon GROUP BY storey ORDER BY total DESC" }
       -> { total: 2, rows: [["Level 2", 12406.3, 141], ["Level 1", 11874.9, 127]] }

Agent: Level 2 has the higher total at 12,406 kgCO2e per year across 141 elements;
       Level 1 has 11,875 across 127. Values come from Pset_NRCOperationalCarbon
       on each element, run id run-2026-07-14-01.
```

The numbers in this exchange are illustrative of the shape of an answer, not measured results;
Section 6.2 will replace them with the recorded run.

## 5.4 The dataflow surface

The second surface is the BimOpenFlow MCP server. Its tools are the same operations that back
the web editor: `describeDatabase`, `getNodeCatalog`, `editGraph`, `evaluate`, `getResult`,
and `createRun`. A question becomes a graph of small nodes rather than one SQL string, and the
graph persists in a store where a person can open it, inspect each intermediate table, and
edit it.

This matters for three reasons. The person who asked can see how the answer was built. The
next question ("now only the doors") is an edit to the same graph. And the graph that colours
the model (Section 4.2) and the graph that answers the question are the same kind of object,
so "colour Level 2 by the values you just summed" is one more node.

Nine tactics made this work on small and large models alike. The four that matter most:

1. A schema summary the model can afford to read, with companion columns folded and empty tables
   given only a name and count.
2. A node guide in the system prompt: the expression language, the aggregate syntax, and the
   fact that `sql.query` exists for anything the table nodes cannot express.
3. One call to build a graph. Applying a list of edits at once and saving once cut input tokens
   per request from 2 to 4 million to 100 to 300 thousand.
4. A check by the host after the model says it is done: every node evaluated, an `answer` node
   present, rows in its table. An empty answer is reported back with the row count of every
   upstream node, and the model gets two more turns to fix it or to say honestly why the answer
   is empty.

On the toolkit's Snowdon test database, twelve requests over rooms, roofs, storeys, doors, and
lineage produced ten correct graphs, one honest answer without a graph, and one correctly empty
graph with an explanation, on a small model, and eleven correct graphs and one honest answer on
a mid-sized one. Where a hand-built graph existed for the same question, the counts matched.

## 5.5 Compliance as a query

A code-compliance rule is a query with a verdict column. The compliance node pack expresses this
directly. A `check.rule` node takes a table of element rows and a Boolean expression, and
appends four columns: `verdict`, `checkId`, `checkTitle`, and `citation`. A true expression is
`Pass`; false is `Fail` (or `NeedsReview` when a second expression says so); a null result,
meaning the fact needed was absent, is `InfoNotAvailable`. Absence is reported, never skipped.

```csharp
verdicts[i] = expr.Eval(lookup) switch
{
    null => Verdict.InfoNotAvailable,
    BooleanScalar { Value: true } => Verdict.Pass,
    _ => review?.Eval(lookup) is BooleanScalar { Value: true } ? Verdict.NeedsReview : Verdict.Fail,
};
```

The verdict table is an ordinary table. It can be coloured onto the model, summed per storey,
exported, or written back into the IFC as a property set. Section 6.3 shows a checker built on
the same four-verdict idea running over real doors.

## 5.6 Recommendation in brief

1. Put the LLM behind a small, typed, read-only tool surface. Do not give it the file.
2. Convert the IFC once to a columnar form and answer questions with SQL over text views.
3. Provide inverted parameter tools so that "which elements have X" is one call.
4. Make every answer carry its derivation: totals on lists, graphs and run records for
   dataflow questions.
5. Treat compliance checks as queries with a verdict column, and require that missing data
   produce an explicit verdict rather than a silent pass.
6. Use MCP so that the same server serves a chat client, a custom agent, and the web editor.
