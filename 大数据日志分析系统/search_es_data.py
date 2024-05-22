from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from pandas._config import dates

es = Elasticsearch(hosts=["http://192.168.232.170:9200"])

if __name__ == '__main__':
    data_list = ip_addresses = [
        '119.28.30.171',
        '165.154.60.103',
        '165.154.42.85',
        '165.154.42.112',
        '165.154.42.182',
        '152.32.185.144',
        '165.154.60.118',
        '165.154.60.64',
        '165.154.60.115',
        '165.154.40.203',
        '165.154.42.132',
        '152.32.175.64',
        '165.154.42.7',
        '45.249.244.218',
        '118.193.44.6',
        '152.32.175.238',
        '152.32.175.85',
        '118.193.39.206',
        '152.32.254.5',
        '165.154.71.230',
        '43.129.250.119',
        '139.155.143.159',
        '132.193.178',  # This entry seems incomplete or incorrect
        '101.32.222.67',
        '39.109.126.89',
        '39.109.122.75',
        '154.221.30.89',
        '156.236.72.232',
        '39.109.116.195',
        '39.109.126.20'
    ]
    for data in data_list:
        res = es.search(index="vpn_log", body={
            "query": {
                "term": {
                    "message": data
                }
            }
        })
        if res['hits']['total']['value'] != 0:
            for hit in res['hits']['hits']:
                print(hit['_source'])
