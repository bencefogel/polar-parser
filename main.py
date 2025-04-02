import pandas as pd
from TrainingParser import TrainingParser

# Process json files containing training data (downloaded from Polar website)
folder = 'polar-user-data-export*'
training_parser = TrainingParser(folder)
training_parser.process_all_files()

training_summary = training_parser.training_summary
training_hr_samples = training_parser.training_hr_samples
