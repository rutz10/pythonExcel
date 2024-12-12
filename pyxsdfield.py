import xml.etree.ElementTree as ET
import csv

def extract_xsd_paths(xsd_file, output_csv):
    try:
        tree = ET.parse(xsd_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XSD: {e}")
        return
    except FileNotFoundError:
        print(f"Error: XSD file not found: {xsd_file}")
        return

    namespace = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    paths = []

    def get_element_name(element):
        name = element.get("name")
        if not name: # Handle anonymous complexTypes and simpleTypes
            type_attr = element.get("type")
            if type_attr:
                name = type_attr
            else:
                parent_tag = element.getparent().tag.replace(f"{{{namespace['xs']}}}", "")
                if parent_tag == "element":
                    name = element.getparent().get("name") + "_content" # Add _content to make it unique
                else:
                    name = "anonymous"
        return name

    def traverse(element, current_path=None):
        tag = element.tag.replace(f"{{{namespace['xs']}}}", "")

        if current_path is None:
            current_path = []
        
        if tag in ("element", "attribute"):
            name = get_element_name(element)
            current_path.append(name)
            full_path = "/".join(current_path)
            paths.append({"fieldname": name, "path": full_path})
            current_path.pop() # important to remove the current element from path before going to next element

        elif tag in ("complexType", "simpleType"):
            name = get_element_name(element)
            if name != "anonymous":
                current_path.append(name)

            for child in element:
                traverse(child, current_path)
            
            if name != "anonymous":
                 current_path.pop()

        elif tag in ("sequence", "choice", "all"):
            for child in element:
                traverse(child, current_path)
        else:
             for child in element:
                traverse(child, current_path)

    # Find top-level elements
    for element in root:
        traverse(element)

    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['fieldname', 'path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(paths)
        print(f"Paths written to {output_csv}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Example usage (using the nested.xsd from before):
xsd_file = "nested.xsd"
output_csv = "nested_xsd_paths.csv"
extract_xsd_paths(xsd_file, output_csv)
