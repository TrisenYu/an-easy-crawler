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
逆过程中遇到的suffix。目前基本是draft状态。
"""
from curl_cffi import requests

from crypto_aux.manual_deobfus import (
	encText_gen,
	dilphabet_16_str_gen
)
from crypto_aux.native_js import native_encSecKey_gen
from misc_utils.args_loader import PARSER
from misc_utils.header import HEADER
from misc_utils.json_opt.conf_reader import PRIVATE_CONFIG

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
# {"csrf_token":""}
direct_msg_api = f"{hostname}/weapi/pl/count" + private_token

# 404 无效页。
_unaccessable_page = f"{hostname}/m/api/encryption/param/get" + private_token

# 只有 200，无其它结果
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

# input: {"logs":"[{\"action\":\"impress\",\"json\":{\"mspm\":"unk-128-bits-in-hex-form",\"page\":\"mainpage\",\"module\":\"nav_bar\",\"target\":\"friends\",\"reddot\":\"1\",\"mainsite\":\"1\"}}]","csrf_token":"-"}
# 如果点了页面的播放，就有
# {"logs":"[{\"action\":\"mobile_monitor\",\"json\":{\"meta._ver\":2,\"meta._dataName\":\"pip_lyric_monitor\",\"action\":\"render\",\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36\",\"chromeVersion\":133,\"resourceId\":408814900,\"resourceType\":\"song\",\"mainsite\":\"1\"}}]","csrf_token":""}
# 同时url变为 https://clientlogusf.music.163.com/weapi/feedback/weblog?csrf_token={}
weblog_api = f"{hostname}/weapi/feedback/weblog" + private_token

# 带有多个参数。这里之前似乎前端就已经向后端发出了歌单查询请求。
get_followers_api = f"{hostname}/weapi/user/getfollows/{PRIVATE_CONFIG[args.poc_user]['user-id']}" + private_token

# input: {"moduleName":"music-web-config","key":"web-comment-delete-userlist","csrf_token":""}
# resp: {
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
# {"rid":"A_PL_0_577991289","threadId":"A_PL_0_577991289","pageNo":"1","pageSize":"20","cursor":"-1","offset":"0","orderType":"1","csrf_token":""}
comment_of_songslist_api = f"{hostname}/weapi/comment/resource/comments/get" + private_token
# playlist_detail_interface = "https://interface.music.163.com/api/v6/playlist/detail"

# 歌词
# input: {"id":408814900,"lv":-1,"tv":-1,"csrf_token":""}
lyrics_api = f'{hostname}/weapi/song/lyric' + private_token

# {"ids":"[26620756]","level":"standard","encodeType":"aac","csrf_token":""}
# # resp: {
#   "data":[
#       {
#           "id":26620756,
#           "url":
#   "http://m804.music.126.net/20250309215344/df3147788a72b2532099994ff4afc3fb/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/14080886886/e8f6/1a16/5cc3/1be47c23b9987b3852078e0ad51754e9.m4a?vuutv=hNTU13MVsiamEVQyGoYv5CTzVZDYl0XmWhyg02RxkjQpB5ziXQUy+WXQNDUzS4p/CKGrAcCTacdmimRzUDSkMhTDhOdsW/Fh8Uui/Fsdkbw=&authSecret=000001957b17fb340b6d0a64f6030006",
#           "br":96017,"size":3641848,
#           "md5":"1be47c23b9987b3852078e0ad51754e9",
#           "code":200,
#           "expi":1200,"
#           type":"m4a",
#           "gain":0.0,
#           "peak":1.2562,
#           "closedGain":0.0,"
#           closedPeak":0.0,
#           "fee":8,"uf":null,"payed":0,"flag":260,
#           "canExtend":false,"freeTrialInfo":null,
#           "level":"standard","encodeType":"aac",
#           "channelLayout":null,
#           "freeTrialPrivilege":{
#               "resConsumable":false,
#               "userConsumable":false,
#               "listenType":null,
#               "cannotListenReason":null,
#               "playReason":null,
#               "freeLimitTagType":null
#           },
#           "freeTimeTrialPrivilege":{"resConsumable":false,"userConsumable":false,"type":0,"remainTime":0},
#           "urlSource":0,"rightSource":0,"podcastCtrp":null,"
#           effectTypes":null,"time":299026,
#           "message":null,
#           "levelConfuse":null,
#           "musicId":"7236094765"}
#       ],
#   "code":200
#   }
player_api = f'{hostname}/weapi/song/enhance/player/url/v1' + private_token

# only token as payload.
play_p2p_api = f'{hostname}/weapi/activity/p2p/flow/switch/get' + private_token

# 歌曲加载比较bizarre，目前看不出什么头猪。
# https://m804.music.126.net/20250309211720/
# 3ce124d5c960000cc409c4df90e56aa5/jdyyaac/obj/
# w5rDlsOJwrLDjj7CmsOj/28481794911/bb2a/6931/7c70/e3d9043c8a191e18ae8732d7eba08549.m4a?
# vuutv=mGgoPEaODs+RP0FPkwV2QbLZ5xFY7odifTl6TuWNro+JcuykYflcSRaBtwlaa0anYwwTtikV6wkOnviIuftprj/
# OMNkae7N9YyY5RJvmH2U=&authSecret=000001957af6aaf60bfb0a3084450dbb
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
