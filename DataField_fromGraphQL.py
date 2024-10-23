import re
import pandas as pd

# Read the GraphQL schema from a text file
with open('schema.txt', 'r') as file:
    graphql_schema = file.read()

# Regular expression to find fields and their types
field_pattern = r'\s*(\w+):\s*([\[\]?\w]+)'

# Create lists to hold the field names and data types
field_names = []
data_types = []

# Find all matches in the schema
for match in re.finditer(field_pattern, graphql_schema):
    field_names.append(match.group(1))
    data_types.append(match.group(2))

# Create a DataFrame to hold the results
df = pd.DataFrame({
    'Field Name': field_names,
    'Data Type': data_types
})

# Display the DataFrame
print(df)
