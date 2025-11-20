import threading
import random
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from misc_utils import *
from multtp.meths.man import poster
from datatypes.ctrip.sqlite_types import ctrip_tbl_refs
"""
半自动爬虫
"""

database_fd = DBfd(
	str(Path(__file__).parent.joinpath('../../assets/dyn/ctrip.db').absolute()),
	ctrip_tbl_refs
)

def comment_api(
	cook: dict,
	location_id: int,
	page_idx: int,
	page_size: int=10,
) -> None:
	global database_fd
	papi = "https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?" \
	        f"_fxpcqlniredt={cook['GUID']}&" \
	         f"x-traceID={cook['GUID']}-{unix_ms()}-{random.random()*1_000_0000}"
	threading.Event().wait(random.randint(6, 17))
	resp = poster(
		url=papi,
		payload=dic2ease_json_str({
			"arg": {
			    "channelType": 2,
			    "collapseType": 0,
			    "commentTagId": -12, # -12 => 差评, -22 消费后评价, 0 默认评价展示序列
			    "pageIndex": page_idx,
			    "pageSize": page_size,
			    "poiId": location_id,
			    "sourceType": 1,
			    "sortType": 3,
			    "starType": 0
			},
			"head": {
				"cid": cook['GUID'],
				"ctok": "",
				"cver": "1.0",
				"lang": "01",
				"sid": "8888",
				"syscode": "09",
				"auth": "",
				"xsid": "",
				"extension": []
			}
		}),
		alter_dict={
			"Content-Type": "application/json",
			"Cookie": cook['cookie'],
			"Cookieorigin": "https://you.ctrip.com",
			"Origin": "https://you.ctrip.com",
			"Priority": "u = 1, i",
			"Referer": "https://you.ctrip.com/",
			"Sec-Fetch-Dest": "empty",
			# 不知道是什么东西
			"X-Ctx-Ubt-Sid": "1",
			"X-Ctx-Ubt-Pageid": "290510",
			"X-Ctx-Ubt-Pvid": "6",
			"X-Ctx-Ubt-Vid": f"{funix_ms()}RZv9R3CK",
		}
	)
	if resp is None:
		print('resp is None...')
		return
	elif 300 <= resp.status_code:
		print(resp.status_code)
		return
	json_resp = load_json_from_str(resp.text)
	if json_resp is None:
		print('unable to load json from reps.text, resp is:', resp.text)
		return
	comments_res = json_resp['result']['items']
	if len(comments_res) == 0:
		print(f'empty comment list at {page_idx}...')
		return
	del resp

	comment_ids = [_['commentId'] for _ in comments_res]
	comment_contents = [_['content'] for _ in comments_res]
	comment_ip_addr = [_['ipLocatedName'] for _ in comments_res]
	comment_liked = [_['usefulCount'] for _ in comments_res]
	comment_score = [_['score'] for _ in comments_res]
	comment_publish_date = [
		re.findall(r'^/Date\((\d+\+\d{4})\)/$', _['publishTime'])[0]
		for _ in comments_res
	]

	database_fd.insert_multivals_to_tbl(
		'comments',
		('comment_id', 'content', 'useful_cnt', 'score', 'ip_addr', 'publish_date'),
		[(v, comment_contents[i], comment_liked[i], comment_score[i], comment_ip_addr[i], comment_publish_date[i])
		 for i, v in enumerate(comment_ids)],
		['comment_id']
	)
	database_fd.insert_multivals_to_tbl(
		'comments_on_spots',
		('spot_id', 'comment_id'),
		[(location_id, v) for v in comment_ids],
		['spot_id', 'comment_id']
	)


def man_control(
	cook: dict,
	location_id: int,
	workers_num: int=3
) -> None:
	"""
	还需要人工调整
	"""
	# task_list = [_ for _ in range(1, 301)]
	task_list = [_ for _ in range(1, 256)]
	database_fd.insert_to_tbl(
		'scenic_spots',
		{'ssid': location_id, 'name': '桂林两江四湖风景区'}
	)
	with ThreadPoolExecutor(max_workers=workers_num) as per_mission:
		for t in task_list:
			per_mission.submit(
				comment_api, cook, location_id, t
			)
	database_fd.commit()
	database_fd.close()


if __name__ == '__main__':
	## 广西桂林
	# 90682 象鼻山
	# 75898 漓江
	# 76822 两江四湖
	## 贵州安顺
	# 79814 黄果树瀑布
	## 西安
	# 75682 兵马俑坑
	## 武汉
	# 77593 黄鹤楼
	## 上海
	# 东方明珠
	man_control(PRIVATE_CONFIG['ctrip']['guest'], 75627)