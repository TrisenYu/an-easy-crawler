#! /usr/bin/python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
"""
对 js 中的 PoC 验证。
"""
import requests
from crypto.bicrypto import (
	encText_gen,
	encSecKey_gen,
	gen_random_16_str
)
from utils.json_paser import PRIVATE_CONFIG

# TODO: 清理以下这里的结构。
private_token = f"?csrf_token={PRIVATE_CONFIG['cloudmusic']['csrf_token']}"
cdns_interface = "https://interface.music.163.com/weapi/cdns" + private_token
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

# 返回版权说明
copyright_interface = "https://interface.music.163.com/weapi/copyright/pay_fee_message/config" + private_token

# 返回评论列表
private_comments_interface = "https://interface.music.163.com/weapi/pl/count" + private_token

# 404 无效页。
target = "https://interface.music.163.com/m/api/encryption/param/get" + private_token

# 只有 200，无其它结果
refresh_login_token_interface = "https://interface.music.163.com/weapi/login/token/refresh" + private_token

# {"code":200,"data":{"title":null,"content":null,"region":null,"urlList":null,"needPop":false},"message":""}
private_info_interface = "https://interface.music.163.com/weapi/privacy/info/get/v2" + private_token

# {
#   "topEventPermission":false,"pubLongMsgEvent":false,"LongMsgNum":1000,"pubEventWithPics":true,
#   "pubEventWithoutResource":false,"pubEventWithPictureForbiddenNotice":"等级达到Lv.0，即可添加图片",
#   "eventVideoUploadNosType":1,"lotteryEventPermission":false,
#   "timingPublishEvent":false,"createChallengeTopic":false,"code":200
# }
user_event_interface = "https://interface.music.163.com/weapi/event/user/permission" + private_token

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
msg_on_mv_interface = "https://interface.music.163.com/weapi/privilege/message/mv" + private_token

weblog_interface = "https://interface.music.163.com/weapi/feedback/weblog" + private_token

# 带有多个参数。
get_followers_interface = f"https://interface.music.163.com/weapi/user/getfollows/{PRIVATE_CONFIG['cloudmusic']['user-id']}" + private_token

# 暂时看不懂这个是干什么的
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
clientconfig_interface = "https://interface.music.163.com/weapi/middle/clientcfg/config/list" + private_token

# 传一堆参数
comment_below_songslist_interface = "https://interface.music.163.com/weapi/comment/resource/comments/get" + private_token

# 破案了 core_52f85c5f5153a7880e60155739395661.js?52f85c5f5153a7880e60155739395661.js 下的
# 第 69 行匿名函数 (function()) 里头有个
# ```
# 	"res-playlist-get": {
#         type: "GET",
#         url: "/api/v6/playlist/detail",
#         format: function(m1x, e1x) {
#             var res = j1x.bsN0x(m1x);
#             res.playlist = res.result;
#             delete res.result;
#             return xr5w(res, e1x)
#         }
#     },
# ```
# 只需要传 id 参数就可以获取到歌单内的所有歌曲。
# playlist_detail_interface = "https://interface.music.163.com/api/v6/playlist/detail"

header = {
	"Accept"                   : "text/html,application/xhtml+xml,application/xml;"
	                             "q=0.9,image/avif,image/webp,image/apng,*/*;"
	                             "q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Accept-Language"          : "zh-CN,zh-TW;q=0.9,zh;q=0.8,th;q=0.7",
	"Cache-Control"            : "no-cache",
	"Connection"               : "keep-alive",
	"Pragma"                   : "no-cache",
	"Referer"                  : f"https://music.163.com/",
	"Sec-Fetch-Dest"           : "iframe",
	"Sec-Fetch-Mode"           : "navigate",
	"Sec-Fetch-Site"           : "same-origin",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent"               : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
	                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
	"sec-ch-ua"                : '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
	"sec-ch-ua-mobile"         : "?0",
	"sec-ch-ua-platform"       : "Windows",
	"cookie"                   : PRIVATE_CONFIG['cloudmusic']['cookie']
}

random_str = gen_random_16_str()
binary_random_str = random_str.encode('utf8')

should_post: bool = True
appended_payload: bool = True


def final_payload_sender(force_post: bool, choice: str):
	"""
	:param force_post: 一定要用 post 方法。
	:param choice: 对接口链接的选择。
	:return: 发请求后接口的响应返回值。
	"""
	if not force_post:
		return requests.get(target, headers=header)
	raw_data = {"csrf_token": PRIVATE_CONFIG['cloudmusic']['csrf_token']}
	if choice == weblog_interface:
		raw_data["logs"] = "[{\"action\":\"mobile_monitor\"," \
		                   "\"json\":{" \
		                   "\"meta._ver\":2," \
		                   "\"meta._dataName\":\"pip_lyric_monitor\"," \
		                   "\"action\":\"impress\"," \
		                   "\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
		                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36\"," \
		                   "\"chromeVersion\":128," \
		                   "\"mainsite\":\"1\"}}]"
	elif choice == get_followers_interface:
		raw_data['offset'] = ' 0'
		raw_data['limit'] = '1000'
		raw_data['order'] = 'true'
	elif choice == clientconfig_interface:
		raw_data['moduleName'] = 'preload'
	elif choice == comment_below_songslist_interface:
		tmp = f"A_PL_0_{PRIVATE_CONFIG['cloudmusic']['list-id']}"
		raw_data["rid"] = tmp
		raw_data["threadId"] = tmp
		raw_data['pageNo'] = '1'
		raw_data['pageSize'] = "50"
		raw_data['cursor'] = '-1'
		raw_data['offset'] = '0'
		raw_data['orderType'] = '1'

	# easy js 断点逆向。
	data = {
		"params"   : encText_gen(binary_random_str, raw_data.__str__()),
		"encSecKey": encSecKey_gen(random_str)
	}
	header["Content-Type"] = "application/x-www-form-urlencoded"
	return requests.post(choice, data=data, headers=header)


# 某些链接需要 GET 而非 POST，编写时忘记写，读者可以自己重试。
response = final_payload_sender(True, comment_below_songslist_interface)
print(response.status_code)
print(response.text)
