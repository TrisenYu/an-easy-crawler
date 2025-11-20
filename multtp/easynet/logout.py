# Last modified at 2025/10/25 星期六 17:34:57
#! /usr/bin/env python3
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
	登出操作。
"""
from loguru import logger

from misc_utils import *
from crypto_aux import *
from misc_utils.opts.json.conf_reader import attempt_modify_json
from multtp.meths.man import poster

logger.remove()
logger.add(GLOB_MAIN_LOG_PATH, colorize=True, format=GLOB_LOG_FORMAT, rotation="16MB", compression='zip')

host = 'music.163.com'
prefix = f'https://{host}'


def user_logout(
	dummy: str,
	cooken: dict[str, str],
	conf_path: str = 'config.json'
) -> None:
	"""
	发请求到后端使之删除 cookie 和 token。同时也修改本地的 json 配置。

	:param dummy: 登出的目标账户在 `config.json` 中的对应字符串键值。
	:param cooken: 目标账户的cookie和token配置。
	:param conf_path: 配置文件路径。默认值给到 config.json。
	"""
	global prefix
	api = f'/weapi/logout?csrf_token='
	payload = dic2ease_json_str({
		"csrf_token": cooken['csrf_token']
	})
	resp = poster(
		url=prefix + api + cooken['csrf_token'],
		payload=netease_encryptor(payload)[0],
		alter_dict={
			'Referer': prefix + '/',
			'Origin': prefix,
			'Content-Type': 'application/x-www-form-urlencoded',
			'Cookie': cooken['cookie'],
		}
	)
	# 做完以后 token 作废，相应地应该删除所提供的token
	if resp is None:
		exit(1)
	elif resp.status_code != 200:
		logger.error(f'{resp.status_code}, {resp.text}')
		exit(1)
	logger.info(f'{resp.text}')
	attempt_modify_json(
		conf_path,
		{
			dummy: {
				'csrf_token': '',
				'cookie': ''
			}
		}
	)

if __name__ == "__main__":
	from configs.args_loader import PARSER
	args = PARSER.parse_args()
	user_logout(args.exit_user, PRIVATE_CONFIG['netease'][args.exit_user])
	# TODO: 退了，但是如退。看样子好像要重新逆了。
