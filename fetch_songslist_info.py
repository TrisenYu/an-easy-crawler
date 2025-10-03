#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/04 星期六 20:46:44
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.
"""
本程序只用于个人爬取网易云歌单的歌曲名等信息以用于留存备份。
使用方式：
	通过浏览器提供自身登录后得到的 cookie、歌单 id，然后运行获取。

会临时生成对应范围的临时文件供多线程临时写入。

命令行传参必要的参数：
	- login_dummy: 傀儡账号。其中 token 和 cookie 必要。
	- songslist_author: 目标歌单。list-id 必要，
						且目前 $(sys.platform)-backup-dir 也必要。

有关访问数据库、组织建表的逻辑仍在施工中🚧，仍不能保证前后向兼容
配置好以后至少保证能跑。
"""

import sys
import random
import threading
from queue import Queue
from typing import Optional
from io import TextIOWrapper
from functools import partial
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor

from rich.progress import Progress, TaskID

from misc_utils.file_operator import (
	write_in_given_mode,
	append_from_ro_file,
	seek_to_remove_file,
	dir2file
)
from misc_utils.wrappers.err_wrap import seize_err_if_any
from misc_utils.http_meths.man import getter, poster
from misc_utils.opts.json.conf_reader import (
	PRIVATE_CONFIG,
	load_json_from_str,
	deserialize_json_or_die
)
from misc_utils.logger import DEBUG_LOGGER
from misc_utils.header import HEADER
from misc_utils.ref_types import (
	SongsResp,
	SongDetails,
	PlaylistDetail,
	PlaylistTrackInfo
)
from misc_utils.time_aux import (
	unix_time,
	unix_ts_to_time,
	US_TIME_FORMAT, 
	unix_ms
)
from misc_utils.args_loader import PARSER
from misc_utils.str_aux import dic2json_str
from misc_utils.opts.db.sqlite import DBfd
from misc_utils.diff_calc import myers_diff_comparer, DiffOp
from crypto_aux.manual_deobfus import netease_encryptor

# TODO: 如果线程执行过程中遇到任何异常，直接通知其它线程结束，管理线程的父进程等待并妥善检查后再退出

_args = PARSER.parse_args()
del PARSER

_HTTPS: str = 'https://'
host: str = "music.163.com"
interface_prefix: str = f'{_HTTPS}interface.{host}'
# just GET
SONGSLIST_API: str = '/api/v6/playlist/detail?id='
SONG_SKIM_API: str = '/api/song/detail?ids='
# POST it
CONTENT_OF_SONG_PAPI: str = "/weapi/rep/ugc/song/get?csrf_token="
# useful urls
target_songslist_url: str = f'{interface_prefix}{SONGSLIST_API}'
target_songs_url: str = f"{interface_prefix}{SONG_SKIM_API}"
song_sniper_url: str = f'{_HTTPS}{host}{CONTENT_OF_SONG_PAPI}'
# concurrency control
_reveal_queue = Queue(maxsize=_args.threadpool_size)
_reveal_sema = threading.Semaphore(
	# 单核 CPU 还有人用吗?
	min(cpu_count(), _args.threadpool_size//2)
)
# database handle
database_fd: Optional[DBfd] = DBfd(_args.database_path)


def song_sniper(sid: int, tok: str) -> any:
	"""
	返回一个比较庞大的结构
	"""
	global host, song_sniper_url
	origin_payload = dic2json_str({
		"songId": sid, "csrf_token": tok
	})
	assert 'Cookie' in HEADER and			\
			len(HEADER['Cookie']) != 0 and	\
			tok in HEADER['Cookie']
	changed_domains = {
		"Accept"			: "*/*",
		"Referer"			: f"{_HTTPS}{host}/reveal/song?songId={sid}&type=2",
		"Content-Type"		: "application/x-www-form-urlencoded",
		"Cookie"			: HEADER['Cookie'],
		"Host"				: host,
		"Origin"			: _HTTPS + host,
		"Priority"			: "u=1, i",
		"Sec-Fetch-Dest"	: "iframe",
		"TE"				: "trailers",
		"X-Requested-With"	: "XMLHttpRequest",
	}
	encrypted_payload, _ = netease_encryptor(origin_payload)
	ret = poster(
		url=song_sniper_url+tok,
		payload=encrypted_payload,
		alter_map=changed_domains
	)
	return ret


def _exam_hidden_sinfo(sid: int, tok: str) -> list:
	global _reveal_sema
	while True:
		_reveal_sema.acquire()
		threading.Event().wait(timeout=random.uniform(3, 6))
		# 因为数量问题这里不太好完整地收集下来，
		# 此外需要注意并发请求的频率和规模
		song_obj = song_sniper(sid, tok)
		if song_obj is None or len(song_obj.text) == 0:
			threading.Event().wait(timeout=random.uniform(3, 6))
			_reveal_sema.release()
			continue
		elif song_obj.status_code != 200:
			return [None, '', '', '', '', '']
		tmp = load_json_from_str(song_obj.text)
		if tmp is None or 'data' not in tmp:
			return [None, '', '', '', '', '']

		tdat = tmp['data']
		if 'playUrl' not in tdat:
			flag = None
		else:
			# TODO: 还有种情况是有，但 vip 才能听
			# 但是还没从混淆js看出什么为什么它懂得无版权的所以然来，这里先鸽
			flag = tdat['playUrl'] is not None
		_jud = lambda x: x not in tdat or tdat[x] is None
		_muxer = lambda x: [] if _jud(x) else tdat[x]
		_texer = lambda x: x if isinstance(x, str) else ''
		lyric = _texer(_muxer('lyricContent'))
		trans = _texer(_muxer('transLyricContent'))
		composers = ', '.join([_['artistName'] for _ in _muxer('composeArtists')])
		arrangers = ', '.join([_['artistName'] for _ in _muxer('arrangeArtists')])
		lyricists = ', '.join([_['artistName'] for _ in _muxer('lyricArtists')])
		return [flag, lyric, trans, composers, arrangers, lyricists]


@seize_err_if_any()
def process_song_info_in_chunk(
	integrated_conf: dict,
	songs_detail: list[SongDetails],
	play_list: list[PlaylistTrackInfo]
) -> None:
	global _reveal_sema, _reveal_queue, database_fd

	st_pos = integrated_conf['st_pos']
	soid = integrated_conf['soid']
	bar_id = integrated_conf['taskID']
	for idx, a_song in enumerate(songs_detail):
		
		duration = a_song['duration']
		mins, ms = duration // 60_000, duration % 1_000
		sec = (duration - mins * 60_000 - ms) % 1_000
		final_dura = f'{mins}:{sec:02d}.{ms:03d}'
		del mins, sec, ms, duration

		song_id = a_song['id']
		# TODO: 如果数据库里能找而且信息都是全的，就没必要去再次请求，想办法保证这一点并给个优化
		attacher = _exam_hidden_sinfo(song_id, integrated_conf['token'])
		copyleft = attacher[0]
		_lyc, _trl = attacher[1], attacher[2]
		arrangers, composers = attacher[3], attacher[4]
		lyricists = attacher[5]
		del attacher
		_reveal_sema.release()

		# 一些内容可以直接传给数据库来做
		album_publish_time: int = a_song['album']['publishTime']
		database_fd.insert_if_not_exist_else_renew(
			'albums', {'album_id': a_song['album']['id'] }, { 
				"company": a_song['album']['company'],
				'name': a_song['album']['name'],
				"publish_time": unix_ts_to_time(album_publish_time/1000)
			}
		)
		# 有些歌的歌词和翻译可能在后面会加入进来
		# 最好还是先插入然后再更新这两个域
		database_fd.update_item_in_tbl(
			"songs", { "song_id": song_id }, {
				'tr_pos': a_song['position'], 
				'album_id': a_song['album']['id'],
				"name": a_song['name'],
				'duration': final_dura,
				"lyrics": _lyc.replace('\n', '\\n'),
				"translatext": _trl.replace('\n', '\\n'),
				"vocals": ', '.join([v['name'] for v in a_song['artists']]), 
				"arrangers": arrangers, "lyricists": lyricists, 
				"composers": composers, "fetchable": copyleft, 
				"subtitle": ', '.join(a_song["alias"])
		})
		by_whom = play_list[idx]['uid']
		status, _ = database_fd.is_item_in_tbl(
			('user_id',), (by_whom,), 'users'
		)
		if not status:
			database_fd.insert_to_tbl(
				'users', { 'user_id': by_whom }
			)
		_tmp_ubid = database_fd.insert_if_not_exist_else_renew(
			'users_behaviors', { 'soid': soid, 'user_id': by_whom }
		)
		if _tmp_ubid is not None:
			ubid = _tmp_ubid
		else:
			status, row = database_fd.is_item_in_tbl(
				('soid', 'user_id'), (soid, by_whom),
				'users_behaviors'
			)
			# 没有出现过的项目，这个时候才应该要插入
			ubid = row["ubid"] \
				if status else database_fd.insert_if_not_exist_else_renew(
				'users_behaviors', { 'soid': soid, 'user_id': by_whom }
			)
			del status, row
		database_fd.update_item_in_tbl(
			'songs_status_in_songslists',
			{ 'song_id': song_id, 'ubid': ubid },
			{ "op_time": unix_ts_to_time(play_list[idx]['at']/1_000, US_TIME_FORMAT) }
		)
		_reveal_queue.put((bar_id, 0.6))


@seize_err_if_any()
def query_song_detail_in_range(
	bar_id: TaskID,
	integrated_conf: dict,
	l: int, r: int,
	play_list: list[PlaylistTrackInfo]
) -> None:
	"""
	{
		"res-song-get": {
			type: "GET",
			url: "/api/song/detail",
			format: function(m1x, e1x) {
				if (!!m1x.songs && m1x.songs.length > 0)
					m1x.song = m1x.songs[0];
				else
					m1x.song = bqK0x;
				delete m1x.songs;
				return xr5w(m1x, e1x)
			},
			filter: function(e1x) {
				e1x.data.ids = "[" + e1x.data.id + "]"
			}
		}
	}
	:return: None
	"""
	global target_songs_url, _reveal_sema, _reveal_queue
	# 随机等 1 ～ 10 秒
	threading.Event().wait(timeout=random.randint(1, 10))
	res = getter(
		url=f'{target_songs_url}{[_s["id"] for _s in play_list]}',
		err_info=f'Catch an Exception in range [{l}, {r}): '
	)
	_check = lambda x: x is None or len(x.text) == 0 or x.status_code != 200
	songs_detail: Optional[SongsResp] = \
			None if _check(res) else	\
			load_json_from_str(res.text)
	del res

	nxt_merger = {
		'token': integrated_conf['token'],
		'taskID': bar_id,
		'st_pos': l,
		'soid': integrated_conf['soid'],
	}
	process_song_info_in_chunk(nxt_merger, songs_detail['songs'], play_list)
	_reveal_queue.put((bar_id, 0.4*(r-l)))
	return


def check_progress_state(prog_man: Progress) -> None:
	"""
	终端进度条显示函数
	"""
	global _reveal_queue
	while not prog_man.finished:
		req: tuple[TaskID, int] = _reveal_queue.get()
		prog_man.update(req[0], advance=req[1])


@seize_err_if_any()
def songs_tasks_distributor(
	integrated_conf: dict,
	task_list: list[PlaylistTrackInfo],
	fn=query_song_detail_in_range
) -> None:
	"""
	返回并发执行前，计算得到的任务列表。
	"""
	global _reveal_queue
	workers = integrated_conf['worker_num']
	split_size = integrated_conf['split_size']

	lena = len(task_list)
	other, reminder = lena // split_size, lena % split_size
	tasks_queue = [(_*split_size, (_+1)*split_size) for _ in range(0, other)]
	tasks_queue.append((other*split_size, (other*split_size)+reminder))

	# 缩进多了就成了横躺着的shxt
	with Progress() as progress_man:
		_prog_rec = []
		for _ in range(len(tasks_queue)):
			tup = tasks_queue[_]
			_tmp = progress_man.add_task(
				# 这辈子把十万首歌整理到一个常听的歌单里很难
				# 特别是定期的观测会让这种数量级的数据爆炸式增长
				f"Range:[{tup[0]:>4d},{tup[1]:>4d})",
				total=tup[1]-tup[0]
			)
			_prog_rec.append(_tmp)
		# 由于加了进度条，线程池需要多扩一个给进度条线程
		nxt_merger = {
			'token': integrated_conf['token'],
			'soid': integrated_conf['soid'],
		}
		with ThreadPoolExecutor(max_workers=workers+1) as per_mission:
			per_mission.submit(check_progress_state, progress_man)
			for i, choice in enumerate(tasks_queue):
				per_mission.submit(
					fn, # 要调用的函数
					_prog_rec[i], nxt_merger,
					choice[0], choice[1],
					task_list[choice[0]:choice[1]]
				)
			del task_list


@seize_err_if_any()
def songslist_info_gen(
	tok: str,
	workersnum: int,
	crawl_conf: dict,
	split_size: int=100
) -> None:
	"""
	分析：core_52f85c5f5153a7880e60155739395661.js^[1]下
	第 69 行匿名函数 (function()) 里有

	{
		"res-playlist-get": {
			type: "GET",
			url: "/api/v6/playlist/detail",
			format: function(m1x, e1x) {
				var res = j1x.bsN0x(m1x);
				res.playlist = res.result;
				delete res.result;
				return xr5w(res, e1x)
			}
		}
	}

	只需传 id 列表就可以获取到列表内的所有歌曲。
	列表长度不能定得太大，否则后果自负

	- [1]: 2025/02/08: core_70d0eefb570184a2b62021346460be95.js，
	       反正理解为 core.js。
	"""
	global interface_prefix, target_songslist_url, database_fd

	response =getter(
		url=f"{target_songslist_url}{crawl_conf['list-id']}",
		err_info='fatal error while fetching songslist: '
	)

	if response is None:
		DEBUG_LOGGER.error('unable to fetch any songslist info')
		return
	elif response.status_code != 200:
		DEBUG_LOGGER.error(response.status_code, response.text)
		exit(1)

	serializer = response.text
	tmp: PlaylistDetail = deserialize_json_or_die(serializer, 'playlist')
	curr_time = unix_ms()
	del serializer, response

	songslist_updatetime = unix_ts_to_time(tmp["updateTime"]/1_000)
	songslist_birthday = unix_ts_to_time(tmp["createTime"]/1_000)
	slid = tmp["id"] # songslist_id
	track_cnt, share_cnt = tmp["trackCount"], tmp["shareCount"]
	likers_num, ref_hits = tmp["subscribedCount"], tmp["playCount"]
	description = tmp["description"]
	songslist_title = tmp["name"]

	creator_info = tmp["creator"]
	creator_id = creator_info["userId"]
	creator_name = creator_info["nickname"]
	creator_brief = creator_info['signature'].replace('\n', '\\n')
	del creator_info
	playlist = tmp['trackIds']
	del tmp
	print(f'For songslist-id {slid}')
	st_time = unix_time()
	# DB insert operations
	database_fd.insert_if_not_exist_else_renew(
		'users',
		{ 'user_id': creator_id },
		{ 'name': creator_name, 'brief': creator_brief }
	)
	database_fd.insert_if_not_exist_else_renew(
		'songslists',
		{ 'songslist_id': slid, 'user_id': creator_id },
		{ 'birthday': songslist_birthday }
	)
	soid = database_fd.insert_to_tbl(
		'songslists_observation', {
		'songslist_id': slid, 'user_id': creator_id, 
		'observation_time': unix_ts_to_time(curr_time/1000)
	})
	assert soid is not None
	def _songslist_attr_tbl_init(name: str, val: int | str) -> None:
		database_fd.insert_if_not_exist_else_renew(name+'_rec', { 'soid': soid }, { name: val })
	_songslist_attr_tbl_init('ref_hits', ref_hits)
	_songslist_attr_tbl_init('likers', likers_num)
	_songslist_attr_tbl_init('share_cnt', share_cnt)
	_songslist_attr_tbl_init('description', description)
	_songslist_attr_tbl_init('titles', songslist_title)
	ubid = database_fd.query_items_in_tbl(
		'users_behaviors',
		{ 'soid': soid, 'user_id': creator_id },
		'ubid', True
	)
	if ubid is None or len(ubid) == 0:
		ubid = database_fd.insert_to_tbl(
			'users_behaviors', 
			{ 'soid': soid, 'user_id': creator_id }
		)
	curr_idxs = [_["id"] for _ in playlist]
	sql_records = database_fd.query_items_in_tbl(
		"curr_songslists",
		{ "songslist_id": slid },
		'pos_val'
	)
	songslist_ids = [_["song_id"] for _ in sql_records] if sql_records is not None else []
	# 先查是否已有歌单的维护记录
	# 如果有直接拿来像git diff一样比较差异
	# 需要看的是上一次的内容？
	# 但是上一次内容是差异，如果要看，每次就都需要在这里算第一次看积累到现在的差异
	# 不妨将这个内容单独记录为位置信息表
	# 每次只需要联合查询，这样就不用折腾来折腾去了，不单独记录
	len_ret = len(sql_records) if sql_records is not None else -1
	del sql_records, creator_id, creator_name, creator_brief
	del description, songslist_title, share_cnt, likers_num, ref_hits
	differs = myers_diff_comparer(songslist_ids, curr_idxs)
	songslist_ids = []
	for idx, edit_item in enumerate(differs):
		if edit_item[0] == DiffOp.keep:
			songslist_ids.append(edit_item[1][0])
			continue
		database_fd.insert_if_not_exist_else_renew('songs', { 'song_id': edit_item[1][0] })
		database_fd.insert_if_not_exist_else_renew(
			'songs_status_in_songslists', {
				'song_id': edit_item[1][0], 
				'ubid': ubid
			}, { f'{str(edit_item[0]).split(".")[-1]}_pos': edit_item[1][1]+1 }
		)
		if edit_item[0] == DiffOp.delete:
			continue
		songslist_ids.append(edit_item[1][0])
	del differs, curr_idxs
	for idx, item in enumerate(songslist_ids):
		if idx < len_ret:
			database_fd.update_item_in_tbl(
				"curr_songslists",
				{ "pos_val": idx+1, "songslist_id": slid }, 
				{ 'song_id': item }
			)
		else:
			database_fd.insert_to_tbl(
				'curr_songslists', 
				{ 'pos_val': idx+1, "songslist_id": slid, 'song_id': item }
			)
	for idx in range(len(songslist_ids), len_ret):
		database_fd.remove_item_in_tbl(
			'curr_songslists',
			{ 'pos_val': idx+1, 'songslist_id': slid }
		)
	ed_time = unix_time()
	# 已经有的不用再去请，只请求没有备份过的
	rows = database_fd.query_null_items_in_tbl(
		'songs_status_in_songslists', 
		{ 'ubid': ubid },
		['delete_pos']
	)
	tmp = set([_['song_id'] for _ in rows ]) if rows is not None else set()
	adjust_playlist = []
	del rows, ubid, songslist_ids
	# 除非是什么也没有才完全获取
	for p in playlist:
		if p['id'] not in tmp:
			continue
		adjust_playlist.append(p)
	del playlist

	integrated_conf = {
		'token': tok,
		'split_size': split_size,
		'soid': soid,
		'worker_num': workersnum
	}

	print(f'Time-consumption-on-setup-Tables: {ed_time - st_time}s. Begin Tasks...')
	songs_tasks_distributor(integrated_conf, adjust_playlist)


if __name__ == '__main__':
	spyon: str = _args.songslist_author
	dummy: str = _args.login_dummy
	workload = _args.threadpool_size
	assert 1 <= workload  # 不设上限，但至少要有。
	del _args

	dummy_conf: dict[str, str] = PRIVATE_CONFIG[dummy]
	victim_conf: dict[str, str] = PRIVATE_CONFIG[spyon]

	csrf_token, _cookie = dummy_conf["csrf_token"], dummy_conf["cookie"]
	del dummy_conf
	assert len(csrf_token) == 32 and f'__csrf={csrf_token}' in _cookie

	HEADER["Cookie"] = _cookie
	HEADER["Host"] = host
	HEADER["Referer"] = f"{_HTTPS}{host}/"
	HEADER["Connection"] = "keep-alive"
	songslist_info_gen(csrf_token, workload, victim_conf)
