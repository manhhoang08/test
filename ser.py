import pandas as pd

def excel_to_service(excel_path, output_path):
    """
    Convert an Excel file to a systemd .service file
    
    Parameters:
    excel_path (str): Path to the input Excel file
    output_path (str): Path to save the output .service file
    """
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Initialize service file content
    service_content = []
    
    # Group by the section (Unit or Service)
    grouped = df.groupby(df['Parameter'].str.split('.').str[0])
    
    # Process Unit section
    if 'Unit' in grouped.groups:
        service_content.append('[Unit]')
        unit_section = grouped.get_group('Unit')
        for _, row in unit_section.iterrows():
            # Extract the key (everything after 'Unit.')
            key = row['Parameter'].split('.')[1]
            value = row['Setup Value']
            service_content.append(f'{key}={value}')
        service_content.append('')  # Add blank line between sections
    
    # Process Service section
    if 'Service' in grouped.groups:
        service_content.append('[Service]')
        service_section = grouped.get_group('Service')
        for _, row in service_section.iterrows():
            # Extract the key (everything after 'Service.')
            key = row['Parameter'].split('.')[1]
            value = row['Setup Value']
            service_content.append(f'{key}={value}')
    
    # Write to .service file
    with open(output_path, 'w') as f:
        f.write('\n'.join(service_content))
    
    print(f'Service file created at {output_path}')

# Example usage
excel_to_service('ser.xlsx', 'output111111.service')