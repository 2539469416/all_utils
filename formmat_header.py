from lxpy import copy_headers_dict

header = """
Accept: application/json
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: keep-alive
Content-Length: 18
Content-Type: application/x-www-form-urlencoded
Cookie: sessionId=ea4eac0999dd436cb21bfb10151b1e74
Host: 39.109.127.251
Origin: http://39.109.127.251
Referer: http://39.109.127.251/home/logList
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42
X-CSRF-TOKEN: undefined
X-Requested-With: XMLHttpRequest
"""
print(copy_headers_dict(header))

