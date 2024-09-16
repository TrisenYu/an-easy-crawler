#! /usr/bin/python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY

"""
之前这里的逻辑没有直接用网易的后端，而是通过解析冗长的前端来完成任务。
编程效率相对比较快但是运行效率有点 low。所以已经全部注释掉了。
"""
import os
from utils.throw_err import throw_err_if_exist


@throw_err_if_exist
def write_to_file_in_a_way(path: str, attr: str, payload: str) -> None:
	with open(path, attr, encoding='utf-8') as _fd:
		_fd.write(payload)


@throw_err_if_exist
def write_from_file(fpath: str, dst_path: str) -> None:
	with open(fpath, 'r', encoding='utf-8') as fd:
		with open(dst_path, 'a', encoding='utf-8') as dd:
			while True:
				tmp = fd.read()
				if tmp is None or len(tmp) <= 0:
					break
				dd.write(tmp)


@throw_err_if_exist
def remove_file(path: str) -> None:
	os.remove(path)

# 40025	641.096437	175.10.207.56	47.100.127.239	TLSv1	583	Client Hello (SNI=interface.music.163.com)
# 40026	641.110462	175.10.207.56	115.236.121.195	TLSv1.2	249	Client Hello (SNI=httpdns.n.netease.com)
# host = f"https://music.163.com"
# header = {
# 	"Accept"                   : "text/html,application/xhtml+xml,application/xml;"
# 	                             "q=0.9,image/avif,image/webp,image/apng,*/*;"
# 	                             "q=0.8,application/signed-exchange;v=b3;q=0.7",
# 	"Accept-Language"          : "zh-CN,zh-TW;q=0.9,zh;q=0.8,th;q=0.7",
# 	"Cache-Control"            : "no-cache",
# 	"Connection"               : "keep-alive",
# 	"Cookie"                   : PRIVATE_CONFIG["cloudmusic"]["cookie"],
# 	"Host"                     : PRIVATE_CONFIG["cloudmusic"]["name"],
# 	"Pragma"                   : "no-cache",
# 	"Referer"                  : f"{host}/",
# 	"Sec-Fetch-Dest"           : "iframe",
# 	"Sec-Fetch-Mode"           : "navigate",
# 	"Sec-Fetch-Site"           : "same-origin",
# 	"Upgrade-Insecure-Requests": "1",
# 	"User-Agent"               : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
# 	                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
# 	"sec-ch-ua"                : '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
# 	"sec-ch-ua-mobile"         : "?0",
# 	"sec-ch-ua-platform"       : "Windows",
# }
# songs_list_id = PRIVATE_CONFIG['cloudmusic']['list-id']
# target = f"{host + PRIVATE_CONFIG['cloudmusic']['target']}?id={songs_list_id}"
#
# songs_list_title: str
# songs_list_birth: str
# songs_list_appid: str
# songs_list_description: str = ''
# songs_list_len: int
# songs_list_hits: str
# songs_info: list[str] = []
# songs_detail: list[str] = []
#
#
# def init_basic_info() -> None:
# 	global songs_list_appid, songs_list_birth, songs_list_title, songs_list_description
# 	global songs_list_hits, songs_list_len
#
# 	@throw_err_if_exist
# 	def load_json_via_str(inp: str) -> dict:
# 		return json.loads(inp)
#
# 	response = requests.get(url=target, headers=header)
# 	if response.status_code != 200:
# 		print(response.status_code, response.text)
# 		exit(1)
# 	parser = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
# 	script_below_meta = load_json_via_str(parser.script.contents[0])
#
# 	# 获取歌单信息
# 	songs_list_title, songs_list_birth = script_below_meta['title'], script_below_meta['pubDate']
# 	songs_list_appid = script_below_meta['appid']
# 	description = parser.findAll('p', {'id': 'album-desc-more'})
# 	songs_list_description = description[0].text
#
# 	songs_list_hits = parser.findAll('div', {'class': 'more s-fc3'})[0].text
# 	songs_list_len = int(parser.findAll('span', {'id': 'playlist-track-count'})[0].text)
#
# 	ul_list = parser.findAll('ul', {'class': 'f-hide'})[0]
# 	for li_item in ul_list:
# 		songs_info.append(f'{li_item.text}')
# 		songs_detail.append(li_item.a["href"])
#
# 	curr_time = datetime.datetime.now()
# 	write_to_file_in_a_way(
# 		path=PRIVATE_CONFIG['cloudmusic']['path-for-backup'],
# 		attr='w',
# 		payload=f'# [UPDATE AT {curr_time}]\n'
# 		        f'# birth: {songs_list_birth}\n'
# 		        f'# author-id: {PRIVATE_CONFIG["cloudmusic"]["user-id"]}\n'
# 		        f'# songs-list-id: {songs_list_id}\n'
# 		        f'# appid: {songs_list_appid}\n'
# 		        f'# total number of sound tracks in songs list: {songs_list_len}\n'
# 		        f'# Clicks (only for reference): {songs_list_hits}\n'
# 		        f'songs_list_title = `{songs_list_title}`\n'
# 		        f'description = `{songs_list_description[3:]}\n`\n\n'
# 	)
#
#
# def song_content_scanner(l: int, r: int):
# 	"""
# 	:param l: 分块内的最左侧歌曲下标。
# 	:param r: 分块内的最右侧歌曲下标。
# 	:return: None
# 	"""
#
# 	def accumulate_sec_to_min_sec(inp: str) -> tuple[str, str]:
# 		print(inp)
# 		_digit = int(inp)
# 		return str(_digit // 60), str(_digit % 60)
#
# 	@throw_err_quietly
# 	def extract_property_item_from_html(payload, i: int) -> None:
# 		cur: str = payload['property']
# 		content: str = payload['content']
# 		if cur == 'og:music:artist':
# 			songs_detail[i] = content + '-' + songs_detail[i]
# 		elif cur == 'music:duration':
# 			m, s = accumulate_sec_to_min_sec(content)
# 			songs_detail[i] = f'{m}:{s}-' + songs_detail[i]
# 		elif cur == 'og:music:album':
# 			songs_detail[i] = f'{content}-{songs_detail[i]}'
#
# 	for idx in range(l, r):
# 		song_detail = host + songs_detail[idx]
# 		_response = requests.get(song_detail, headers=header)
#
# 		st = time.perf_counter()
# 		_parser = BeautifulSoup(_response.content.decode('utf-8'), 'html.parser')
# 		meta_infos = _parser.findAll('meta')
# 		for meta_info in meta_infos:
# 			extract_property_item_from_html(meta_info, idx)
#
# 		print(songs_detail[idx], songs_info[idx])
# 		ed = time.perf_counter()
# 		if 0 < ed - st < 1:
# 			time.sleep(2.)
#
#
# if __name__ == "__main__":
# 	init_basic_info()
# 	song_content_scanner(0, 1)
