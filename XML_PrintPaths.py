import xml.etree.ElementTree as ET
import csv

def extract_paths(element, parent_path=""):
    """ Recursively extract paths for each field in the XML tree """
    paths = []
    
    # If the element has text (not just tags), add it to the list with the current path
    if element.text and element.text.strip():
        paths.append((element.tag, parent_path + "/" + element.tag))
    
    # Recursively process all children
    for child in element:
        paths.extend(extract_paths(child, parent_path + "/" + element.tag))
    
    return paths

def xml_to_csv(xml_file_path, output_csv):
    """ Convert XML file to CSV with field names and full paths """
    # Parse XML from the file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    # Extract all paths from the XML
    paths = extract_paths(root)
    
    # Write to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Field Name', 'Path'])  # Write header
        for field_name, path in paths:
            writer.writerow([field_name, path])

# Example usage
xml_file_path = 'input.xml'  # Replace this with the path to your XML file
output_csv = 'output.csv'    # Output CSV file path

# Convert XML to CSV
xml_to_csv(xml_file_path, output_csv)
