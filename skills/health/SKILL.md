---
name: health
description: Build and update a normalized personal health profile from Apple Health XML imports and structured questionnaire answers for higher-quality lifestyle recommendations.
user-invocable: true
---

# Health

Use this skill when:

- the user invokes `/health`
- the user wants more personalized recommendations
- the user uploads Apple Health export XML
- the user is answering health baseline questions

Rules:

- Reply in the user's language.
- V1 supports Apple Health XML and structured questionnaire answers.
- Do not promise direct HealthKit sync, wearable APIs, or lab parsing in this version.
- Keep recommendations lifestyle-only.

Questionnaire flow:

1. Ask only the missing structured questions needed to update goals, constraints, preferences, and baseline notes.
2. Save a temp JSON file with fields such as `goals`, `constraints`, `preferences`, and `questionnaire`.
3. Run:

```bash
python3 "{baseDir}/../../scripts/health/profile_store.py" \
  --data-root "{baseDir}/../../longevityOS-data" \
  merge-questionnaire \
  --input-json /tmp/health_questionnaire.json
```

Apple Health import flow:

1. If the user uploaded `export.xml`, summarize it with:

```bash
python3 "{baseDir}/../../scripts/health/import_apple_health.py" \
  --input-xml /path/to/export.xml > /tmp/apple_health_summary.json
```

2. Merge the normalized summary into the profile with:

```bash
python3 "{baseDir}/../../scripts/health/profile_store.py" \
  --data-root "{baseDir}/../../longevityOS-data" \
  merge-import \
  --input-json /tmp/apple_health_summary.json
```

3. Tell the user what profile context is now available for future recommendations.

To inspect the current profile:

```bash
python3 "{baseDir}/../../scripts/health/profile_store.py" \
  --data-root "{baseDir}/../../longevityOS-data" \
  show
```
