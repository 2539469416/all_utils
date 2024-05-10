import openpyxl


def extract_urls(filename):
  """
  从xlsx文件中提取所有url

  Args:
    filename: xlsx文件名

  Returns:
    所有url的列表
  """

  wb = openpyxl.load_workbook(filename)
  urls = []
  domain = []
  for sheet in wb.worksheets:
    for row in sheet.iter_rows():
      for cell in row:
        if cell.value is not None:
          # 使用正则表达式匹配url
          import re
          urls.extend(re.findall(r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/])?", cell.value))
  for url in urls:
    domain.append(url[1])
  return set(domain)


if __name__ == "__main__":
  # 输入xlsx文件名
  filename = "E:\\00密码\赌博线索\\2\\微信群聊（群号-34600106065）.xlsx"
  filename2 = "E:\\00密码\\赌博线索\\3\\微信群聊（微信id-2634436548）.xlsx"

  # 提取所有url
  urls = extract_urls(filename)
  urls2 = extract_urls(filename2)
  urls = list(urls) + list(urls2)

  # 打印所有url
  for url in set(urls):
    print(url)
