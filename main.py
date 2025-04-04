import pandas as pd
from TrainingParser import TrainingParser
from ActivityParser import ActivityParser

# Process json files containing training data (downloaded from Polar website)

# save excel files when done?
save_excels = False
# common pattern in the names of zip files
folder_pattern = 'polar-user-data-export*'
# folder where all the zip files are. Folder must be in the same directory as this script. If none, script will look in the current directory.
folder_of_zip_files = None
training_parser = TrainingParser(folder_pattern=folder_pattern, folder_of_zip_files=folder_of_zip_files)

training_summary = training_parser.training_summary
training_hr_df = training_parser.training_hr_df

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

if save_excels:
    # Save training summary to Excel
    training_summary.to_excel("training_summary.xlsx", index=False)
    # Save training HR samples to Excel
    training_hr_df.to_excel("training_hr_samples.xlsx", index=False)

print("done")

activity_parser = ActivityParser(folder_pattern=folder_pattern, folder_of_zip_files=folder_of_zip_files)
activity_summary = activity_parser.activity_summary
step_series = activity_parser.step_series_df
acitivty_hr = activity_parser.hr_247_df
