import os
import redis
import rdbtools


db_num = 0
r = redis.Redis(host='httpdaili-gz.redis.rds.aliyuncs.com', port=6379, password='Qwerty123456', db=db_num,decode_responses=True)
filename = 'export/'
all_keys = r.keys('*')
keys = []

for key in all_keys:
    keys.append(key)

if not os.path.exists(f'{filename}{db_num}'):
    os.makedirs(f'{filename}{db_num}')

# 导出数据到文件
for key in keys:
    try:
        value = r.dump(key)
        with open(f'{filename}{db_num}/{key}.dump', 'wb') as f:
            print(value)
            f.write(value)  # 写入时再次编码为utf-8
    except Exception as e:
        print(e)

print('备份完成')
