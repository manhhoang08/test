import pandas as pd
import yaml

def convert_excel_to_yaml(excel_file, yaml_file):
    df = pd.read_excel(excel_file)

    yaml_dict = {}

    for _, row in df.iterrows():
        keys = row["Parameter"].split(".")
        value = row["Value"]

        flag = False

        # Kiểm tra và xử lý giá trị NaN
        if pd.isna(value):  
            value = None
        # Kiểm tra TRUE và FALSE trong chuỗi
        elif isinstance(value, str) and value.upper() == "TRUE":  
            value = True  
        elif isinstance(value, str) and value.upper() == "FALSE":  
            value = False  
        # Giữ nguyên từ điển rỗng
        elif isinstance(value, dict) and len(value) == 0:  
            pass  # Giữ nguyên từ điển rỗng
        # Giữ nguyên chuỗi rỗng
        elif value == "":  
            pass  # Giữ nguyên chuỗi rỗng
        # Giữ chuỗi có dấu phẩy như là chuỗi
        elif isinstance(value, str) and ',' in value:
            value = str(value)  # Đảm bảo giá trị là chuỗi
        # Chuyển đổi số thực thành số nguyên nếu phần thập phân là 0
        elif isinstance(value, float) and value.is_integer():  
            value = int(value)

        temp = yaml_dict

        for key in keys[:-1]:
            if key == "kubeadm":
                index = keys.index(key)  
                spec = '.'.join(keys[index:])
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

    # Dùng yaml.dump để xuất ra YAML, bảo đảm định dạng không thay đổi
    with open(yaml_file, "w") as f:
        yaml.dump(yaml_dict, f, default_flow_style=False, sort_keys=False)

    print(f"Done!")

if __name__ == "__main__":
    input_excel = "config.xlsx" 
    output_yaml = "output2.yaml"  
    convert_excel_to_yaml(input_excel, output_yaml)
