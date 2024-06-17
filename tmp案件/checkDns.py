import json
import re
import socket
import ipaddress

from concurrent.futures import ThreadPoolExecutor

count = 0


def check_port(host, pro):
    port = 53
    """
    检查指定主机和端口是否开放

    :param host: 主机名或IP地址
    :param port: 端口号
    :return: True if the port is open, False otherwise
    """
    try:
        # 创建一个socket对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 设置超时时间，防止阻塞
        global count
        global dns_servers
        # 尝试连接到指定端口
        result = sock.connect_ex((host, port))

        # 关闭socket
        sock.close()

        # 如果连接没有问题（返回值为0），则端口是开放的
        if result == 0:
            if pro in dns_servers:
                if host not in dns_servers[pro]:
                    dns_servers[pro].append(host)
            else:
                dns_servers[pro] = [host]
            print(f"host{host},pro{pro}")
        else:
            count += 1
        return result == 0
    except socket.error as e:
        print(f"Socket error: {e}")
        return False


provinces = ['北京', '天津', '河北', '山西', '内蒙', '辽宁', '吉林', '黑龙', '上海', '江苏', '浙江', '安徽', '福建',
             '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏',
             '陕西', '甘肃', '青海', '宁夏', '新疆']

dns_servers = {}


def format_line(l):
    try:
        l = l.replace("\n", "")
        s = l.split("\t")
        s[0] = re.sub(r'（.*?）', '', s[0])
        if len(s) < 2 or s[0][0].isdigit():
            return False
        elif s[0][0].isalpha() and s[0][0].isascii() and len(s[0]) > 4:
            province = s[0][:3]
        else:
            province = s[0][:2]
        d = {"province": province, "server": []}
        for i in range(1, len(s)):
            try:
                s[i] = re.sub(r'（.*?）', '', s[i])
                ipaddress.IPv4Address(s[i])
                d["server"].append(s[i])
            except Exception as e:
                return False
        return d
    except IndexError as e:
        return False


# if __name__ == '__main__':
#     filename = "./log1.txt"
#     print('的'.isalpha())
#     with open("provinces.json", 'w', encoding='utf-8') as f:
#         #     json.dump(data, f, ensure_ascii=False, indent=4)
#         # print(li)
#         futures = []
#         with ThreadPoolExecutor(max_workers=50) as executor:
#             with open(filename, "r", encoding='utf-8') as f:
#                 for line in f:
#                     data = format_line(line)
#                     if not data:
#                         continue
#                     for s in data['server']:
#                         futures.append(executor.submit(check_port, s, data['province']))
#                 executor.shutdown(wait=True)
#                 with open("provinces.json", 'w', encoding='utf-8') as f:
#                     json.dump(dns_servers, f, ensure_ascii=False, indent=4)
#                 print(dns_servers)

if __name__ == '__main__':
    maps = json.load(open('provinces.json', encoding='utf-8'))
    lis = []
    for m in maps:
        for l in maps[m]:
           if l not in lis:
                lis.append(l)
           else:
               print(l)
    print(maps)
