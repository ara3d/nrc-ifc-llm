"""Check that an enriched IFC file differs from its source only by the new property sets.

Usage: python poc/check_enriched_ifc.py <source.ifc> <enriched.ifc> <psets.csv> [--sha256 HEX]

Passes when all of these hold, and prints one line per check:
  - the enriched file is the source with a block of lines inserted, every source byte kept in
    place (the prefix before the block and the suffix after it are byte-identical);
  - every inserted line is an IFCPROPERTYSINGLEVALUE, IFCPROPERTYSET or
    IFCRELDEFINESBYPROPERTIES with an id above the source's highest id;
  - every inserted property set is attached by exactly one inserted relationship to entities
    that exist in the source, and every inserted value belongs to exactly one inserted set;
  - the inserted sets carry exactly the rows of the CSV (entity, set, property, value);
  - with --sha256, the enriched file has that SHA-256 (the hash in poc/results/enrich-report.json).

Exit code 0 when every check passes, 1 otherwise. Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ifc_step import Ref, Typed, entity_lines, parse_line  # noqa: E402

ADDED_TYPES = {"IFCPROPERTYSINGLEVALUE", "IFCPROPERTYSET", "IFCRELDEFINESBYPROPERTIES"}


def inserted_block(source: list[bytes], target: list[bytes]) -> tuple[int, list[bytes]] | None:
    """The insertion point and inserted lines when target is source with one block inserted."""
    extra = len(target) - len(source)
    if extra < 0:
        return None
    prefix = 0
    while prefix < len(source) and source[prefix] == target[prefix]:
        prefix += 1
    if source[prefix:] != target[prefix + extra:]:
        return None
    return prefix, target[prefix:prefix + extra]


def csv_rows(path: Path) -> Counter:
    rows = Counter()
    with open(path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            value = r["paramValue"]
            if r["valueType"] == "Real":
                value = float(value)
            elif r["valueType"] == "Integer":
                value = int(value)
            rows[(int(r["entityId"]), r["psetName"], r["paramName"], value)] += 1
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source", type=Path)
    ap.add_argument("enriched", type=Path)
    ap.add_argument("psets", type=Path)
    ap.add_argument("--sha256")
    a = ap.parse_args()

    results: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))

    src_bytes, dst_bytes = a.source.read_bytes(), a.enriched.read_bytes()
    src, dst = entity_lines(src_bytes), entity_lines(dst_bytes)
    block = inserted_block(src, dst)
    check("source bytes kept, one inserted block", block is not None,
          f"{len(dst) - len(src)} lines inserted" if block else "the files differ outside one inserted block")
    if block is None:
        return report(results)
    at, lines = block

    source_ids = {e.id for e in map(parse_line, src) if e is not None}
    max_source_id = max(source_ids)
    added = [parse_line(line) for line in lines]
    check("every inserted line is an entity", all(e is not None for e in added))
    added = [e for e in added if e is not None]
    by_id = {e.id: e for e in added}
    types = Counter(e.type for e in added)
    check("only property-set entity types inserted", set(types) <= ADDED_TYPES, repr(dict(types)))
    check("inserted ids above the source's highest id and unique",
          all(e.id > max_source_id for e in added) and len(by_id) == len(added),
          f"source max #{max_source_id}, inserted #{min(by_id)}..#{max(by_id)}")
    check("block inserted before ENDSEC of the DATA section", src[at].strip() == b"ENDSEC;")

    psets = {e.id: e for e in added if e.type == "IFCPROPERTYSET"}
    values = {e.id: e for e in added if e.type == "IFCPROPERTYSINGLEVALUE"}
    rels = [e for e in added if e.type == "IFCRELDEFINESBYPROPERTIES"]

    owners = Counter(ref.id for p in psets.values() for ref in p.args[4])
    check("every inserted value in exactly one inserted set",
          set(owners) == set(values) and all(n == 1 for n in owners.values()))
    attached = Counter(r.args[5].id for r in rels)
    check("every inserted set attached by exactly one inserted relationship",
          set(attached) == set(psets) and all(n == 1 for n in attached.values()))
    targets = {ref.id for r in rels for ref in r.args[4]}
    check("relationships attach only to source entities", targets <= source_ids,
          f"{len(targets)} entities")
    refs_ok = all(
        ref.id in source_ids or ref.id in by_id
        for e in added for ref in _refs(e.args))
    check("every reference resolves", refs_ok)

    written = Counter()
    for r in rels:
        pset = psets[r.args[5].id]
        for target in r.args[4]:
            for ref in pset.args[4]:
                v = values[ref.id].args[2]
                written[(target.id, pset.args[2], values[ref.id].args[0], v.value if isinstance(v, Typed) else v)] += 1
    expected = csv_rows(a.psets)
    missing, extra = expected - written, written - expected
    check("inserted values equal the CSV rows", not missing and not extra,
          f"{sum(written.values())} values in {len(psets)} sets"
          + (f"; missing {list(missing)[:3]}, extra {list(extra)[:3]}" if missing or extra else ""))

    if a.sha256:
        actual = hashlib.sha256(dst_bytes).hexdigest()
        check("enriched SHA-256 matches", actual == a.sha256.lower(), actual)
    return report(results)


def _refs(args):
    for v in args:
        if isinstance(v, Ref):
            yield v
        elif isinstance(v, list):
            yield from _refs(v)
        elif isinstance(v, Typed) and isinstance(v.value, (list, Ref)):
            yield from _refs(v.value if isinstance(v.value, list) else [v.value])


def report(results: list[tuple[str, bool, str]]) -> int:
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
    failed = sum(not ok for _, ok, _ in results)
    print(f"{len(results) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
