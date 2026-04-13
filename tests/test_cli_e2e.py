from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "demo_codex_session.jsonl"


class CliE2ETests(unittest.TestCase):
    def test_analyze_auto_switches_to_xianxia_card(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "vibecoding_skill.cli",
                    "analyze",
                    "--path",
                    str(DEMO),
                    "--source",
                    "codex",
                    "--no-memory",
                    "--card-dir",
                    tmpdir,
                ],
                cwd=ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            self.assertTrue((Path(tmpdir) / "vibecoding-card-xianxia.svg").exists())
            self.assertTrue((Path(tmpdir) / "vibecoding-card-xianxia.png").exists())

    def test_export_emits_end_to_end_bundle_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "vibecoding_skill.cli",
                    "export",
                    "--path",
                    str(DEMO),
                    "--source",
                    "codex",
                    "--export-dir",
                    tmpdir,
                ],
                cwd=ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            root = Path(tmpdir)
            self.assertTrue((root / "README.md").exists())
            self.assertTrue((root / ".cursor" / "rules").exists())
            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("assets/vibecoding-card-xianxia.png", readme)
            self.assertIn(".cursor/rules/", readme)

    def test_export_captures_model_and_renders_platform_model_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "vibecoding_skill.cli",
                    "export",
                    "--path",
                    str(DEMO),
                    "--source",
                    "codex",
                    "--export-dir",
                    tmpdir,
                ],
                cwd=ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            root = Path(tmpdir)
            snapshot = json.loads((root / "snapshot.json").read_text(encoding="utf-8"))
            self.assertEqual(snapshot["transcript"]["models"], ["openai/gpt-5.4"])
            self.assertEqual(snapshot["transcript"]["providers"], ["openai"])
            svg = (root / "assets" / "vibecoding-card-xianxia.svg").read_text(encoding="utf-8")
            self.assertIn("Codex · gpt-5.4", svg)


if __name__ == "__main__":
    unittest.main()
