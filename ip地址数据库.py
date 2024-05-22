import json
import struct
import socket
import time

from 本地IP数据库 import IPCz


class SearchIp:
    def __init__(self):
        self.data_list = []
        self.data_map = []
        self.init_data()

    def get_address(self, ip):
        int_ip = self.get_ip(ip)
        return self.data_map.get(str(int_ip))

    def ip_to_string(self, ip):
        """
        整数IP转化为IP字符串
        :param ip:
        :return:
        """
        return str(ip >> 24) + '.' + str((ip >> 16) & 0xff) + '.' + str((ip >> 8) & 0xff) + '.' + str(ip & 0xff)

    def string_to_ip(self, s):
        """
        IP字符串转换为整数IP
        :param s:
        :return:
        """
        (ip,) = struct.unpack('I', socket.inet_aton(s))
        return ((ip >> 24) & 0xff) | ((ip & 0xff) << 24) | ((ip >> 8) & 0xff00) | ((ip & 0xff00) << 8)

    def get_ip(self, ip):
        datas = self.data_list
        if type(ip) == str:
            ip = self.string_to_ip(ip)
        lens = len(datas)
        L = 0
        R = lens - 1
        if ip < datas[0]:
            return datas[0]
        while L < R - 1:
            M = int((L + R) / 2)
            if (ip == datas[M] or (ip > datas[M] and ip < datas[M + 1]) or (ip < datas[M] and ip > datas[M - 1])):
                return datas[M]
            if ip > datas[M]:
                L = M
            elif ip < datas[M]:
                R = M

    def init_data(self):
        with open('./tmp/ip.json', 'r') as file:
            data = json.load(file)
            self.data_list = data['list']
            self.data_map = data['map']

if __name__ == '__main__':
    start = time.time()
    searchip = SearchIp()
    print(searchip.get_address('172.16.31.10'))
    end = time.time()
    ipcz = IPCz('./tmp/ip.dat')
    print(ipcz.get_ip_address('172.16.31.10'))
    end1 = time.time()
    print(end-start)
    print(end1-end)


