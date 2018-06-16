from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium_test import ReuseChrome
import redis
import time
import re
# import psutil
import sys
from lxml import etree

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, db=0)
r = redis.Redis(connection_pool=pool)



def automatic():

    # executor_url = db.get('url')
    # session_id = db.get('id')
    # print(session_id)
    # print(executor_url)
    # driver = ReuseChrome(command_executor=executor_url, session_id=session_id)
    # print(driver.current_url)
    # username = driver.verify_login()
    # print(username)
    lists = r.lrange("urls", 0,-1)
    print(lists)
    for data in lists:
        print(data)
        driver = webdriver.Chrome()
        driver.get(data)
        html = etree.HTML(driver.page_source)
        name = html.xpath('//*[contains(@class, "J_MemberNick")]/text()')
        if len(name) >= 1:
            #self.login_signal = 1
            username = name[0]
            print(username)
            time.sleep(1)
            elem = driver.find_element_by_name("q")
            # 输入关键词
            elem.send_keys("男装")
            time.sleep(1)
            elem.send_keys(Keys.RETURN)
            #浏览网页
            driver.find_element_by_xpath("//a[@class='J_Ajax num icon-tag']/span[1]").click()
            time.sleep(1)
            #继续点击下一页
            driver.find_element_by_xpath("//a[@class='J_Ajax num icon-tag']/span[1]").click()
            time.sleep(2)
            #选择一个宝贝
            driver.find_element_by_xpath("//*[@id='mainsrp-itemlist']/div/div/div[1]/div[2]/div[1]/div/div[1]").click()

            time.sleep(1)
            print("下单成功，退出浏览器")
            driver.quit()
            r.lrem("urls", data)
        else:
            time.sleep(1)
            driver.quit()
            print('验证登录中')
            r.lrem("urls", data)
            continue






automatic()


