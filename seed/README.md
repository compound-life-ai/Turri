# Seed Data

Fixture files that mirror `longevityOS-data/` for development and testing.

## Contents

| File | Description |
|---|---|
| `nutrition/meals.csv` | 3 days of meals (7 meals, 20 ingredient rows) |
| `health/profile.json` | Health profile with goals, questionnaire answers, and Apple Health import |
| `insights/experiments.json` | 1 active + 1 completed experiment |
| `insights/checkins.json` | 9 check-ins across both experiments |
| `news/cache.json` | 6 sample news items from the 3 configured sources |

## Usage

For an installed OpenClaw bundle, use the installer so the data lands in the managed bundle path:

```bash
python3 scripts/install_bundle.py --seed-data
```

For repo-local development, copy the seed files into the repo data directory:

```bash
cp -r seed/* longevityOS-data/
```

To reset back to empty:

```bash
rm longevityOS-data/nutrition/meals.csv
rm longevityOS-data/health/profile.json
rm longevityOS-data/insights/experiments.json
rm longevityOS-data/insights/checkins.json
rm longevityOS-data/news/cache.json
```
