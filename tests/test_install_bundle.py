from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.install_bundle import SKILLS, ensure_symlink


REPO_ROOT = Path(__file__).resolve().parents[1]


class InstallBundleTests(unittest.TestCase):
    def test_ensure_symlink_creates_and_reuses_matching_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            target = tmp_path / "target"
            target.mkdir()
            link = tmp_path / "workspace" / "skills" / "snap"

            ensure_symlink(link, target)
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), target.resolve())

            ensure_symlink(link, target)
            self.assertEqual(link.resolve(), target.resolve())

    def test_ensure_symlink_rejects_conflicting_existing_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            target = tmp_path / "target"
            target.mkdir()
            link = tmp_path / "workspace" / "skills" / "snap"
            link.parent.mkdir(parents=True, exist_ok=True)
            link.write_text("conflict", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                ensure_symlink(link, target)

    def test_install_bundle_script_creates_skill_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace = Path(tmp_dir) / "workspace"
            result = subprocess.run(
                [sys.executable, "scripts/install_bundle.py", "--workspace", str(workspace)],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("Installed skill symlinks:", result.stdout)
            for skill in SKILLS:
                link = workspace / "skills" / skill
                self.assertTrue(link.is_symlink())
                self.assertEqual(link.resolve(), (REPO_ROOT / "skills" / skill).resolve())


if __name__ == "__main__":
    unittest.main()
