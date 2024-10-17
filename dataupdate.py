import pandas as pd
import os

# Specify the path for the CSV file
csv_file_path = 'data.csv'  # Replace with your actual file path

# Read the existing CSV file
df = pd.read_csv(csv_file_path)

# Merge semester, subject, and year into one column
df['merged_column'] = df['semester'] + ' ' + df['subject'] + ' ' + df['year']

# Drop the original columns
df.drop(['semester', 'subject', 'year'], axis=1, inplace=True)

# Save the updated DataFrame back to the same CSV file
df.to_csv(csv_file_path, index=False)

# Confirm the update
print(f"Updated database saved as '{csv_file_path}'.")
