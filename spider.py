import requests
import re
import json
from requests.exceptions import RequestException
import pymongo
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_url_function(url):
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        return None


def parser_function(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?title="(.*?)".*?</a>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    result = re.findall(pattern, html)
    for item in result:
        yield {
            '排名': item[0],
            '电影名称': item[1],
            '上映时间': item[2].strip()[5:],
            '评分': item[3] + item[4]
        }

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('成功')
    except Exception:
        print('失败')


#def write_function(item):
    #with open('/Users/yifang.gao/Downloads/result.txt', 'a', encoding='utf-8') as f:
        #f.write(json.dumps(item, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    url = 'https://maoyan.com/board/4?offset='
    for i in range(10):
        urlt = url + str(i * 10)
        html = get_url_function(urlt)
        for item in parser_function(html):
            print(item)
            save_to_mongo(item)