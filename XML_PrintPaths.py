import xml.etree.ElementTree as ET
import csv
import os

def extract_paths(element, parent_path="", seen=None):
    """Recursively extract unique XML paths for each level"""
    if seen is None:
        seen = set()
    data = []

    if element is None:
        return data

    current_path = f"{parent_path}/{element.tag}" if parent_path else element.tag

    # Ensure each path is captured only once
    if current_path not in seen:
        seen.add(current_path)
        data.append((element.tag, current_path))

    # Recursively process child elements
    for child in element or []:
        data.extend(extract_paths(child, current_path, seen))

    return data

def xml_to_csv(xml_file, csv_file):
    """Reads XML, extracts paths, and writes to CSV"""
    if not os.path.exists(xml_file):
        print(f"Error: The file '{xml_file}' does not exist.")
        return

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error: Unable to parse XML file. {e}")
        return

    # Extract paths
    seen = set()
    data = extract_paths(root, seen=seen)

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Level Name", "XML Path"])  # Column headers
        writer.writerows(data)

    print(f"CSV file '{csv_file}' successfully created!")

# Example usage
xml_to_csv("input.xml", "output.csv")
