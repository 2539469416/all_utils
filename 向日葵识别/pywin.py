import base64
import json
import time

import cv2
import pytesseract
import redis
import numpy as np

redis_client = redis.StrictRedis(host='192.168.232.128', port=6379, db=0)


def png_format(b):
    try:
        np_array = np.frombuffer(b, dtype=np.uint8)
        image = cv2.imdecode(np_array, flags=cv2.IMREAD_COLOR)
        retval, binary_image = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)
        # 显示原始图像和灰度图像
        text = pytesseract.image_to_string(binary_image)
        c, p = text.rsplit(" ", 1)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(f'识别到验证码{c}')
        return c, p
    except Exception as e:
        print(f'line{e.__traceback__.tb_lineno} :::{e}')


def redis_format():
    pic_map = redis_client.hgetall("user:id")
    for dic in pic_map:
        try:
            hostname = dic.decode('utf-8')
            bytes = pic_map[dic].decode('utf-8')
            json_map = json.loads(bytes)
            datetime = json_map['datetime']
            src = json_map['src']
            binary_data = base64.b64decode(src)
            code, password = png_format(binary_data)
            data = json.dumps({"datetime": datetime, "code": code, "password": password})
            redis_client.hset('user:name', hostname, data)

        except Exception as e:
            print(f'line{e.__traceback__.tb_lineno} :::{e}')


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
    while True:
        redis_format()
        time.sleep(3600)
