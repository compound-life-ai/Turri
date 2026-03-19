from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.common.paths import repo_root


SKILLS = ["snap", "health", "news", "insights"]


def ensure_symlink(link_path: Path, target: Path) -> None:
    link_path.parent.mkdir(parents=True, exist_ok=True)
    if link_path.is_symlink() or link_path.exists():
        if link_path.resolve() == target.resolve():
            return
        raise FileExistsError(f"{link_path} already exists and points elsewhere")
    link_path.symlink_to(target)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Symlink this bundle's skills into an OpenClaw workspace."
    )
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()

    root = repo_root()
    workspace = args.workspace.expanduser().resolve()
    for skill in SKILLS:
        ensure_symlink(workspace / "skills" / skill, root / "skills" / skill)

    print("Installed skill symlinks:")
    for skill in SKILLS:
        print(f"- {workspace / 'skills' / skill} -> {root / 'skills' / skill}")
    print("")
    print("Next:")
    print("1. Start a new OpenClaw session so the skill snapshot refreshes.")
    print("2. Add the cron jobs from cron/README.md using your Telegram DM chat id.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
