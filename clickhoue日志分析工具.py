import os
import time
import mmap

from clickhouse_driver import Client
from pygrok import Grok

from 本地IP数据库 import IPCz

clickhouse_ip = '192.168.232.168'
client = Client(host=clickhouse_ip, port=9000, user='default', password='')

# 创建一个表
client.execute("DROP TABLE IF EXISTS falcon_table")
client.execute("""
CREATE TABLE IF NOT EXISTS falcon_table
(
    src String,
    count Int32,
    timestamp DateTime,
    address String,
    status Int32
) ENGINE = MergeTree
PARTITION BY toYYYYMM(timestamp) 
ORDER BY (src, timestamp)
SETTINGS index_granularity = 8192;""")


def match_nginx_log_bt(log):
    pattern = "%{GREEDYDATA:timestamp} %{GREEDYDATA:source_file} src\:%{GREEDYDATA:src} dst\:%{GREEDYDATA:dst} %{GREEDYDATA:source_file}"
    grok = Grok(pattern)
    match = grok.match(log)
    if match is not None:
        match['timestamp'] = match['timestamp'].split(" ")[0]
        match['src'] = match['src'].split(":")[0]
        match['dst'] = match['dst'].split(":")[0]
        return match
    else:
        print("error no match: " + log)
        return None


def read_nginx_log(filename):
    ipcz = IPCz('./tmp/ip.dat')
    with open(filename, 'r') as file:
        try:
            # 创建内存映射对象
            mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            line = mm.readline()
            while line:
                log_line = line.decode().strip()
                source_data = match_nginx_log_bt(log_line)
                src = source_data['src']
                timestamp = source_data['timestamp']
                address = ipcz.get_ip_address(src)
                # 条件
                if source_data is None:
                    line = mm.readline()
                    continue
                # if source_data["errno"] == '404':
                #     line = mm.readline()
                #     continue
                exits_query = f'select 1 from falcon_table where src= \'{src}\''
                exists = client.execute(exits_query)
                if exists:
                    # 如果存在，则执行计数加一的操作\
                    update_query = f'ALTER TABLE falcon_table UPDATE count = count + 1 WHERE src = \'{src}\''
                    print(update_query)
                    client.execute(update_query)
                else:
                    # 如果不存在，则插入新的记录
                    insert_query = f'INSERT INTO falcon_table (src, count, timestamp, address) VALUES (\'{src}\', 1, \'{timestamp}\', \'{address}\')'
                    client.execute(insert_query)
                time.sleep(1)
                line = mm.readline()
            mm.close()


        except Exception as e:
            print(f'line{e.__traceback__.tb_lineno}' + str(e))
    # 关闭内存映射对象


directory = "./tmp_file/"


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
