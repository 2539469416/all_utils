import base64
import json
import os
import socket
import subprocess
import time

import pyautogui
import redis

# 连接到Redis服务器
redis_client = redis.StrictRedis(host='192.168.1.251', port=6379, db=0, decode_responses=True)


def capture():
    file_list = ["D:/xiangrikui/SunloginClient/SunloginClient.exe",
                 "C:/Program Files/Oray/SunLogin/SunloginClient/SunloginClient.exe"]
    for file_name in file_list:
        if os.path.exists(file_name):
            subprocess.Popen(file_name)
            time.sleep(1)
    # 获取所有记事本窗口
    windows = pyautogui.getWindowsWithTitle("向日葵远程控制")
    # 如果找到记事本窗口
    if windows:
        # 获取向日葵
        window = windows[0]
        # 获取窗口位置和大小
        left = window.left
        top = window.top
        right = window.right
        bottom = window.bottom
        width = right - left
        height = bottom - top
        check_dlg(left, top, width, height)
        try:
            loc = pyautogui.locateCenterOnScreen("./tmp/target.png", region=(left, top, width, height))
            print("识别到code隐藏")
            pyautogui.moveTo(*loc, duration=0.5)
            pyautogui.click()
            check_dlg(left, top, width, height)
            pyautogui.moveTo(0, 0)
            x, y, w, h = left + width / 4, top + height / 4, width / 3 * 2, height / 4
            pyautogui.screenshot("./tmp/shot.png", region=(int(x), int(y), int(w), int(h)))
            print("获取成功")
        except Exception as e:
            print(f'not found {e}')
    else:
        return False
    return True


def check_dlg(x, y, w, h):
    try:
        loc = pyautogui.locateCenterOnScreen("./tmp/cancel.png",
                                             region=(x + int(w / 4), y + int(w / 5), w, h))
        if loc:
            print("检测到弹窗，尝试关闭")
            pyautogui.moveTo(*loc, duration=0.5)
            pyautogui.click()
    except Exception as e:
        print(e)


def png_format():
    # 读取图片文件为二进制数据
    with open('./tmp/shot.png', 'rb') as image_file:
        image_data = image_file.read()
    # 将图片数据转换为Base64字符串
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    return image_base64


def save(byte):
    hostname = socket.gethostname()
    datatime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    data = json.dumps({"datetime": datatime, "src": byte})
    redis_client.hset('user:id', hostname, data)


if __name__ == '__main__':
    res = capture()
    if not res:
        print("获取失败")
    img_byte = png_format()
    save(img_byte)
