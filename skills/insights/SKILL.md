---
name: insights
description: Guide structured self-experiments using observation, hypothesis, design, check-ins, analysis, and next-step recommendations grounded in local health and nutrition data.
user-invocable: true
---

# Insights

Use this skill when:

- the user invokes `/insights`
- the user wants a hypothesis, experiment, or analysis of recent health data

Rules:

- Reply in the user's language.
- Follow structured phases: observation, hypothesis, experiment design, active trial, check-in, analysis, next step.
- Keep recommendations lifestyle-only.
- If data is insufficient, do not improvise a strong recommendation. Run a gap analysis and ask for the missing data.

Start every `/insights` session with:

```bash
python3 "{baseDir}/../../scripts/insights/experiments.py" \
  --data-root "{baseDir}/../../longevityOS-data" \
  gap-report
```

If the user wants to start an experiment:

1. Build a JSON payload with `title`, `domain`, `hypothesis`, `null_hypothesis`, `intervention`, `primary_outcome`, and optional `secondary_outcomes`, windows, and questions.
2. Run:

```bash
python3 "{baseDir}/../../scripts/insights/experiments.py" \
  --data-root "{baseDir}/../../longevityOS-data" \
  create \
  --input-json /tmp/insights_experiment.json
```

For a daily check-in:

1. Capture compliance, 1 to 2 primary outcome scores, confounders, and a short note.
2. Run:

```bash
python3 "{baseDir}/../../scripts/insights/experiments.py" \
  --data-root "{baseDir}/../../longevityOS-data" \
  checkin \
  --input-json /tmp/insights_checkin.json
```

For experiment review:

```bash
python3 "{baseDir}/../../scripts/insights/experiments.py" \
  --data-root "{baseDir}/../../longevityOS-data" \
  analyze \
  --experiment-id <id>
```

When the script says more data is needed:

- explain exactly what is missing
- ask the user to collect that data
- tell them to return to `/insights` after enough data exists
