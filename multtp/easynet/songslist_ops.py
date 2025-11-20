# TODO TODO TODO TODO
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com> in 2025
# Created at 2025/10/25 星期六 15:37:31
# Last modified at 2025/10/25 星期六 15:49:42
from typing import Optional

from curl_cffi import Response

from crypto_aux.manual_deobfus import netease_encryptor
from misc_utils import *
from multtp.meths.man import poster

def get_shield_config() -> None:
	"""
	https://ac.dun.163.com/v2/config/js
	?pn=YD00000558929251&cvk=&cb=__wmjsonp_25a5b880&t=1761494935342
	"""
	"""
	safeMailBind.js
	window.initWatchman({
        productNumber: "YD00000558929251",
        onload: function(e) {
            window.WM = e,
            t()
    },)
	"""
	timestamp = unix_ms()
	pn = ''


def update_songslist_attrs(
	cooken: dict[str, str]
) -> Optional[Response]:
	api = "/weapi/batch?csrf_token="
	msp = "https://music.163.com"
	payload = dic2ease_json_str({
		"/api/playlist/desc/update": dic2ease_json_str({
			# checkToken <=> config-hash, 如果想完善就绕不开易盾了，要知其然知其所以然才能一直行
			'id': '', "desc": "",
			# e = localStorage.getItem("default:wm_cf").split(',') 生成配置的字符串表示
			# 更具体是从
			"checkToken": "9ca170a1abeedba16ba1f2ac96ed26f3eafdcfe265aff1bad3ae70e2f4ee83e27"
			              "fe2e6ee82e226a8aba2cfb43ef1f2ad90f025b6eee183a128e2bca4c3b92ae2f4"
			              "ee8ee867e2e6fbd1af2aafbba7c3b939f4f0e4c3e26faffef6d3b328e2bdab8aa"
			              "132f1f000cda161a7b3eedbb43cf0fea586ec2afaed00d1af2aa6bba3c3b93af4"
			              "f4ee87e863e2e6fdd1b328e2adab8ea132f2f0e4c3f26fabfef6d4b33cf0feab8"
			              "be270e2e6aa82ef79a7f4ee86e579e2e6aa82ef79a7f4ee86f679e2e6aa82ef79"
			              "a7f4ee93e880e2e6ffcda169afb2eedbb128e2bda7c3b93bf4f0e4c3ee80a7b3e"
			              "edbb83cf0fea195e863e2e6fdd1b328e2b3bc86f02afaeb00cda167b8bba7c3b9"
			              "39f4f0e4c3f366e2e6eebac73cf4f000d1b83ffce7fedab13ff3fee4c3e870a1f"
			              "ef695f17fa7f4ee83ef2afafeeecda163b6b0eedbb23cf4f000d1af2aa8acba91"
			              "a132fceafcd1b33cf4f0e4c3f780adfef6d3b33cf4f4ee86e47fe2e6aa82ef79a"
			              "7f4ee82e780e2e6fbd1af2aa7acadc3b96ea3b4bd86af2ab8bdbcc3b93cbf"
		}),
		"/api/playlist/tags/update": dic2ease_json_str({
			'id': '', "tags": ''
		}),
		# 这里命名就相比前两个显得很怪
		# 另外就是可能并不想更新歌单名，这里如果提交上去了就不太行
		# 需要做一个是否改动的判断
		"/api/playlist/update/name": dic2ease_json_str({
			'id': '', "name": ''
		}),
		"csrf_token": cooken['csrf_token']
	})
	encrypted_payload, _ = netease_encryptor(payload)
	return poster(
		url=msp+api+cooken['csrf_token'],
		payload=encrypted_payload,
		err_info="unable to post payload to remote cloud server",
		alter_dict={
			# 这里还没细看
			'Cookie': cooken['cookie'],
			'Referer': msp+"/my/",
			'Origin': msp,
		},
	)


if __name__ == '__main__':
	get_shield_config()
