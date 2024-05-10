import re

import pyshark

cap = pyshark.FileCapture(r"E:\2023-龙信杯检材容器\2023龙信杯检材\流量包\流量包\数据包1.cap",
                          display_filter='http.request or (http.request and mime_multipart) or (http.response and data-text-lines)')
cookies = []
for pkt in cap:
    try:
        http = pkt['HTTP']
        try:
            print(re.findall(r"\(#cmd='(.*?)'\)", http.content_type)[0])
        except:
            pass
    except:
        pass
