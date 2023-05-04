from lxpy import copy_headers_dict

header = """
Host: www.cnnvd.org.cn
Content-Length: 111
Sec-Ch-Ua: "Chromium";v="109", "Not_A Brand";v="99"
Accept: application/json, text/plain, */*
Content-Type: application/json;charset=UTF-8
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36
Sec-Ch-Ua-Platform: "Windows"
Origin: https://www.cnnvd.org.cn
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://www.cnnvd.org.cn/home/loophole
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
"""
print(copy_headers_dict(header))

