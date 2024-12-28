# 爬取b站评论

还是中文的写起来舒服（来自不会英语的笨蛋）

## 项目结构

get_bilibili_comment:

- bv_commprehensive_hot.py:获取当前的综合热门bv
	
- bv_leader_board.py:获取当前的排行榜bv
	
- get_bilibili_cookies.py:获取cookies
	
- get_comment_information_by_bv.py:根据bv号获取评论
	
- main.py:程序入口

get_weekly_comment:

- get_comment_information_by_bv.py:根据bv号获取评论

- get_weekly_bv_list.py:获取每周热门的bv，从第一期开始（更改循环我记得是）

- main.py:程序入口

- test.py:我忘了

result:

- must_see_weekly/weekly_bv.csv:爬取的每周必看列表
