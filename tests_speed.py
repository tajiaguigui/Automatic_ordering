from selenium import webdriver
import time

s = time.time()
driver = []
for i in range(5):
    driver.append(webdriver.Chrome())

e = time.time()
cost = e - s
print(cost)
print(driver)
