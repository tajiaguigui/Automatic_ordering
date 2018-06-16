from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium_test import ReuseChrome
import redis
import time
import re
# import psutil
import sys


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
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
    elem = driver.find_element_by_name("q")
    # 输入关键词
    elem.send_keys("男装")
    time.sleep(1)
    elem.send_keys(Keys.RETURN)
    #浏览网页
    driver.find_element_by_xpath("//a[@class='J_Ajax num icon-tag']/span[1]").click()
    time.sleep(3)
    #继续点击下一页
    driver.find_element_by_xpath("//a[@class='J_Ajax num icon-tag']/span[1]").click()
    time.sleep(2)
    #选择一个宝贝
    driver.find_element_by_xpath("//*[@id='mainsrp-itemlist']/div/div/div[1]/div[2]/div[1]/div/div[1]").click()

    time.sleep(1)
    driver.quit()

automatic()

import redis  
  
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)  
r = redis.Redis(connection_pool=pool)  
  
pipe = r.pipeline()  
pipe_size = 100000  
  
len = 0  
key_list = []  
print r.pipeline()  
keys = r.keys()  
for key in keys:  
    key_list.append(key)  
    pipe.get(key)  
    if len < pipe_size:  
        len += 1  
    else:  
        for (k, v) in zip(key_list, pipe.execute()):  
            print k, v  
        len = 0  
        key_list = []  
  
for (k, v) in zip(key_list, pipe.execute()):  
    print k, v  
