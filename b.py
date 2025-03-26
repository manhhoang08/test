# Mở và duyệt từng dòng trong file input.yaml
with open('b.yaml', 'r') as file:
    lines = file.readlines()

# Xử lý và thay thế từng dòng
with open('b.yaml', 'w') as file:
    for line in lines:
        # Thay thế '{}' (dấu nháy đơn) thành {} (không dấu nháy đơn)
        new_line = line.replace("'{}'", dict{})
        new_line = line.replace('""', "")
        file.write(new_line)
