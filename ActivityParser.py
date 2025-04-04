from __future__ import annotations

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import zipfile


class ActivityParser:
    def __init__(self, folder_of_zip_files: str | None = None, folder_pattern: str = "polar-user-data-export*"):
        """Initialize the parser and process activity & 24/7 HR data."""
        self.directory = Path(folder_of_zip_files) if folder_of_zip_files else Path.cwd()
        if not self.directory.exists():
            raise FileNotFoundError(f"The folder '{self.directory}' does not exist.")
        if not self.directory.is_dir():
            raise NotADirectoryError(f"The path '{self.directory}' is not a directory.")

        self.folder_pattern = folder_pattern
        self.activity_summary = pd.DataFrame()
        self.step_series_df = pd.DataFrame()
        self.hr_247_df = pd.DataFrame()

        self.process_all_files()

    def process_all_files(self):
        """Process all matched ZIP files and extract activity and 24/7 HR data."""
        matching_zips = [str(zip_path) for zip_path in self.directory.glob(self.folder_pattern)]
        if not matching_zips:
            print("No matching ZIP files found.")
            return

        for zip_path in matching_zips:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for filemember in zip_ref.namelist():
                    if filemember.startswith("activity-") and filemember.endswith(".json"):
                        with zip_ref.open(filemember) as file:
                            data = json.load(file)
                            self.parse_activity_file(data)
                    elif filemember.startswith("247ohr_") and filemember.endswith(".json"):
                        with zip_ref.open(filemember) as file:
                            data = json.load(file)
                            self.parse_247ohr_file(data)

    def parse_activity_file(self, data: dict):
        """Extracts activity summary + steps."""
        try:
            date = data.get("date")
            summary = data.get("summary", {})
            steps = data.get("samples", {}).get("steps", [])

            activity_entry = {
                "date": date,
                "start": summary.get("startTime"),
                "end": summary.get("endTime"),
                "calories": summary.get("calories"),
                "step_total": summary.get("stepCount"),
            }

            self.activity_summary = pd.concat([self.activity_summary, pd.DataFrame([activity_entry])], ignore_index=True)

            # Time series step data (many per day)
            if steps:
                step_df = pd.DataFrame(steps)
                step_df["date"] = date  # associate samples with their day
                self.step_series_df = pd.concat([self.step_series_df, step_df], ignore_index=True)

        except Exception as e:
            print(f"Error parsing activity file: {e}")

    def parse_247ohr_file(self, data: dict):
        """Extracts 24/7 heart rate samples."""
        try:
            for day in data.get("deviceDays", []):
                user_id = day.get("userId")
                date = day.get("date")
                samples = day.get("samples", [])
                if not samples:
                    continue

                day_hr_df = pd.DataFrame(samples)
                day_hr_df["userId"] = user_id
                day_hr_df["date"] = date

                self.hr_247_df = pd.concat([self.hr_247_df, day_hr_df], ignore_index=True)

        except Exception as e:
            print(f"Error parsing 24/7 HR file: {e}")
