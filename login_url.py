import redis
import requests
import json
import sys

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

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, db=0)
r = redis.Redis(connection_pool=pool)

def login():
    lists = r.lrange("tokens", 0,-1)
    # print(lists)
    for data in lists:
        token = eval(data)
        lgToken = token[0]
        umid_token = token[1]
        # print(lgToken)
        # print(umid_token)
        url = "https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken=" + str(lgToken)
        url += "&defaulturl=https%3A%2F%2Fwww.taobao.com%2F&_ksTS=1460659151617_231&umid_token=" + str(umid_token)
        # print(url)
        rsp = sess.get(url)
        b = json.loads(rsp.text)
        code = int(b['code'])
        print(code)

        if 10006 == code:
            successLoginURL = b['url'] + "&umid_token=" + str(umid_token)
            r.lpush("urls", successLoginURL)
            # print(r.lindex("urls", 0))
            print(successLoginURL)
            r.lrem("tokens", token)
            print("登录成功，正在跳转")
#        if 10000 == code:
#            print("请扫描二维码登录")
#            return "请扫描二维码登录"
#            continue
#        elif 10001 == code:
#            print("已扫描二维码，请在确认登录")
#            return "已扫描二维码，请在确认登录"
#
#        elif 10004 == code:
#            print("已过期请重新扫描")
#            #get_login()
#            return "已过期请重新扫描"


        else:
            r.lrem("tokens", token)
            print("未知错误，退出执行")
            #sys.exit(0)
            #cookies = rsp.cookies.get_dict()
            #print(cookies)
            #print(rsp.cookies)
            #print(c)
            #对应第 4 步
            # r = sess.get(b['url'])
            # cookies = rsp.cookies.get_dict()
            # print(cookies)



if __name__ == '__main__':
    login()
