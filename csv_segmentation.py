import csv
import mmap
import os.path

# target = 20
csv_name = input("请输入文件名")
target = int(input("请输入截取大小"))
basename, extension = os.path.splitext(os.path.basename(csv_name))
init = os.path.dirname(csv_name) + "/" + basename + "/"


# 导入csv
def export_csv(data_list, name):
    with open(name, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_list)


def read_csv(filename):
    with open(filename, 'r+b') as f:
        nmap = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        alist = []
        count = 0
        page = 1
        while True:
            line = nmap.readline().decode().replace("\r\n", "")
            source = line.split(",")
            # 最后文件导入
            if not line:
                export_csv(alist, init + str(page) + '.csv')
                break
            alist.append(source)
            count += 1
            print("正在生成第" + str(count + (page - 1) * target) + "行")
            # 文件上限生成
            if count == target:
                count = 0
                if not os.path.exists(init):
                    os.mkdir(init)
                export_csv(alist, init + str(page) + '.csv')
                page += 1
                alist = []


read_csv(csv_name)
