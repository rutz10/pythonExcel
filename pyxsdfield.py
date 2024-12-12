import xml.etree.ElementTree as ET
import csv
import os

def extract_xsd_paths(xsd_file, output_csv):
    """
    Extracts field names and their full paths from an XSD file and writes them to a CSV.

    Args:
        xsd_file: Path to the XSD file.
        output_csv: Path to the output CSV file.
    """

    try:
        tree = ET.parse(xsd_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XSD: {e}")
        return
    except FileNotFoundError:
        print(f"Error: XSD file not found: {xsd_file}")
        return

    namespace = {'xs': 'http://www.w3.org/2001/XMLSchema'}  # Define the namespace

    paths = []

    def traverse(element, current_path=""):
        tag = element.tag.replace(f"{{{namespace['xs']}}}", "") # Remove namespace
        if tag in ("element", "attribute"): # Extract only elements and attributes
            name = element.get("name")
            if name:
                full_path = f"{current_path}/{name}" if current_path else name
                paths.append({"fieldname": name, "path": full_path})
        
        # Handle complexType and sequence within complexType
        if tag == "complexType":
            for child in element:
                if child.tag.replace(f"{{{namespace['xs']}}}", "") == "sequence":
                    for grandchild in child:
                        traverse(grandchild, current_path)
                else:
                    traverse(child, current_path)
        elif tag == "sequence":
            for child in element:
                traverse(child, current_path)
        else:
            for child in element: # Generic traversal for other tags
                traverse(child, current_path)

    # Find the root element (usually a schema element)
    for child in root:
        if child.tag.replace(f"{{{namespace['xs']}}}", "") == "element":
            traverse(child)

    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['fieldname', 'path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(paths)
        print(f"Paths written to {output_csv}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")


# Example usage:
xsd_file = "your_xsd_file.xsd"  # Replace with your XSD file path
output_csv = "xsd_paths.csv"
extract_xsd_paths(xsd_file, output_csv)

xsd_file = "nested.xsd" # The nested example from previous response
extract_xsd_paths(xsd_file, "nested_xsd_paths.csv")
