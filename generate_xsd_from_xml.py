import xml.etree.ElementTree as ET
from collections import Counter

def generate_xsd_from_xml(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Function to generate XSD from XML elements
    def element_to_xsd(element, element_counts):
        xsd_str = ''
        element_name = element.tag
        
        # Count occurrences of the element
        occurrences = element_counts[element_name]
        
        # Determine minOccurs and maxOccurs
        min_occurs = 1
        max_occurs = occurrences if occurrences > 1 else 1
        if occurrences > 1:
            max_occurs = 'unbounded'  # If more than one occurrence, set maxOccurs to unbounded
        
        # Add element with minOccurs and maxOccurs attributes
        if len(element):
            xsd_str += f'<xs:element name="{element.tag}" minOccurs="{min_occurs}" maxOccurs="{max_occurs}">'
            xsd_str += '<xs:complexType><xs:sequence>'
            for child in element:
                xsd_str += element_to_xsd(child, element_counts)
            xsd_str += '</xs:sequence></xs:complexType></xs:element>'
        else:
            # For elements with no children (simple elements), set minOccurs and maxOccurs
            xsd_str += f'<xs:element name="{element.tag}" type="xs:string" minOccurs="{min_occurs}" maxOccurs="{max_occurs}"/>'
        
        # Handle attributes (hardcode minOccurs="0" and maxOccurs="0" for attributes)
        for attr_name, attr_value in element.attrib.items():
            xsd_str += f'<xs:attribute name="{attr_name}" type="xs:string" minOccurs="0" maxOccurs="0"/>'

        return xsd_str

    # Count the occurrences of each element in the XML tree
    def count_elements(element):
        element_counts = Counter()
        for child in element.iter():
            element_counts[child.tag] += 1
        return element_counts
    
    # Get the element counts
    element_counts = count_elements(root)

    # Start XSD schema definition
    xsd_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xsd_content += '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n'
    
    # Generate the XSD for the root element
    xsd_content += element_to_xsd(root, element_counts)
    
    # End XSD schema definition
    xsd_content += '\n</xs:schema>'

    return xsd_content

# Save the generated XSD to a file
def save_xsd(xsd_content, output_file):
    with open(output_file, 'w') as f:
        f.write(xsd_content)

# Example usage
xml_file = 'company.xml'  # Replace with your XML file path
xsd_content = generate_xsd_from_xml(xml_file)
save_xsd(xsd_content, 'generated_schema_company.xsd')

print("XSD generated successfully!")
