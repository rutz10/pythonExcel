import csv
from lxml import etree

def generate_xsd_from_csv(csv_file):
    # Create the root of the XSD (xs:schema)
    xsd_root = etree.Element("xs:schema", xmlns_xs="http://www.w3.org/2001/XMLSchema")

    # Function to add elements to the schema, including complex types
    def add_element(parent, path):
        # Split the path into individual tags (elements)
        elements = path.split('/')
        
        # Traverse through each element in the path
        for i, element in enumerate(elements):
            # Look for existing elements with this name
            found = parent.xpath(f"xs:element[@name='{element}']", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"})
            
            if found:
                parent = found[0]  # Move to the found element's parent
            else:
                # If it's the last element, create an element of simple type (string)
                if i == len(elements) - 1:
                    new_element = etree.SubElement(parent, "xs:element", name=element, minOccurs="0", maxOccurs="1")
                    simple_type = etree.SubElement(new_element, "xs:simpleType")
                    restriction = etree.SubElement(simple_type, "xs:restriction", base="xs:string")
                    parent = new_element  # Move to the newly created element
                else:
                    # If it's not the last element, create an element with complex type (children to be defined)
                    new_element = etree.SubElement(parent, "xs:element", name=element, minOccurs="0", maxOccurs="1")
                    complex_type = etree.SubElement(new_element, "xs:complexType")
                    sequence = etree.SubElement(complex_type, "xs:sequence")
                    parent = new_element  # Move to the newly created complex element

    # Read the CSV file and process each XML path
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Skip empty rows
                path = row[0]  # Assuming each row has one XML path in the first column
                add_element(xsd_root, path)

    # Create the final XSD tree
    tree = etree.ElementTree(xsd_root)
    
    # Output the generated XSD as a string
    return etree.tostring(xsd_root, pretty_print=True, encoding="UTF-8").decode("utf-8")

# Example: CSV file path (update the path to your actual CSV file)
csv_file = "xml_paths.csv"

# Generate the XSD
xsd_output = generate_xsd_from_csv(csv_file)
print(xsd_output)
