#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/04 星期六 03:11:26
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
from crypto_aux.manual_deobfus import netease_encryptor

from misc_utils.http_meths.man import poster, getter
from misc_utils.str_aux import dic2json_str
from misc_utils.opts.json.conf_reader import PRIVATE_CONFIG
from misc_utils.args_loader import PARSER
from misc_utils.header import (
	HEADER, BROWSER
)

hostname = f"https://interface.music.163.com"

def refresh_token(cookie: str, token: str) -> None:
	# TODO: 搞清楚这个是做什么的, 为什么是get
	global hostname
	# post payload: ?
	#   {"code":200,"data":{},"message":""}
	target = f"{hostname}/weapi/login/token/refresh?csrf_token={token}"
	resp = getter(url=target, alter_map={'Cookie': cookie})
	if resp is None:
		exit(1)
	elif resp.status_code != 200:
		print(f'{resp.status_code}, {resp.text}')
		return
	print(f'{resp.status_code}, {resp.text}, {resp.content}')


def refresh_dev_token(cook: str, token: str) -> None:
	# TODO 搞清楚区别
	target = f"{hostname}/weapi/middle/user/device/browser-type/update?csrf_token={token}"
	enc_data, _ran_str = netease_encryptor(
		dic2json_str({
			"browserType" : 1,
			"csrf_token"  : f"{token}"
		})
	)

	resp = poster(url=target, payload=enc_data, alter_map={'Cookie': cook})

	if resp is None:
		exit(1)
	elif resp.status_code != 200:
		print(f'{resp.status_code}, {resp.text}')
		return
	print(f'{resp.status_code}, {resp.text}')


if __name__ == '__main__':
	_args = PARSER.parse_args()
	_token = PRIVATE_CONFIG[_args.refresh_dummy]["csrf_token"]
	_cookie = PRIVATE_CONFIG[_args.refresh_dummy]["cookie"]
	assert len(_token) == 32 and f'__csrf={_token}' in _cookie

	refresh_token(_cookie, _token)
	refresh_dev_token(_cookie, _token)
