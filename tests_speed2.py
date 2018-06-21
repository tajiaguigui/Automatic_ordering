from multiprocessing import Pool
from selenium import webdriver
import time


def run(url):
    lists = []
    q = webdriver.Chrome()
    q.get(url)
    print(q)
    lists.append(q)
    return lists



if __name__ == '__main__':
    s = time.time()
    urls = ['https://www.taobao.com', 'https://www.taobao.com',
        'https://www.taobao.com', 'https://www.taobao.com',
        'https://www.taobao.com']
    pool = Pool(processes=3)
    result = pool.map(run, urls)
    e = time.time()
    print(e - s)
    print(result)
    print(result.get(timeout=1))
