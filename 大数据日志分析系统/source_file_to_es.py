import mmap
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# 创建一个连接


# 选择或创建数据库
es = Elasticsearch(hosts=["http://192.168.232.170:9200"])


# 数据持久化，ip地址解析
def upload_data(data_list):
    try:
        res = bulk(es, data_list, index="vpn_log")
        print(f'成功上传{threading.current_thread().name} :::')
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
        with ThreadPoolExecutor(max_workers=8) as executor:
            while line:
                try:
                    log_line = line.decode().strip()
                    source = {"_source": {"message": log_line}}
                    data_list.append(source)
                    if len(data_list) % 1000 == 0:
                        executor.submit(upload_data, data_list)
                        data_list = []
                    line = mm.readline()
                except Exception as e:
                    line_num += 1
                    print(f'line{e.__traceback__.tb_lineno}' + str(e) + "::::" + str(line))
        upload_data(data_list)
        mm.close()
    # 关闭内存映射对象


directory = "../tmp_file/"


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
