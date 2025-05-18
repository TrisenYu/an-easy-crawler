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
from curl_cffi import requests

from misc_utils.json_opt.conf_reader import PRIVATE_CONFIG
from misc_utils.args_loader import PARSER
from misc_utils.header import HEADER, BROWSER


_args = PARSER.parse_args()

_token = PRIVATE_CONFIG[_args.login_dummy]["csrf_token"]
assert len(_token) == 32

_cookie = PRIVATE_CONFIG[_args.login_dummy]["cookie"]
assert f'__csrf={_token}' in _cookie

HEADER['Cookie'] = _cookie
csrf_token = f"csrf_token={_token}"
hostname = f"https://interface.music.163.com"


def refresh_token() -> None:
    target = f"{hostname}/weapi/login/token/refresh?{csrf_token}"
    resp = requests.get(target, headers=HEADER, impersonate=BROWSER)
    if resp.status_code != 200:
        print(f'{resp.status_code}, {resp.text}')
        return
    # 疑似只有两百。
    print(f'{resp.status_code}, {resp.text}, {resp.content}')


if __name__ == '__main__':
    refresh_token()
