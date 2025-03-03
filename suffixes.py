#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
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
逆过程中遇到的suffix汇总
"""
import requests
from crypto.manual_deobfuscation import (
	encText_gen,
	dilphabet_16_str_gen
)
from crypto.native_js import native_encSecKey_gen
from utils.json_conf_reader import PRIVATE_CONFIG
from utils.args_loader import PARSER
from utils.header import HEADER

args = PARSER.parse_args()

token = PRIVATE_CONFIG[args.poc_user]['csrf_token']
private_token = f"?csrf_token={token}"
host_root = 'music.163.com'
hostname = f"https://interface.{host_root}"


# 返回 CDN 连接
# {
#   "data": [
#       ["v3.music.126.net"], ["v5.music.126.net"], ["sv1.music.126.net", "sv2.music.126.net"],
#       ["m10.music.126.net"], ["m8.music.126.net", "m7.music.126.net"], ["v4.music.126.net"],
#       ["m701.music.126.net", "m801.music.126.net"], ["m3.music.126.net"], ["m11.music.126.net"],
#       ["m1.music.126.net", "m2.music.126.net"]
#    ],
#    "code": 200
# }
cdns_api = f"{hostname}/weapi/cdns" + private_token


# 版权声明
copyright_api = f"{hostname}/weapi/copyright/pay_fee_message/config" + private_token


# 返回私信
direct_msg_api = f"{hostname}/weapi/pl/count" + private_token


# 404 无效页。
_unaccessable_page = f"{hostname}/m/api/encryption/param/get" + private_token


# 只有 200，无其它结果
# TODO: 后面这里应该会用到？
refresh_login_token_interface = f"{hostname}/weapi/login/token/refresh" + private_token


# {"code":200,"data":{"title":null,"content":null,"region":null,"urlList":null,"needPop":false},"message":""}
persona_api = f"{hostname}/weapi/privacy/info/get/v2" + private_token


# {
#   "topEventPermission":false,"pubLongMsgEvent":false,"LongMsgNum":1000,"pubEventWithPics":true,
#   "pubEventWithoutResource":false,"pubEventWithPictureForbiddenNotice":"等级达到Lv.0，即可添加图片",
#   "eventVideoUploadNosType":1,"lotteryEventPermission":false,
#   "timingPublishEvent":false,"createChallengeTopic":false,"code":200
# }
user_event_api = f"{hostname}/weapi/event/user/permission" + private_token


# {
#   "code":200,
#   "data":{"mvOnlyMusicPackage":"版权方要求，当前资源仅限音乐包用户使用",
#   "mvOnlyMusicPackageButton":"开通音乐包",
#   "mvOnlyVinylVip":"版权方要求，当前资源仅限黑胶VIP使用","mvOnlyVinylVipButton":"开通黑胶VIP",
#   "onlyBuyMv":"版权方要求，当前资源需单独付费使用","onlyBuyMvButton":"去购买",
#   "mvOnlyDownload":"版权方要求，当前资源需下载后播放","mvOnlyPlay":"版权方要求，当前资源不能下载",
#   "unauthorizedMv":"版权方要求，当前资源暂时无法使用"}
# }
#
msg_on_mv_interface = f"{hostname}/weapi/privilege/message/mv" + private_token

weblog_api = f"{hostname}/weapi/feedback/weblog" + private_token


# 带有多个参数。这里之前似乎前端就已经向后端发出了歌单查询请求。
get_followers_api = f"{hostname}/weapi/user/getfollows/{PRIVATE_CONFIG[args.poc_user]['user-id']}" + private_token

# {
# 	"code"   : 200,
# 	"data"   : {
# 		"preload#security"     : {
# 			"emojiStatus": [{"platform": "web", "product": "cloudmusic", "status": 1, "type": "EMOJY"}]
# 		},
# 		"preload#webNewVipIcon": "true"
# 	},
# 	"message": ""
# }
clientconfig_api = f"{hostname}/weapi/middle/clientcfg/config/list" + private_token

# 传一堆参数
comment_of_songslist_api = f"{hostname}/weapi/comment/resource/comments/get" + private_token
# playlist_detail_interface = "https://interface.music.163.com/api/v6/playlist/detail"
HEADER["Referer"] = f"https://{host_root}/"
HEADER["Cookie"] = PRIVATE_CONFIG[args.poc_user]['cookie']

def __payload_sender(force_post: bool, choice: str):
	"""
	:param force_post: 一定要用 post 方法。
	:param choice: 对接口链接的选择。
	:return: 发请求后接口的响应返回值。
	"""
	if not force_post:
		return requests.get(_unaccessable_page, headers=HEADER)
	raw_data = {"csrf_token": token}
	if choice == weblog_api:
		raw_data["logs"] = "[{\"action\":\"mobile_monitor\"," \
		                   "\"json\":{" \
		                   "\"meta._ver\":2," \
		                   "\"meta._dataName\":\"pip_lyric_monitor\"," \
		                   "\"action\":\"impress\"," \
		                   "\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
		                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36\"," \
		                   "\"chromeVersion\":128," \
		                   "\"mainsite\":\"1\"}}]"
	elif choice == get_followers_api:
		raw_data['offset'] = ' 0'
		raw_data['limit'] = '1000'
		raw_data['order'] = 'true'
	elif choice == clientconfig_api:
		raw_data['moduleName'] = 'preload'
	elif choice == comment_of_songslist_api:
		tmp = f"A_PL_0_{PRIVATE_CONFIG[args.poc_user]['list-id']}"
		raw_data["rid"] = tmp
		raw_data["threadId"] = tmp
		raw_data['pageNo'] = '1'
		raw_data['pageSize'] = "50"
		raw_data['cursor'] = '-1'
		raw_data['offset'] = '0'
		raw_data['orderType'] = '1'

	# easy js 断点逆向。
	random_str: str = dilphabet_16_str_gen()
	print(f'random-str: {random_str}\n')
	data = {
		"params"   : encText_gen(random_str, raw_data.__str__()),
		"encSecKey": native_encSecKey_gen(random_str)
	}
	HEADER["Content-Type"] = "application/x-www-form-urlencoded"
	return requests.post(choice, data=data, headers=HEADER)


# 某些链接需要 GET 而非 POST，编写时忘记写，读者可以自己重试。
if __name__ == "__main__":
	response = __payload_sender(True, comment_of_songslist_api)
	print(response.status_code)
	print(response.text)