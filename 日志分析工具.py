import mmap
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from clickhouse_driver import Client

from ip地址数据库 import SearchIp

# 创建一个连接


# 选择或创建数据库


ip_search = SearchIp()


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



# 数据持久化，ip地址解析
def upload_data(data_list):
    try:
        client = Client(host='192.168.232.168', port=9000)
        target_data = []
        for data in data_list:
            address = ip_search.get_address(data['src'])
            data['address'] = address
            data['timestamp'] = datetime.strptime(data['timestamp'], '%Y/%m/%d').isoformat()
            target_data.append(data)
        # collection.insert_many(target_data)
        query = "INSERT INTO vpn (timestamp, src, dst, address) VALUES"
        # 添加数据的占位符
        query += ' (%(timestamp)s, %(src)s, %(dst)s, %(address)s),' * len(data)
        query = query[:-1]
        client.execute(query, data)
        print(f'成功上传{threading.current_thread().name} :::')
        client.disconnect()
        return True
    except Exception as e:
        print(f'line{e.__traceback__.tb_lineno} :::{e}')


def read_nginx_log(filename):
    with open(filename, 'r') as file:
        # 创建内存映射对象
        mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
        data_list = []
        line_num = 0
        line = mm.readline()
        with ThreadPoolExecutor(max_workers=20) as executor:
            while line:
                try:
                    log_line = line.decode().strip()
                    source_data = match_nginx_log_bt(log_line)
                    if source_data is None:
                        line = mm.readline()
                        continue
                    line_num += 1
                    data_list.append(source_data)
                    if line_num % 10 == 0:
                        executor.submit(upload_data, data_list)
                        data_list = []
                    line = mm.readline()
                except Exception as e:
                    line_num += 1
                    print(f'line{e.__traceback__.tb_lineno}' + str(e) + "::::" + str(line))
        upload_data(data_list)
        mm.close()
    # 关闭内存映射对象


directory = "./tmp_file/"


def load_file():
    for root, dirs, files in os.walk(directory):
        start = time.time()
        for filename in files:
            print(f'filename:{filename}')
            # 可以在这里对文件进行操作，例如打印文件名
            path = os.path.join(root, filename)
            # 筛选条件  只筛选log 后缀 不包含报错
            read_nginx_log(path)
        end = time.time()

        print(f"all time:{end - start}")



# load_file()
if __name__ == '__main__':
    load_file()
