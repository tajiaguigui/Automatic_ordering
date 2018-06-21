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
    tb_id = l[0]["tb_url"]
    # print(words)
    return words


def automatic(word, tb_id):
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
    lists = r.lrange("urls", 0, -1)
    # drivers = []
    # for i in range(len(lists)):
    #   drivers.append(webdriver.Chrome())

    # map(lambda x:x[0].get(x[1]),zip(drivers, lists))

    # print(lists)
    for data in lists:
        print(data)
        driver = webdriver.Chrome()
        driver.get(data)
        # driver.maximize_window()
        html = etree.HTML(driver.page_source)
        name = html.xpath('//*[contains(@class, "J_MemberNick")]/text()')
        if len(name) >= 1:
            # self.login_signal = 1
            username = name[0]
            print(username)
            time.sleep(1)
            elem = driver.find_element_by_name("q")
            # 输入关键词
            elem.send_keys(word)
            # elem.send_keys("男装")
            time.sleep(1)
            elem.send_keys(Keys.RETURN)
            # 浏览网页
            # com_id = "//*[@id='J_Itemlist_TLink_{}']".format(tb_id)
            # com_id = "//*[@id='J_Itemlist_Pic_{}']".format(tb_id)
            com_id = "//*[@id='J_Itemlist_PLink_{}']".format(tb_id)
            print(com_id)
            commodity = []
            while len(commodity) < 1:
                driver.maximize_window()
                js = "var q=document.documentElement.scrollTop=100000"
                driver.execute_script(js)
                time.sleep(3)
                html = etree.HTML(driver.page_source)
                commodity = html.xpath(com_id)
                print(commodity)
                # driver.find_element_by_xpath(
                #     "//a[@class='J_Ajax num icon-tag']/span[1]"
                # ).click()
                if len(commodity) > 0:
                    time.sleep(1)
                    # driver.find_element_by_xpath(com_id).send_keys(Keys.RETURN)
                    driver.find_element_by_xpath(com_id).click()
                else:
                    driver.execute_script(
                        "document.querySelector('.icon-btn-next-2').click();"
                    )
                    time.sleep(2)

            print("找到宝贝")
            # driver.find_element_by_xpath(
            #     "//a[@class='J_Ajax num icon-tag']/span[1]"
            # ).click()
            # time.sleep(1)
            # # 继续点击下一页
            # driver.find_element_by_xpath(
            #     "//a[@class='J_Ajax num icon-tag']/span[1]"
            # ).click()
            # time.sleep(2)
            # # 选择一个宝贝
            # driver.find_element_by_xpath(
            #     "//*[@id='mainsrp-itemlist']/div/div/div[1]/div[2]/div[1]/div/div[1]"
            # ).click()

            time.sleep(4)
            print("下单成功，退出浏览器")
            r.lrem("urls", data)
            driver.quit()
        else:
            time.sleep(1)
            driver.quit()
            print("验证登录中")
            r.lrem("urls", data)
            continue


if __name__ == "__main__":
    words = ordering()
    tb_id = 567393849346
    print(words)
    print(tb_id)
    word = words[1][1]
    print(word)
    automatic(word, tb_id)
