"""
梳理一下流程：
1.爬取当日视频的bv，在综合热门和排行榜当中
    1.1 综合热门 bv_comprehensive_hot.py
    1.2 排行榜 bv_leader_board.py
2.根据bv得到网址，使用playwright打开 get_comment_information_by_bv.py
3.获得该网页的源代码
    3.1 分析html，得到标题、简介、tag
4.模拟下滑操作，使评论加载完毕
5.获得所有request和response
6.遍历所有request和response，找到特定的请求并获取响应内容
    6.1分析response_content.json，得到评论
    6.2 保存到文件当中
"""
import time

from bv_leader_board import get_leader_bv
from final_crawler.get_bilibili_comment.bv_comprehensive_hot import get_com_bv
from get_comment_information_by_bv import get_video_information


def main():
    # 获取日期信息
    date = time.strftime("%Y.%m.%d", time.localtime())
    # 获取综合热门的bv号
    bv_list = get_com_bv()
    get_video_information(date, 'comprehensive', bv_list)
    # 获取排行榜的bv号
    bv_list = get_leader_bv()
    get_video_information(date, 'leaderboard', bv_list)


if __name__ == '__main__':
    main()
