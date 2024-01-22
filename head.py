import base64
import datetime
import hmac
import subprocess

import requests


######################替换区#################################################
# 替换为自己的AccessKeyId和AccessKeySecret
access_key_id = 'LTAI5t9ufxsji36pezahbSeJ'
access_key_secret = 'ebtOL5T9NRxvASwo7qVDCOIrnCgi04'
# 设置Bucket和Object名称
bucket_name = 'test-buk2'
object_name = 'Shadowfly-4.1.9.rar'
# oss位置
path = 'test-buk2.oss-cn-beijing.aliyuncs.com'
command = "D:\download\Shadowfly-4.1.9.rar"
result_file = "./result.txt"
#########################################################################
# 设置GMT时间戳
gmt_date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')


# 本地crc计算
def local_crc():
    process = subprocess.Popen('ossutil64.exe hash ' + command + ' --type=crc64', shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # 等待命令执行完成
    process.wait()

    # 获取命令的输出和错误信息
    output = process.stdout.read()
    error = process.stderr.read()

    # 将输出和错误信息解码为字符串
    output = output.decode(encoding="gbk")
    error = error.decode(encoding="gbk")

    # 返回命令的输出和错误信息
    print(output)
    hash_code = output.split(":")[1]
    return hash_code


def get_only_verify():
    # 构造字符串ToSign
    canonicalized_resource = '/' + bucket_name + '/' + object_name
    string_to_sign = 'HEAD\n\n\n' + gmt_date + '\n' + canonicalized_resource
    # 计算签名
    signature = base64.b64encode(hmac.new(
        access_key_secret.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        digestmod='sha1').digest())
    authorization = 'OSS ' + access_key_id + ':' + signature.decode('utf-8')
    print(authorization)
    # 构造请求头部
    headers = {
        'Host': path,
        'Date': gmt_date,
        'Authorization': authorization
    }

    # 发送请求
    response = requests.head('http://' + path + '/' + object_name, headers=headers)
    return response


def hash_code():
    process = subprocess.Popen('certutil -hashfile ' + command + ' SHA256', shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # 等待命令执行完成
    process.wait()

    # 获取命令的输出和错误信息
    output = process.stdout.read()
    error = process.stderr.read()

    # 将输出和错误信息解码为字符串
    output = output.decode(encoding="gbk")
    error = error.decode(encoding="gbk")
    hash_code = output.split("\r\n")[1]
    return hash_code


# 输出响应结果
res = get_only_verify()
print(res.status_code)
target = res.headers
print(target)
server_crc = target['X-Oss-Hash-Crc64ecma']
print("服务器CRC地址为:" + server_crc)
local_crc = local_crc().strip()
# 本地计算方法
# ossutil64.exe hash test.txt --type=crc64

if (local_crc == server_crc):
    result = "服务器与本地文件，校验成功，与阿里云文件相同"
else:
    result = "服务器与本地文件，校验失败,filed"
print(result)
sha256 = hash_code()
print('sha256:' + sha256)
