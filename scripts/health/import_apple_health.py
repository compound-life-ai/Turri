from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))


SLEEP_TYPES = {
    "HKCategoryValueSleepAnalysisAsleep",
    "HKCategoryValueSleepAnalysisAsleepCore",
    "HKCategoryValueSleepAnalysisAsleepDeep",
    "HKCategoryValueSleepAnalysisAsleepREM",
    "HKCategoryValueSleepAnalysisAsleepUnspecified",
}


def parse_dt(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S %z")


def average(values: list[float]) -> float:
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)


def summarize_export(xml_path: Path) -> dict[str, Any]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    step_days: dict[str, float] = defaultdict(float)
    sleep_days: dict[str, float] = defaultdict(float)
    resting_hr: list[float] = []
    heart_rate: list[float] = []
    active_energy_days: dict[str, float] = defaultdict(float)
    exercise_minutes_days: dict[str, float] = defaultdict(float)
    workout_minutes: list[float] = []

    record_count = 0
    workout_count = 0

    for record in root.findall("Record"):
        record_count += 1
        record_type = record.attrib.get("type")
        value = record.attrib.get("value", "0")
        start_date = record.attrib.get("startDate")
        end_date = record.attrib.get("endDate")
        if not start_date or not end_date:
            continue
        start = parse_dt(start_date)
        end = parse_dt(end_date)
        date_key = start.date().isoformat()

        if record_type == "HKQuantityTypeIdentifierStepCount":
            step_days[date_key] += float(value)
        elif record_type == "HKCategoryTypeIdentifierSleepAnalysis":
            if value in SLEEP_TYPES:
                hours = max((end - start).total_seconds() / 3600.0, 0.0)
                sleep_days[date_key] += hours
        elif record_type == "HKQuantityTypeIdentifierRestingHeartRate":
            resting_hr.append(float(value))
        elif record_type == "HKQuantityTypeIdentifierHeartRate":
            heart_rate.append(float(value))
        elif record_type == "HKQuantityTypeIdentifierActiveEnergyBurned":
            active_energy_days[date_key] += float(value)
        elif record_type == "HKQuantityTypeIdentifierAppleExerciseTime":
            exercise_minutes_days[date_key] += float(value)

    for workout in root.findall("Workout"):
        workout_count += 1
        duration = float(workout.attrib.get("duration", "0") or 0.0)
        if workout.attrib.get("durationUnit") == "min":
            workout_minutes.append(duration)
        elif duration:
            workout_minutes.append(duration)

    step_values = list(step_days.values())
    sleep_values = [round(value, 2) for value in sleep_days.values()]
    active_energy_values = list(active_energy_days.values())
    exercise_minutes_values = list(exercise_minutes_days.values())

    summary = {
        "imported_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": "apple_health_export_xml",
        "file_name": xml_path.name,
        "counts": {
            "records": record_count,
            "workouts": workout_count,
            "days_with_steps": len(step_days),
            "days_with_sleep": len(sleep_days),
        },
        "activity": {
            "daily_steps_avg": round(average(step_values)),
            "daily_active_energy_kcal_avg": round(average(active_energy_values), 2),
            "daily_exercise_minutes_avg": round(average(exercise_minutes_values), 2),
            "step_days": len(step_days),
        },
        "sleep": {
            "daily_sleep_hours_avg": round(average(sleep_values), 2),
            "sleep_days": len(sleep_days),
            "daily_sleep_hours_values": sleep_values[-14:],
        },
        "heart": {
            "resting_heart_rate_avg": round(average(resting_hr), 2),
            "heart_rate_avg": round(average(heart_rate), 2),
            "sample_count": len(resting_hr) + len(heart_rate),
        },
        "workouts": {
            "workout_count": workout_count,
            "average_workout_minutes": round(average(workout_minutes), 2),
        },
    }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize Apple Health export XML.")
    parser.add_argument("--input-xml", type=Path, required=True)
    args = parser.parse_args()

    print(json.dumps(summarize_export(args.input_xml), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
