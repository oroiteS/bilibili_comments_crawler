# 根据bv号获取视频的评论（大概100条）和标题、简介、tag
import json
import sys
import time

import pymongo
from playwright.sync_api import sync_playwright

'''
2.根据bv得到网址，使用playwright打开 finish
3.获得该网页的源代码 
    3.1 分析html，得到标题、简介、tag
4.模拟下滑操作，使评论加载完毕
5.获得所有request和response
6.遍历所有request和response，找到特定的请求并获取响应内容
    6.1分析response_content.json，得到评论
    6.2 保存到文件当中
'''


def get_video_information(date, kinds, bv_list):
    # 得到 cookies
    with open('b站cookie.json', 'r', encoding='utf-8') as file:
        cookies = json.load(file)

    # 设置 User-Agent
    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 "
        "Safari/537.36 QuarkPC/1.9.0.151")

    # 打开数据库
    myclient = pymongo.MongoClient("mongodb://localhost:27017")  # Host以及port
    db = myclient["big_data"]
    coll = db['bilibili']

    with (sync_playwright() as playwright):
        browser = playwright.chromium.launch(headless=False)  # 设置 headless=False 以显示浏览器窗口
        context = browser.new_context()
        context.add_init_script(f"navigator.__proto__.userAgent={user_agent}")
        for i, bv in enumerate(bv_list):
            print(index)
            data = {"date": date, "kinds": kinds, "bv": bv}
            url = f'https://www.bilibili.com/video/{bv}'
            page = context.new_page()
            page.context.add_cookies(cookies)
            # 定义列表来存储网络请求和响应
            network_requests = []
            network_responses = []

            # 定义事件处理函数，用于捕获网络请求和响应
            def handle_request(net_request):
                network_requests.append(net_request)

            def handle_response(net_response):
                network_responses.append(net_response)

            # 绑定请求和响应事件
            page.on("request", handle_request)
            page.on("response", handle_response)
            # 访问页面以应用 cookies
            page.goto(url)
            # 等待加载完成，同时降低速度
            time.sleep(4)
            intro = ''
            # 先获取到标题、简介、tag
            try:
                title = page.locator('h1.video-title.special-text-indent').text_content().replace('\x00', '')
            except:
                try:
                    title = page.locator('a.mediainfo_mediaTitle__Zyiqh').text_content().replace('\x00', '')
                    intro = page.locator('p.mediainfo_content_placeholder__Tgx67').text_content().replace('\x00', '')
                except:
                    title = ''
            if intro == '':
                try:
                    # 获取简介
                    intro = page.locator('span.desc-info-text').text_content().replace('\x00', '')
                except:
                    pass

            # 获取 tag
            tag_list = []
            try:
                # 特殊的置顶 tag
                topic_tags = page.locator('span.tag-txt')
            except:
                pass
            if topic_tags.count() > 0:
                for topic_tag in topic_tags.all():
                    tag_list.append(topic_tag.text_content())
            try:
                # 普通 tag
                tags = page.locator('a.tag-link[target="_blank"]')
            except:
                pass
            if tags.count() > 0:
                for tag in tags.all():
                    tag_list.append(tag.text_content())
            data['title'] = title
            data['intro'] = intro.replace("\n", "  ")
            tag_str = ''
            for tag in tag_list:
                tag_str += tag + ','
            data['tags'] = tag_str.replace('\x00', '')

            # 定义一个函数来模拟下滑操作
            def scroll_page():
                for _ in range(10):  # 大约下滑 10 次
                    page.mouse.wheel(0, 7500)  # 模拟鼠标滚轮下滑
                    page.wait_for_timeout(700)  # 等待页面加载，700 毫秒

            # 等待加载完成，同时降低速度
            time.sleep(1)
            # 执行下滑操作
            scroll_page()

            if network_requests is None or network_responses is None:
                # dic = {'content': '', 'uname': '', 'sex': '', 'sign': ''}
                data['comment'] = []
                coll.insert_one(data)

                page.close()
                context.close()
                # 关闭浏览器
                browser.close()
                return
            comments = []
            # 遍历网络请求和响应，找到特定的请求并获取响应内容
            for request in network_requests:
                for response in network_responses:
                    if request.url == response.url and request.url.startswith(
                            "https://api.bilibili.com/x/v2/reply/wbi/main"):
                        if response.status != 200:
                            sys.exit(1)
                        # 获取响应内容
                        response_content = response.json()
                        if response_content['message'] == '当前页面评论功能已关闭' or response_content['message'] == 'UP主已关闭评论区':
                            data['comment'] = []
                            coll.insert_one(data)

                            page.close()
                            context.close()
                            # 关闭浏览器
                            browser.close()
                            return
                        # 置顶评论
                        if response_content['data']['top_replies'] is not None:
                            for index in response_content['data']['top_replies']:
                                top_replies_content = index['content']['message']
                                top_replies_member = index['member']
                                top_replies_replies_content = []
                                top_replies_replies_member = []
                                # 置顶评论的回复
                                for index_next in index['replies']:
                                    top_replies_replies_content.append(index_next['content']['message'])
                                    top_replies_replies_member.append(index_next['member'])
                                dic = {'content': top_replies_content.replace("\n", "  ").replace('\x00', ''),
                                       'uname': top_replies_member['uname'].replace('\x00', ''),
                                       'sex': top_replies_member['sex'],
                                       'sign': top_replies_member['sign'].replace("\n", "  ").replace('\x00', '')}
                                comments.append(dic)
                                for i in range(len(top_replies_replies_content)):
                                    dic = {
                                        'content': top_replies_replies_content[i].replace("\n", "  ").replace('\x00',
                                                                                                              ''),
                                        'uname': top_replies_replies_member[i]['uname'].replace('\x00', ''),
                                        'sex': top_replies_replies_member[i]['sex'],
                                        'sign': top_replies_replies_member[i]['sign'].replace("\n", "  ").replace(
                                            '\x00', '')}
                                    comments.append(dic)

                        # 插入普通评论
                        if response_content['data']['replies'] is not None:
                            for index in response_content['data']['replies']:
                                replies_content = index['content']['message']
                                replies_member = index['member']
                                replies_content_replies = []
                                replies_member_replies = []
                                # 普通评论的回复
                                for index_next in index['replies']:
                                    replies_content_replies.append(index_next['content']['message'])
                                    replies_member_replies.append(index_next['member'])
                                dic = {'content': replies_content.replace("\n", "  ").replace('\x00', ''),
                                       'uname': replies_member['uname'].replace('\x00', ''),
                                       'sex': replies_member['sex'],
                                       'sign': replies_member['sign'].replace("\n", "  ").replace('\x00', '')}
                                comments.append(dic)
                                for i in range(len(replies_content_replies)):
                                    dic = {
                                        'content': replies_content_replies[i].replace("\n", "  ").replace('\x00', ''),
                                        'uname': replies_member_replies[i]['uname'].replace('\x00', ''),
                                        'sex': replies_member_replies[i]['sex'],
                                        'sign': replies_member_replies[i]['sign'].replace("\n", "  ").replace('\x00',
                                                                                                              '')}
                                    comments.append(dic)

            data['comment'] = comments
            # print(data)
            coll.insert_one(data)
            page.close()
        context.close()
        # 关闭浏览器
        browser.close()
