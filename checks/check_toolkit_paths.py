"""Fail when a file in this repository names a path into the BIM Open Toolkit that does not
exist at the commit the bim-open-toolkit submodule is pinned to.

Usage: python checks/check_toolkit_paths.py [--verbose]

What it scans: tracked and new (not ignored) Markdown, scripts, and configuration files in
this repository (README.md, CLAUDE.md, .mcp.json, .claude/launch.json, poc/, paper/, csproj
files, workflows). It skips recorded evidence (poc/results/, poc/store/), data folders, and
the submodule itself.

What counts as a toolkit path:
  - anything containing "bim-open-toolkit/" (relative, ../.., absolute, or with backslashes):
    the part after the last "bim-open-toolkit/" is the toolkit path;
  - a path that starts with one of the toolkit's top-level folders (src/, scripts/,
    bimopenflow/, viz/, samples/, ...) that this repository does not also have at its root.

Where a path is looked up: in the toolkit's file list at the pinned commit (the gitlink in
this repository's index), so a working copy that has moved does not hide a broken path.
Paths inside the toolkit's own submodules are looked up at their pinned commits when they are
checked out. Build outputs cannot be in git, so they are checked through what produces them:
"<dir>/node_modules/..." needs "<dir>/package.json", and "artifacts/<name>/..." needs some
tracked toolkit file that mentions "artifacts/<name>".

Not checked: GitHub URLs pinned to a commit (".../blob/71790a7/..."), which are citations;
GitHub URLs on a branch, which point at the live repository rather than the pin (listed with
--verbose); and paths with placeholders such as <id> or {DUCKDB}.

A reference already known to be missing at the pin is listed, with its reason, in
checks/known-missing-paths.txt (one "file | toolkit path | reason" per line). It is reported
as KNOWN and does not fail the check; an entry that no longer matches a missing reference
fails it, so the list shrinks when a reference is fixed.

Exit code 0 when every recognised path exists or is known missing, 1 otherwise. Standard
library only.
"""
from __future__ import annotations

import fnmatch
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMODULE = "bim-open-toolkit"
SCANNED_SUFFIXES = {".md", ".py", ".mjs", ".js", ".ts", ".json", ".yml", ".yaml", ".csproj",
                    ".cs", ".ps1", ".sh", ".props", ".targets"}
SKIPPED_PREFIXES = ("poc/results/", "poc/store/", "poc/data/", "data/", "IFC-Test-Kit/",
                    f"{SUBMODULE}/", "checks/")
# Recorded evidence from 2026-08-04 about ara3d-sdk, the toolkit's predecessor; every path in
# them is pinned by a commit link to that repository, not to this submodule.
SKIPPED_FILES = {"bos-validation-evidence.md", "door-clearance-demo.md", "door-clearance-summary.md"}
# Tokens shaped like toolkit paths that are not paths: MCP method names.
NOT_PATHS = {"tools/call", "tools/list"}
KNOWN_MISSING = Path(__file__).resolve().with_name("known-missing-paths.txt")
TOKEN = re.compile(r"[A-Za-z0-9_.~:/\\@+\-*{}<>$%]+")
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(https?://[^)]*\)")
COMMIT_URL = re.compile(r"github\.com/[^/]+/bim-open-toolkit/(?:blob|tree|raw|commit)/[0-9a-f]{7,40}(?:/|$)")
BRANCH_URL = re.compile(r"github\.com/[^/]+/bim-open-toolkit/(?:blob|tree|raw)/")
LINE_SUFFIX = re.compile(r"(?::\d+(?:[-,:]\d+)*|#L\d+(?:-L\d+)?|#[\w-]*)$")


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True, encoding="utf-8").stdout


def pinned_commit(repo: Path, path: str) -> str:
    """The commit a submodule is pinned to in repo's index."""
    return git("ls-files", "-s", "--", path, cwd=repo).split()[1]


class Tree:
    """The files, folders and nested submodules of one repository at one commit."""

    def __init__(self, repo: Path, commit: str):
        self.repo, self.commit = repo, commit
        self.files: set[str] = set()
        self.dirs: set[str] = set()
        self.gitlinks: dict[str, str] = {}
        for line in git("ls-tree", "-r", "-t", commit, cwd=repo).splitlines():
            meta, path = line.split("\t", 1)
            _mode, kind, sha = meta.split()
            if kind == "blob":
                self.files.add(path)
            elif kind == "tree":
                self.dirs.add(path)
            elif kind == "commit":
                self.gitlinks[path] = sha
        self.top = {p.split("/", 1)[0] for p in self.files | self.dirs | set(self.gitlinks)}

    def exists(self, path: str) -> bool | None:
        """True or False when the path can be decided; None when it lies in a nested
        submodule that is not checked out."""
        path = path.strip("/")
        if any(ch in path for ch in "*?["):
            return any(fnmatch.fnmatch(p, path) for p in self.files | self.dirs)
        if path in self.files or path in self.dirs or path in self.gitlinks:
            return True
        for link, sha in self.gitlinks.items():
            if path.startswith(link + "/"):
                nested = self.repo / link
                if not (nested / ".git").exists():
                    return None
                return nested_tree(str(nested), sha).exists(path[len(link) + 1:])
        return False


@lru_cache(maxsize=None)
def nested_tree(repo: str, commit: str) -> Tree:
    return Tree(Path(repo), commit)


@lru_cache(maxsize=None)
def mentioned_at_pin(tree: Tree, text: str) -> bool:
    result = subprocess.run(["git", "grep", "-q", "-F", text, tree.commit],
                            cwd=tree.repo, capture_output=True)
    return result.returncode == 0


def scanned_files() -> list[str]:
    listed = git("ls-files", "--cached", "--others", "--exclude-standard").splitlines()
    return sorted(
        f for f in set(listed)
        if Path(f).suffix in SCANNED_SUFFIXES and not f.startswith(SKIPPED_PREFIXES)
        and f not in SKIPPED_FILES
        and "/bin/" not in f and "/obj/" not in f and (ROOT / f).is_file())


def clean(token: str) -> str:
    token = token.replace("\\\\", "/").replace("\\", "/")
    token = token.strip("`'\"()[]<>,;.:")
    token = LINE_SUFFIX.sub("", token)
    return token.rstrip(".,;:")


def candidates(text: str, local_top: set[str], tree: Tree):
    """(line number, toolkit path) for each toolkit path the text names."""
    for lineno, line in enumerate(text.splitlines(), 1):
        # The text of a link to a web page names that page, not a path in the submodule.
        line = MARKDOWN_LINK.sub(" ", line)
        for m in TOKEN.finditer(line):
            raw = m.group(0)
            if "://" in raw or raw.startswith("github.com"):
                continue
            token = clean(raw)
            if not token or token in NOT_PATHS or any(ch in token for ch in "<>{}$%") or "..." in token.replace("../", ""):
                continue
            marker = f"{SUBMODULE}/"
            if marker in token:
                rest = token.rsplit(marker, 1)[1]
                if rest:
                    yield lineno, rest
                continue
            parts = re.sub(r"^(\.\.?/)+", "", token).split("/")
            if (len(parts) >= 2 and parts[1] and parts[0] in tree.top
                    and parts[0] not in local_top and not token.startswith(("/", "~"))):
                yield lineno, "/".join(parts)


def generated_ok(tree: Tree, path: str) -> bool | None:
    """Build outputs: checked through the file or folder that produces them."""
    if "/node_modules/" in path or path.startswith("node_modules/"):
        owner = path.split("node_modules/", 1)[0].rstrip("/")
        return tree.exists(f"{owner}/package.json" if owner else "package.json")
    if path.startswith("artifacts/"):
        parts = path.split("/")
        return mentioned_at_pin(tree, "/".join(parts[:2])) if len(parts) > 1 else True
    if "/bin/" in path or "/obj/" in path:
        return tree.exists(re.split(r"/(?:bin|obj)/", path, 1)[0])
    return None


def known_missing() -> dict[tuple[str, str], str]:
    known = {}
    if KNOWN_MISSING.exists():
        for line in KNOWN_MISSING.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                f, path, reason = (part.strip() for part in line.split("|", 2))
                known[(f, path)] = reason
    return known


def main() -> int:
    verbose = "--verbose" in sys.argv
    commit = pinned_commit(ROOT, SUBMODULE)
    tree = Tree(ROOT / SUBMODULE, commit)
    local_top = {p.split("/", 1)[0] for p in git("ls-files").splitlines()}

    missing, checked, unknown, branch_urls = [], 0, [], []
    for f in scanned_files():
        text = (ROOT / f).read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            if BRANCH_URL.search(line) and not COMMIT_URL.search(line):
                branch_urls.append(f"{f}:{lineno}")
        for lineno, path in candidates(text, local_top, tree):
            checked += 1
            found = generated_ok(tree, path)
            if found is None:
                found = tree.exists(path)
            if found is None:
                unknown.append(f"{f}:{lineno}: {path}")
            elif not found:
                missing.append((f, lineno, path))

    known = known_missing()
    seen = {(f, path) for f, _, path in missing}
    stale = [k for k in known if k not in seen]
    failing = [m for m in missing if (m[0], m[2]) not in known]

    print(f"Toolkit pinned at {commit[:7]}; {checked} path references checked.")
    for line in unknown:
        print(f"UNCHECKED (nested submodule not checked out)  {line}")
    if verbose:
        for line in branch_urls:
            print(f"BRANCH URL (not checked)  {line}")
    for f, lineno, path in missing:
        reason = known.get((f, path))
        print(f"{'KNOWN  ' if reason else 'MISSING'}  {f}:{lineno}: {path}" + (f"  ({reason})" if reason else ""))
    for f, path in stale:
        print(f"STALE ENTRY  {f} | {path}: no longer missing; remove it from {KNOWN_MISSING.name}")
    print(f"{len(failing)} missing at {commit[:7]}, {len(missing) - len(failing)} known, {len(stale)} stale entries.")
    return 1 if failing or stale else 0


if __name__ == "__main__":
    sys.exit(main())
