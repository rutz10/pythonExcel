import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_field_names(input_dir, output_dir):
    """
    Reads field names from files in the input directory, converts them to lowercase for the first letter,
    and writes the results to new files in the output directory.
    
    Args:
        input_dir (str): Path to the directory containing input files
        output_dir (str): Path to the directory where processed files will be saved
    
    Raises:
        ValueError: If input_dir or output_dir is invalid
        IOError: If there are issues reading/writing files
    """
    # Input validation
    if not os.path.exists(input_dir):
        raise ValueError(f"Input directory '{input_dir}' does not exist")
    
    if not isinstance(input_dir, str) or not isinstance(output_dir, str):
        raise ValueError("Input and output directories must be strings")

    os.makedirs(output_dir, exist_ok=True)
    
    # Track processing statistics
    processed_files = 0
    processed_fields = 0

    try:
        for input_file in os.listdir(input_dir):
            if input_file.endswith(".txt"):
                input_path = os.path.join(input_dir, input_file)
                output_path = os.path.join(output_dir, f"{input_file}_processed.txt")

                try:
                    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
                        for line in infile:
                            field_name = line.strip()
                            if field_name:  # Skip empty lines
                                processed_field_name = field_name[0].lower() + field_name[1:]
                                outfile.write(f"{field_name}, {processed_field_name}\n")
                                processed_fields += 1
                    
                    processed_files += 1
                    logging.info(f"Successfully processed {input_file}")
                
                except IOError as e:
                    logging.error(f"Error processing file {input_file}: {str(e)}")
                    continue

        logging.info(f"Processing complete. Processed {processed_fields} fields in {processed_files} files.")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        input_directory = "output"
        output_directory = "processed_field_names"
        process_field_names(input_directory, output_directory)
    except Exception as e:
        logging.error(f"Program failed: {str(e)}")