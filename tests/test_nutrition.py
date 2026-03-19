from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.nutrition.estimate_and_log import (
    FIELDNAMES,
    load_payload,
    log_payload,
    parse_timestamp,
    slug_date,
    summarize_day,
    to_float,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class NutritionScriptTests(unittest.TestCase):
    def test_load_payload_and_scalar_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "payload.json"
            payload = {"ingredients": [{"name": "egg"}]}
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(load_payload(path), payload)
            self.assertEqual(parse_timestamp("2026-03-18T12:30:00Z"), "2026-03-18T12:30:00+00:00")
            self.assertEqual(slug_date("2026-03-18T12:30:00+00:00"), "2026-03-18")
            self.assertEqual(to_float("1.236"), 1.24)
            self.assertEqual(to_float(""), 0.0)

    def test_load_payload_rejects_missing_ingredients(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "bad.json"
            path.write_text(json.dumps({"ingredients": []}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_payload(path)

    def test_log_payload_writes_ingredient_rows_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_root = Path(tmp_dir)
            payload = {
                "timestamp": "2026-03-18T12:30:00-07:00",
                "meal_type": "lunch",
                "source": "photo",
                "confidence": 0.8,
                "ingredients": [
                    {
                        "name": "salmon",
                        "portion": "150 g",
                        "calories_kcal": 280,
                        "protein_g": 30,
                        "fat_g": 18,
                        "carbs_g": 0,
                        "fiber_g": 0,
                        "micronutrients": {"vitamin_d_iu": 540},
                    },
                    {
                        "name": "rice",
                        "portion": "1 bowl",
                        "calories_kcal": 240,
                        "protein_g": 4,
                        "fat_g": 1,
                        "carbs_g": 53,
                        "fiber_g": 1,
                        "micronutrients": {"manganese_mg": 0.7},
                    },
                ],
            }

            result = log_payload(payload, data_root)

            self.assertEqual(result["ingredient_count"], 2)
            self.assertEqual(result["meal_totals"]["calories_kcal"], 520.0)
            self.assertEqual(result["day_summary"]["top_micros"][0]["name"], "manganese_mg")
            summary = summarize_day(data_root, "2026-03-18")
            self.assertEqual(summary["meal_count"], 1)
            self.assertEqual(summary["entries"], 2)
            self.assertEqual(summary["protein_g"], 34.0)
            with (data_root / "nutrition" / "meals.csv").open(
                "r", encoding="utf-8", newline=""
            ) as handle:
                reader = csv.DictReader(handle)
                self.assertEqual(reader.fieldnames, FIELDNAMES)
                rows = list(reader)
            self.assertEqual(rows[0]["ingredient_name"], "salmon")

    def test_log_payload_rejects_bad_ingredient_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_root = Path(tmp_dir)
            with self.assertRaises(ValueError):
                log_payload({"ingredients": [{"name": " ", "micronutrients": {}}]}, data_root)
            with self.assertRaises(ValueError):
                log_payload({"ingredients": [{"name": "rice", "micronutrients": []}]}, data_root)

    def test_cli_log_and_summary_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_root = Path(tmp_dir)
            payload_path = data_root / "payload.json"
            payload_path.parent.mkdir(parents=True, exist_ok=True)
            payload_path.write_text(
                json.dumps(
                    {
                        "timestamp": "2026-03-18T08:00:00+00:00",
                        "meal_type": "breakfast",
                        "source": "manual",
                        "ingredients": [
                            {
                                "name": "oats",
                                "portion": "1 bowl",
                                "calories_kcal": 200,
                                "protein_g": 8,
                                "carbs_g": 34,
                                "fat_g": 4,
                                "fiber_g": 5,
                                "micronutrients": {"iron_mg": 3.5},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            log_result = subprocess.run(
                [
                    sys.executable,
                    "scripts/nutrition/estimate_and_log.py",
                    "--data-root",
                    str(data_root),
                    "log",
                    "--input-json",
                    str(payload_path),
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            summary_result = subprocess.run(
                [
                    sys.executable,
                    "scripts/nutrition/estimate_and_log.py",
                    "--data-root",
                    str(data_root),
                    "summary",
                    "--date",
                    "2026-03-18",
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            log_payload_out = json.loads(log_result.stdout)
            summary_payload = json.loads(summary_result.stdout)
            self.assertTrue(log_payload_out["ok"])
            self.assertEqual(summary_payload["meal_count"], 1)
            self.assertEqual(summary_payload["entries"], 1)


if __name__ == "__main__":
    unittest.main()
