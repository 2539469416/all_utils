import subprocess
import time


def brute_force_7z_password(archive_file, password_list):
    for password in password_list:
        command = f'7z -y x -p"{password}" {archive_file}'
        result = subprocess.run(command, shell=True)
        # time.sleep(5)
        if result.returncode == 0:
            print(f"爆破成功: {password}")
            break
        else:
            print(f"尝试: {password}")


def init_pass(formatted_number):
    with open(password_dict_file, 'w', encoding='utf-8') as file:
        for i in range(10000):
            # 使用 '{:04d}' 格式化字符串来保证生成的数字始终有四位，不足四位的前面会填充零
            formatted_number = '{:04d}'.format(i)
            file.write(formatted_number + '\n')
        file.close()


if __name__ == "__main__":
    # 7z文件路径和密码字典文件路径
    archive_file = "C:/Users/86135/Desktop/QR_code.7z"
    password_dict_file = "password.txt"

    # 从密码字典文件中读取密码列表
    with open(password_dict_file, 'r', encoding="utf-8") as f:
        password_list = [line.strip() for line in f]

    # 开始密码爆破
    brute_force_7z_password(archive_file, password_list)