import openpyxl

# 打开Excel文件
workbook = openpyxl.load_workbook("C:/Users/liwen/Desktop/表格样式.xlsx")
# 获取第一个工作表
sheet = workbook.active

# 遍历每一行
for row in sheet.iter_rows(values_only=True):
    # 打印每一行的数据
    num = row[0]
    title = row[1]
    insert_date = row[2]
    source_web = row[3]
    tendency = row[4]
    author = row[5]
    type = row[6]
    meg_info = row[7]
    read_num = row[8]
    comm_num = row[9]
    transmit_num = row[10]
    like_num = row[11]
    fans_num = row[12]
    url = row[13]
    jd = row[14]
    key_word = row[15]
    rows = [author]
    table_rows = []
    table_data = ''.join(f'<td>{url}</td>')
    table_row = f'<tr onclick="window.location.href=\'{url}\';">{table_data}</tr>'
    print(table_row)
    table_rows.append(table_row)

# 关闭Excel文件
workbook.close()
