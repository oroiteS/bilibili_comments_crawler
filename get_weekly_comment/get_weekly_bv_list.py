# 获得每周必看的全部的bv号
import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver


def get_weekly_bv_list():
    driver = webdriver.Edge()
    # bv_list = []
    for i in range(295, 296):
        print(i)
        bv_l = []
        url = f'https://www.bilibili.com/v/popular/weekly?num={i}'
        driver.get(url)
        # 等待
        time.sleep(6)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        divs = soup.find_all('div', class_='video-card__content')
        for div in divs:
            a = div.find('a', attrs={'target': '_blank'})
            bv = a.get('href')[25:]
            bv_l.append(bv)
        # bv_list.append(bv_l)
        # 保存到文件当中
        with open('../result/must_see_weekly/weekly_bv.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for bv in bv_l:
                writer.writerow([i, bv])
    # 关闭浏览器
    driver.quit()
    # 保存到文件当中
    # with open('../result/must_see_weekly/weekly_bv.csv', 'a', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     for i in range(len(bv_list)):
    #         for bv in bv_list[i]:
    #             writer.writerow([i + 1, bv])


get_weekly_bv_list()
