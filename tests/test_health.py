from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.health.import_apple_health import average, parse_dt, summarize_export
from scripts.health.profile_store import (
    default_profile,
    merge_import,
    merge_questionnaire,
    profile_path,
    read_json,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


APPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<HealthData>
  <Record type="HKQuantityTypeIdentifierStepCount" sourceName="Apple Watch" unit="count" value="8000" startDate="2026-03-17 09:00:00 -0700" endDate="2026-03-17 10:00:00 -0700" />
  <Record type="HKQuantityTypeIdentifierStepCount" sourceName="Apple Watch" unit="count" value="4000" startDate="2026-03-18 09:00:00 -0700" endDate="2026-03-18 10:00:00 -0700" />
  <Record type="HKCategoryTypeIdentifierSleepAnalysis" sourceName="Apple Watch" value="HKCategoryValueSleepAnalysisAsleep" startDate="2026-03-17 23:00:00 -0700" endDate="2026-03-18 06:30:00 -0700" />
  <Record type="HKQuantityTypeIdentifierRestingHeartRate" sourceName="Apple Watch" unit="count/min" value="58" startDate="2026-03-18 08:00:00 -0700" endDate="2026-03-18 08:00:00 -0700" />
  <Workout workoutActivityType="HKWorkoutActivityTypeRunning" duration="45" durationUnit="min" startDate="2026-03-18 07:00:00 -0700" endDate="2026-03-18 07:45:00 -0700" />
</HealthData>
"""


class HealthScriptTests(unittest.TestCase):
    def test_parse_dt_and_average_helpers(self) -> None:
        parsed = parse_dt("2026-03-18 08:00:00 -0700")
        self.assertEqual(parsed.year, 2026)
        self.assertEqual(average([]), 0.0)
        self.assertEqual(average([1.0, 2.0, 3.0]), 2.0)

    def test_apple_health_summary_extracts_basics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            xml_path = Path(tmp_dir) / "export.xml"
            xml_path.write_text(APPLE_XML, encoding="utf-8")
            summary = summarize_export(xml_path)
            self.assertEqual(summary["counts"]["days_with_steps"], 2)
            self.assertGreater(summary["sleep"]["daily_sleep_hours_avg"], 7.0)
            self.assertEqual(summary["heart"]["resting_heart_rate_avg"], 58.0)
            self.assertEqual(summary["workouts"]["workout_count"], 1)
            self.assertEqual(summary["workouts"]["average_workout_minutes"], 45.0)

    def test_profile_merges_questionnaire_and_import(self) -> None:
        profile = default_profile()
        profile = merge_questionnaire(
            profile,
            {
                "goals": ["better sleep"],
                "constraints": ["no late caffeine"],
                "preferences": {"language": "bilingual"},
                "questionnaire": {"sleep_notes": "wake up once"},
                "diet_notes": "more protein",
            },
        )
        profile = merge_import(profile, {"source": "apple_health_export_xml", "file_name": "export.xml"})
        self.assertEqual(profile["goals"], ["better sleep"])
        self.assertEqual(profile["constraints"], ["no late caffeine"])
        self.assertEqual(profile["preferences"]["language"], "bilingual")
        self.assertEqual(profile["questionnaire"]["diet_notes"], "more protein")
        self.assertTrue(profile["imports"])

    def test_read_json_rejects_non_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "bad.json"
            path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")
            with self.assertRaises(ValueError):
                read_json(path)

    def test_profile_store_cli_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            data_root = Path(tmp_dir)
            questionnaire_path = data_root / "questionnaire.json"
            questionnaire_path.write_text(
                json.dumps(
                    {
                        "goals": ["better recovery"],
                        "questionnaire": {"training_notes": "hard sessions on Tue/Thu"},
                    }
                ),
                encoding="utf-8",
            )
            import_path = data_root / "apple.json"
            import_path.write_text(
                json.dumps({"source": "apple_health_export_xml", "file_name": "export.xml"}),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "scripts/health/profile_store.py",
                    "--data-root",
                    str(data_root),
                    "merge-questionnaire",
                    "--input-json",
                    str(questionnaire_path),
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    sys.executable,
                    "scripts/health/profile_store.py",
                    "--data-root",
                    str(data_root),
                    "merge-import",
                    "--input-json",
                    str(import_path),
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            show_result = subprocess.run(
                [
                    sys.executable,
                    "scripts/health/profile_store.py",
                    "--data-root",
                    str(data_root),
                    "show",
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(show_result.stdout)
            self.assertEqual(payload["goals"], ["better recovery"])
            self.assertEqual(payload["imports"][0]["file_name"], "export.xml")

    def test_import_apple_health_cli_outputs_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            xml_path = Path(tmp_dir) / "export.xml"
            xml_path.write_text(APPLE_XML, encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/health/import_apple_health.py",
                    "--input-xml",
                    str(xml_path),
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual(payload["file_name"], "export.xml")
            self.assertEqual(payload["counts"]["workouts"], 1)


if __name__ == "__main__":
    unittest.main()
