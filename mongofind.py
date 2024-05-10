import pymongo
import scrapy
from queue import Queue

name = "github"
myclient = pymongo.MongoClient("mongodb://admin:123456@localhost:27017/")
mydb = myclient["vul"]
mycol = mydb["cnnvd"]
mycol.create_index("cnnvdCode", unique=True)
data_queue = Queue()


def get_data(page_num):
    page_size = 10
    skip = page_size * (page_num - 1)
    mongo_datas = mycol.find(None).limit(page_size).skip(skip)
    for mongo_data in mongo_datas:
        data_queue.put(mongo_data)


get_data(1)
print(data_queue.get())
print(data_queue._qsize())
