"""Tests for how check_toolkit_paths.py resolves deps/<name>/ paths, built on small git
repositories in a temporary folder laid out as node deps.mjs leaves the toolkit: every
repository the build reaches checked out once under deps/.

Run: python -m unittest discover -s checks -p "test_*.py"
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_toolkit_paths import Tree  # noqa: E402


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=repo,
                          check=True, capture_output=True, text=True).stdout.strip()


def commit(repo: Path, files: dict[str, str]) -> str:
    """Write files into repo (initialising it if needed), commit them, and return the commit."""
    if not (repo / ".git").exists():
        repo.mkdir(parents=True, exist_ok=True)
        git(repo, "init", "-q")
    for name, text in files.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "c")
    return git(repo, "rev-parse", "HEAD")


def deps_json(pins: dict[str, str]) -> str:
    return json.dumps({name: {"url": f"https://example.invalid/{name}", "commit": c} for name, c in pins.items()})


class TransitiveDeps(unittest.TestCase):
    """toolkit pins sdk; sdk pins leaf. leaf has LICENSE at its first commit only."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name) / "toolkit"
        deps = root / "deps"
        self.leaf_old = commit(deps / "leaf", {"LICENSE": "MIT"})
        git(deps / "leaf", "rm", "-q", "LICENSE")
        self.leaf_new = commit(deps / "leaf", {"NOTICE": "moved"})
        self.sdk = commit(deps / "sdk", {"deps.json": deps_json({"leaf": self.leaf_old})})
        commit(root, {".gitignore": "deps/\n"})
        self.root, self.deps = root, deps

    def tearDown(self):
        self.tmp.cleanup()

    def toolkit(self, pins: dict[str, str]) -> Tree:
        return Tree(self.root, commit(self.root, {"deps.json": deps_json(pins)}))

    def test_a_dependency_of_a_dependency_is_checked_at_its_pin(self):
        tree = self.toolkit({"sdk": self.sdk})
        self.assertTrue(tree.exists("deps/leaf/LICENSE"))
        self.assertFalse(tree.exists("deps/leaf/README.md"))
        self.assertFalse(tree.exists("deps/other/LICENSE"))

    def test_the_toolkit_pin_wins_over_a_dependency_pin(self):
        tree = self.toolkit({"sdk": self.sdk, "leaf": self.leaf_new})
        self.assertEqual(tree.deps["leaf"], self.leaf_new)
        self.assertFalse(tree.exists("deps/leaf/LICENSE"))

    def test_a_dependency_not_checked_out_adds_no_names(self):
        (self.deps / "sdk" / ".git").rename(self.deps / "sdk" / "git-moved")
        tree = self.toolkit({"sdk": self.sdk})
        self.assertIsNone(tree.exists("deps/sdk/deps.json"))
        self.assertNotIn("leaf", tree.deps)


if __name__ == "__main__":
    unittest.main()
