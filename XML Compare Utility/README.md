# XML Compare Utility

This utility compares two XML files (source and target) based on a list of XPaths provided in a CSV file. It reports which fields (by XPath) and values are present in the source XML but missing in the target XML, with support for ignoring specified fields or parent nodes.

## Features
- Compares XML files based on tag names and XPaths.
- Ignores specified fields or entire parent nodes (and their children) as configured.
- Uses a CSV file to specify which fields (XPaths) to compare.
- For repeating fields/containers, checks that all values from the source are present in the target (including duplicates).
- Outputs a text file listing missing fields and values (by XPath) in the target XML.
- Order of XML elements does not matter.

## Requirements
- Python 3.7+
- [lxml](https://lxml.de/) library

Install lxml with:
```
pip install lxml
```

## Usage

### 1. Prepare Your Files
- `source.xml`: The source XML file.
- `target.xml`: The target XML file.
- `fields_to_compare.csv`: CSV file with one XPath per line (no header).
- `ignore_fields.txt`: (Optional) Text file with one XPath per line to ignore (parents or specific fields).

### 2. Run the Script
Edit the file paths in the `main()` call at the bottom of `xml_compare.py` if needed. Then run:
```
python xml_compare.py
```

### 3. Output
- `missing_fields.txt`: Text file listing the XPaths and values present in the source XML (and in the CSV) but missing in the target XML. Each line is formatted as:
  ```
  <XPath> | Missing value: <value>
  ```

## Example
**source.xml**
```xml
<root>
  <users>
    <user>
      <id>1</id>
      <profile>
        <name>John</name>
        <contacts>
          <email>john@example.com</email>
          <phone>12345</phone>
        </contacts>
      </profile>
      <roles>
        <role>admin</role>
        <role>user</role>
      </roles>
    </user>
    <user>
      <id>2</id>
      <profile>
        <name>Jane</name>
        <contacts>
          <email>jane@example.com</email>
          <phone>67890</phone>
        </contacts>
      </profile>
      <roles>
        <role>user</role>
      </roles>
    </user>
  </users>
  <settings>
    <theme>dark</theme>
    <notifications>
      <email>true</email>
      <sms>false</sms>
    </notifications>
  </settings>
</root>
```

**target.xml**
```xml
<root>
  <users>
    <user>
      <id>1</id>
      <profile>
        <name>John</name>
        <contacts>
          <email>john@example.com</email>
        </contacts>
      </profile>
      <roles>
        <role>admin</role>
      </roles>
    </user>
    <user>
      <id>2</id>
      <profile>
        <name>Jane</name>
        <contacts>
          <email>jane@example.com</email>
        </contacts>
      </profile>
      <roles>
        <role>user</role>
      </roles>
    </user>
  </users>
  <settings>
    <theme>dark</theme>
    <notifications>
      <email>true</email>
    </notifications>
  </settings>
</root>
```

**fields_to_compare.csv**
```
/root/users/user/id
/root/users/user/profile/name
/root/users/user/profile/contacts/email
/root/users/user/profile/contacts/phone
/root/users/user/roles/role
/root/settings/theme
/root/settings/notifications/email
/root/settings/notifications/sms
```

**ignore_fields.txt**
```
/root/users/user/roles
```

**Expected missing_fields.txt output:**
```
/root/users/user/profile/contacts/phone | Missing value: 12345
/root/users/user/profile/contacts/phone | Missing value: 67890
/root/settings/notifications/sms | Missing value: false
```

## Notes
- Only fields present in the source XML and listed in the CSV are compared.
- If a parent is ignored, all its children are ignored.
- The script does not check for fields missing in the source XML.
- For repeating fields, all values from the source must be present in the target (including duplicates).

## Customization
- Adjust file paths in the `main()` function as needed.
- You can adapt the script for more advanced comparison (e.g., attribute comparison) if required.

## License
MIT License
