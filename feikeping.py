import time

import requests

while True:
    time.sleep(1)
    try:
        rep = requests.get("http://192.168.5.200/login", timeout=1)
        print(rep.status_code)
    except Exception as e:
        print("runtime")
