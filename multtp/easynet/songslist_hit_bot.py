# Last modified at 2025/10/25 星期六 17:27:17
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
import time, random, os

from loguru import logger

from misc_utils import *
from datatypes import *
from multtp.meths.man import poster
from crypto_aux import *

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

@seize_err_if_any(logger_enable=False)
def check_sh(inp: str) -> bool:
	# hash val auto-modified by shell-script, do not edit
	flag = len(inp) != 0 and sha256(inp.encode('utf-8')) == \
	"5f2fc98c081231746381172202726e1e5a239bd164104991e7e07f50d328289c"
	# end of modified zone
	return flag


def remedy_for_post_crash(inparam: BotHitsParam) -> None:
	""" 闭环控制系统 """
	if inparam is None:
		# 你这个祥子还要救什么？
		logger.warning('invalid argv!')
		return None

	if os.name == 'nt':
		logger.warning(
			"Please implement the logic by yourself. "
			"The author won't do it for you at present."
		)
		return None

	import subprocess

	try:
		content = unsafe_read_text(inparam['shell_path'])
	except Exception as e:
		logger.error(f'unexpected exception happened: {e}')
		return None

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
	list_id: str,
	user_conf: JsonUserConf,
	init_pad: BotHitsParam,
) -> None:
	# 歌单 id 和 csrf-token 传入加密。以 post 方式查询。
	# 调用前必须要手动设定好 Cookie。
	_HTTPS = 'https://'
	MSP = 'music.163.com'
	PREFIX = _HTTPS + MSP
	api = f'/weapi/playlist/update/playcount'
	enc_data, _ran_str = netease_encryptor(
		dic2ease_json_str({
			"id": f"{list_id}",
			"csrf_token": f"{user_conf['csrf_token']}"
		})
	)
	time.sleep(random.randint(1, 17))
	resp = poster(
		url=f'{PREFIX}{api}?csrf_token={user_conf["csrf_token"]}',
		payload=enc_data,
		alter_dict={
			"Host": MSP,
			"Origin": PREFIX,
			"Cookie": user_conf['cookie'],
			"Referer": f"{PREFIX}/playlist?id={list_id}"
		}
	)
	if resp is None:
		remedy_for_post_crash(init_pad)
		return
	elif resp.status_code != 200:
		logger.warning(f'{resp.status_code}: {resp.content}, {resp.text}')
		return

	logger.info(f"{resp.text}")

if __name__ == "__main__":
	from configs.args_loader import PARSER

	args = PARSER.parse_args()
	params: BotHitsParam = {
		"shell_path": args.bot_sh_path,
		"dummy_idx": args.dummy,
		"author_idx": args.author
	}

	bot_hit(
		PRIVATE_CONFIG['netease'][params["author_idx"]]["list-id"],
		PRIVATE_CONFIG['netease'][params["dummy_idx"]],
		params,
	)
