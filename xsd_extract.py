from lxml import etree

def extract_enumerations(xsd_file):
    """
    Extract field names and their enumerations from an XSD file.
    """
    # Parse the XSD file
    tree = etree.parse(xsd_file)
    root = tree.getroot()

    # Define the XML namespace to handle qualified names in the XSD
    ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}

    # Store the result as a dictionary of field names and their enumerations
    enumerations = {}

    # Iterate over all elements in the XSD that are of type 'xs:simpleType'
    for simple_type in root.xpath('//xs:simpleType', namespaces=ns):
        # Look for the 'xs:restriction' child within the 'xs:simpleType'
        restriction = simple_type.find('xs:restriction', namespaces=ns)
        if restriction is not None:
            # Check if there's an 'xs:enumeration' element inside the restriction
            enumerations_list = restriction.xpath('xs:enumeration', namespaces=ns)
            if enumerations_list:
                # Extract enumeration values
                enum_values = [enum.attrib.get('value') for enum in enumerations_list]
                if enum_values:
                    # Extract the name of the field (use 'Unnamed Field' if no name attribute exists)
                    field_name = simple_type.attrib.get('name', 'Unnamed Field')
                    enumerations[field_name] = enum_values

    return enumerations

def write_enumerations_to_file(xsd_file, output_file):
    """
    Write the field names and enumerations to a text file.
    """
    enumerations = extract_enumerations(xsd_file)

    # Open the output file for writing
    with open(output_file, 'w') as file:
        # Write the header
        file.write(f"{'Field Name'.ljust(30)} {'Enumerations'}\n")
        file.write("=" * 60 + "\n")

        # Write each field and its enumerations
        for field, enums in enumerations.items():
            enum_values = ', '.join(enums)  # Join the enumeration values into a string
            file.write(f"{field.ljust(30)} {enum_values}\n")

    print(f"Enumerations have been written to {output_file}")

# Example usage
xsd_file = 'your_schema.xsd'  # Replace with your XSD file path
output_file = 'enumerations_output.txt'  # Output file path

# Write enumerations to the specified output file
write_enumerations_to_file(xsd_file, output_file)
