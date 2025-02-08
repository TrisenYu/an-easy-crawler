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
	- login_dummy: 自己的账号。其中 token 和 cookie 必要。
	- songlist_author: 目标歌单。list-id 必要，且目前 path-for-backup 也必要。user-id 找到了可以填，找不到最好留成 ''。
"""
import random
from utils.json_conf_reader import (
	PRIVATE_CONFIG,
	load_json_from_str,
	json2dict_via_str_or_die
)
from utils.args_loader import PARSER
from utils.logger import DEBUG_LOGGER
from utils.file_operator import (
	write_in_assigned_mode,
	append_from_read_only_file,
	remove_file
)
import time, requests, threading

args = PARSER.parse_args()

host = "music.163.com"
csrf_token = PRIVATE_CONFIG[args.login_dummy]["csrf_token"]
assert len(csrf_token) == 32
interface_prefix = f'https://interface.{host}'
songs_list_suffix = f'/api/v6/playlist/detail?id='
song_detail_suffix = f'/api/song/detail?ids='
target_song_list = f"{interface_prefix}{songs_list_suffix}{PRIVATE_CONFIG[args.songlist_author]['list-id']}"
target_song_prefix = f"{interface_prefix}{song_detail_suffix}"

header = {
	"Accept"                   : "text/html,application/xhtml+xml,application/xml;"
	                             "q=0.9,image/avif,image/webp,image/apng,*/*;"
	                             "q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Accept-Language"          : "zh-CN,zh-TW;q=0.9,zh;q=0.8,th;q=0.7",
	"Cache-Control"            : "no-cache",
	"Connection"               : "keep-alive",
	"Cookie"                   : PRIVATE_CONFIG[args.login_dummy]["cookie"],
	"Host"                     : host,
	"Pragma"                   : "no-cache",
	"Referer"                  : f"https://{host}/",
	"Sec-Fetch-Dest"           : "iframe",
	"Sec-Fetch-Mode"           : "navigate",
	"Sec-Fetch-Site"           : "same-origin",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent"               : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
	                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
	"sec-ch-ua"                : '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
	"sec-ch-ua-mobile"         : "?0",
	"sec-ch-ua-platform"       : "Windows",
}


def query_detailed_info_of_song_in_range(l: int, r: int, play_list: list):
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

	:param l: 左闭端点
	:param r: 右开端点
	:param play_list: 歌单内歌曲 id 构成的列表
	:return: None
	"""
	tmp_file_name = f'./{l}-{r}.tmp'
	cluster: list[int] = [play_list[i]['id'] for i in range(l, r)]
	time.sleep(random.randint(1, 10))  # 算了，留着这个烂的写法吧

	# 像这种多参数的查询 [33399045, 2150468782, 2622292778, 2622295278, 2622295928] 是可以的
	res = requests.get(f'{target_song_prefix}{cluster}', headers=header)
	songs_detail = load_json_from_str(res.text)
	with open(tmp_file_name, 'w', encoding='utf-8') as fd:
		if songs_detail is None:
			DEBUG_LOGGER.log(f'[error happened before writing into {tmp_file_name}]')
			fd.write(f'\n# failed to fetch songs which in the range of {l}-{r}.\n\n')
			return
		# 格式对照 ./human_readable.json 来操作。
		for a_song in songs_detail['songs']:
			name, album = a_song['name'], a_song['album']['name']
			duration = a_song['duration']
			author_name = [_['name'] for _ in a_song['artists']]
			minutes, millisec = duration // 60000, duration % 1000
			sec = (duration - minutes * 60000 - millisec) % 1000
			fd.write(f'\t{name}--{minutes}:{sec:02d}.{millisec:03d}--{author_name}--{album}\n')


def songs_tasks_distributor(
	task_list: list,
	split_size: int = 100,
	fn=query_detailed_info_of_song_in_range
) -> list:
	"""
	:param task_list:  待爬取的任务
	:param split_size: 分片大小
	:param fn: 待子线程执行的函数。函数格式应为 (int, int, list) -> None。
	:return: 并发执行前计算得到的任务列表。
	"""
	lena = len(task_list)
	other, reminder = lena // split_size, lena % split_size
	task_queue: list[tuple[int, int]] = [(_ * split_size, (_ + 1) * split_size) for _ in range(0, other)]
	task_queue.append((other * split_size, (other * split_size) + reminder))
	ts: list[threading.Thread] = [
		threading.Thread(target=fn, args=(val[0], val[1], task_list)) for val in task_queue
	]
	for t in ts:
		t.start()

	for t in ts:
		t.join()

	return task_queue


def generate_info_of_songlist(
	username: str = "user1",
	split_size: int = 100
) -> None:
	"""
	流程：
		- 发请求获取歌单的所有信息
		- 将部分必要信息写入最终文件
		- 将歌曲 id 列表均匀分片形成子任务
		- 并发发请求获取各个子任务待求内容以形成十几个临时文件
		- 所有线程执行结束后，按顺序汇总后删除临时文件
	:param username: 目标用户。以抽取对应json内的歌单id。默认 `user1`。
	:param split_size: 分片大小。默认 100。
	:return: 不返回
	"""
	response = requests.get(target_song_list, headers=header)
	if response.status_code != 200:
		DEBUG_LOGGER.error(response.status_code, response.text)
		exit(1)

	serializer = response.text
	tmp = json2dict_via_str_or_die(serializer, 'playlist')
	write_in_assigned_mode(
		path=PRIVATE_CONFIG[username]['path-for-backup'],
		attr='w',
		payload=f'# [UPDATE AT {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((tmp["updateTime"] / 1000.)))}]\n'
		        f'# birth: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tmp["createTime"] / 1000.))}\n'
		        f'# author-id: {PRIVATE_CONFIG[username]["user-id"]}\n'
		        f'# songs-list-id: {tmp["id"]}\n'
		        f'# comment-thread-id: {tmp["commentThreadId"]}\n'
		        f'# trackCount: {tmp["trackCount"]}\n'
		        f'# hits (only for reference): {tmp["playCount"]}\n\n'
		        f'songs_list_title = `{tmp["name"]}`\n'
		        f'description = `\n{tmp["description"]}\n`\n\n'
		        f'songs\n'
	)
	playlist = tmp['trackIds']
	del tmp

	# 做完了再写
	for seq in songs_tasks_distributor(playlist, split_size):
		src_tmp_file = f'./{seq[0]}-{seq[1]}.tmp'
		append_from_read_only_file(
			src_tmp_file,
			# TODO: 语义有点怪，不应该是 login_dummy 的文件夹吗？
			PRIVATE_CONFIG[username]['path-for-backup']
		)
		remove_file(src_tmp_file)


if __name__ == '__main__':
	generate_info_of_songlist(args.songlist_author)
