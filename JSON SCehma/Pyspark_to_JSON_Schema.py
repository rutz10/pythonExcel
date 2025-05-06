from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, ArrayType, DoubleType, DateType, LongType
import json


def spark_type_to_bson(spark_type):
    """Convert PySpark type to MongoDB BSON type."""
    mapping = {
        StringType: "string",
        IntegerType: "int",
        BooleanType: "bool",
        DoubleType: "double",
        LongType: "long",
        DateType: "date",
    }
    return mapping.get(type(spark_type), "object")  # default to "object" for unknown types


def convert_struct_field(field):
    """Convert a single StructField to a JSON Schema type."""
    field_schema = {
        "bsonType": spark_type_to_bson(field.dataType),
        "description": f"Field: {field.name}"
    }
    
    # If it's a nested StructType, recurse
    if isinstance(field.dataType, StructType):
        field_schema["properties"] = convert_struct_type(field.dataType)
    
    # If it's an ArrayType, handle it
    elif isinstance(field.dataType, ArrayType):
        field_schema["items"] = convert_struct_field(StructField("item", field.dataType.elementType))["bsonType"]
    
    return field_schema


def convert_struct_type(struct_type):
    """Recursively convert a StructType to a JSON Schema."""
    properties = {}
    for field in struct_type.fields:
        properties[field.name] = convert_struct_field(field)
    return properties


def pyspark_schema_to_jsonschema(pyspark_schema):
    """Convert the entire PySpark schema to a MongoDB JSON Schema."""
    json_schema = {
        "bsonType": "object",
        "properties": convert_struct_type(pyspark_schema)
    }
    return json_schema


# Example Usage

# Sample PySpark schema
pyspark_schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("email", StringType(), True),
    StructField("isActive", BooleanType(), True),
    StructField("address", StructType([
        StructField("street", StringType(), True),
        StructField("city", StringType(), True)
    ]), True),
    StructField("tags", ArrayType(StringType()), True),
])

# Convert PySpark schema to JSON Schema
json_schema = pyspark_schema_to_jsonschema(pyspark_schema)

# Pretty print the JSON Schema
print(json.dumps(json_schema, indent=4))
