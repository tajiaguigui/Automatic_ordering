#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, redirect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from lxml import etree
import requests
from functools import wraps
from flask import make_response, request, jsonify, session
import requests
import re
import json
import os
import pickle
from selenium_test import ReuseChrome
import redis


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun

class Browser(object):
    def __init__(self):
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.PhantomJS()
        # 登录信号
        self.login_signal = 0
        # 设置超时任务时间
        self.start_time = time.time()

    def create_qrcode(self):
        """
        生成一个二维码
        :return: 二维码图片地址
        """
        browser = self.driver
        browser.get('https://login.taobao.com/member/login.jhtml')
        html = etree.HTML(browser.page_source)
        qrcode_img = html.xpath('//div[@id="J_QRCodeImg"]/img/@src')
        qrcode_img = 'https:' + qrcode_img[0]
        print(qrcode_img)
        return qrcode_img, browser

    def verify_login(self):
        """
        判断是否登录成功
        :return:
        """
        if int(time.time() - self.start_time) >= 60:
            self.driver.quit()
            return '任务超时'
        result = re.search(r'待收货', self.driver.page_source, re.S)
        if result:
            print('success')
            html = etree.HTML(self.driver.page_source)
            name = html.xpath('//*[contains(@class, "J_MemberNick")]/text()')
            if len(name) >= 1:
                self.login_signal = 1
                username = name[0]
                print(username)
                return username
        else:
            time.sleep(1)
            print('验证登录中')
            self.verify_login()

    def ordering(self):
        driver = self.driver
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
        time.sleep(2)
        #选择一尺码175/XL
        #driver.find_element_by_xpath("//*[@id='J_DetailMeta']/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li[3]/a/span[1]").click()
        #选择颜色
        #driver.find_element_by_xpath("//*[@id='J_DetailMeta']/div[1]/div[1]/div/div[4]/div/div/dl[2]/dd/ul/li[1]/a/span[1]").click()
        #time.sleep(1)
        #点击确认
        #driver.find_element_by_xpath("//*[@id='J_LinkBasket']").click()
        time.sleep(1)
        driver.quit()




#def ordering(action_string)
# browser = Browser()

@app.route('/')
@allow_cross_domain
def index():
    return render_template('bb.html')


@app.route('/ordering', methods=['GET', 'POST'])
def ordering():
    action_string = request.args.get('action_string')
    task_id = request.args.get('task_id')
    r = requests.get('handler.ashx?action_string={}&task_id={}'.
                     format(action_string, task_id))
    if r.status_code != 200:
        response = {
            "resultcode": "404",
            "reason": "查询失败",
            "result": None
        }
        return jsonify(response)
    data = json.loads(r.content.decode('utf-8'))
    l = json.loads(data['data']['task_list'])
    words = l[0]['tb_words']
    return words


@app.route('/qrcode', methods=['GET', 'POST'])
@allow_cross_domain
def qrcode():
    browser = Browser()
    img, driver = browser.create_qrcode()
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    print(executor_url)
    print(session_id)
    b_id = os.getpid()
    db.set(b_id, [executor_url, session_id])
    # db.set('url', executor_url)
    # db.set('id', session_id)
    # session['url'] = executor_url
    # session['id'] = session_id
    print(b_id)
    print(img)
    r = requests.get('https://api.qrserver.com/v1/read-qr-code/?fileurl=' + img)
    data = json.loads(r.content)
    q_url = data[0]['symbol'][0]['data']
    print(q_url)
    if q_url is not None:
        return redirect(q_url)
    else:
        os.exit(0)

@app.route('/automatic', methods=['GET', 'POST'])
def automatic():
    # browser = Browser()
    executor_url = session.get('url')
    session_id = session.get('id')
    print(executor_url)
    print(session_id)
    driver = ReuseChrome(command_executor=executor_url, session_id=session_id)
    print(driver.current_url)
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

#    if username is not None:
#        g.ordering()
#        response = {
#            'code':200,
#            'msg':'自动下单成功'
#        }
#        return jsonify(response)
#    else:
#        response = {
#            'code':404,
#            'msg':'未授权'
#        }
#        return jsonify(response)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
