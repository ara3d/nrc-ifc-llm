"""A minimal reader for the DATA section of an IFC STEP file (ISO 10303-21), enough for the
checks in this folder: entity ids, types, and attribute lists. Standard library only.

It handles the forms the Duplex model and the enrichment writer produce: references (#12),
strings with doubled quotes, numbers, enumerations (.T.), unset ($ and *), nested lists, and
typed values such as IFCREAL(1.5). It does not decode \\X2\\ escapes; strings are returned as
written.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

LINE = re.compile(rb"^#(\d+)\s*=\s*([A-Z0-9_]+)\s*\((.*)\);\s*$", re.S)


@dataclass(frozen=True)
class Ref:
    id: int


@dataclass(frozen=True)
class Typed:
    type: str
    value: object


@dataclass(frozen=True)
class Entity:
    id: int
    type: str
    args: list


def entity_lines(data: bytes) -> list[bytes]:
    """The raw lines of the file; the writer and the Duplex model put one entity per line."""
    return data.split(b"\n")


def parse_line(line: bytes) -> Entity | None:
    m = LINE.match(line.rstrip(b"\r"))
    if not m:
        return None
    return Entity(int(m.group(1)), m.group(2).decode("ascii"), parse_args(m.group(3).decode("latin-1")))


def read_entities(path: Path) -> dict[int, Entity]:
    entities = {}
    for line in entity_lines(path.read_bytes()):
        e = parse_line(line)
        if e is not None:
            entities[e.id] = e
    return entities


def parse_args(text: str) -> list:
    values, pos = _parse_list(text, 0, top=True)
    return values


def _parse_list(s: str, i: int, top: bool = False) -> tuple[list, int]:
    out = []
    while i < len(s):
        c = s[i]
        if c in " \t\r\n,":
            i += 1
        elif c == ")":
            if top:
                raise ValueError(f"unbalanced ')' at {i}")
            return out, i + 1
        else:
            value, i = _parse_value(s, i)
            out.append(value)
    if not top:
        raise ValueError("unterminated list")
    return out, i


NUMBER = re.compile(r"[-+]?(\d+\.?\d*|\.\d+)([eE][-+]?\d+)?")
NAME = re.compile(r"[A-Z0-9_]+")


def _parse_value(s: str, i: int):
    c = s[i]
    if c == "#":
        m = re.compile(r"#(\d+)").match(s, i)
        return Ref(int(m.group(1))), m.end()
    if c == "'":
        j, buf = i + 1, []
        while True:
            k = s.index("'", j)
            buf.append(s[j:k])
            if k + 1 < len(s) and s[k + 1] == "'":
                buf.append("'")
                j = k + 2
            else:
                return "".join(buf), k + 1
    if c == "(":
        return _parse_list(s, i + 1)
    if c in "$*":
        return None, i + 1
    if c == ".":
        k = s.index(".", i + 1)
        return s[i:k + 1], k + 1
    m = NUMBER.match(s, i)
    if m:
        text = m.group(0)
        return (float(text) if any(ch in text for ch in ".eE") else int(text)), m.end()
    m = NAME.match(s, i)
    if m and m.end() < len(s) and s[m.end()] == "(":
        inner, j = _parse_list(s, m.end() + 1)
        return Typed(m.group(0), inner[0] if len(inner) == 1 else inner), j
    raise ValueError(f"cannot parse STEP value at {i}: {s[i:i + 30]!r}")


def property_sets(entities: dict[int, Entity]) -> dict[int, dict[str, dict[str, object]]]:
    """Element id -> property set name -> property name -> value, through
    IFCRELDEFINESBYPROPERTIES, IFCPROPERTYSET and IFCPROPERTYSINGLEVALUE."""
    out: dict[int, dict[str, dict[str, object]]] = {}
    for e in entities.values():
        if e.type != "IFCRELDEFINESBYPROPERTIES":
            continue
        pset = entities[e.args[5].id]
        if pset.type != "IFCPROPERTYSET":
            continue
        values = {}
        for ref in pset.args[4]:
            prop = entities[ref.id]
            if prop.type == "IFCPROPERTYSINGLEVALUE":
                v = prop.args[2]
                values[prop.args[0]] = v.value if isinstance(v, Typed) else v
        for related in e.args[4]:
            out.setdefault(related.id, {})[pset.args[2]] = values
    return out


def storey_of(entities: dict[int, Entity]) -> dict[int, str]:
    """Element id -> storey name, walking up IFCRELCONTAINEDINSPATIALSTRUCTURE (an element in a
    space or a storey) and IFCRELAGGREGATES (a stair flight in a stair, a space in a storey)
    until a storey is reached. A storey maps to itself."""
    contained, parent = {}, {}
    for e in entities.values():
        if e.type == "IFCRELCONTAINEDINSPATIALSTRUCTURE":
            for ref in e.args[4]:
                contained[ref.id] = e.args[5].id
        elif e.type == "IFCRELAGGREGATES":
            for ref in e.args[5]:
                parent[ref.id] = e.args[4].id

    def resolve(eid: int) -> str | None:
        seen = set()
        while eid not in seen:
            seen.add(eid)
            e = entities[eid]
            if e.type == "IFCBUILDINGSTOREY":
                return e.args[2]
            if eid in contained:
                eid = contained[eid]
            elif eid in parent:
                eid = parent[eid]
            else:
                return None
        return None

    return {eid: name for eid in entities if (name := resolve(eid)) is not None}
