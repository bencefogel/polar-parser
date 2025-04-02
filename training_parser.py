import json
import pandas as pd
from datetime import datetime, timedelta
import isodate

# Read json file (downloaded from Polar website)
fpath = ('polar-user-data-export_893fd6db-18ac-476f-926f-b14580234d91-0411707/'
     'training-session-2025-02-21-8069454250-37672a75-5c69-4638-b765-17e954ed785f.json')
with open(fpath) as f:
    data = json.load(f)

# Convert exercises into a DataFrame
exercises = data["exercises"]
exercise_list = []

for ex in exercises:
    # Convert start and stop time to datetime and apply timezone offset
    start = datetime.fromisoformat(ex["startTime"]) + timedelta(minutes=ex["timezoneOffset"])
    stop = datetime.fromisoformat(ex["stopTime"]) + timedelta(minutes=ex["timezoneOffset"])

    # Convert duration from ISO 8601 to timedelta
    duration = isodate.parse_duration(ex["duration"])  # Returns timedelta

    exercise_list.append(
        {
            "start": start,
            "stop": stop,
            "duration": str(duration),  # Keeping as string for better readability
            "calories": ex["kiloCalories"],
            "hr_avg": ex["heartRate"]["avg"],
            "hr_min": ex["heartRate"]["min"],
            "hr_max": ex["heartRate"]["max"],
        }
    )

df_exercises = pd.DataFrame(exercise_list)

# Convert heart rate samples into a separate DataFrame
hr_samples = []
for ex in exercises:
    for sample in ex["samples"]["heartRate"]:
        sample_time = datetime.fromisoformat(sample["dateTime"]) + timedelta(
            minutes=ex["timezoneOffset"]
        )
        hr_samples.append({"dateTime": sample_time, "heartRate": sample["value"]})

df_hr_samples = pd.DataFrame(hr_samples)