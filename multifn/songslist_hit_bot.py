# Last modified at 2025/10/04 星期六 21:50:56
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
一天 24 小时，实测发现**同一用户**只有每 5~6 分钟调用一次脚本才能让歌单播放量增加。
且经逆向获知，cookie可用期限为申请后的一年以内。

单个傀儡一天最多能增加目标歌单的 [240~288] * 4 次播放。
找十个一天就能刷 9600~11500。但风控大概率会是个问题。

目前一次cookie经观测可用一周。怀疑为MUSIC_U域过期
"""
from misc_utils.opts.json.conf_reader import PRIVATE_CONFIG
from misc_utils.ref_types import (
	Bot_hits_param,
	json_user_conf
)
from misc_utils.header import HEADER, BROWSER, alter_header
from misc_utils.wrappers.err_wrap import seize_err_if_any
from misc_utils.file_operator import unsafe_read_text

from misc_utils.http_meths.man import poster
from misc_utils.str_aux import dic2json_str

from crypto_aux.manual_deobfus import (
	netease_encryptor,
	sha256
)

import time, random, os

_https = 'https://'
host = 'music.163.com'
prefix = f'{_https}{host}'
suffix = f'/weapi/playlist/update/playcount'

HEADER["Host"] = host
HEADER["Origin"] = f"{_https}{host}"

@seize_err_if_any(logger_enable=False)
def check_sh(inp: str) -> bool:
	# hashval auto-modified by shell-script
	flag = len(inp) != 0 and sha256(inp.encode('utf-8')) == \
	"1b11d16a2de0cb9c46794cc6ce975d3747b101c2d33344de2e7fbf25ca46278f"
	return flag


def remedy_for_post_crash(inparam: Bot_hits_param) -> None:
	""" 闭环控制系统 """
	if inparam is None or not isinstance(inparam, Bot_hits_param):
		# 你这个祥子还要救什么？
		print('invalid argv!')
		return

	if os.name == 'nt':
		print(
			"Please implement the logic by yourself. "
			"The author won't do it for you at present."
		)
		return

	import subprocess

	try:
		content = unsafe_read_text(inparam['shell_path'])
	except Exception as e:
		print(f'unexpected exception happened: {e}')
		return

	@seize_err_if_any(logger_enable=False)
	def __run() -> None:
		subprocess.call([
			'bash', f'{content}',
			f'-f clean_crontab',
			f'-s {inparam["author_idx"]}',
			f'-d {inparam["dummy_idx"]}'
		])

	# 实际开始位置
	return __run() if check_sh(content) else None


def bot_hit(
	init_pad: Bot_hits_param,
	list_id: str,
	user_conf: json_user_conf
) -> None:
	# 歌单 id 和 csrf-token 传入加密。以 post 方式查询。
	# 调用前必须要手动设定好 Cookie。
	global prefix, suffix, _https, host
	enc_data, _ran_str = netease_encryptor(
		dic2json_str({
			"id": f"{list_id}",
			"csrf_token": f"{user_conf['csrf_token']}"
		})
	)
	time.sleep(random.randint(1, 17))
	resp = poster(
		url=f'{prefix}{suffix}?csrf_token={user_conf["csrf_token"]}',
		payload=enc_data,
		alter_map={
			"Cookie": user_conf['cookie'],
			"Referer": f"{HEADER['Origin']}/playlist?id={list_id}"
		}
	)
	if resp is None:
		remedy_for_post_crash(init_pad)
		return
	elif resp.status_code != 200:
		print(f'{resp.status_code}: {resp.content}, {resp.text}')
		return

	print(f"{resp.text}")

if __name__ == "__main__":
	from misc_utils.args_loader import PARSER

	args = PARSER.parse_args()
	params: Bot_hits_param = {
		"shell_path": args.bot_sh_path,
		"dummy_idx": args.dummy,
		"author_idx": args.author
	}

	bot_hit(
		params,
		PRIVATE_CONFIG[params["author_idx"]]["list-id"],
		PRIVATE_CONFIG[params["dummy_idx"]]
	)
