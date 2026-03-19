---
name: news
description: Fetch and summarize a curated daily digest of health, longevity, nutrition, sleep, exercise, and aging news from predefined sources.
user-invocable: true
---

# News

Use this skill when:

- the user invokes `/news`
- a scheduled digest needs to be generated

Rules:

- Reply in the user's language.
- Use the curated source list in the script, not open-ended web search, unless the user explicitly asks for research beyond the bundle.
- Keep health claims cautious and tied to the article context.

Run:

```bash
python3 "{baseDir}/../../scripts/news/fetch_digest.py" \
  --data-root "{baseDir}/../../longevityOS-data" \
  --limit 6
```

Then:

- summarize the top items
- mention source names
- explain relevance to nutrition, sleep, exercise, aging, or self-experimentation
- keep the scheduled digest compact
