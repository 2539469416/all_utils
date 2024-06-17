import mmap

filename = "C:/Users/86135/Desktop/xianll.xwamwh.cn.log用户代理分析/xianll.xwamwh.cn.log用户代理分析.csv"
with open(filename, 'r') as file:
    mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    line = mm.readline()
    while line:
        log = line.decode('utf-8').strip()
        if "106" not in log and "36.110" not in log:
            print(log)
        line = mm.readline()
    mm.close()
