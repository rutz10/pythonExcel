import os
import json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, BooleanType, ArrayType
from pyspark.sql.types import LongType, DoubleType, BinaryType, DateType, TimestampType, DecimalType, MapType

def json_to_pyspark_schema(json_schema):
    """
    Converts a JSON schema to a PySpark StructType schema.
    """
    def parse_field(field):
        field_type = field["type"]
        if isinstance(field_type, dict):
            if field_type["type"] == "struct":
                return StructField(
                    field["name"],
                    StructType([parse_field(f) for f in field_type["fields"]]),
                    field["nullable"]
                )
            elif field_type["type"] == "array":
                element_type = parse_field({"type": field_type["elementType"], "name": "", "nullable": field_type.get("containsNull", True)}).dataType
                return StructField(
                    field["name"],
                    ArrayType(element_type, field_type.get("containsNull", True)),
                    field["nullable"]
                )
            elif field_type["type"] == "map":
                key_type = parse_field({"type": field_type["keyType"], "name": "", "nullable": False}).dataType
                value_type = parse_field({"type": field_type["valueType"], "name": "", "nullable": field_type.get("valueContainsNull", True)}).dataType
                return StructField(
                    field["name"],
                    MapType(key_type, value_type, field_type.get("valueContainsNull", True)),
                    field["nullable"]
                )
            elif field_type["type"] == "decimal":
                return StructField(
                    field["name"],
                    DecimalType(precision=field_type["precision"], scale=field_type["scale"]),
                    field["nullable"]
                )
        else:
            type_mapping = {
                "string": StringType(),
                "integer": IntegerType(),
                "long": LongType(),
                "float": FloatType(),
                "double": DoubleType(),
                "boolean": BooleanType(),
                "binary": BinaryType(),
                "date": DateType(),
                "timestamp": TimestampType()
            }
            return StructField(field["name"], type_mapping[field_type], field["nullable"])
    
    return StructType([parse_field(f) for f in json_schema["fields"]])

def list_field_names(json_schema):
    """
    Extracts all field names from the JSON schema, including nested fields.
    Only the child names are included in the output.
    """
    field_names = []

    def extract_names(fields):
        for field in fields:
            field_names.append(field["name"])
            if isinstance(field["type"], dict) and field["type"]["type"] == "struct":
                extract_names(field["type"]["fields"])
            elif isinstance(field["type"], dict) and field["type"]["type"] == "array":
                if isinstance(field["type"]["elementType"], dict) and field["type"]["elementType"]["type"] == "struct":
                    extract_names(field["type"]["elementType"]["fields"])

    extract_names(json_schema["fields"])
    return field_names

if __name__ == "__main__":
    # Directory containing JSON schema files
    schema_dir = "json_schemas"
    output_dir = "output"

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process each JSON schema file in the directory
    for schema_file in os.listdir(schema_dir):
        if schema_file.endswith(".json"):
            schema_path = os.path.join(schema_dir, schema_file)
            with open(schema_path, "r") as f:
                json_schema = json.load(f)

            # Convert JSON schema to PySpark schema
            pyspark_schema = json_to_pyspark_schema(json_schema)
            print(f"Processed schema for {schema_file}:")
            print(pyspark_schema)

            # List all field names
            field_names = list_field_names(json_schema)

            # Write field names to a text file
            output_file = os.path.join(output_dir, f"{schema_file}_field_names.txt")
            with open(output_file, "w") as f:
                f.write("\n".join(field_names))

            print(f"Field names written to {output_file}")