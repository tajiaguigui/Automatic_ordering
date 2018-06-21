from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium_test import ReuseChrome
import redis
import time
import re

# import psutil
import sys
from lxml import etree
import requests
import json
from multiprocessing import Pool

pool = redis.ConnectionPool(host="localhost", port=6379, decode_responses=True, db=0)
r = redis.Redis(connection_pool=pool)


def ordering():
    action_string = "Get_task_by_id"
    task_id = r.get("task_id")
    print(task_id)
    rsp = requests.get(
        "http://antqi.net/handler.ashx?action_string={}&task_id={}".format(
            action_string, task_id
        )
    )
    if rsp.status_code != 200:
        response = {"resultcode": "404", "reason": "查询失败", "result": None}
        return response
    data = json.loads(rsp.content.decode("utf-8"))
    l = json.loads(data["data"]["task_list"])
    words = l[0]["tb_words"]
    # print(words)
    return words


def automatic(data):
    """
    word 是输入的淘宝搜索关键词
    """

    # executor_url = db.get('url')
    # session_id = db.get('id')
    # print(session_id)
    # print(executor_url)
    # driver = ReuseChrome(command_executor=executor_url, session_id=session_id)
    # print(driver.current_url)
    # username = driver.verify_login()
    # print(username)
    # drivers = []
    # for i in range(len(lists)):
    #   drivers.append(webdriver.Chrome())

    # map(lambda x:x[0].get(x[1]),zip(drivers, lists))

    print(lists)
    print(data)
    driver = webdriver.Chrome()
    driver.get(data)
    html = etree.HTML(driver.page_source)
    name = html.xpath('//*[contains(@class, "J_MemberNick")]/text()')
    if len(name) >= 1 and name[0] != "你好":
        # self.login_signal = 1
        username = name[0]
        print(username)
        time.sleep(1)
        elem = driver.find_element_by_name("q")
        # 输入关键词
        # elem.send_keys(word)
        elem.send_keys("男装")
        time.sleep(1)
        elem.send_keys(Keys.RETURN)
        # 浏览网页
        # com_id = "J_Itemlist_TLink_" + tb_id
        # while len(commodity) > 0:
        #     html = etree.HTML(driver.page_source)
        #     commodity = html.xpath(com_id)
        #     time.sleep(1)
        #     driver.find_element_by_xpath(
        #         "//a[@class='J_Ajax num icon-tag']/span[1]"
        #     ).click()
        driver.find_element_by_xpath(
            "//a[@class='J_Ajax num icon-tag']/span[1]"
        ).click()
        time.sleep(1)
        # 继续点击下一页
        driver.find_element_by_xpath(
            "//a[@class='J_Ajax num icon-tag']/span[1]"
        ).click()
        time.sleep(2)
        # 选择一个宝贝
        driver.find_element_by_xpath(
            "//*[@id='mainsrp-itemlist']/div/div/div[1]/div[2]/div[1]/div/div[1]"
        ).click()

        time.sleep(4)
        print("下单成功，退出浏览器")
        r.lrem("urls", data)
        driver.quit()
    else:
        time.sleep(1)
        driver.quit()
        print("验证登录中")
        r.lrem("urls", data)
        # continue


if __name__ == "__main__":
    words = ordering()
    print(words)
    word = words[0][0]
    # lists = r.lrange("urls", 0, -1)
    lists = ['https://login.taobao.com/member/loginByIm.do?uid=cntaobaolife%E5%B0%B1100&token=4a72ce0a61fd64fa288dde2b82ad6827&time=1529403212659&asker=qrcodelogin&ask_version=1.0.0&defaulturl=https%3A%2F%2Fwww.taobao.com%2F&webpas=52eaa03079cc832272465a2721303fbf1660156188&umid_token=C1529403202326788503468141529403202326218', 'https://login.taobao.com/member/loginByIm.do?uid=cntaobaolife%E5%B0%B1100&token=4a72ce0a61fd64fa288dde2b82ad6827&time=1529403212659&asker=qrcodelogin&ask_version=1.0.0&defaulturl=https%3A%2F%2Fwww.taobao.com%2F&webpas=52eaa03079cc832272465a2721303fbf1660156188&umid_token=C1529403202326788503468141529403202326218']
    print(lists)
    pool = Pool(processes=2)
    # automatic(word)
    pool.map(automatic, lists)
    # pool.apply_async(automatic, (word, data))
