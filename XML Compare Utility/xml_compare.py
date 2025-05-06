import lxml.etree as ET
import csv

def load_xpaths_from_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0].strip() for row in reader if row and row[0].strip()]

def load_ignore_xpaths(ignore_path):
    with open(ignore_path, encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

def is_ignored(xpath, ignore_xpaths):
    for ignore in ignore_xpaths:
        if xpath == ignore or xpath.startswith(ignore + '/'):
            return True
    return False

def get_node_values(root, xpath):
    # Returns a list of text values for all nodes matching the xpath
    nodes = root.xpath(xpath)
    values = []
    for node in nodes:
        # If node is an element, get its text
        if isinstance(node, ET._Element):
            if node.text is not None:
                values.append(node.text.strip())
            else:
                values.append('')
        # If node is an attribute or text, just append
        else:
            values.append(str(node).strip())
    return values

def main(source_xml_path, target_xml_path, csv_path, ignore_path, output_path):
    compare_xpaths = load_xpaths_from_csv(csv_path)
    ignore_xpaths = load_ignore_xpaths(ignore_path)
    source_tree = ET.parse(source_xml_path)
    source_root = source_tree.getroot()
    target_tree = ET.parse(target_xml_path)
    target_root = target_tree.getroot()
    missing_fields = []
    for xpath in compare_xpaths:
        if is_ignored(xpath, ignore_xpaths):
            continue
        source_values = get_node_values(source_root, xpath)
        if not source_values:
            continue  # Nothing to compare if not present in source
        target_values = get_node_values(target_root, xpath)
        # For each value in source, check if it exists in target (remove as found to handle duplicates)
        unmatched = list(target_values)  # Copy to allow removal
        for val in source_values:
            if val in unmatched:
                unmatched.remove(val)
            else:
                # Report missing value for this xpath
                missing_fields.append(f"{xpath} | Missing value: {val}")
    with open(output_path, 'w', encoding='utf-8') as f:
        for field in missing_fields:
            f.write(field + '\n')

if __name__ == "__main__":
    # Example usage; replace with your actual file paths
    main(
        source_xml_path="source.xml",
        target_xml_path="target.xml",
        csv_path="fields_to_compare.csv",
        ignore_path="ignore_fields.txt",
        output_path="missing_fields.txt"
    )
