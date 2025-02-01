# !/usr/env/python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY

"""
每次调用成功会使歌单增加 4 次播放量。
一天 24 小时，实测发现**同一用户**只有每 5~6 分钟调用一次脚本才能让歌单播放量增加。
因持续使用，暂时不考虑token过期。单个程序一天最多能增加 [240~288] * 4 次播放。
再找十个人的账号，一天就能刷 9600~11500。但风控也是个问题。偶尔这么做还行，天天这么做如果深究，理论上不行。

建议自动化交给服务器做.

	crontab -e

	*/6 * */2 * * /usr/env/your-venv/python3 update_song_list_cnt.py --author=[author] --dummy=[dummy] >> /your/path/to/log.txt 2>&1
	* * */5 * * /dev/null >> /your/path/to/log.txt
"""
import time, random
from utils.json_paser import PRIVATE_CONFIG
from args_loader import PARSER
from crypto.manual_deobfuscation import cloud_music_encryptor
from requests import post as req_poster

# 调过来自己加。
PARSER.add_argument('author', type=str, help='歌单作者')
PARSER.add_argument('dummy', type=str, help='指定傀儡')
args = PARSER.parse_args()

host = 'music.163.com'
token = PRIVATE_CONFIG[args.dummy]["csrf_token"]
csrf_token = f'?csrf_token={token}'
suspect = f'/api/playlist/update/playcount' + csrf_token
# 经过前端处理后，以上的 suspect 变为以下的 suffix。
suffix = f'/weapi/playlist/update/playcount'+ csrf_token
prefix = f'https://interface.{host}'

header = {
	"Accept"                   : "text/html,application/xhtml+xml,application/xml;"
	                             "q=0.9,image/avif,image/webp,image/apng,*/*;"
	                             "q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Accept-Language"          : "zh-CN,zh-TW;q=0.9,zh;q=0.8,th;q=0.7",
	"Cache-Control"            : "no-cache",
	"Connection"               : "keep-alive",
	"Cookie"                   : PRIVATE_CONFIG[args.dummy]["cookie"],
	"Host"                     : host,
	"Pragma"                   : "no-cache",
	"Origin"                   : f"https://{host}",
	"Referer"                  : f"https://{host}/playlist?id={PRIVATE_CONFIG[args.author]['list-id']}",
	"Sec-Fetch-Dest"           : "iframe",
	"Sec-Fetch-Mode"           : "navigate",
	"Sec-Fetch-Site"           : "same-origin",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent"               : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
	                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
	"sec-ch-ua"                : '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
	"sec-ch-ua-mobile"         : "?0",
	"sec-ch-ua-platform"       : "Windows",
}

# 歌单 id 和 csrf-token 传入加密。以 post 方式查询。
prepared_ingredient = cloud_music_encryptor(f'{"{"}"id":"{PRIVATE_CONFIG[args.author]["list-id"]}",'
                                         f'"csrf_token":"{token}"{"}"}')
# 随机性
time.sleep(random.randint(1, 31))
resp = req_poster(prefix + suffix, data=prepared_ingredient[0], headers=header)
if resp.status_code != 200:
	# 不需要在文本中显示颜色——
	print(f'{resp.status_code}: {resp.content}, {resp.text}')
else:
	print(f"{resp.text}")
