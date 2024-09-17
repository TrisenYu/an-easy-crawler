#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY

"""
本项目只用于个人爬取网易云歌单的歌曲名等信息以用于留存备份。
使用方式：
	通过浏览器提供自身登录后得到的 cookie、歌单 id，然后运行爬取。
"""
import random
from utils.json_paser import (
	PRIVATE_CONFIG,
	load_json_from_str,
	json2dict_via_str_or_die
)
from utils.logger import DEBUG_LOGGER
from file_operator import (
	write_to_file_in_a_way,
	write_from_file,
	remove_file
)
import time, requests, threading

host = "music.163.com"
csrf_token = PRIVATE_CONFIG["cloudmusic"]["csrf_token"]
interface_prefix = f'https://interface.{host}'
songs_list_suffix = f'/api/v6/playlist/detail?id='
song_detail_suffix = f'/api/song/detail?ids='

target_song_list = f"{interface_prefix}{songs_list_suffix}{PRIVATE_CONFIG['cloudmusic']['list-id']}"
target_song_prefix = f"{interface_prefix}{song_detail_suffix}"

header = {
	"Accept"                   : "text/html,application/xhtml+xml,application/xml;"
	                             "q=0.9,image/avif,image/webp,image/apng,*/*;"
	                             "q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Accept-Language"          : "zh-CN,zh-TW;q=0.9,zh;q=0.8,th;q=0.7",
	"Cache-Control"            : "no-cache",
	"Connection"               : "keep-alive",
	"Cookie"                   : PRIVATE_CONFIG["cloudmusic"]["cookie"],
	"Host"                     : PRIVATE_CONFIG["cloudmusic"]["name"],
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
response = requests.get(target_song_list, headers=header)
if response.status_code != 200:
	print(response.status_code, response.text)
	exit(1)

serializer = response.text

tmp = json2dict_via_str_or_die(serializer, 'playlist')
birthday = time.localtime(tmp["createTime"] / 1000.)
last_update = time.localtime((tmp["updateTime"] / 1000.))
write_to_file_in_a_way(
	path=PRIVATE_CONFIG['cloudmusic']['path-for-backup'],
	attr='w',
	payload=f'# [UPDATE AT {time.strftime("%Y-%m-%d %H:%M:%S", last_update)}]\n'
	        f'# birth: {time.strftime("%Y-%m-%d %H:%M:%S", birthday)}\n'
	        f'# author-id: {PRIVATE_CONFIG["cloudmusic"]["user-id"]}\n'
	        f'# songs-list-id: {tmp["id"]}\n'
	        f'# comment-thread-id: {tmp["commentThreadId"]}\n'
	        f'# trackCount: {tmp["trackCount"]}\n'
	        f'# hits (only for reference): {tmp["playCount"]}\n\n'
	        f'songs_list_title = `{tmp["name"]}`\n'
	        f'description = `\n{tmp["description"]}\n`\n\n'
	        f'songs <=\n'
)
playlist = tmp['trackIds']
del tmp
lena, slicer = len(playlist), 100
other, reminder = lena // slicer, lena % slicer


def query_detailed_info_of_song_in_range(l: int, r: int):
	global playlist, slicer
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
	},
	:param l: 左闭端点
	:param r: 右开端点
	:return: None
	"""
	# 像是这种多个参数的查询 [33399045, 2150468782, 2622292778, 2622295278, 2622295928] 是可以用的
	tmp_file_name = f'./{l}-{r}.tmp'
	cluster: list[int] = [playlist[i]['id'] for i in range(l, r)]
	time.sleep(random.randint(1, 10))
	res = requests.get(f'{target_song_prefix}{cluster}', headers=header)
	songs_detail = load_json_from_str(res.text)
	with open(tmp_file_name, 'w', encoding='utf-8') as fd:
		if songs_detail is None:
			DEBUG_LOGGER.info(f'[error happened before writing into {tmp_file_name}]')
			fd.write(f'\n# failed to fetch songs which in the range of {l}-{r}.\n\n')
			return
		for a_song in songs_detail['songs']:
			name, album = a_song['name'], a_song['album']['name']
			duration = a_song['duration']
			author_name = [_['name'] for _ in a_song['artists']]
			minutes, millisec = duration // 60000, duration % 1000
			sec = (duration - minutes * 60000 - millisec) % 1000
			fd.write(f'\t{name}--{minutes}:{sec:02d}.{millisec:03d}--{author_name}--{album}\n')


task_queue: list[tuple[int, int]] = [(_ * slicer, (_ + 1) * slicer) for _ in range(0, other)]
task_queue.append((other * slicer, (other * slicer) + reminder))
ts: list[threading.Thread] = [threading.Thread(target=query_detailed_info_of_song_in_range,
                                               args=(val[0], val[1])) for val in task_queue]

for t in ts:
	t.start()
for t in ts:
	t.join()

# 做完了再写
for seq in task_queue:
	src_tmp_file = f'./{seq[0]}-{seq[1]}.tmp'
	write_from_file(
		src_tmp_file,
		PRIVATE_CONFIG['cloudmusic']['path-for-backup']
	)
	remove_file(src_tmp_file)
