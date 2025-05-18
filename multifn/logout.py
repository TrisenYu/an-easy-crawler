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
from misc_utils.json_opt.conf_reader import (
	PRIVATE_CONFIG,
	attempt_modify_json
)
from crypto_aux.manual_deobfus import netease_encryptor
from misc_utils.logger import DEBUG_LOGGER
from misc_utils.header import HEADER, BROWSER
from curl_cffi import requests


host = 'music.163.com'
prefix = f'https://{host}'
suffix = f'/weapi/logout?csrf_token='

HEADER['Referer'] = f'{prefix}/'
HEADER['Origin'] = prefix
HEADER['Content-Type'] = 'application/x-www-form-urlencoded'


def user_logout(
	dummy: str,
	token: str,
	conf_file: str = 'config.json'
) -> None:
	"""
	发请求到后端使之删除 cookie 和 token。同时也修改本地的 json 配置。

	:param dummy: 登出的目标账户在 `config.json` 中的对应字符串键值。
	:param token: 目标账户的 token。
	:param conf_file: 配置文件。默认值给到 config.json。
	"""
	global prefix, suffix
	payload = f'{"{"}"csrf_token":"{token}"{"}"}'
	resp = requests.post(
		prefix + suffix + token,
		data=netease_encryptor(payload)[0],
		headers=HEADER, impersonate=BROWSER)
	# 做完以后 token 作废，相应地应该删除所提供的token
	if resp.status_code != 200:
		DEBUG_LOGGER.error(f'{resp.status_code}, {resp.text}')
		exit(1)
	else:
		DEBUG_LOGGER.info(f'{resp.text}')

		attempt_modify_json(
			conf_file,
			{
				dummy: {
					'csrf_token': '',
					'cookie': ''
				}
			}
		)

if __name__ == "__main__":
	from misc_utils.args_loader import PARSER
	args = PARSER.parse_args()
	victim = args.exit_user
	victim_conf = PRIVATE_CONFIG[victim]
	del args

	tk = victim_conf['csrf_token']
	HEADER['Cookie'] = victim_conf['cookie']

	user_logout(victim, tk)
	# TODO: 退了，但是如退。看样子好像要重新逆了。
