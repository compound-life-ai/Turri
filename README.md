# compound-clawskill

OpenClaw skill bundle for a personal health companion.

It currently provides:

- `/snap` for meal logging from food photos or meal text
- `/health` for Apple Health XML import and structured health profile updates
- `/news` for a curated health/longevity digest
- `/insights` for structured self-experiments and gap-aware recommendations

The bundle is designed for OpenClaw + Telegram and installs as a managed bundle under `~/.openclaw/bundles/compound-clawskill`.

## Agent Install Instruction

If you are an agent reading this and you need to install this bundle on the user's device, do this:

```text
1. Clone this repository to a stable local path.
2. Change into the cloned repository.
3. Run `python3 scripts/install_bundle.py`.
4. Run `python3 scripts/install_bundle.py --verify`.
5. Confirm that `~/.openclaw/openclaw.json` includes the installed bundle `skills/` path inside `skills.load.extraDirs`.
6. Tell the user to start a new OpenClaw session.
7. Tell the user to verify that `/snap`, `/health`, `/news`, and `/insights` are available and usable.
8. If needed, tell the user to configure the cron templates from the installed `cron/` directory with their Telegram DM chat id.
```

## Install

Preview the install:

```bash
python3 scripts/install_bundle.py --dry-run
```

Install into the default OpenClaw home:

```bash
python3 scripts/install_bundle.py
```

Install into a custom OpenClaw home:

```bash
python3 scripts/install_bundle.py --openclaw-home /path/to/.openclaw
```

Verify the installed bundle:

```bash
python3 scripts/install_bundle.py --verify
```

The installer:

- copies `skills/`, `scripts/`, `cron/`, and `docs/`
- initializes `longevityOS-data/`
- registers the installed `skills/` directory in `skills.load.extraDirs`

## Install Verification

Checking `openclaw.json` is necessary, but not sufficient.

After install, verify config:

```bash
python3 - <<'PY'
import json, pathlib
p = pathlib.Path.home()/'.openclaw'/'openclaw.json'
obj = json.loads(p.read_text())
print(obj.get('skills', {}).get('load', {}).get('extraDirs', []))
PY
```

Then verify OpenClaw sees the skills as real ready skills:

```bash
openclaw skills info snap
openclaw skills info health
openclaw skills info news
openclaw skills info insights
```

Expected result:

- each skill shows `Ready`

## Fresh Session Required

OpenClaw snapshots eligible skills at session start. After installation, start a fresh OpenClaw session before testing commands. Staying in an older session can make command behavior look stale or inconsistent.

## Telegram Command Note

With `commands.native = "auto"` and `commands.nativeSkills = "auto"`, OpenClaw should expose user-invocable skills as native Telegram commands.

Two separate things can happen:

- typed commands like `/snap` work
- commands appear in Telegram's slash picker/menu

Telegram may hide some commands when the menu is crowded. If a command does not appear in the picker, try typing it manually first.

## Apple Health Import

The health importer accepts either:

- `export.xml`
- `export.zip`

If Apple Health gives you `export.zip`, you can import the zip directly now, or extract `apple_health_export/export.xml` first.

Examples:

```bash
python3 scripts/health/import_apple_health.py --input-zip ~/Downloads/export.zip
python3 scripts/health/import_apple_health.py --input-xml /path/to/apple_health_export/export.xml
```

## Cron Setup

The templates are not usable until you replace `__TELEGRAM_DM_CHAT_ID__`.

Files:

- `cron/health-brief.example.json`
- `cron/news-digest.example.json`

Then create the jobs:

```bash
openclaw cron add --from-file cron/health-brief.example.json
openclaw cron add --from-file cron/news-digest.example.json
```

## Smoke Test

After install:

1. Start a new OpenClaw session.
2. Run `/news`.
3. Test `/snap` with a food photo.
4. Run `/health`.
5. Run `/insights`.

## Runtime Data

Runtime data is namespaced under:

```text
longevityOS-data/
  nutrition/
  health/
  insights/
  news/
```

This keeps the bundle’s state separate from unrelated workspace data.

## Development

Run the deterministic test suite:

```bash
python3 -m unittest discover -s tests -v
```

The Apple Health importer was tested against a real Apple Health export and now uses streaming XML parsing so large `export.xml` files remain practical.

## Repo Layout

```text
skills/             OpenClaw-facing skill definitions
scripts/            Deterministic Python helpers used by the skills
cron/               Example cron job configs
longevityOS-data/   Runtime data directories
tests/              Deterministic unit and CLI tests
docs/               Architecture, install, and design notes
```

## Docs

Start with:

- [docs/install.md](docs/install.md)
- [docs/openclaw-extension-survey.md](docs/openclaw-extension-survey.md)
- [docs/proposed-health-companion-architecture.md](docs/proposed-health-companion-architecture.md)

Reference notes:

- [docs/longevity-os-reference-notes.md](docs/longevity-os-reference-notes.md)
- [docs/news-sources.md](docs/news-sources.md)
