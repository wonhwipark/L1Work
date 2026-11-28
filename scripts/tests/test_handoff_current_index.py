import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("idx", HERE / "build_handoff_current_index.py")
idx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(idx)

class HandoffIndexTests(unittest.TestCase):
    def setUp(self):
        t = tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root = Path(t.name)
        (self.root / "handoffs").mkdir()
        (self.root / "handoffs/README.md").write_text("# old\n")
        (self.root / "handoffs/EXAMPLE_HANDOFF_r0001.md").write_text("# Example\n")
        for args in [("init", "-q"), ("config", "user.email", "test@example.com"),
                     ("config", "user.name", "test"), ("add", "."),
                     ("commit", "-qm", "baseline")]:
            subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)
        baseline = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                           cwd=self.root, text=True).strip()
        self.data = {"schema":"HANDOFF_CURRENT_INDEX_V1","baseline_commit":baseline,
                     "projects":[{"id":"test","title":"Test project","primary":"EXAMPLE_HANDOFF_r0001.md",
                                  "primary_label":"r0001","related":[],"status":"인계","next_action":"검증"}]}
        self.save()

    def save(self):
        (self.root/"handoffs/current-index.json").write_text(
            json.dumps(self.data, ensure_ascii=False), encoding="utf-8")

    def render(self):
        original = idx.ROOT
        original_readme = idx.README
        idx.ROOT = self.root
        idx.README = self.root / "handoffs/README.md"
        try:
            return idx.build()
        finally:
            idx.ROOT = original
            idx.README = original_readme

    def test_preserves_history_and_is_idempotent(self):
        result = self.render()
        self.assertIn("# old", result)
        self.assertIn("Test project", result)
        (self.root / "handoffs/README.md").write_text(result)
        self.assertEqual(result, self.render())

    def test_new_document_shown_pending_not_promoted(self):
        (self.root / "handoffs/EXAMPLE_HANDOFF_r0002.md").write_text("# New\n")
        subprocess.run(["git","add","."], cwd=self.root, check=True)
        subprocess.run(["git","commit","-qm","new"], cwd=self.root, check=True)
        text = self.render()
        self.assertIn("EXAMPLE_HANDOFF_r0002.md", text)
        self.assertIn("정본 미분류 / 실제 적용 미확인", text)
        self.assertIn("[r0001](EXAMPLE_HANDOFF_r0001.md)", text)

    def test_missing_file_rejected(self):
        self.data["projects"][0]["primary"] = "../missing.md"
        self.save()
        with self.assertRaises(ValueError):
            self.render()

    def test_duplicate_projects_rejected(self):
        self.data["projects"].append(dict(self.data["projects"][0]))
        self.save()
        with self.assertRaises(ValueError):
            self.render()

    def test_damaged_markers_rejected(self):
        (self.root / "handoffs/README.md").write_text(idx.START)
        with self.assertRaises(ValueError):
            self.render()

if __name__ == "__main__":
    unittest.main()
