import yaml

def process_yaml_file(input_file, output_file):
    # Read the file and process lines
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Process each line
    processed_lines = []
    for line in lines:
        # Replace '{}' with an actual empty dict
        if "'{}'" in line:
            line = line.replace("'{}'", "{}")
        
        # Replace '""' with an actual empty string
        if "'\"\"'" in line:
            line = line.replace("'\"\"'", '""')

        # Replace '"0"' with "0"
        if "'\"0\"'" in line:
            line = line.replace("'\"0\"'", '"0"')
        
        processed_lines.append(line)
    
    # Write processed lines to output file
    with open(output_file, 'w') as file:
        file.writelines(processed_lines)
    
    print(f"Processed file saved to {output_file}")

# Example usage
input_file = 'output1.yaml'
output_file = 'hhhhh.yaml'
# output_file = 'b_processed.yaml'
process_yaml_file(input_file, output_file)