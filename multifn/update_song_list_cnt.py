# !/usr/env/python3
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
一天 24 小时，实测发现**同一用户**只有每 5~6 分钟调用一次脚本才能让歌单播放量增加。且 csrf_token 貌似可用一周。
如需要持续可用，还得实现登录获取 token 的逻辑。

因持续使用，暂时不考虑token过期。单个程序一天最多能增加 [240~288] * 4 次播放。
再找十个人的账号，一天就能刷 9600~11500。但风控也是个问题。偶尔这么做还行，天天这么做如果深究，理论上不行。

建议自动化交给服务器做.

	crontab -e

	*/6 * */2 * * /usr/env/your-venv/python3 update_song_list_cnt.py --author=[author] --dummy=[dummy] >> /your/path/to/log.txt 2>&1
	* * */5 * * /dev/null >> /your/path/to/log.txt

	# 配虚拟环境能少很多事。如果想直接用全局的，可能需要
"""
import time, random
from utils.json_conf_reader import PRIVATE_CONFIG
from utils.args_loader import PARSER
from crypto.manual_deobfuscation import netease_encryptor
from requests import post as req_poster

args = PARSER.parse_args()

host = 'music.163.com'
token = PRIVATE_CONFIG[args.dummy]["csrf_token"]
csrf_token = f'?csrf_token={token}'
suspect = f'/api/playlist/update/playcount' + csrf_token
# 经过前端处理后，以上的 suspect 变为以下的 suffix。
suffix = f'/weapi/playlist/update/playcount' + csrf_token
prefix = f'https://interface.{host}'
# TODO: header 重复有点多，日后评估能否集成到某个文件中。
header = {
	"Accept"                   : "text/html,application/xhtml+xml,application/xml;"
	                             "q=0.9,image/avif,image/webp,image/apng,*/*;"
	                             "q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Accept-Language"          : "zh-CN,zh-TW;q=0.9,zh;q=0.8,th;q=0.7",
	"Cache-Control"            : "no-cache",
	"Connection"               : "keep-alive",
	"Cookie"                   : PRIVATE_CONFIG[args.dummy]["cookie"],
	"Host"                     : host,
	"Origin"                   : f"https://{host}",
	"Referer"                  : f"https://{host}/playlist?id={PRIVATE_CONFIG[args.author]['list-id']}",
	"Sec-Fetch-Dest"           : "iframe",
	"Pragma"                   : "no-cache",
	"Sec-Fetch-Mode"           : "navigate",
	"Sec-Fetch-Site"           : "same-origin",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent"               : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
	                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
	"sec-ch-ua"                : '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
	"sec-ch-ua-mobile"         : "?0",
	"sec-ch-ua-platform"       : "Windows",
}

def bot_hit(identity: str, tk: str):
	# 歌单 id 和 csrf-token 传入加密。以 post 方式查询。
	global header
	enc_data, _ran_str = netease_encryptor(f'{"{"}"id":"{identity}","csrf_token":"{tk}"{"}"}')
	# 随机性，但不需要真随机熵源。
	time.sleep(random.randint(1, 17))
	resp = req_poster(prefix + suffix, data=enc_data, headers=header)
	if resp.status_code != 200:
		# 不需要在文本中显示颜色——
		print(f'{resp.status_code}: {resp.content}, {resp.text}')
	else:
		print(f"{resp.text}")


if __name__ == "__main__":
	bot_hit(PRIVATE_CONFIG[args.author]["list-id"], token)