import argparse
import re
import os
import pandas as pd
from tqdm import tqdm
from TrainingParser import TrainingParser
from ActivityParser import ActivityParser
from save_data import save_data_files


def process_polar_data(zip_data_directory, output_dir, save_format):
    print(f"Processing data from: {zip_data_directory}")

    training_parser = TrainingParser(folder_of_zip_files=zip_data_directory, zip_file_pattern='polar-user-data-export*')
    training_summary = training_parser.training_summary
    training_hr_df = training_parser.training_hr_df

    activity_parser = ActivityParser(folder_of_zip_files=zip_data_directory, zip_file_pattern='polar-user-data-export*')
    activity_summary = activity_parser.activity_summary
    step_series = activity_parser.step_series_df
    activity_hr = activity_parser.hr_247_df

    users = activity_summary['username'].unique()
    if save_format is not None:
        for user in tqdm(users, desc="Saving user data"):
            user_training_summary = training_summary[training_summary['username'] == user]
            user_training_hr_df = training_hr_df[training_hr_df['username'] == user]
            user_activity_summary = activity_summary[activity_summary['username'] == user]
            user_step_series = step_series[step_series['username'] == user]
            user_activity_hr = activity_hr[activity_hr['username'] == user]

            match = re.search(r'\.(\d+)@', user)
            if not match:
                print(f"Could not extract folder name for user: {user}")
                continue
            folder_name = match.group(1)

            data_to_save = {
                "training_summary": user_training_summary,
                "training_hr_samples": user_training_hr_df,
                "activity_summary": user_activity_summary,
                "step_series": user_step_series,
                "activity_hr": user_activity_hr
            }
            save_data_files(folder_name, data_to_save, output_dir, save_format=save_format)
            print(f"\n Saved files for user: {user} in: {os.path.join(output_dir, folder_name)}")


def main():
    parser = argparse.ArgumentParser(description="Process and export Polar user data.")
    parser.add_argument('--input-dir', type=str, default='../input', help='Path to directory containing zip files')
    parser.add_argument('--output-dir', type=str, default='../output', help='Directory where output will be saved')
    parser.add_argument('--save-format', type=str, choices=['csv', 'excel', 'both', 'none'], default='csv',
                        help='Save format for the data: csv, excel, both or none')

    args = parser.parse_args()

    save_format = None if args.save_format == 'none' else args.save_format
    process_polar_data(args.input_dir, args.output_dir, save_format)


if __name__ == '__main__':
    main()
