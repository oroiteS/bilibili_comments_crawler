"""
大致流程如下：
1.获取所有的每周必看的bv，按照第几期分类 get_weekly_bv_list.py
2.将爬取的所有的bv保存到一个文件当中（必须的，不然不知道从哪里开始） bingo ☑️
3.根据bv获取视频的标题、简介、tag、评论
4.保存到文件当中
"""
import csv
import time

from get_comment_information_by_bv import get_video_information


def get_bv_list():
    bv_list = []
    with open('../result/must_see_weekly/weekly_bv.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            bv_list.append(row)
            # print(row[1])
    return bv_list[1:]


def main():
    start = time.time()
    print(start)
    bv_list = get_bv_list()
    for i in range(8610, 10419):
        print(f"第{i+1}行，第{bv_list[i][0]}期，bv号是{bv_list[i][1]}")
        get_video_information(bv_list[i][0], bv_list[i][1])
    end = time.time()
    print(end)
    # 输出运行时间
    print(f"{(end-start)/3600}h")


main()
