import pandas as pd
import yaml

def convert_excel_to_yaml(excel_file, yaml_file):
    df = pd.read_excel(excel_file)

    yaml_dict = {}
    
    for _, row in df.iterrows():
        keys = row["Parameter"].split(".")
        value = row["Value"]

        flag = False

        # # Chuyển đổi giá trị thành kiểu phù hợp  
        # if pd.isna(value):  # Kiểm tra nếu value là NaN (trống)  
        #     value = None  # Gán None vào value thay vì bỏ qua  
        # elif isinstance(value, str) and value.upper() == "TRUE":  
        #     value = True  
        # elif isinstance(value, str) and value.upper() == "FALSE":  
        #     value = False  
        # elif isinstance(value, float) and value.is_integer():  
        #     value = int(value) 
        # elif value == "0"

        if pd.isna(value):  # Kiểm tra nếu value là NaN (trống)  
            value = None  # Gán None vào value thay vì bỏ qua  
        elif isinstance(value, str) and value.upper() == "TRUE":  
            value = True  
        elif isinstance(value, str) and value.upper() == "FALSE":  
            value = False  
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

if __name__ == "__main__":
    input_excel = "config.xlsx" 
    output_yaml = "output1.yaml"  
    convert_excel_to_yaml(input_excel, output_yaml)