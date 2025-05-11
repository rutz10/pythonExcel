import xml.etree.ElementTree as ET
import xmlschema
from collections import OrderedDict
import copy

# Hardcoded file paths
XSD_FILE = 'schema.xsd'
XML_FILE = 'input.xml'
OUTPUT_FILE = 'output_corrected.xml'

def parse_xsd_sequence(xsd_path):
    """
    Parse the XSD file and extract the element sequence and required elements.
    Returns a dict mapping parent elements to ordered child elements.
    """
    schema = xmlschema.XMLSchema(xsd_path)
    structure = {}

    def extract_sequence(xsd_type):
        sequence = []
        required = []
        if hasattr(xsd_type, 'content') and hasattr(xsd_type.content, 'model'):
            if xsd_type.content.model == 'sequence':
                for child in xsd_type.content:
                    if hasattr(child, 'name') and child.name:
                        sequence.append(child.name)
                        if child.min_occurs > 0:
                            required.append(child.name)
        return sequence, required

    for element in schema.elements.values():
        if element.type.is_complex():
            seq, req = extract_sequence(element.type)
            structure[element.name] = {
                'sequence': seq,
                'required': req
            }
    return structure


def reorder_and_check(xml_path, xsd_structure):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    missing_elements = []
    misordered_elements = []

    def process_element(elem, expected_structure):
        if elem.tag not in expected_structure:
            return

        expected_seq = expected_structure[elem.tag]['sequence']
        required = expected_structure[elem.tag]['required']
        children = list(elem)

        child_map = {child.tag: child for child in children}
        present_tags = [child.tag for child in children]

        # Check missing required elements
        for req in required:
            if req not in present_tags:
                missing_elements.append(f"{elem.tag}/{req}")

        # Check order of present elements
        correct_order = [tag for tag in expected_seq if tag in present_tags]
        current_order = [tag for tag in present_tags if tag in expected_seq]
        if correct_order != current_order:
            misordered_elements.append(f"{elem.tag}: {current_order} -> {correct_order}")

        # Reorder children
        new_children = []
        for tag in expected_seq:
            if tag in child_map:
                new_children.append(child_map[tag])

        # Replace children in correct order
        for child in children:
            elem.remove(child)
        for child in new_children:
            elem.append(child)

        # Recursively process children
        for child in elem:
            process_element(child, expected_structure)

    process_element(root, xsd_structure)
    return tree, missing_elements, misordered_elements


def main():
    print(f"Reading XSD from: {XSD_FILE}")
    xsd_structure = parse_xsd_sequence(XSD_FILE)

    print(f"Processing XML: {XML_FILE}")
    corrected_tree, missing, misordered = reorder_and_check(XML_FILE, xsd_structure)

    # Save corrected XML
    corrected_tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
    print(f"\n✅ Corrected XML written to: {OUTPUT_FILE}\n")

    # Report
    if missing:
        print("❌ Missing required elements:")
        for el in missing:
            print(f"  - {el}")
    else:
        print("✅ No missing required elements found.")

    if misordered:
        print("\n🔀 Misordered elements:")
        for el in misordered:
            print(f"  - {el}")
    else:
        print("✅ No misordered elements found.")

if __name__ == "__main__":
    main()
