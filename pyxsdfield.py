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

    def traverse(element, current_path=""):
        tag = element.tag.replace(f"{{{namespace['xs']}}}", "")

        if tag in ("element", "attribute"):
            name = element.get("name")
            if name:
                full_path = f"{current_path}/{name}" if current_path else name
                paths.append({"fieldname": name, "path": full_path})
        elif tag == "simpleType":  # Handle simpleType
            name = element.get("name")
            if name and current_path: # Only add if it has a name and is nested
                full_path = f"{current_path}/{name}"
                paths.append({"fieldname": name, "path": full_path})

        # Improved complexType handling (handles both named and inline):
        if tag == "complexType" or (tag == "element" and element.find(f".//{{{namespace['xs']}}}complexType") is not None):
            complex_type_element = element if tag == "complexType" else element.find(f".//{{{namespace['xs']}}}complexType")
            for child in complex_type_element:
                if child.tag.replace(f"{{{namespace['xs']}}}", "") in ("sequence", "choice", "all"):
                    for grandchild in child:
                        traverse(grandchild, current_path)
                else:
                    traverse(child, current_path)
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


# Example usage (using an xsd with inline complex types):
xsd_file = "inline_complex_types.xsd"
output_csv = "inline_xsd_paths.csv"
extract_xsd_paths(xsd_file, output_csv)

