# 爬取当天的综合热门的bv
import time

from playwright.sync_api import sync_playwright
import json

'''
大致流程为：
打开对应的网址
执行下滑操作
获取request和response并解析内容
返回bv列表
'''


def get_bv_list(response):
    bv_list = []
    # 解析json文件
    datas = response['data']['list']
    for data in datas:
        bv_list.append(data['short_link_v2'][15:])
    return bv_list


def get_com_bv():
    url = 'https://www.bilibili.com/v/popular/all'
    # 得到cookies
    with open('b站cookie.json', 'r', encoding='utf-8') as file:
        cookies = json.load(file)
    # 设置 User-Agent
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 "
        "Safari/537.36 QuarkPC/1.9.0.151")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)  # 设置 headless=False 以显示浏览器窗口
        context = browser.new_context()
        context.add_init_script(f"navigator.__proto__.userAgent={user_agent}")
        page = context.new_page()
        page.context.add_cookies(cookies)
        # 定义列表来存储网络请求和响应
        network_requests = []
        network_responses = []
        bv_list = []

        # 定义事件处理函数，用于捕获网络请求和响应
        def handle_request(net_request):
            network_requests.append(net_request)

        def handle_response(net_response):
            network_responses.append(net_response)

        # 绑定请求和响应事件
        page.on("request", handle_request)
        page.on("response", handle_response)
        # 再次访问页面以应用 cookies
        page.goto(url)

        # 定义一个函数来模拟下滑操作
        def scroll_page():
            for _ in range(15):  # 大约下滑15次，可以得到大概140个bv
                page.mouse.wheel(0, 600)  # 模拟鼠标滚轮下滑
                page.wait_for_timeout(500)  # 等待页面加载，500毫秒

        # 等待加载完成，同时降低速度
        time.sleep(2)
        # 执行下滑操作
        scroll_page()
        # 打印捕获的网络请求和响应
        for request in network_requests:
            for response in network_responses:
                if request.url == response.url and request.url.startswith("https://api.bilibili.com/x/web-interface"
                                                                          "/popular?ps=20&pn"):
                    bv_list.extend(get_bv_list(response.json()))
        # 关闭浏览器
        browser.close()
    return bv_list


if __name__ == '__main__':
    print(len(get_com_bv()))

