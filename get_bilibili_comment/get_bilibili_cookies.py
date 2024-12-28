# 得到我的cookies
import time
import json
from selenium import webdriver

driver = webdriver.Edge()
driver.get("https://www.bilibili.com")
driver.delete_all_cookies()
time.sleep(10)
input("111111")

dictions = driver.get_cookies()
jsons = json.dumps(dictions)

with open("/b站cookie.json", 'w') as f:
    f.write(jsons)
driver.quit()
