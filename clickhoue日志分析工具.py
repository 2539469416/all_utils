import os
import time
import mmap

import pymongo

from 本地IP数据库 import IPCz

client = pymongo.MongoClient("mongodb://admin:123456@192.168.232.143:27017/")

# 选择或创建数据库
db = client["log"]
collection = db["vpn"]


def match_nginx_log_bt(log):
    try:
        if "src" not in log:
            return None
        log_map = log.split(" ")
        item = {}
        item['timestamp'] = log_map[0]
        for log in log_map:
            if "src:" in log:
                item["src"] = log.split(":")[1]
            if "pro:" in log:
                item["pro"] = log.split(":")[1]
            if "dst:" in log:
                item["dst"] = log.split(":")[1]
        return item
    except Exception as e:
        print(f'line{e.__traceback__.tb_lineno} :::' + str(log))


def read_nginx_log(filename):
    ipcz = IPCz('./tmp/ip.dat')
    with open(filename, 'r') as file:
        try:
            # 创建内存映射对象
            mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            data_list = []
            line_num = 0
            line = mm.readline()
            line_num += 1
            while line:
                log_line = line.decode().strip()
                source_data = match_nginx_log_bt(log_line)
                if source_data is None:
                    line = mm.readline()
                    continue
                address = ipcz.get_ip_address(source_data['src'])
                source_data['address'] = address
                data_list.append(source_data)
                if line_num % 1000 == 0:
                    collection.insert_many(data_list)
                    data_list = []
                line = mm.readline()
            collection.insert_many(data_list)
            mm.close()


        except Exception as e:
            print(f'line{e.__traceback__.tb_lineno}' + str(e))
    # 关闭内存映射对象


directory = "./tmp1/"


def load_file():
    for root, dirs, files in os.walk(directory):
        for filename in files:
            print(f'filename:{filename}')
            # 可以在这里对文件进行操作，例如打印文件名
            path = os.path.join(root, filename)
            # 筛选条件  只筛选log 后缀 不包含报错
            if not filename.endswith("log"):
                continue
            read_nginx_log(path)


# load_file()
if __name__ == '__main__':
    load_file()
