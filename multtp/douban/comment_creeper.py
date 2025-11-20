from pathlib import Path
from typing import Optional
from random import uniform
from concurrent.futures import ThreadPoolExecutor
from threading import Event as ThreadEvent
from threading import Semaphore
import re

from bs4 import BeautifulSoup
from curl_cffi import Response
from loguru import logger

from misc_utils import *
from multtp import *
from datatypes.douban.sqlite_types import douban_tbl_refs
"""
课程作业的一个附属实现

WARN: 网页版坠机了，爬着爬着封禁IP，得用代理池才行

或者等到弹出证明请求的时候尝试证明？不过感觉怪怪的，一边消耗一边又将其加入到任务队列中
<form method="POST" id="form" action="/misc/sorry"><div style="display:none;"><input type="hidden" name="ck" value="lZQ4"/></div>
	<input type="hidden" id="ticket" name="ticket" value="">
	<input type="hidden" id="randstr" name="randstr" value="">
	  <input type="hidden" name="original-url" value="https://movie.douban.com/subject/36516431/comments?start=400&amp;limit=20&amp;status=P&amp;sort=time" />
	<button id="tcaptcha_btn" type="button" click=>点击证明</button>
</form>

但哪怕过了验证码测试，最多最多只能从网页爬400个下来

好消息是移动端没限得那么死，而且还提供结构化json接口。
"""
logger.remove()
logger.add(
	GLOB_TEST_LOG_PATH,
	level='DEBUG',
	colorize=True,
	format=GLOB_LOG_FORMAT,
	rotation="16MB",
	compression='zip',
	encoding='utf-8'
)


class _CeaserObj:
	def __init__(self):
		self._lock = Semaphore(1)
		self._cease_flag = False

	def flip_flag(self):
		self._lock.acquire()
		self._cease_flag ^= True
		self._lock.release()

	@property
	def read_flag(self):
		self._lock.acquire()
		ret = self._cease_flag
		self._lock.release()
		return ret

cease_flag = _CeaserObj()
# TODO: 这个可能用改到配置里更好
movie_comment_db_path = Path(__file__).parent.joinpath('../../assets/dyn/douban.db').resolve()
database_fd = DBfd(
	str(movie_comment_db_path),
	douban_tbl_refs
)

def skim_one_movie_info(subject_id: int, cook: dict) -> Optional[Response]:
	host = 'https://movie.douban.com'
	api = f'/subject/{subject_id}/comments?status=P&sort=new_score'
	return getter(
		url=host+api,
		alter_dict={
			'Referer': f'https://movie.douban.com/subject/{subject_id}/',
			"Upgrade-Insecure-Requests": '1',
			# "Priority": "u=0, i",
			"Cookie": cook['cookie']
		}
	)


def comment_and_likes_dumper(
	movie_id: int,
	html_str: str
):
	global database_fd, cease_flag
	comment_info_list = BeautifulSoup(html_str, 'html.parser')
	comment_list = comment_info_list.find_all(name='div', class_='comment')
	nxt_page_checker = comment_info_list.find_all(name='span', class_='next')
	if isinstance(nxt_page_checker, list) and len(nxt_page_checker) > 0:
		cease_flag.flip_flag()
	vote_on_curr_comment, comment_content = [], []
	comment_timestamps, comment_ids = [], []
	for c in comment_list:
		vote_num = c.find_all(name='span', class_='votes vote-count')
		vote_on_curr_comment.append(vote_num[0].text)
		content = c.find_all(name='span', class_='short')
		comment_content.append(content[0].text)
		comment_time = c.find_all(name='span', class_='comment-time')
		comment_timestamps.append(comment_time[0]['title'])
		comment_id = c.find_all(name='a', class_='j vote-comment')
		comment_ids.append(int(comment_id[0]['data-id']))

	database_fd.insert_multivals_to_tbl(
		'comments', ('comment_id', 'votes', 'content', 'publish_date'), [
			(comment_ids[i], v, comment_content[i], comment_timestamps[i])
			for i, v in enumerate(vote_on_curr_comment)
		], ['comment_id']
	)
	database_fd.insert_multivals_to_tbl(
		'comment_on_movies', ('comment_id', 'movie_id'), [
			(v, movie_id) for v in comment_ids
		], ['comment_id', 'movie_id']
	)


def get_one_page(
	subject_id: int,
	cook: dict,
	start_pos: int
) -> None:
	"""
	得到json之后还得自己去解析html，比较麻烦的api
	很遗憾，limit不可更改。
	"""
	global cease_flag
	host = 'https://movie.douban.com'
	api = f'/subject/{subject_id}/comments?' \
	      f'percent_type=&start={start_pos}&limit=20&status=P&' \
	      f'sort=new_score&comments_only=1&ck={cook["ck"]}'

	alter_dict = {
		'Referer': f'https://m.douban.com/subject/{subject_id}/'
		           f'comments?limit={start_pos}&status=P&sort=new_score',
		'Cookie': cook['cookie'],
		"Priority": "u=0, i",
	}
	if cease_flag.read_flag:
		return
	ThreadEvent().wait(uniform(6, 23))
	resp = getter(url=host+api, alter_dict=alter_dict)
	if resp is None:
		print('resp is None...')
		return
	elif 300 <= resp.status_code:
		print(start_pos, resp.status_code)
		cease_flag.flip_flag()
		return
	comments_html_text: dict = load_json_from_str(resp.text)
	if comments_html_text is None or not isinstance(comments_html_text, dict):
		logger.warning(f'unable to properly convert json to dict in python at {start_pos}')
		return
	comment_and_likes_dumper(subject_id, comments_html_text['html'])


def get_one_json(
	subject_id: int,
	cook: dict,
	start_pos: int,
	comment_num: int
) -> None:

	global cease_flag
	gapi = f'https://m.douban.com/rexxar/api/v2/tv/{subject_id}/interests?' \
	       f'count={comment_num}&order_by=hot&anony=0&start={start_pos}&ck={cook["ck"]}&for_mobile=1'
	if cease_flag.read_flag:
		return
	ThreadEvent().wait(uniform(6, 23))
	print(start_pos)
	resp = getter(url=gapi, alter_dict={
		"Referer": f"https://m.douban.com/movie/subject/{subject_id}",
		"X-Requested-With"  : "XMLHttpRequest",
		"Sec-Fetch-Dest"    : "empty",
		"Sec-Fetch-Mode"    : "navigate",
		"Sec-Fetch-Site"    : "same-origin",
		"User-Agent"        : f"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
		"Sec-Ch-Ua-Platform": '"Android"',
		"Sec-Ch-Ua"         : '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
		"Sec-Ch-Ua-mobile"  : '?1',
	})
	if resp is None:
		print('resp is None...')
		return
	elif 300 <= resp.status_code:
		print(start_pos, resp.status_code, 'soon we will terminate...')
		cease_flag.flip_flag()
		return
	short_comments_info = load_json_from_str(resp.text)
	if short_comments_info is None or not isinstance(short_comments_info, dict):
		print(
			'unable to convert resp.text into dict for python and further database operation...'
			f'\nthe resp.text is: {resp.text}'
		)
		cease_flag.flip_flag()
		return
	if len(short_comments_info['interests']) == 0:
		print(f'empty interests list at {start_pos}. soon we will terminate...')
		print(short_comments_info)
		cease_flag.flip_flag()
		return

	comments_ids = [_['id'] for _ in short_comments_info['interests']]
	comment_content = [_['comment'] for _ in short_comments_info['interests']]
	comment_timestamps = [_['create_time'] for _ in short_comments_info['interests']]
	vote_on_curr_comment = [_['vote_count'] for _ in short_comments_info['interests']]
	ip_addrs = [_['ip_location'] for _ in short_comments_info['interests']]
	ratings = [f"{_['rating']['star_count']}/{_['rating']['max']}" for _ in short_comments_info['interests']]
	database_fd.insert_multivals_to_tbl(
		'comments',
		('comment_id', 'votes', 'content', 'publish_date', 'ip_addr', 'rating'), [
			(comments_ids[i], v, comment_content[i], comment_timestamps[i], ip_addrs[i], ratings[i])
			for i, v in enumerate(vote_on_curr_comment)
		], ['comment_id']
	)
	database_fd.insert_multivals_to_tbl(
		'comment_on_movies', ('comment_id', 'movie_id'), [
			(v, subject_id) for v in comments_ids
		], ['comment_id', 'movie_id']
	)


def comment_evaluator(
	subject_id: int,
	cook: dict[str, str],
	worker_num: int=2,
	split_size: int=20
) -> None:
	resp = skim_one_movie_info(subject_id, cook)
	if resp is None:
		print('resp is None...')
		exit(1)
	elif resp.status_code != 200:
		print(resp.status_code)
		exit(1)

	main_page_info = BeautifulSoup(resp.text, 'html.parser')
	movie_name = main_page_info.find_all(name='h1')[0].text.split(' ')[0]
	database_fd.insert_to_tbl(
		'movies', { 'movie_id': subject_id, 'name': movie_name }
	)

	meta_task_count = main_page_info.find_all(name='ul', class_='fleft CommentTabs')
	if len(meta_task_count) != 1:
		print('invalid task_count')
		return
	task_count_str = meta_task_count[0].find_all(name='li', class_='is-active')
	task_count_res = re.findall(r'看过\(([0-9]+)\)', task_count_str[0].text)
	assert len(task_count_res) == 1
	# 不完全是
	# <div id="paginator" class="center">
	#   <a href="?start=0&amp;limit=20&amp;sort=new_score&amp;status=P&amp;percent_type=" data-page='first'><< 首页</a>
	#   <a href="?start=360&amp;limit=-20&amp;sort=new_score&amp;status=P&amp;percent_type=" data-page='prev'>< 前页</a>
	#   <span class="next" data-page='next'>后页 ></span>
	# </div>
	# 如果有后一页那就是a标签，否则就是span标签
	task_ranges = [_ for _ in range(0, int(task_count_res[0]), split_size)]
	with ThreadPoolExecutor(max_workers=worker_num) as per_mission:
		for choice in task_ranges:
			per_mission.submit(
				get_one_page, subject_id, cook, choice,
			)
	database_fd.commit()
	database_fd.close()


def json_evaluator(
	subject_id: int,
	cook: dict[str, str],
	worker_num: int = 2,
	split_size: int = 20
) -> None:
	gapi = f'https://m.douban.com/rexxar/api/v2/tv/{subject_id}?ck={cook["ck"]}&for_mobile=1'
	resp = getter(
		url=gapi,
		alter_dict={
			"Accept"            : "application/json",
			"Cookie"            : cook['cookie'],
			"Referer"           : f"https://m.douban.com/movie/subject/{subject_id}/",
			"Priority"          : "u=1, i",
			"X-Requested-With"  : "XMLHttpRequest",
			"Sec-Fetch-Dest"    : "empty",
			"Sec-Fetch-Mode"    : "navigate",
			"Sec-Fetch-Site"    : "same-origin",
			"User-Agent"        : f"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
			"Sec-Ch-Ua-Platform": '"Android"',
			"Sec-Ch-Ua"         : '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
			"Sec-Ch-Ua-mobile"  : '?1',
		}
	)
	if resp is None:
		print('resp is None...')
		exit(1)
	elif resp.status_code != 200:
		print(resp.status_code)
		exit(1)
	brief_info = load_json_from_str(resp.text)
	if brief_info is None:
		print('empty resp!', resp.text)
		exit(1)

	database_fd.renew_if_exist_else_insert(
		'movies', {'movie_id': subject_id},
		# 这里不知道name
		# 如果拿走interests留后缀?ck={cook["ck"]}&for_mobile=1在title还是可查的
		{
			'name': brief_info['title']
		}
	)

	task_ranges = [(_, split_size) for _ in range(120, int(brief_info['comment_count']), split_size)]
	last_item = task_ranges.pop()
	task_ranges.append((last_item[0], int(brief_info['comment_count'])%split_size))
	with ThreadPoolExecutor(max_workers=worker_num) as per_mission:
		for st_pos, comment_num in task_ranges:
			per_mission.submit(
				get_one_json, subject_id, cook, st_pos, comment_num
			)
	database_fd.commit()
	database_fd.close()

if __name__ == '__main__':
	# database_fd.query_items_in_tbl('movies', {'movie_id': 36516431}, limit_num=1)
	# # database_fd.recover_from_journal()
	# database_fd.insert_to_tbl('movies', {'movie_id': 0, 'name': 'test'})
	# database_fd.commit()
	# comment_evaluator(
	# 	36516431, PRIVATE_CONFIG['douban']['guest']
	# )
	json_evaluator(
		36516431, PRIVATE_CONFIG['douban']['guest']
	)
