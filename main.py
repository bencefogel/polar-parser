import pandas as pd
from TrainingParser import TrainingParser
from ActivityParser import ActivityParser

# Process json files containing training data (downloaded from Polar website)

# save excel files when done?
save_excels = True
# Should we print the dataframes?
verbose = False
# common pattern in the names of zip files
folder_pattern = 'polar-user-data-export*'
# folder where all the zip files are. Folder must be in the same directory as this script. If none, script will look in the current directory.
folder_of_zip_files = None
training_parser = TrainingParser(folder_pattern=folder_pattern, folder_of_zip_files=folder_of_zip_files)
training_summary = training_parser.training_summary
training_hr_df = training_parser.training_hr_df

if verbose:
    print("Training summary size:")
    print(training_summary.shape)
    print("Training summary columns:")
    print(training_summary.columns)
    print("Training summary:")
    print(training_summary)
    print("Training HR samples size:")
    print(training_hr_df.shape)
    print("Training HR samples columns:")
    print(training_hr_df.columns)
    print("Training HR samples:")
    print(training_hr_df)

activity_parser = ActivityParser(folder_pattern=folder_pattern, folder_of_zip_files=folder_of_zip_files)
activity_summary = activity_parser.activity_summary
step_series = activity_parser.step_series_df
acitivty_hr = activity_parser.hr_247_df

if save_excels:
    # Save training summary to Excel
    try:
        training_summary.to_excel("training_summary.xlsx", index=False)
    except Exception as e:
        print(f"Error saving training summary to Excel: {e}")
    # Save training HR samples to Excel
    try:
        training_hr_df.to_excel("training_hr_samples.xlsx", index=False)
    except Exception as e:
        print(f"Error saving training HR samples to Excel: {e}")
    
    # Save activity summary to Excel
    try:
        activity_summary.to_excel("activity_summary.xlsx", index=False)
    except Exception as e:
        print(f"Error saving activity summary to Excel: {e}")
    
    # Save step series to Excel
    try:
        step_series.to_excel("step_series.xlsx", index=False)
    except Exception as e:
        print(f"Error saving step series to Excel: {e}")
    
    # Save activity HR to Excel
    try:
        acitivty_hr.to_excel("activity_hr.xlsx", index=False)
    except Exception as e:
        print(f"Error saving activity HR to Excel: {e}")

    print("done")

