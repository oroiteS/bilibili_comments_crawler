# 爬取当天的排行榜
import time

from bs4 import BeautifulSoup
from selenium import webdriver


def get_leader_bv():
    # 通过selenium来获取
    url = 'https://www.bilibili.com/v/popular/rank/all'
    driver = webdriver.Edge()
    driver.get(url)
    # 等待页面加载完成
    time.sleep(2)
    # 解析html
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    bv_list = []
    bvs = soup.find_all('a', attrs={'target': '_blank', 'class': 'title'})
    for bv in bvs:
        bv_list.append(bv.get('href')[25:])
    return bv_list


if __name__ == '__main__':
    print(len(get_leader_bv()))
