# ==================================================================
#       文 件 名: IPCz.py
#       概    要:  纯真IP解析类
#       作    者: IT小强
#       创建时间: 12/19/19 7:14 PM
#       修改时间:
#       copyright (c) 2016 - 2019 mail@xqitw.cn
# ==================================================================
import json
import socket
import time
from os.path import abspath, dirname
import struct

import redis


class IPCz:
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

    # 数据文件路径
    __cur_start_ip = None
    __cur_end_ip_offset = None
    __cur_end_ip = None

    def __init__(self, filename):

        self.__f_db = open(filename, "rb")
        # 文件头记录 4 字节 第一条索引偏离 和 4 字节 最后一条索引偏离
        bs = self.__f_db.read(8)
        (self.__first_index, self.__last_index) = struct.unpack('II', bs)
        # 记录总数
        self.__index_count = int((self.__last_index - self.__first_index) / 7 + 1)

    def get_version(self):
        """
        获取版本信息，最后一条IP记录 255.255.255.0-255.255.255.255 是版本信息
        :return: str
        """
        s = self.get_ip_address(0xffffff00)
        return s

    def __get_area_addr(self, offset=0):
        if offset:
            self.__f_db.seek(offset)
        bs = self.__f_db.read(1)
        (byte,) = struct.unpack('B', bs)
        if byte == 0x01 or byte == 0x02:
            p = self.__get_long3()
            if p:
                return self.__get_offset_string(p)
            else:
                return ""
        else:
            self.__f_db.seek(-1, 1)
            return self.__get_offset_string(offset)

    def __get_addr(self, offset):
        """
        获取offset处记录区地址信息(包含国家和地区)
        如果是中国ip，则是 "xx省xx市 xxxxx地区" 这样的形式
        (比如:"福建省 电信", "澳大利亚 墨尔本Goldenit有限公司")
        :param offset:
        :return:str
        """
        self.__f_db.seek(offset + 4)
        bs = self.__f_db.read(1)
        (byte,) = struct.unpack('B', bs)
        if byte == 0x01:  # 重定向模式1
            country_offset = self.__get_long3()
            self.__f_db.seek(country_offset)
            bs = self.__f_db.read(1)
            (b,) = struct.unpack('B', bs)
            if b == 0x02:
                country_addr = self.__get_offset_string(self.__get_long3())
                self.__f_db.seek(country_offset + 4)
            else:
                country_addr = self.__get_offset_string(country_offset)
            area_addr = self.__get_area_addr()
        elif byte == 0x02:  # 重定向模式2
            country_addr = self.__get_offset_string(self.__get_long3())
            area_addr = self.__get_area_addr(offset + 8)
        else:  # 字符串模式
            country_addr = self.__get_offset_string(offset + 4)
            area_addr = self.__get_area_addr()
        return country_addr + " " + area_addr

    def __set_ip_range(self, index):
        offset = self.__first_index + index * 7
        self.__f_db.seek(offset)
        buf = self.__f_db.read(7)
        # 无符号4有符号2无符号1
        (self.__cur_start_ip, of1, of2) = struct.unpack("IHB", buf)
        # 计算出记录区偏移量
        self.__cur_end_ip_offset = of1 + (of2 << 16)
        self.__f_db.seek(self.__cur_end_ip_offset)
        # 终止ip
        buf = self.__f_db.read(4)
        (self.__cur_end_ip,) = struct.unpack("I", buf)

    def get_ip_address(self, ip):
        """
        通过ip查找其地址
        :param ip: (int or str)
        :return: str
        """
        if type(ip) == str:
            ip = self.string_to_ip(ip)
        # 二分查找
        L = 0
        R = self.__index_count - 1
        while L < R - 1:
            M = int((L + R) / 2)
            self.__set_ip_range(M)
            if ip == self.__cur_start_ip:
                L = M
                break
            if ip > self.__cur_start_ip:
                L = M
            else:
                R = M
        self.__set_ip_range(L)
        # version information, 255.255.255.X, urgy but useful
        if ip & 0xffffff00 == 0xffffff00:
            self.__set_ip_range(R)
        if self.__cur_start_ip <= ip <= self.__cur_end_ip:
            address = self.__get_addr(self.__cur_end_ip_offset)
        else:
            address = "未找到该IP的地址"
        return address

    def get_ip(self, datas, ip):
        lens = len(datas)
        if type(ip) == str:
            ip = self.string_to_ip(ip)
        L = 0
        R = lens - 1
        while L < R - 1:
            M = int((L + R) / 2)
            if (ip == datas[M] or (ip > datas[M] and ip < datas[M + 1]) or (ip < datas[M] and ip > datas[M - 1])):
                return datas[M]
            if ip > datas[M]:
                L = M
            elif ip < datas[M]:
                R = M

    def get_ip_range(self, ip):
        """
        返回ip所在记录的IP段
        :param  ip
        :return: str
        """
        if type(ip) == str:
            ip = self.string_to_ip(ip)
        self.get_ip_address(ip)
        return self.ip_to_string(self.__cur_start_ip) + ' - ' + self.ip_to_string(self.__cur_end_ip)

    def __get_offset_string(self, offset=0):
        """
        获取文件偏移处的字符串(以'\0'结尾)
        :param offset: 偏移
        :return: str
        """
        if offset:
            self.__f_db.seek(offset)
        bs = b''
        ch = self.__f_db.read(1)
        (byte,) = struct.unpack('B', ch)
        while byte != 0:
            bs += ch
            ch = self.__f_db.read(1)
            (byte,) = struct.unpack('B', ch)
        return bs.decode('gbk')

    def __get_long3(self, offset=0):
        """
        3字节的数值
        :param offset:
        :return:
        """
        if offset:
            self.__f_db.seek(offset)
        bs = self.__f_db.read(3)
        (a, b) = struct.unpack('HB', bs)
        return (b << 16) + a

    def load_data(self):
        r = redis.Redis(host='192.168.232.168', port=6379, db=0)
        print(f'all count is {self.__index_count}')
        data_list = []
        data_map = {}
        for index in range(0, self.__index_count):
            offset = self.__first_index + index * 7
            self.__f_db.seek(offset)
            buf = self.__f_db.read(7)
            # 无符号4有符号2无符号1
            (self.__cur_start_ip, of1, of2) = struct.unpack("IHB", buf)
            self.__cur_end_ip_offset = of1 + (of2 << 16)
            self.__f_db.seek(self.__cur_end_ip_offset)
            buf = self.__f_db.read(4)
            (self.__cur_end_ip,) = struct.unpack("I", buf)
            address = self.__get_addr(self.__cur_end_ip_offset)
            startip = self.__cur_start_ip
            endip = self.__cur_end_ip
            data_list.append(endip)
            data_map[endip] = address
            # r.zadd('ip_search', {address: endip})
            print(endip, address)
        print('写入中')
        with open('./tmp/ip.json', 'w') as file:
            json.dump({'list': data_list, 'map': data_map}, file)
        print('写入完成')
        return address


if __name__ == "__main__":
    ipcz = IPCz('./tmp/ip.dat')
    ipcz.load_data()
    # print(IPCz().get_version())
    # print(IPCz().get_ip_range('127.0.0.1'))
    # print(IPCz().get_ip_address('8.8.8.8'))
