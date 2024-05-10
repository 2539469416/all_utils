from datetime import datetime
import mmap
import os
import re

import pandas as pd


def match_nginx_log_bt(log):
    pattern = r'^([\d.]+) - - \[(.*?)\] "(\S+).*?" (\d+) \d+ "(.*?)" "(.*?)"'
    matches = re.match(pattern, log)
    if matches:
        ip_address = matches.group(1)
        timestamp = matches.group(2)
        # 定义原始日期时间字符串的格式
        raw_format = "%d/%b/%Y:%H:%M:%S %z"
        # 定义目标日期时间字符串的格式
        target_format = "%Y-%m-%d"
        # 解析原始日期时间字符串
        parsed_datetime = datetime.strptime(timestamp, raw_format)
        # 将解析后的日期时间字符串格式化为目标格式
        formatted_datetime_str = parsed_datetime.strftime(target_format)
        request_method = matches.group(3)
        status_code = matches.group(4)
        user_agent = matches.group(6)
        source = {"ip_address": ip_address, "timestamp": formatted_datetime_str, "request_method": request_method,
                  "status_code": status_code, "user_agent": user_agent}
        return source
    else:
        return None


def read_nginx_log(filename):
    print(filename)
    with open(filename, 'r') as file:
        ip_map = {}
        try:
            # 创建内存映射对象
            mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            line = mm.readline()
            while line:
                log_line = line.decode().strip()
                source_data = match_nginx_log_bt(log_line)
                if source_data is None or source_data["status_code"] == '400':
                    line = mm.readline()
                    continue
                item = {"count": 1, "starttime": source_data["timestamp"],
                        "endtime": source_data["timestamp"]}
                if source_data["ip_address"] not in ip_map:
                    ip_map[source_data["ip_address"]] = item
                else:
                    ip_map[source_data["ip_address"]]["count"] = ip_map[source_data["ip_address"]]["count"] + 1
                    ip_map[source_data["ip_address"]]["endtime"] = item["endtime"]
                line = mm.readline()
            mm.close()
            df = pd.DataFrame(ip_map).transpose()
            csv_filename = "./tmp/" + filename.split("\\")[-1] + ".csv"
            df.to_csv(csv_filename)
        except Exception as e:
            print(f'line{e.__traceback__.tb_lineno}' + str(e))
    # 关闭内存映射对象


directory = "C:/hlnet/1-1715224009/tmp.qcow2/分区2/www/wwwlogs"


def load_file():
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 可以在这里对文件进行操作，例如打印文件名
            ipaddress_map = {}
            path = os.path.join(root, filename)
            # 筛选条件  只筛选log 后缀 不包含报错
            if path.endswith(".log") and "error" not in path:
                read_nginx_log(path)


load_file()
