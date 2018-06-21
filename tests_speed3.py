from concurrent import futures
import time

from selenium import webdriver


def run(url):
    q = webdriver.Chrome()
    q.get(url)
    return q


def run_many():
    urls = ['https://www.taobao.com', 'https://www.taobao.com',
            'https://www.taobao.com', 'https://www.taobao.com',
            'https://www.taobao.com']
    with futures.ThreadPoolExecutor(5) as executor:
        res = executor.map(run, urls)

    return len(list(res))


def main(run_many):
    t0 = time.time()
    count = run_many()
    cost = time.time() - t0
    print(count)
    print(cost)


if __name__ == '__main__':
    main(run_many)
