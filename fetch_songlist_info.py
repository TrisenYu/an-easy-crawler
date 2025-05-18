#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
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
	通过浏览器提供自身登录后得到的 cookie、歌单 id，然后运行爬取。

会临时生成对应范围的临时文件，多线程执行完成和会按顺序写入 song-list.txt，而后删除临时文件。
命令行传参必要的参数：
	- login_dummy: 傀儡账号。其中 token 和 cookie 必要。
	- songlist_author: 目标歌单。list-id 必要，且目前 backup-dir 也必要。user-id 找到了可以填，找不到最好留成 ''。
"""
import random
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from curl_cffi import requests
from misc_utils.file_operator import (
	write_in_given_mode,
	append_from_ro_file,
	seek_to_remove_file,
	dir2file
)
from misc_utils.header import HEADER, BROWSER
from misc_utils.json_opt.conf_reader import (
	PRIVATE_CONFIG,
	load_json_from_str,
	deserialize_json_or_die
)
from misc_utils.json_opt.resp_types import (
	SongsResp,
	PlaylistDetail,
	PlaylistTrackInfo
)
from misc_utils.logger import DEBUG_LOGGER
from misc_utils.time_aux import (
	unix_ts_to_time,
	curr_time_formatter
)

host = "music.163.com"
_https = 'https://'
interface_prefix = f'{_https}interface.{host}'
songlist_api = f'/api/v6/playlist/detail?id='
song_detail_api = f'/api/song/detail?ids='
target_songs_api = f"{interface_prefix}{song_detail_api}"


def query_song_detail_in_range(
	target_dir: str,
	l: int, r: int,
	play_list: list[PlaylistTrackInfo]
) -> None:
	"""
	>>> {
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
	:param target_dir: 目标目录
	:param l: 左闭端点
	:param r: 右开端点
	:param play_list: 歌单内歌曲 id 构成的列表
	:return: None
	"""
	global target_songs_api
	threading.Event().wait(random.randint(1, 10))
	try:
		# 搞不懂为什么后端要用 get 而不用 post
		res = requests.get(
			f'{target_songs_api}{[play_list[i]["id"] for i in range(l, r)]}',
			headers=HEADER, impersonate=BROWSER
		)
		songs_detail: Optional[SongsResp] = load_json_from_str(res.text)
	except Exception as e:
		DEBUG_LOGGER.log(f'Catch an Exception in range [{l}, {r}]: {e}')
		songs_detail = None

	tmp_file = f'{l}-{r}.tmp'
	with open(dir2file(target_dir, tmp_file), 'w', encoding='utf-8') as fd:
		if songs_detail is None:
			DEBUG_LOGGER.log(f'Error happened before writing into {tmp_file}')
			fd.write(f'\n# Failed to fetch songs which in the range of {l}-{r}.\n\n')
			return

		for a_song in songs_detail['songs']:
			song_name, album_name = a_song['name'], a_song['album']['name']
			author_name = [_author['name'] for _author in a_song['artists']]
			duration = a_song['duration']
			mins, ms = duration // 60_000, duration % 1_000
			sec = (duration - mins * 60_000 - ms) % 1_000
			fd.write(
				f'\t{song_name}--{mins}:{sec:02d}.{ms:03d}--'
				f'{author_name}--{album_name}\n'
			)


def songs_tasks_distributor(
	workers: int,
	task_list: list[PlaylistTrackInfo],
	split_size: int = 100,
	output_dir: str = '',
	fn=query_song_detail_in_range
) -> list:
	"""
	:param workers: 线程池大小
	:param output_dir: 目标目录
	:param task_list:  待爬取的任务
	:param split_size: 分片大小
	:param fn: 待子线程执行的函数。函数格式应为 (int, int, list) -> None。
	:return: 并发执行前计算得到的任务列表。
	"""
	lena = len(task_list)
	other, reminder = lena // split_size, lena % split_size
	tasks_queue = [(_ * split_size, (_ + 1) * split_size) for _ in range(0, other)]
	tasks_queue.append((other * split_size, (other * split_size) + reminder))
	with ThreadPoolExecutor(max_workers=workers) as per_mission:
		for choice in tasks_queue:
			per_mission.submit(fn, output_dir, choice[0], choice[1], task_list)
	return tasks_queue


def songlist_info_gen(
	workers: int,
	victimName: str = "user1",
	output_dir: str = '',
	split_size: int = 100
) -> None:
	"""
	流程：
		- 发请求获取歌单的所有信息
		- 将部分必要信息写入最终文件
		- 将歌曲 id 列表均匀分片形成子任务
		- 并发发请求获取各个子任务待求内容以形成十几个临时文件
		- 所有线程执行结束后，按顺序汇总后删除临时文件

	现有策略：留给用户自己管理生成文件。

	可行性分析：core_52f85c5f5153a7880e60155739395661.js^[1]下
	第 69 行匿名函数 (function()) 里有

	>>> {
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

	只需传 id 参数就可以获取到歌单内的所有歌曲。

	:param workers: 线程池大小
	:param victimName: 目标用户。以抽取对应json内的歌单id。默认 `user1`。
	:param output_dir: 提供给输出文件的文件夹。
	:param split_size: 分片大小。默认 100。

	- [1]: 2025/02/08: core_70d0eefb570184a2b62021346460be95.js，反正理解为 core.js。
	"""
	global interface_prefix, songlist_api

	target_songlist = f"{interface_prefix}{songlist_api}" \
	                  f"{PRIVATE_CONFIG[victimName]['list-id']}"
	try:
		response = requests.get(
			target_songlist,
			headers=HEADER,
			impersonate=BROWSER
		)
	except Exception as e:
		DEBUG_LOGGER.info(f'fatal error while fetching songlist: {e}')
		return
	if response.status_code != 200:
		DEBUG_LOGGER.error(response.status_code, response.text)
		exit(1)

	serializer = response.text
	# 尝试反序列化为 TypedDict 对象
	tmp: PlaylistDetail = deserialize_json_or_die(serializer, 'playlist')
	playlist_rec_path = dir2file(output_dir, f'playlist_info_at_{curr_time_formatter()}.json')
	with open(playlist_rec_path, 'w+', encoding='utf-8') as fd:
		fd.write(serializer)

	final_file = dir2file(output_dir, f'songs_list_at_{curr_time_formatter()}.txt')
	write_in_given_mode(
		path=final_file,
		mode='w',
		# 注意到 updateTime, createTime 精度到了 ms 。
		payload=f'# [UPDATE AT {unix_ts_to_time(tmp["updateTime"] // 1_000)}]\n'
		        f'# birth: {unix_ts_to_time(tmp["createTime"] // 1_000)}\n'
		        f'# songs-list-id: {tmp["id"]}\n'
		        f'# comment-thread-id: {tmp["commentThreadId"]}\n'
		        f'# trackCount: {tmp["trackCount"]}\n'
		        f'# hits (only for reference): {tmp["playCount"]}\n\n'
		        f'songs_list_title = `{tmp["name"]}`\n'
		        f'description = `\n{tmp["description"]}\n`\n\n'
		        f'# songs:\n'
	)
	playlist = tmp['trackIds']
	del tmp
	for seq in songs_tasks_distributor(workers, playlist, split_size, output_dir):
		src_tmp_file = dir2file(output_dir, f'{seq[0]}-{seq[1]}.tmp')
		append_from_ro_file(src_tmp_file, final_file)
		seek_to_remove_file(src_tmp_file)


if __name__ == '__main__':
	from misc_utils.args_loader import PARSER

	_args = PARSER.parse_args()
	del PARSER

	victim: str = _args.songlist_author
	dummy: str = _args.login_dummy
	work_size = _args.threadpool_size
	assert 1 <= work_size  # 不设上限，但至少要有。
	del _args

	dummy_conf: dict[str, str] = PRIVATE_CONFIG[dummy]
	victim_conf: dict[str, str] = PRIVATE_CONFIG[victim]

	csrf_token, _cookie = dummy_conf["csrf_token"], dummy_conf["cookie"]
	assert len(csrf_token) == 32 and f'__csrf={csrf_token}' in _cookie

	HEADER["Cookie"] = _cookie
	HEADER["Host"] = host
	HEADER["Referer"] = f"{_https}{host}/"
	HEADER["Connection"] = "keep-alive"

	songlist_info_gen(work_size, victim, victim_conf['backup-dir'])
