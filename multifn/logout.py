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
from utils.json_conf_reader import PRIVATE_CONFIG
from crypto.manual_deobfuscation import netease_encryptor
from utils.args_loader import PARSER
from utils.logger import DEBUG_LOGGER
from utils.file_operator import attempt_modify_json
from requests import post as rep

args = PARSER.parse_args()

token = PRIVATE_CONFIG[args.exit_user]['csrf_token']
csrf_token = f'?csrf_token={token}'
suffix = '/weapi/logout' + csrf_token
host = 'music.163.com'
prefix = f'https://{host}'
header = {
	# ':authority:'       : host,
	# ':method:'          : 'POST',
	# ':path:'            : suffix,
	# ':scheme:'          : 'https',
	'accept'            : '*/*',
	'accept-language'   : 'zh-CN,zh-TW;q=0.9,zh;q=0.8,th;q=0.7',
	'cache-control'     : 'no-cache',
	'content-length'    : '410',
	'content-type'      : 'application/x-www-form-urlencoded',
	'cookie'            : PRIVATE_CONFIG[args.exit_user]['cookie'],
	'nm-gcore-status'   : '1',
	'origin'            : prefix,
	"pragma"            : 'no-cache',
	'priority'          : "u=1, i",
	"referer"           : f"{prefix}/",
	"sec-ch-ua"         : '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
	"sec-ch-ua-mobile"  : '?0',
	"sec-ch-ua-platform": '"Windows"',
	"sec-fetch-dest"    : "empty",
	"sec-fetch-mode"    : "cors",
	"sec-fetch-site"    : "same-origin",
	"user-agent"        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
	                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}


def user_logout(conf_file: str = 'config.json') -> None:
	"""
	发请求到后端使之删除 cookie 和 token。同时也修改本地的 json 配置。
	:param conf_file: 配置文件。给个默认值。
	"""
	global token, header
	payload = f'{"{"}"csrf_token":"{token}"{"}"}'
	resp = rep(prefix + suffix, headers=header, data=netease_encryptor(payload)[0])
	# 做完以后 token 作废，相应地应该删除所提供的token
	if resp.status_code != 200:
		DEBUG_LOGGER.error(f'{resp.status_code}, {resp.text}')
		exit(1)
	else:
		DEBUG_LOGGER.info(f'{resp.text}')

		attempt_modify_json(
			conf_file,
			{   # 置空就行
				args.exit_user: {
					'csrf_token': '',
					'cookie': ''
				}
			}
		)

if __name__ == "__main__":
	user_logout()
	# TODO: 退了，但是如退。看样子好像要重新逆了。
