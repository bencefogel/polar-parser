import json
import isodate
import glob
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


class TrainingParser:
    def __init__(self, folder_pattern: str = "polar-user-data-export*"):
        """Initialize the parser and find matching files."""
        self.folder_pattern = folder_pattern
        self.files = self.list_training_filenames()
        self.training_summary = pd.DataFrame()
        self.training_hr_samples = []

    def list_training_filenames(self) -> list:
        """Finds all training session JSON files in the first matching folder."""
        matching_folders = glob.glob(self.folder_pattern)
        if not matching_folders:
            print("No matching folders found.")
            return []
        folder_path = Path(matching_folders[0])  # Use the first matching folder, should be updated to handle multiple folders!!!
        return [f for f in folder_path.glob("training-session*.json")]

    def read_exercises(self, file_path: Path) -> dict:
        """Reads a JSON file and returns its content."""
        with open(file_path, "r") as f:
            data = json.load(f)
        return data.get("exercises", {})

    def parse_exercise_summary(self, exercises: list):
        """Parses exercise summary and appends to the DataFrame."""
        exercise_list = []
        for ex in exercises:
            try:
                start = datetime.fromisoformat(ex["startTime"]) + timedelta(minutes=ex.get("timezoneOffset", 0))
                stop = datetime.fromisoformat(ex["stopTime"]) + timedelta(minutes=ex.get("timezoneOffset", 0))
                duration = isodate.parse_duration(ex.get("duration", "PT0S")).total_seconds()

                exercise_list.append({
                    "start": start,
                    "stop": stop,
                    "duration_sec": duration,
                    "calories": ex.get("kiloCalories", 0),
                    "hr_avg": ex.get("heartRate", {}).get("avg"),
                    "hr_min": ex.get("heartRate", {}).get("min"),
                    "hr_max": ex.get("heartRate", {}).get("max"),
                })
            except (KeyError, ValueError, TypeError) as e:
                print(f"Skipping invalid exercise entry: {e}")

        self.training_summary = pd.concat([self.training_summary, pd.DataFrame(exercise_list)], ignore_index=True)


    def parse_hr_samples(self, exercises: list) -> pd.DataFrame:
        """Parses heart rate samples and returns a DataFrame."""
        hr_samples = []
        for ex in exercises:
            try:
                for sample in ex.get("samples", {}).get("heartRate", []):
                    sample_time = datetime.fromisoformat(sample["dateTime"]) + timedelta(minutes=ex.get("timezoneOffset", 0))
                    hr_samples.append({"dateTime": sample_time, "heartRate": sample["value"]})
            except (KeyError) as e:
                print(f"Missing heart rate value for timepoint {sample['dateTime']}")
        return pd.DataFrame(hr_samples)

    def process_all_files(self):
        """Processes all training session files and updates DataFrames."""
        for file in self.files:
            exercises = self.read_exercises(file)

            self.parse_exercise_summary(exercises)
            hr_df = self.parse_hr_samples(exercises)
            if not hr_df.empty:
                self.training_hr_samples.append(hr_df)  # Append each file's heart rate data separately

