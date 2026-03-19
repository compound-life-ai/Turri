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
4. Confirm that `~/.openclaw/openclaw.json` now includes the installed bundle `skills/` path inside `skills.load.extraDirs`.
5. Tell the user to start a new OpenClaw session.
6. Tell the user to verify that `/snap`, `/health`, `/news`, and `/insights` are available.
7. If needed, tell the user to configure the cron templates from the installed `cron/` directory with their Telegram DM chat id.
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

The installer:

- copies `skills/`, `scripts/`, `cron/`, and `docs/`
- initializes `longevityOS-data/`
- registers the installed `skills/` directory in `skills.load.extraDirs`

After install:

1. Start a new OpenClaw session.
2. Verify `/snap`, `/health`, `/news`, and `/insights` are available.
3. Configure the cron templates in `cron/` with your Telegram DM chat id.

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
