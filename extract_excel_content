import pandas as pd
import os

# Specify the directory containing the Excel files
input_dir = 'data'

# Path to your output Excel file
output_file = 'zzzz.xlsx'

# List all files in the directory and filter for Excel files
input_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.xlsx')]

# Initialize a dictionary to store DataFrames for each collection
data_collections = {}

# Process each file in the list
for file_path in input_files:
    try:
        # Load data from sheet 'fgf'
        df_fgf = pd.read_excel(file_path, sheet_name='fgf')
        # Load data from sheet 'xy'
        df_xy = pd.read_excel(file_path, sheet_name='xy')
        # Load collection names from sheet 'collectionname'
        df_collections = pd.read_excel(file_path, sheet_name='collectionname')

        # Create a dictionary to map 'ref' to 'cont'
        ref_to_cont = pd.Series(df_xy['cont'].values, index=df_xy['ref']).to_dict()

        # Replace 'RM' values in 'fgf' with 'cont' values using the 'ref_to_cont' map
        df_fgf['RM'] = df_fgf['RM'].map(ref_to_cont).fillna(df_fgf['RM'])

        # Filter the DataFrame to include only the columns 'RM' and 'RQ'
        df_filtered = df_fgf[['RM', 'RQ']].copy()

        # Create a new column 'RMRQ' by concatenating 'RM' and 'RQ' with a period separator using .loc
        df_filtered.loc[:, 'RMRQ'] = df_filtered['RM'].astype(str) + '.' + df_filtered['RQ'].astype(str)

        # Append data to the respective collections
        for collection in df_collections['collection'].unique():
            if collection not in data_collections:
                data_collections[collection] = df_filtered.copy()
            else:
                data_collections[collection] = pd.concat([data_collections[collection], df_filtered], ignore_index=True)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Write each collection's data to a new sheet in the Excel workbook
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for collection, data in data_collections.items():
        data.to_excel(writer, sheet_name=collection, index=False)

print("All data has been successfully aggregated and written to the new Excel workbook.")
