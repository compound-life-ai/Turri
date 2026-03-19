---
name: snap
description: Log meals from food photos or meal text with ingredient-centric calorie and micronutrient estimates, brief confirmations, and daily running totals.
user-invocable: true
---

# Snap

Use this skill when:

- the user invokes `/snap`
- the user sends a likely food photo
- the user sends a meal description they want logged

Behavior rules:

- Reply in the user's language.
- If a photo-only message has low confidence, ask a brief confirmation before logging anything.
- If confidence is high, proceed directly.
- Prefer fast, clearly-labeled estimates over fake precision.
- Store the full micronutrient payload, but only mention the top 3 notable micronutrient signals in the visible confirmation.

Logging flow:

1. Infer a meal-level estimate and decompose it into ingredients.
2. Write a JSON payload to a temp file.
3. Run:

```bash
python3 "{baseDir}/../../scripts/nutrition/estimate_and_log.py" \
  --data-root "{baseDir}/../../longevityOS-data" \
  log \
  --input-json /tmp/snap_payload.json
```

Payload shape:

```json
{
  "timestamp": "2026-03-18T12:30:00-07:00",
  "meal_type": "lunch",
  "source": "photo",
  "photo_ref": "telegram:file-id-or-message-ref",
  "confidence": 0.82,
  "notes": "optional free text",
  "ingredients": [
    {
      "name": "salmon",
      "portion": "150 g",
      "calories_kcal": 280,
      "protein_g": 30,
      "carbs_g": 0,
      "fat_g": 18,
      "fiber_g": 0,
      "micronutrients": { "vitamin_d_iu": 540, "selenium_mcg": 54 },
      "confidence": 0.78
    }
  ]
}
```

After logging:

- confirm what was logged
- show meal calories/macros
- include today's running totals if they are useful
- keep the response short unless the user asks for detail
