# !/usr/bin/env/python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.
"""
每次调用成功会使歌单增加 4 次播放量。
一天 24 小时，实测发现**同一用户**只有每 5~6 分钟调用一次脚本才能让歌单播放量增加。且经逆向获知，cookie可用期限为申请后的一年以内。

单个傀儡一天最多能增加目标歌单的 [240~288] * 4 次播放。
找十个一天就能刷 9600~11500。但风控大概率会是个问题。

目前一次cookie可用一到两周。
"""
from misc_utils.json_opt.conf_reader import PRIVATE_CONFIG
from misc_utils.file_operator import unsafe_read
from misc_utils.header import HEADER, BROWSER
from crypto_aux.manual_deobfus import netease_encryptor
from misc_utils.wrappers.err_wrap import seize_err_if_any
import time, random, os

from curl_cffi import requests

_https = 'https://'
host = 'music.163.com'
prefix = f'{_https}{host}'
suffix = f'/weapi/playlist/update/playcount'

HEADER["Host"] = host
HEADER["Origin"] = f"{_https}{host}"


def remedy_for_post_crash(init_pad: tuple[str, str, str]) -> None:
	""" 闭环控制系统。 """
	if init_pad is None or not isinstance(init_pad, tuple):
		# 你这个祥子还要救什么？
		print('invalid argv!')
		return

	if os.name != 'nt':
		import subprocess
		from crypto_aux.manual_deobfus import sha256

		@seize_err_if_any(logger_enable=False)
		def check_sh() -> bool:
			ok = subprocess.run(['bash', f'{init_pad[2]}', '-f self_validate'])
			content = unsafe_read(init_pad[2])
			flag = len(content) != 0 and ok == sha256(content.encode('utf-8'))
			return flag and ok == "0276d3dd2669ac51275c3adf89ceb4b1428107feb732f6cbd1e013eb19ef09e0"
		@seize_err_if_any(logger_enable=False)
		def __run() -> None:
			subprocess.call(
				# bash ./bot_hit.sh clean_crontab "user1" "user1"
				['bash', f'{init_pad[2]}', 'clean_crontab', f'{init_pad[1]}', f'{init_pad[0]}']
			)

		# 实际开始位置
		if check_sh():
			__run()
		return

	print("Please implement the logic by yourself. The author won't do it for you at present.")


def bot_hit(
	init_pad: tuple[str, str, str],
	identity: str, 
	tk: str
) -> None:
	# 歌单 id 和 csrf-token 传入加密。以 post 方式查询。
	# 调用前必须要手动设定好 Cookie。
	global prefix, suffix, _https, host
	HEADER["Referer"] = f"{HEADER['Origin']}/playlist?id={identity}"
	enc_data, _ran_str = netease_encryptor(f'{"{"}"id":"{identity}","csrf_token":"{tk}"{"}"}')
	time.sleep(random.randint(1, 17))
	try:
		resp = requests.post(
			f'{prefix}{suffix}?csrf_token={tk}',
		    data=enc_data,
			headers=HEADER,
		    impersonate=BROWSER
		)
		if resp.status_code != 200:
			print(f'{resp.status_code}: {resp.content}, {resp.text}')
			return
		print(f"{resp.text}")
	except Exception as e:
		print(f'{e}')
		remedy_for_post_crash(init_pad)


if __name__ == "__main__":
	from misc_utils.args_loader import PARSER
	args = PARSER.parse_args()
	_paras = (args.author, args.dummy, args.bot_sh_path)
	HEADER["Cookie"] = PRIVATE_CONFIG[_paras[1]]['cookie']
	bot_hit(
		_paras, PRIVATE_CONFIG[_paras[0]]["list-id"],
		PRIVATE_CONFIG[_paras[1]]["csrf_token"]
	)
