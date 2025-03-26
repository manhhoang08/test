import pandas as pd
import yaml

def compare_yaml(excel_file, yaml_file):
    def convert_excel_to_yaml(excel_file, yaml_file):
        df = pd.read_excel(excel_file)

        yaml_dict = {}
        
        for _, row in df.iterrows():
            keys = row["Parameter"].split(".")
            value = row["Setup Value"]

            flag = False

            # Chuyển đổi giá trị thành kiểu phù hợp  
            if pd.isna(value):  # Kiểm tra nếu value là NaN (trống)  
                value = None  # Gán None vào value thay vì bỏ qua  
            elif value == 0:
                value = int(0)

            elif isinstance(value, str) and value.upper() == "TRUE":  
                value = "true"  
            elif isinstance(value, str) and value.upper() == "FALSE":  
                value = "false"
            elif value == {}:  # Kiểm tra nếu value là từ điển rỗng
                pass  # Giữ nguyên, không thay đổi
            elif value == "":  # Kiểm tra nếu value là chuỗi rỗng
                pass  # Giữ nguyên, không thay đổi
            elif isinstance(value, float) and value.is_integer():  
                value = int(value) 
            
            
            temp = yaml_dict
                      
            for key in keys[:-1]:
                if key == "kubeadm":
                    index = keys.index(key)  
                    spec = '.'.join(keys[index:])
                    # last_key = row["Parameter"]  
                    temp[spec] = value
                    flag = True
                    break 

                if "[" in key and "]" in key: 
                    base_key, index = key.split("[")
                    index = int(index.rstrip("]"))
                    temp = temp.setdefault(base_key, [])
                    while len(temp) <= index:
                        temp.append({})
                    temp = temp[index]
                else:
                    temp = temp.setdefault(key, {})

            if flag:
                continue

            last_key = keys[-1]
            if "[" in last_key and "]" in last_key: 
                base_key, index = last_key.split("[")
                index = int(index.rstrip("]"))
                temp = temp.setdefault(base_key, [])
                while len(temp) <= index:
                    temp.append(None)
                temp[index] = value
            else:
                temp[last_key] = value


        with open(yaml_file, "w") as f:
            yaml.dump(yaml_dict, f, default_flow_style=False, sort_keys=False)

        print(f"Done!")

    # if __name__ == "__main__":
    #     input_excel = "etcd.xlsx" 
    #     output_yaml = "output.yaml"  
    convert_excel_to_yaml(excel_file, yaml_file)   

    # def process_yaml_file(yaml_file):
    #     # Read the file and process lines
    #     with open(yaml_file, 'r') as file:
    #         lines = file.readlines()
        
    #     # Process each line
    #     processed_lines = []
    #     for line in lines:
    #         # Replace '{}' with an actual empty dict
    #         if "'{}'" in line:
    #             line = line.replace("'{}'", "{}")
            
    #         # Replace '""' with an actual empty string
    #         if "'\"\"'" in line:
    #             line = line.replace("'\"\"'", '""')

    #         # Replace '"0"' with "0"
    #         if "'\"0\"'" in line:
    #             line = line.replace("'\"0\"'", '"0"')
            
    #         processed_lines.append(line)
        
    #     # Write processed lines to output file
    #     with open(yaml_file, 'w') as file:
    #         file.writelines(processed_lines)
        
    #     # print(f"Processed file saved to {output_file}")

    # # Example usage
    # # input_file = 'b.yaml'
    # # output_file = 'b_processed.yaml'
    # process_yaml_file(yaml_file)

compare_yaml('config1.xlsx', 'hhhhh111.yaml')