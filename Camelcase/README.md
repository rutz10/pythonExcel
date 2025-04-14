# Project Documentation

## Overview
This project is designed to convert a JSON schema into a PySpark schema and extract all field names from the schema. The extracted field names are written to a text file for further use. Additionally, the project includes functionality to process field names and generate processed outputs.

## Prerequisites
- Python 3.7 or higher
- Apache Spark (PySpark library)
- A JSON schema file (e.g., `spark_json_schema.json`)

## Setup Instructions

1. **Clone or Download the Repository**
   - Ensure you have the project files in your working directory. The key files are:
     - `convert_schema.py`: The main Python script for schema conversion and field name extraction.
     - `process_field_names.py`: A script to process extracted field names.
     - `requirements.txt`: Contains the required Python dependencies.
     - JSON schema files located in the `json_schemas/` directory (e.g., `example_schema1.json`).

2. **Install Dependencies**
   - Open a terminal in the project directory and run the following command:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Scripts**
   - To convert the JSON schema and extract field names:
     ```bash
     python convert_schema.py
     ```
   - To process the extracted field names:
     ```bash
     python process_field_names.py
     ```

4. **Output Files**
   - The scripts generate the following outputs:
     - **Field Names**: Written to files in the `output/` directory (e.g., `example_schema1.json_field_names.txt`).
     - **Processed Field Names**: Written to files in the `processed_field_names/` directory (e.g., `example_schema1.json_field_names.txt_processed.txt`).

## Code Explanation

### `convert_schema.py`
#### `json_to_pyspark_schema`
This function converts a JSON schema into a PySpark `StructType` schema. It recursively parses the JSON schema to handle nested structures and arrays.

- **Input**: JSON schema (dictionary format).
- **Output**: PySpark `StructType` schema.

#### `list_field_names`
This function extracts all field names from the JSON schema, including nested fields. It uses recursion to traverse the schema and appends field names to a list.

- **Input**: JSON schema (dictionary format).
- **Output**: List of field names.

#### Main Script
1. Reads the JSON schema from files in the `json_schemas/` directory.
2. Converts the JSON schema to a PySpark schema and prints it.
3. Extracts all field names and writes them to the `output/` directory.

### `process_field_names.py`
This script processes the extracted field names to generate additional outputs.

- **Input**: Field names files from the `output/` directory.
- **Output**: Processed field names written to the `processed_field_names/` directory.

## Example JSON Schema
Here is an example of a JSON schema that the script can process:
```json
{
  "fields": [
    {"name": "id", "type": "integer", "nullable": false},
    {"name": "name", "type": "string", "nullable": true},
    {"name": "details", "type": {"type": "struct", "fields": [
      {"name": "age", "type": "integer", "nullable": true},
      {"name": "address", "type": "string", "nullable": true}
    ]}, "nullable": true}
  ]
}
```

## Notes
- Ensure the JSON schema files are correctly formatted and placed in the `json_schemas/` directory.
- The scripts handle nested structures and arrays in the schema.

## Troubleshooting
- If you encounter issues with PySpark, ensure that the `pyspark` library is installed and properly configured in your environment.
- Verify the JSON schema files for syntax errors.
- Check the `output/` and `processed_field_names/` directories for generated files.