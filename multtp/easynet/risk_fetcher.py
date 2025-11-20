# Last modified at 2025/10/02 星期四 11:44:11
#!/usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025-06>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.

from curl_cffi import requests

from crypto_aux.manual_deobfus import netease_encryptor
from misc_utils import *
from multtp.meths.man import poster

# TODO: 功能拆分+降低爬取速度
def access_a_song(
	idx: int, tk: str, ck: str,
	path2song: str,
) -> None:
	host = "https://music.163.com"

	origin_payload = dic2ease_json_str({
		"songId"    : f"{idx}",
		"csrf_token": f"{tk}"
	})
	encrypted_payload, _ = netease_encryptor(origin_payload)
	song_api = f"{host}/weapi/rep/ugc/song/get?csrf_token={tk}"
	alter_dict = {
		"Accept"      : "*/*",
		"Referer"     : f"{host}/wiki/song?songId={idx}&type=2",
		"Content-Type": "application/x-www-form-urlencoded",
		"Cookie"      : ck,
		"Origin"      : host,
		"Priority"    : "u=1, i"
	}
	resp = poster(url=song_api, data=encrypted_payload, alter_dict=alter_dict)
	if resp is None:
		return resp
	song_info = load_json_from_str(resp.text)
	if 'data' not in song_info or 'playUrl' not in song_info['data']:
		return None
	song_url = song_info['data']['playUrl']
	if song_url is None:
		print('copyright or vip issue')
		exit(1)
	what_we_have = requests.get(
		song_url,
		headers={
			"Range"          : "bytes=0-",
			"Referer"        : song_url,
			"Accept"         : "*/*",
			"Accept-Encoding": "identity;q=1, *;q=0"
		}
	).content
	print(song_url)
	with open(path2song, 'wb') as fd:
		fd.write(what_we_have)
	return None

"""
	POST API: /weapi/rep/ugc/user/privilege?csrf_token={tk}
			  /weapi/rep/ugc/user/res/privilege?csrf_token=
	INP:
		{"bizType":3,"bizId":"song_id","csrf_token":""}
		{"resType":3,"resId":"song_id","csrf_token":""}
	RESP:
"""

if __name__ == "__main__":
	from misc_utils.args_loader import PARSER
	from misc_utils.opts.json.conf_reader import PRIVATE_CONFIG

	args = PARSER.parse_args()
	dummy = PRIVATE_CONFIG[args.dummy]
	# access_a_song(
	# 	22843672,
	# 	dummy['csrf_token'], dummy['cookie'],
	# 	'trouble-maker.mp3'
	# )