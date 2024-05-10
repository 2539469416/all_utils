import time
from datetime import datetime
import mmap
import os
import re

import pandas as pd

from 本地IP数据库 import IPCz


def match_nginx_log_bt(log):
    try:
        patterns = {
            "auth": r"auth:(\"-\"|\w+)",
            "src": r"src:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
            "dst": r"dst:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
            "upstr": r"upstr:(-|\w+)",
            "reqid": r"reqid:(\w+)",
            "req": r"req:\"([^\"]+)\"",
            "reqlen": r"reqlen:(\d+)",
            "fin": r"fin:(\w+)",
            "pro": r"pro:(-|\w+)",
            "ssl": r"ssl:(on|off)",
            "sslpro": r"sslpro:(\w+)",
            "sni": r"sni:(-|\w+)",
            "host": r"host:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
            "errno": r"errno:(\d+)",
            "upserrno": r"upserrno:(-|\d+)",
            "gid": r"gid:(-|\d+)",
            "rid": r"rid:(-|\d+)",
            "os": r"os:(-|\w+)",
            "client": r"client:(-|\w+)",
            "hostv": r"hostv:(-|\w+)",
            "ipv": r"ipv:(-|\w+)",
            "nodev": r"nodev:(-|\w+)",
            "country": r"country:(-|\w+)",
            "respsize": r"respsize:(\d+)",
            "acc": r"acc:([^,]+)",
            "acclang": r"acclang:(-|\w+)",
            "refer": r"refer:\"([^\"]+)\"",
            "xff": r"xff:\"([^\"]+)\"",
            "reqtime": r"reqtime:(\d+\.\d+)",
            "agent": r"agent:\"([^\"]+)\""
        }

        # 使用正则表达式提取字段值
        log_dict = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, log)
            if match:
                log_dict[field] = match.group(1)
            else:
                log_dict[field] = "-"
        log_dict["timestamp"] = log.split(",")[1].split("T")[0]
        return log_dict
    except Exception as e:
        print(log)
        print(f'error_line{e.__traceback__.tb_lineno}:  ' + str(e))
    return None


def read_nginx_log(filename, ip_map):
    ipcz = IPCz()
    with open(filename, 'r') as file:
        try:
            # 创建内存映射对象
            mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            line = mm.readline()
            while line:
                log_line = line.decode().strip()
                source_data = match_nginx_log_bt(log_line)
                if source_data is None or source_data["errno"] == '404':
                    line = mm.readline()
                    continue
                if source_data["src"] not in ip_map:
                    item = {"count": 1, "starttime": source_data["timestamp"],
                            "endtime": source_data["timestamp"], "address": ipcz.get_ip_address(source_data["src"])}
                    ip_map[source_data["src"]] = item
                else:
                    ip_map[source_data["src"]]["count"] = ip_map[source_data["src"]]["count"] + 1
                    ip_map[source_data["src"]]["endtime"] = source_data["timestamp"]
                line = mm.readline()
            mm.close()
            return ip_map

        except Exception as e:
            print(f'line{e.__traceback__.tb_lineno}' + str(e))
    # 关闭内存映射对象


directory = "D:/code/py/all_utils/tmp_file"


def load_file():
    ipaddress_map = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            print(f'filename:{filename}')
            # 可以在这里对文件进行操作，例如打印文件名
            path = os.path.join(root, filename)
            # 筛选条件  只筛选log 后缀 不包含报错
            ipaddress_map = read_nginx_log(path, ipaddress_map)
            print(len(ipaddress_map))
    print(f'all len is {len(ipaddress_map)}')
    df = pd.DataFrame(ipaddress_map).transpose()
    csv_filename = "./tmp1/运维.csv"
    df.to_csv(csv_filename)


load_file()
