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
此外，偶尔这么做还行，天天这么做如果深究起来，理论上不行。

先前因云服务提供商更新了笔者的服务器，导致python依赖缺失，所以才导致不可用。因此在部署时也需要留意系统是否因为更新而导致执行失败。
"""
import time, random
from utils.json_conf_reader import PRIVATE_CONFIG
from utils.args_loader import PARSER
from utils.header import HEADER

from crypto.manual_deobfuscation import netease_encryptor
from requests import post as req_poster

args = PARSER.parse_args()

host = 'music.163.com'
token = PRIVATE_CONFIG[args.dummy]["csrf_token"]
csrf_token = f'?csrf_token={token}'
suffix = f'/weapi/playlist/update/playcount' + csrf_token
_https = 'https://'
prefix = f'{_https}interface.{host}'

HEADER["Referer"] = f"{_https}{host}/playlist?id={PRIVATE_CONFIG[args.author]['list-id']}"
HEADER["Host"] = host
HEADER["Origin"] = f"{_https}{host}"
HEADER["Cookie"] = PRIVATE_CONFIG[args.dummy]['cookie']

def bot_hit(identity: str, tk: str) -> None:
	# 歌单 id 和 csrf-token 传入加密。以 post 方式查询。
	enc_data, _ran_str = netease_encryptor(f'{"{"}"id":"{identity}","csrf_token":"{tk}"{"}"}')
	time.sleep(random.randint(1, 17))
	try:
		resp = req_poster(prefix + suffix, data=enc_data, headers=HEADER)
		if resp.status_code != 200:
			print(f'{resp.status_code}: {resp.content}, {resp.text}')
			return
		print(f"{resp.text}")
	except Exception as e:
		print(f'{e}')
		# TODO: 出现异常了。应该清除定时程序。或者根据某个量而不发包。

if __name__ == "__main__":
	bot_hit(PRIVATE_CONFIG[args.author]["list-id"], token)
