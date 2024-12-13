import xml.etree.ElementTree as ET
import csv

# Function to traverse XML and extract field names with their paths
def traverse_xml(element, path=""):
    fields = []
    # Get the field name and complete path
    if element.text and element.text.strip():
        fields.append((element.tag, path + '/' + element.tag))
    
    # Traverse child elements recursively
    for child in element:
        fields.extend(traverse_xml(child, path + '/' + element.tag))
    
    return fields

# Function to write the extracted fields into a CSV file
def write_to_csv(fields, filename="output.csv"):
    # Open the CSV file in write mode
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Writing header row
        writer.writerow(["Field Name", "Complete Path"])

        # Writing data rows
        for field, path in fields:
            writer.writerow([field, path])
    
    print(f"Data has been written to {filename}")

# Main function to process the XML and generate CSV
def process_xml_to_csv(xml_file, csv_filename="xml_paths.csv"):
    # Parse the XML from a file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Get all field names and their complete paths
    fields = traverse_xml(root)

    # Write fields to a CSV file
    write_to_csv(fields, csv_filename)

# Example: Path to the XML file
xml_file = 'st.xml'  # Replace with the path to your XML file

# Run the process to convert XML to CSV
process_xml_to_csv(xml_file)
