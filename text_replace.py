import csv

# Function to read CSV and create a dictionary of replacements
def read_replacement_csv(csv_file):
    replacements = {}
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) == 2:  # Ensure the row has two columns (Key, Replace)
                key, replace = row
                replacements[key] = replace
    return replacements

# Function to replace words in the text file
def replace_text_in_file(input_file, output_file, replacements):
    with open(input_file, 'r') as file:
        text = file.read()

    # Perform replacements
    for key, replace in replacements.items():
        text = text.replace(key, replace)

    # Save the modified text to a new file (or overwrite the existing one)
    with open(output_file, 'w') as file:
        file.write(text)
    print(f"Replacements done. The modified text has been saved to {output_file}")

# Example usage
def main():
    csv_file = 'replacements.csv'  # Path to the CSV file
    input_file = 'input.txt'       # Path to the text file to be modified
    output_file = 'output.txt'     # Path to the output file
    
    replacements = read_replacement_csv(csv_file)  # Read replacements from CSV
    replace_text_in_file(input_file, output_file, replacements)  # Replace in text file

if __name__ == "__main__":
    main()
