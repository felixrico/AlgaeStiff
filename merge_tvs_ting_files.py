import pandas as pd

# Load the files
file1_path = 'viscoElasticity_ting_results_356.csv'
file2_path = 'map-data-2025.06.06-11.56.16.356.jpk-force-map.txt'

# Read the first file, skipping the first row to correctly parse the header
file1 = pd.read_csv(file1_path, sep=';', skiprows=1, header=None)

# Assign column names based on the first row of the original file
with open(file1_path, 'r') as f:
    header = f.readline().strip().split(';')

file1.columns = header

# Read the second file
file2 = pd.read_table(file2_path, sep='\t')

# Merge the two files on the index columns, keeping all rows and filling NaN for missing values
merged_df = pd.merge(
    file1, file2,
    left_on='curve_idx', right_on='Position Index',
    how='outer',
    suffixes=('_file1', '_file2')
)

# Save the merged dataframe to a new CSV file
merged_df.to_csv('merged_output.csv', index=False)
