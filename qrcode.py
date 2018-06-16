import requests
import time
import sys
import json
from random import random
#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'}
headers = {'authority': 'login.taobao.com',
            'method': 'GET',
            'path': '/member/loginByIm.do?uid=cntaobao%E5%91%A8%E5%B0%8F%E6%BB%91&token=6b9aeb3f02410a1c8a892015d3470fd2&time=1527148256106&asker=qrcodelogin&ask_version=1.0.0&defaulturl=https%3A%2F%2Fwww.taobao.com%2F&webpas=b622a87cc7af5e5135fb015ac99e2a8e21524234',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
proxies = {

  "https": "http://192.168.2.175:1080",
}
sess = requests.session()
sess.headers = headers

def empower():
    # 获取随机umid_token
    date = ''.join(str(time.time()).split('.'))[0:13]
    print(date)
    print(len(date))

    r_11 = ''.join(str(random()).split('.'))[1:12]
    print(r_11)
    print(len(r_11))

    r_3 = ''.join(str(random()).split('.'))[13:16]
    print(r_3)
    print(len(r_3))

    umid_token = "C" + date + r_11 + date +r_3

    print(umid_token)
    print(len(umid_token))
    #对应第 1 步
    #rsp = requests.get("https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?from=BGG请求登陆")
    #rsp = requests.get("https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=333&appkey=00000000&umid_token=C1527134546551258528758571527134546551723&_ksTS=1527134942603_4683")
    rsp = requests.get("https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?shortURL=true&adUrl=&adImage=&adText=&viewFd4PC=&viewFd4Mobile=&from=333&appkey=00000000&umid_token=" + str(umid_token))
    b = json.loads(rsp.text)


    #对应第 2 步，将以下打印的二维码 url 贴到浏览器，用手机淘宝扫描
    url = b['url']
    lgToken = b['lgToken']
    print(b['url'])
    print(b['lgToken'])
    return url, lgToken, umid_token
    
    
    
    
    
    
    
    