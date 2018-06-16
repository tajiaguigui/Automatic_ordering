from selenium import webdriver
import time
from lxml import etree


l = webdriver.Chrome()
time.sleep(2)
js = 'window.open("https://login.taobao.com/member/login.jhtml");'

for i in range(3):
    l.execute_script(js)

handles = l.window_handles
del handles[0]
print(handles)

time.sleep(4)
imgs = []
for handle in handles:
    l.switch_to_window(handle)
    print(l.current_window_handle)
    html = etree.HTML(l.page_source)
    qrcode_img = html.xpath('//div[@id="J_QRCodeImg"]/img/@src')
    qrcode_img = 'https:' + qrcode_img[0]
    imgs.append(qrcode_img)


print(imgs)
