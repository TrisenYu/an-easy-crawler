#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/26 星期日 21:56:22
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
# 
# TODO: 如果线程执行过程中遇到任何异常，直接通知其它线程结束
#       管理线程的父进程等待并妥善检查后再退出
#       另外在测试过程中发现ctrl+C不好使，可能是进度条导致的，需要换用终止信号的机制
#       还有数据库的回滚，这里一执行出错就必须把sqlite临时生成的journal日志给自动删了
# TODO: 如果改一下数据库表段的定义，那这里一堆函数不就炸了吗？另外能不能用一个异步的任务队列？
# TODO: 考虑整个项目的入口怎么写，这个文件最好移到multtp.easynet存放
# TODO: 如果没有先进的IDE，人怎么读写第三方提供的代码？
# NOTE<开放性问题>: 有冇图灵机能直接从机器码/混淆文本中读出这些api？
"""
本程序仅只用于个人对云服务器**道德**地爬取歌单的歌曲名等信息以用于本地留存备份。
使用方式：
	通过浏览器提供自身登录后得到的 cookie、歌单 id，然后运行获取。

会临时生成对应范围的临时文件供多线程临时写入。

命令行传参必要的参数：
	- login_dummy: 傀儡账号。其中 token 和 cookie 必要。
	- songslist_author: 目标歌单。list-id 必要

每次提交不保证前后向兼容，正确配置后至少保证能跑。
"""

import random
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from pathlib import Path
from queue import Queue
from typing import Optional

from curl_cffi import Response
from loguru import logger
from rich.progress import Progress, TaskID

from configs.args_loader import PARSER
from crypto_aux.manual_deobfus import netease_encryptor
from datatypes import *
from datatypes.easynet.sqlite_types import netease_db_tbl_refs
from misc_utils import *
from multtp import *

logger.remove()
logger.add(
	GLOB_MAIN_LOG_PATH,
	level='DEBUG',
	colorize=True,
	format=GLOB_LOG_FORMAT,
	rotation="16MB",
	compression='zip',
	encoding='utf-8'
)

_args = PARSER.parse_args()
del PARSER

_HTTPS: str = 'https://'
MSP: str = "music.163.com"  # music service provider
# TODO: APIs shall access from configuration
INTERFACE_PREFIX: str = f'{_HTTPS}interface.{MSP}'
# just GET
SONGSLIST_API: str = '/api/v6/playlist/detail?id='
SONG_SKIM_API: str = '/api/song/detail?ids='
# POST it
CONTENT_OF_SONG_PAPI: str = "/weapi/rep/ugc/song/get?csrf_token="
# useful urls
TARGET_SONGSLIST_URL: str = INTERFACE_PREFIX + SONGSLIST_API
TARGET_SONGS_URL: str = INTERFACE_PREFIX + SONG_SKIM_API
SONG_SNIPER_URL: str = _HTTPS + MSP + CONTENT_OF_SONG_PAPI
## 并发控制
_reveal_queue = Queue(maxsize=_args.threadpool_size)
_reveal_sema = threading.Semaphore(
	# 单核 CPU 还有人用吗?
	min(max(cpu_count() // 2, 1), _args.threadpool_size // 2)
)
# database handle
### 看起来比较糟糕，里面是在用动态类型声明出来的表
## 后续将继续进一步分离与数据库交互的定义，只要发起顺序不影响，
## 就将代指关系抽象为任务，将其送到并发队列里让数据库一个一个执行
database_fd: Optional[DBfd] = DBfd(_args.database_path, netease_db_tbl_refs)
assert database_fd is not None


def song_sniper(sid: int, cooken: dict[str, str]) -> Optional[Response]:
	"""
	提供song_id和token，对单曲精准嗅探
	如果正常工作，返回结构比较斯蒂庞克的字典
	"""
	global MSP, SONG_SNIPER_URL
	origin_payload = dic2ease_json_str({
		"songId": sid, "csrf_token": cooken["token"]
	})
	host_name = _HTTPS + MSP
	return poster(
		url=SONG_SNIPER_URL + cooken["token"],
		payload=netease_encryptor(origin_payload)[0],
		alter_dict={
			"Accept"          : "*/*",
			"Referer"         : host_name + f"/reveal/song?songId={sid}&type=2",
			"Content-Type"    : "application/x-www-form-urlencoded",
			"Cookie"          : cooken['cookie'],
			"Host"            : MSP,
			"Origin"          : host_name,
			"Priority"        : "u=1, i",
			"Sec-Fetch-Dest"  : "iframe",
			"TE"              : "trailers",
			"X-Requested-With": "XMLHttpRequest",
		}
	)


def _extract_hidden_sinfo(sid: int, cooken: dict[str, str]) -> list:
	"""
	从云服务器获取单曲的附加信息，将其写入数据库中
	如果配置有本地保存需求，则视存在情况而尝试获取
	"""
	global _reveal_sema, _args, database_fd
	ret = [None, '', '', '', '', '']
	texer = lambda x: x if isinstance(x, str) else ''

	_reveal_sema.acquire()
	threading.Event().wait(timeout=random.uniform(3, 6))
	# 需要注意并发请求的频率和规模
	song_obj = song_sniper(sid, cooken)
	_reveal_sema.release()


	if song_obj is None or len(song_obj.text) == 0 or song_obj.status_code != 200:
		return ret
	tmp = load_json_from_str(song_obj.text)
	if tmp is None or 'data' not in tmp:
		logger.warning(
			f'No data field was found in response json object when fetching for {sid}'
		)
		return ret

	tdat = tmp['data']
	del tmp, song_obj
	# TODO: 还有种情况是有但 vip 才能听
	#       但是还没从混淆js看出什么为什么它懂得无版权的所以然来，这里先鸽
	# 		另外底下几行的校验有点太丑了
	flag = None if tdat is None or 'playUrl' not in tdat else (tdat['playUrl'] is not None)
	tr_url = tdat['playUrl'] if flag is not None and flag else ''
	_jud = lambda x: tdat is None or x not in tdat or tdat[x] is None
	_muxer = lambda x: [] if _jud(x) else tdat[x]
	texpecter = lambda x: texer(_muxer(x))
	_name_conc = lambda x: ', '.join([_['artistName'] for _ in _muxer(x)])
	ret = [
		int(flag) if isinstance(flag, bool) else None,
		texpecter('lyricContent'), texpecter('transLyricContent'),
		_name_conc('composeArtists'), _name_conc('arrangeArtists'),
		_name_conc('lyricArtists')
	]
	tmp = texer(_muxer('songName')) + '-' + str(sid)
	
	local_tr_path = str(Path(_args.tracks_path).joinpath(streplacer(tmp)+'.mp3').absolute())
	if tmp != '-' + str(sid):
		database_fd.update_item_in_tbl(
			'songs', {'song_id': sid},
			{'download_path': local_tr_path }
		)
	if len(tr_url) <= 0 or not _args.need_download or is_path_ok(local_tr_path):
		# 如果没有track_url、不需要下载或已经有过音轨的，直接返回
		return ret

	_reveal_sema.acquire()
	# 有些音轨大小很大，这里爬虫必须要把时间尽可能放大
	threading.Event().wait(timeout=random.uniform(6, 18))
	snd_tr_wrp = getter(url=tr_url, no_header=True)
	_reveal_sema.release()

	if snd_tr_wrp is None or snd_tr_wrp.status_code != 200:
		return ret
	snd_tr = snd_tr_wrp.content
	del snd_tr_wrp
	write_in_given_mode(
		path=local_tr_path,
		payload=snd_tr, mode='wb'
	)
	del snd_tr
	return ret


@seize_err_if_any()
def _song_info_to_db(
	soid: int,
	a_song: SongDetails,
	tr_info: PlaylistTrackInfo,
	final_dura: str,
	attacher: list
) -> None:
	"""
	soid: 歌单在数据库(目前为sqlite)内的观测ID
	a_song: 上一阶段获得的歌曲详情json
	tr_info: 在歌单内的歌曲信息
	final_dura: 最终计算出的歌曲时长
	attacher: [play_url_is_available, lyric, translation, composer, arranger, lyricist]
	"""
	global _reveal_sema, _args, database_fd
	# TODO: 后续做分布式同步的话cover域就不要同步，但要能基于这个域来传实际的cover
	covers_path = Path(_args.covers_path)
	curr_cover_name = streplacer(
		a_song['album']['name'] + '-' + str(a_song['album']['id'])
	)
	local_cv_path = str(covers_path / curr_cover_name)
	if _args.need_download and a_song['album']['picUrl'] is not None and \
		len(list(covers_path.rglob(f'{curr_cover_name}.'))) == 0:

		_reveal_sema.acquire()
		threading.Event().wait(timeout=random.uniform(3, 12))
		_wrapper = getter(url=a_song['album']['picUrl'], no_header=True)
		_reveal_sema.release()
	else:
		_wrapper = None
	database_fd.renew_if_exist_else_insert(
		'albums', {'album_id': a_song['album']['id']}, {
			"company"     : a_song['album']['company'],
			'name'        : a_song['album']['name'],
			"publish_time": unix_ts_to_time(a_song['album']['publishTime'] / 1000)
		}
	)

	if _wrapper is None or _wrapper.status_code != 200:
		pic_bytes = b''
		local_cv_path = local_cv_path[:-4] + '.null'
		logger.warning(f'unable to fetch {soid}, url: {a_song["album"]["picUrl"]}.')
	else:
		pic_bytes = _wrapper.content
		_header = pic_bytes[:8].hex().lower() if len(pic_bytes) >= 8 else pic_bytes.hex()
		if _header == 'ffd8ffe000104a46':
			local_cv_path += '.jpg'
		elif _header == '89504e470d0a1a0a':
			local_cv_path += '.png'
		else:
			logger.warning(f'unknown file preamble:`{pic_bytes}` was found for {soid}')
			local_cv_path += '.unk'

	if _args.need_download and not is_path_ok(local_cv_path):
		# TODO: 这里只是简单以路径名来判断文件是否存在
		#       如果文件相比云上获取的文件不同，是不是要验证哈希？留本地还是留云端传过来的？
		#       如何判断和你说话的那个人是你认识的那个人
		write_in_given_mode(
			local_cv_path,
			payload=pic_bytes,
			mode='wb'
		)
	del _wrapper, pic_bytes
	database_fd.update_item_in_tbl(
		'albums', {'album_id': a_song['album']['id']},
		{"cover": local_cv_path}
	)
	# 这两个域出现在json就有点太割裂了
	_pos, _num = a_song['position'], a_song['no']
	assert isinstance(_pos, int) and isinstance(_num, int)
	if _pos == _num:
		position = 1 if _num == 0 else _num
	elif _num > _pos:
		position = _num
	else:
		position = _pos
	del _pos, _num
	database_fd.update_item_in_tbl(
		"songs", {"song_id": a_song['id']}, {
			'tr_pos'     : position,
			'album_id'   : a_song['album']['id'],
			"name"       : a_song['name'],
			'duration'   : final_dura,
			"fetchable"  : attacher[0],
			"lyrics"     : attacher[1].replace('\n', '\\n'),
			"translatext": attacher[2].replace('\n', '\\n'),
			"arrangers"  : attacher[3],
			"composers"  : attacher[4],
			"lyricists"  : attacher[5],
			"vocals"     : ', '.join([v['name'] for v in a_song['artists']]),
			"subtitle"   : ', '.join(a_song['alias']),
		}
	)
	by_whom = tr_info['uid']
	database_fd.renew_if_exist_else_insert(
		'users', {'user_id': by_whom}
	)
	_ubid = database_fd.renew_if_exist_else_insert(
		'user_behaviors', {'soid': soid, 'user_id': by_whom}
	)
	if isinstance(_ubid, int):
		ubid = _ubid
		logger.debug(f'apply for a new ubid: {ubid}')
	elif _ubid is not None:
		assert isinstance(_ubid, list) and len(_ubid) == 1
		ubid: int = _ubid[0]['ubid']
		logger.debug(f'ubid is not None: {ubid}')
	else:
		raise ValueError('unable to properly generate ubid!')
	database_fd.update_item_in_tbl(
		'songs_status_in_songslists',
		{'song_id': a_song['id'], 'ubid': ubid},
		{"op_time": unix_ts_to_time(tr_info['at'] / 1_000.0, US_TIME_FORMAT)}
	)


@seize_err_if_any()
def process_song_info_in_chunk(
	integrated_conf: dict,
	songs_detail: list[SongDetails],
	play_list: list[PlaylistTrackInfo]
) -> None:
	global _reveal_queue
	soid = integrated_conf['soid']
	for idx, a_song in enumerate(songs_detail):
		duration = a_song['duration']
		mins, ms = duration // 60_000, duration % 1_000
		sec = (duration - mins * 60_000 - ms) // 1_000
		final_dura = f'{mins}:{sec:02d}.{ms:03d}'
		del mins, sec, ms, duration

		attacher = _extract_hidden_sinfo(a_song['id'], integrated_conf)
		_song_info_to_db(soid, a_song, play_list[idx], final_dura, attacher)
		del attacher
		_reveal_queue.put((integrated_conf['taskID'], 1))


@seize_err_if_any()
def query_song_detail_in_range(
	bar_id: TaskID,
	integrated_conf: dict,
	l: int, r: int,
	play_list: list[PlaylistTrackInfo]
) -> None:
	"""
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
	"""
	global TARGET_SONGS_URL, _reveal_sema, _reveal_queue, MSP, _HTTPS
	# 随机等 5~9 秒
	threading.Event().wait(timeout=random.uniform(5, 9))
	res = getter(
		url=f'{TARGET_SONGS_URL}{[_s["id"] for _s in play_list]}',
		err_info=f'Catch an Exception in range [{l}, {r}): ',
		alter_dict={
			'Cookie'    : integrated_conf['cookie'],
			'Host'      : MSP,
			'Referer'   : _HTTPS + MSP + '/',
			'Connection': 'keep-alive'
		}
	)
	_check = lambda x: x is None or len(x.text) == 0 or x.status_code != 200
	songs_detail: Optional[SongsResp] = None if _check(res) else \
		load_json_from_str(res.text)
	# logger.debug(f'{songs_detail}')
	if songs_detail is None:
		logger.warning(f'songs_detail is None at {l} - {r}, the res.text is: {res.text}')
		return
	del res
	process_song_info_in_chunk(
		{
			'cookie': integrated_conf['cookie'],
			'token' : integrated_conf['token'],
			'soid'  : integrated_conf['soid'],
			'taskID': bar_id
		}, songs_detail['songs'], play_list
	)


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
	if lena == 0:
		return
	other, reminder = lena // split_size, lena % split_size
	tasks_queue = [(_ * split_size, (_ + 1) * split_size) for _ in range(0, other)]
	tasks_queue.append((other * split_size, (other * split_size) + reminder))

	# NOTE: 缩进多了就成了横躺着的shxt
	with Progress() as progress_man:
		prog_rec = [
			progress_man.add_task(
				f"Range:[{lp:>4d},{rp:>4d})",
				total=rp - lp
			)
			for lp, rp in tasks_queue
		]
		nxt_dict = {
			'cookie': integrated_conf['cookie'],
			'token' : integrated_conf['token'],
			'soid'  : integrated_conf['soid'],
		}
		# 由于加了进度条，线程池需要多扩一个给进度条线程
		with ThreadPoolExecutor(max_workers=workers + 1) as per_mission:
			per_mission.submit(check_progress_state, progress_man)
			for i, choice in enumerate(tasks_queue):
				per_mission.submit(
					fn,  # 要调用的函数
					prog_rec[i], nxt_dict,
					choice[0], choice[1],
					task_list[choice[0]:choice[1]]
				)
			del task_list


# TODO: 如果爬取失败，必须要有一个判断的机制来确定要不要commit数据库，不然就commit了不完整的数据


@seize_err_if_any()
def _renew_songslist_status(
	soid: int,
	creator_id: int,
	updatime: str,
	differs: list
) -> tuple[list, int]:
	global database_fd
	_ubid = database_fd.query_items_in_tbl(
		'user_behaviors',
		{'soid': soid, 'user_id': creator_id},
		{'ubid': 'DESC'}, ['ubid'],
		limit_num=1
	)
	if _ubid is None or (isinstance(_ubid, list) and len(_ubid) == 0):
		ubid = database_fd.insert_to_tbl(
			'user_behaviors',
			{'soid': soid, 'user_id': creator_id}
		)
	else:
		assert isinstance(_ubid, list) and len(_ubid) == 1
		logger.debug(str(type(_ubid)) + str(len(_ubid)) + str(_ubid[0]))
		ubid = _ubid[0]['ubid']

	retlist, upd_songs, songstatus = [], [], []
	for idx, edit_item in enumerate(differs):
		if edit_item[0] == DiffOp.keep:
			retlist.append(edit_item[1][0])
			continue
		song_id, pos = edit_item[1][0], edit_item[1][1] + 1
		upd_songs.append((song_id,))
		songstatus.append(
			# song_id, attr, pos
			(song_id, f'{str(edit_item[0]).split(".")[-1]}', pos)
		)
		if edit_item[0] == DiffOp.delete:
			continue
		retlist.append(song_id)

	merge_dict = {}
	for song_id, attr, pos in songstatus:
		if song_id not in merge_dict:
			merge_dict[song_id] = {'delete_pos': None, 'insert_pos': None}
		merge_dict[song_id][f'{attr}_pos'] = pos
	songstatus = [
		(ubid, *(song_id, val['delete_pos'], val['insert_pos']), updatime)
		for song_id, val in merge_dict.items()
	]
	del merge_dict

	database_fd.insert_multivals_to_tbl(
		'songs', ('song_id',),
		upd_songs, ['song_id']
	)
	database_fd.insert_multivals_to_tbl(
		'songs_status_in_songslists',
		('ubid', 'song_id', 'delete_pos', 'insert_pos', 'op_time'),
		songstatus, ['song_id', 'ubid']
	)
	del upd_songs, songstatus, differs
	return retlist, ubid


@seize_err_if_any()
def _update_current_songslist(
	slid: int,
	songslist_ids: list[int],
	len_ret: int  # 数据库内的长度
) -> None:
	"""
	根据给定的歌单id和歌单内变动的歌曲id列表来更新整个歌单内容
	"""
	global database_fd
	database_fd.insert_multivals_to_tbl(
		'curr_songslists', ('pos_val', "songslist_id", 'song_id'),
		[(idx + 1, slid, item) for idx, item in enumerate(songslist_ids)],
		['songslist_id', 'pos_val']
	)
	logger.debug(f'{len(songslist_ids)}')
	for idx in range(len(songslist_ids), len_ret):
		database_fd.remove_item_in_tbl(
			'curr_songslists',
			{'pos_val': idx + 1, 'songslist_id': slid}
		)


@die_if_err()
def _main_thread_db_ops(
	inpict: PlaylistDetail
) -> tuple[int, list[PlaylistTrackInfo]]:
	"""
	:param inpict: input_dict
	解释起来比较复杂，自己看代码吧
	"""
	global database_fd

	creator_info = inpict['creator']
	creator_id = creator_info['userId']
	slid = inpict['id']
	print(f'For songslist {slid}')
	st_time = unix_time()
	database_fd.renew_if_exist_else_insert(
		'users',
		{'user_id': creator_id}, {
			'name' : creator_info['nickname'],
			'brief': creator_info['signature'].replace('\n', '\\n')
		}
	)
	del creator_info
	database_fd.renew_if_exist_else_insert(
		'songslists',
		{'songslist_id': slid, 'creator_id': creator_id},
		{'birthday': unix_ts_to_time(inpict['createTime'] / 1_000.0)}
	)
	soid = database_fd.insert_to_tbl(
		'songslists_observations', {
			'songslist_id'    : slid,
			'observer_id'     : creator_id,
			'observation_time': unix_ts_to_time(unix_ms() / 1_000.0)
		}
	)
	assert soid is not None

	def _init_sl_attr_tbl(name: str, val: int | str) -> None:
		# initiate songslist attributes-related tables
		database_fd.renew_if_exist_else_insert(
			name + '_rec', {'soid': soid}, {name: val}
		)

	_init_sl_attr_tbl('ref_hit', inpict['playCount'])
	_init_sl_attr_tbl('liker', inpict['subscribedCount'])
	_init_sl_attr_tbl('share_cnt', inpict['shareCount'])
	_init_sl_attr_tbl('description', inpict['description'])
	_init_sl_attr_tbl('title', inpict['name'])
	print(f'{unix_time() - st_time} after sl_attrs')

	records = database_fd.query_items_in_tbl(
		"curr_songslists",
		{"songslist_id": slid},
		{'pos_val': ''},
		["song_id"]
	)

	songslist_ids = [] if records is None else [_["song_id"] for _ in records]
	len_ret = -1 if records is None else len(records)
	playlist, updatime = inpict["trackIds"], inpict["updateTime"]
	print('playlist len is', len(playlist))
	del records, inpict

	differs = myers_diff_comparer(songslist_ids, [_["id"] for _ in playlist])
	print(f'{unix_time() - st_time} after myers-algorithm, diff-len is {len(differs)}')

	songslist_ids, ubid = _renew_songslist_status(
		soid, creator_id,
		unix_ts_to_time(updatime / 1000), differs
	)
	print(f'{unix_time() - st_time} after _renew_songslist_status')
	del differs

	_update_current_songslist(slid, songslist_ids, len_ret)
	# 已经有的就不用再去请，只请求没有备份过的
	rows = database_fd.query_null_items_in_tbl(
		'songs_status_in_songslists',
		# 通过行为表选当前新插入到歌单里的歌曲列表
		{'ubid': ubid}, ['delete_pos']
	)
	# TODO: 或者也看因为位置调整而产生变动的？
	print(f'Time-consumption-on-setup-Tables: {unix_time() - st_time}s. Begin Tasks...')
	inpict = set() if rows is None else set([_['song_id'] for _ in rows])
	songslist_ids = list(filter(lambda x: x['id'] in inpict, playlist))
	del playlist, inpict, rows, ubid
	return soid, songslist_ids


@seize_err_if_any()
def songslist_info_gen(
	cooken: dict[str, str],
	worker_num: int,
	crawl_conf: dict,
	split_size: int = 100
) -> None:
	"""
	分析：core_52f85c5f5153a7880e60155739395661.js^[1]下
	的某个匿名函数 (function()) 里有

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

	只需传 id 列表就可以获取到列表内的所有歌曲。
	列表长度不能定得太大，否则后果自负

	- [1]: 2025/02/08: core_70d0eefb570184a2b62021346460be95.js
	       反正理解为 core.js。
	"""
	global TARGET_SONGSLIST_URL, database_fd, MSP, _HTTPS
	response = getter(
		url=f"{TARGET_SONGSLIST_URL}{crawl_conf['list-id']}",
		err_info='fatal error while fetching songslist: ',
		no_header=True
	)

	if response is None:
		logger.error(f'unable to fetch any songslist info for {crawl_conf["list-id"]}')
		return
	elif response.status_code != 200:
		logger.error(f'{response.status_code}, {response.text}')
		exit(1)
	# NOTE: 怎么可能不想用pydantic？只是这里用会导致奇怪的死循环，所以暂时用弱一点的类型dict
	songslist_info: PlaylistDetail = deserialize_json_or_die(response.text, 'playlist')
	del response
	soid, adjust_playlist = _main_thread_db_ops(songslist_info)
	del songslist_info
	integrated_conf = {
		'cookie'    : cooken['cookie'],
		'token'     : cooken['token'],
		'split_size': split_size,
		'soid'      : soid,
		'worker_num': worker_num
	}
	songs_tasks_distributor(integrated_conf, adjust_playlist)
	database_fd.commit()
	database_fd.close()


if __name__ == '__main__':
	spyon: str = _args.songslist_author
	dummy: str = _args.login_dummy
	assert 1 <= _args.threadpool_size  # 不设上限，但至少要有。
	dummy_cooken = {
		'cookie': PRIVATE_CONFIG['netease'][dummy]['cookie'],
		'token' : PRIVATE_CONFIG['netease'][dummy]['csrf_token']
	}
	assert len(dummy_cooken["token"]) == 32 and \
	       f'__csrf={dummy_cooken["token"]}' in dummy_cooken["cookie"]
	songslist_info_gen(
		dummy_cooken, _args.threadpool_size,
		PRIVATE_CONFIG['netease'][spyon]
	)


	"""
	### 如果想跑局部，下面提供两个例子
	## 案例1
	_resp = song_sniper(2754489208, dummy_cooken)
	print((_resp.status_code, _resp.text) if _resp is not None else None)

	## 案例2
	for sid in [2757833873]:
		print(sid)
		_attacher = _extract_hidden_sinfo(sid, dummy_cooken)
		database_fd.update_item_in_tbl(
			"songs",
			{"song_id": sid}, {
			"fetchable"  : _attacher[0],
			"lyrics"     : _attacher[1].replace('\n', '\\n'),
			"translatext": _attacher[2].replace('\n', '\\n'),
			"arrangers"  : _attacher[3],
			"composers"  : _attacher[4],
			"lyricists"  : _attacher[5]
		}
	)
	database_fd.commit()
	database_fd.close()
	"""
