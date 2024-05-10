import mmap
import os

import pandas as pd
from pygrok import Grok
from 本地IP数据库 import IPCz


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


def read_nginx_log(filename, ip_map):
    ipcz = IPCz('../tmp/ip.dat')
    all_data = pd.DataFrame()
    with open(filename, 'r') as file:
        try:
            # 创建内存映射对象
            mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            line = mm.readline()
            while line:
                log_line = line.decode().strip()
                source_data = match_nginx_log_bt(log_line)
                if source_data is None:
                    line = mm.readline()
                    continue
                # if source_data["errno"] == '404':
                #     line = mm.readline()
                #     continue
                df = df.set_index('src')
                if source_data["src"] not in df['src']:
                    item = {"count": 1, "starttime": source_data["timestamp"],
                            "endtime": source_data["timestamp"], "address": ipcz.get_ip_address(source_data["src"])}
                    df.append(item)
                else:
                    ip_map[source_data["src"]]["count"] = ip_map[source_data["src"]]["count"] + 1
                    ip_map[source_data["src"]]["endtime"] = source_data["timestamp"]
                line = mm.readline()
            mm.close()
            return ip_map

        except Exception as e:
            print(f'line{e.__traceback__.tb_lineno}' + str(e))
    # 关闭内存映射对象


directory = "../tmp_file/"


def load_file():
    ipaddress_map = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            print(f'filename:{filename}')
            # 可以在这里对文件进行操作，例如打印文件名
            path = os.path.join(root, filename)
            # 筛选条件  只筛选log 后缀 不包含报错
            if not filename.endswith("log"):
               continue
            ipaddress_map = read_nginx_log(path, ipaddress_map)
            print(len(ipaddress_map))
    print(f'all len is {len(ipaddress_map)}')
    df = pd.DataFrame(ipaddress_map).transpose()
    csv_filename = "../tmp/运维2.csv"
    df.to_csv(csv_filename)


# load_file()
if __name__ == '__main__':
    load_file()
