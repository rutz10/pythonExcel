import pandas as pd

# Load the Excel file
file_path = 'your_excel_file.xlsx'  # Replace with your actual file path

# Read the sheets into DataFrames
map1_df = pd.read_excel(file_path, sheet_name='Map1')
map2_df = pd.read_excel(file_path, sheet_name='Map2')

# Display the first few rows of each sheet to understand the structure
print(map1_df.head())
print(map2_df.head())

# Case-sensitive match between 'Product' columns
# Map1 'Product' column has 50 values, Map2 'Product' column has 500 values.
# We'll merge the data on 'Product' column, making sure it's case-sensitive.

# Perform case-sensitive merge using pandas.merge
merged_df = pd.merge(map1_df, map2_df, on='Product', how='inner', suffixes=('_Map1', '_Map2'))

# 'inner' join will keep only the rows that have matching products in both Map1 and Map2
# You can specify additional columns to merge on if needed (e.g., 'Category' or 'Price' from Map2)

# Optionally, if you only want certain columns from Map2:
columns_to_select = ['Product', 'Price', 'Category']  # Example columns from Map2
merged_df = merged_df[['Product'] + columns_to_select]  # Keep only the columns you want

# Save the resulting merged data into a new sheet in the same Excel file (or to a new file)
output_file_path = 'matched_data.xlsx'  # Replace with your desired output file path
with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    merged_df.to_excel(writer, sheet_name='MatchedData', index=False)

print(f"Matched data saved to {output_file_path}")
