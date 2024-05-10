import requests

def download_file(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"文件已下载到 {destination}")
    else:
        print(f"下载失败，状态码: {response.status_code}")


# 使用示例
file_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Kokbayraq_flag.svg/255px-Kokbayraq_flag.svg.png'  # 将URL替换为您要下载的文件的URL
file_destination = 'local_file.ext'  # 将local_file.ext替换为您希望文件保存到的本地路径

download_file(file_url, file_destination)
