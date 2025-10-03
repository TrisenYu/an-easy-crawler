#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/04 星期六 21:17:05
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
from misc_utils.args_loader import PARSER
from misc_utils.opts.json.conf_reader import PRIVATE_CONFIG


args = PARSER.parse_args()
token = PRIVATE_CONFIG[args.poc_user]['csrf_token']
private_token = f"?csrf_token={token}"
host_root = 'music.163.com'
hostname = f"https://interface.{host_root}"

"""
返回 CDN 连接
{
	"data": [
		["v3.music.126.net"], ["v5.music.126.net"], ["sv1.music.126.net", "sv2.music.126.net"],
		["m10.music.126.net"], ["m8.music.126.net", "m7.music.126.net"], ["v4.music.126.net"],
		["m701.music.126.net", "m801.music.126.net"], ["m3.music.126.net"], ["m11.music.126.net"],
		["m1.music.126.net", "m2.music.126.net"]
	],
	"code": 200
}
"""
cdns_api = f"{hostname}/weapi/cdns" + private_token

# 版权声明
"""
inp: {"csrf_token": ""}
"""
copyright_api = f"{hostname}/weapi/copyright/pay_fee_message/config" + private_token

# 返回私信
# {"csrf_token":""}
direct_msg_api = f"{hostname}/weapi/pl/count" + private_token

# 404 无效页。疑似遗留矢山
_unaccessable_page = f"{hostname}/m/api/encryption/param/get" + private_token

# 只有 200，无其它结果
refresh_login_token_interface = f"{hostname}/weapi/login/token/refresh" + private_token

# {"code":200,"data":{"title":null,"content":null,"region":null,"urlList":null,"needPop":false},"message":""}
persona_api = f"{hostname}/weapi/privacy/info/get/v2" + private_token

"""
POST API
INP: {"csrf_token":""}
RESP: {
		"topEventPermission":false,"pubLongMsgEvent":false,"LongMsgNum":1000,"pubEventWithPics":true,
		"pubEventWithoutResource":false,"pubEventWithPictureForbiddenNotice":"等级达到Lv.0，即可添加图片",
		"eventVideoUploadNosType":1,"lotteryEventPermission":false,
		"timingPublishEvent":false,"createChallengeTopic":false,"code":200
	}
"""
user_event_api = f"{hostname}/weapi/event/user/permission" + private_token

"""
{
	"code":200,
	"data":{"mvOnlyMusicPackage":"版权方要求，当前资源仅限音乐包用户使用",
	"mvOnlyMusicPackageButton":"开通音乐包",
	"mvOnlyVinylVip":"版权方要求，当前资源仅限黑胶VIP使用","mvOnlyVinylVipButton":"开通黑胶VIP",
	"onlyBuyMv":"版权方要求，当前资源需单独付费使用","onlyBuyMvButton":"去购买",
	"mvOnlyDownload":"版权方要求，当前资源需下载后播放","mvOnlyPlay":"版权方要求，当前资源不能下载",
	"unauthorizedMv":"版权方要求，当前资源暂时无法使用"}
}
"""
msg_on_mv_interface = f"{hostname}/weapi/privilege/message/mv" + private_token

"""
inp:

"""
"""
POST API
INP:
{
	"logs":"[{
		"action":"bannerimpress",
		"json":{
			"adLocation":"",
			"adSource":"",
			"adid":"",
			"backgroundColor":"",
			"backgroundImageUrl":"",
			"encodeId":"",
			"exclusive":false,
			"extMonitor":[],
			"imageUrl":"http://p1.music.126.net/Mp_EfLmIdmiOuqVB7HYz9Q==/109951171297664027.jpg",
			"monitorBlackList":[],
			"monitorClick":"",
			"monitorClickList":[],
			"monitorImpress":"",
			"monitorImpressList":[],
			"monitorType":"",
			"scm":"1.music-homepage.homepage_banner_force.banner.15915025.362688623.null",
			"targetId":"13828789752",
			"targetType":"1000",
			"titleColor":"red",
			"typeTitle":"歌单推荐",
			"url":"/playlist?id=13828789752",
			"picUrl":"http://p1.music.126.net/Mp_EfLmIdmiOuqVB7HYz9Q==/109951171297664027.jpg",
			"type":"1000_歌单",
			"id":"13828789752",
			"position":"13828789752",
			"requestid":"undefined_1749746639251_9452",
			"impressid":"undefined_1749746639251_9452_1749747049002_7799",
			"mainsite":"1"
		}
	}]",
	"csrf_token":""
}
如果点了页面的播放，就有
{
	"logs":"[{
		"action":"mobile_monitor",
		"json":{
			"meta._ver":2,
			"meta._dataName":"pip_lyric_monitor",
			"action":"render",
			"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
			"chromeVersion":133,
			"resourceId":13456,
			"resourceType":"song",
			"mainsite":"1"
		}
	}]",
	"csrf_token":""
}
同时url变为 https://clientlogusf.music.163.com/weapi/feedback/weblog?csrf_token={}
"""
weblog_api = f"{hostname}/weapi/feedback/weblog" + private_token

"""
POST API
INP: {
	'offset': 0
	'limit': 1000
	'order': true
	'csrf_token': ''
}
"""
get_followers_api = f"{hostname}/weapi/user/getfollows/{PRIVATE_CONFIG[args.poc_user]['user-id']}" + private_token

"""
POST API
INP: {
	"moduleName":"music-web-config", 或者 "preload"
	"key":"web-comment-delete-userlist",
	"csrf_token":""
}
RESP: {
	"code"   : 200,
	"data"   : {
		"preload#security"     : {
			"emojiStatus": [{"platform": "web", "product": "cloudmusic", "status": 1, "type": "EMOJY"}]
		},
		"preload#webNewVipIcon": "true"
	},
	"message": ""
}
"""
clientconfig_api = f"{hostname}/weapi/middle/clientcfg/config/list" + private_token

"""
POST API
INP: {
	"rid":"A_PL_0_577991289",
	"threadId":"A_PL_0_577991289",
	"pageNo":"1",
	"pageSize":"20",
	"cursor":"-1",
	"offset":"0",
	"orderType":"1",
	"csrf_token":""
}
"""
comment_of_songslist_api = f"{hostname}/weapi/comment/resource/comments/get" + private_token
# playlist_detail_interface = "https://interface.music.163.com/api/v6/playlist/detail"


# 歌词
# INP: {"id":408814900,"lv":-1,"tv":-1,"csrf_token":""}
lyrics_api = f'{hostname}/weapi/song/lyric' + private_token

"""
POST API
INP:
	{"ids":"[26620756]","level":"standard","encodeType":"aac","csrf_token":""}
RESP: {
"data":[
	{
		"id":26620756,
		"url":
		"http://m804.music.126.net/20250309215344/df3147788a72b2532099994ff4afc3fb/ \
		jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/14080886886/e8f6/1a16/5cc3/  \
		1be47c23b9987b3852078e0ad51754e9.m4a  \
		?vuutv=hNTU13MVsiamEVQyGoYv5CTzVZDYl0XmWhyg02RxkjQpB5ziXQUy+WXQNDUzS4p/CKGrAcCTacdmimRzUDSkMhTDhOdsW/Fh8Uui/Fsdkbw= \
		&authSecret=000001957b17fb340b6d0a64f6030006",
		"br":96017,"size":3641848,
		"md5":"1be47c23b9987b3852078e0ad51754e9",
		"code":200,
		"expi":1200,"
		type":"m4a",
		"gain":0.0,
		"peak":1.2562,
		"closedGain":0.0,"
		closedPeak":0.0,
		"fee":8,"uf":null,"payed":0,"flag":260,
		"canExtend":false,"freeTrialInfo":null,
		"level":"standard","encodeType":"aac",
		"channelLayout":null,
		"freeTrialPrivilege":{
		  "resConsumable":false,
		  "userConsumable":false,
		  "listenType":null,
		  "cannotListenReason":null,
		  "playReason":null,
		  "freeLimitTagType":null
		},
		"freeTimeTrialPrivilege":{"resConsumable":false,"userConsumable":false,"type":0,"remainTime":0},
		"urlSource":0,"rightSource":0,"podcastCtrp":null,"
		effectTypes":null,"time":299026,
		"message":null,
		"levelConfuse":null,
		"musicId":"7236094765"}
	],
"code":200
}
"""
player_api = f'{hostname}/weapi/song/enhance/player/url/v1' + private_token

# only token as payload.
play_p2p_api = f'{hostname}/weapi/activity/p2p/flow/switch/get' + private_token

unk_enc_api = '/m/api/encryption/param/get' + private_token

# {"moduleName":"preload","csrf_token":""}
# {"moduleName":"user","csrf_token":""}
middle_api = '/api/middle/clientcfg/config/list' + private_token

"""
GET API.
RESP:
{
	"g_ref":null,
	"g_envType":"online",
	"vipWebCashierRedirect":1,
	"GUserAcc": {
		"reward":false,
		"topic":2
	},
	"allowRejectComment":false,
	"g_visitor":{
		"userId":123123123,
		"userType":0,
		"nickname":"123123",
		"avatarImgId":123123,
		"avatarUrl":"http://p4.music.126.net/[base64-enc-1]/[id].jpg",
		"backgroundImgId":[id],
		"backgroundUrl":"http://p1.music.126.net/[base64-enc-2]/[id].jpg",
		"signature":"***",
		"createTime":1503670614456,
		"userName":"1_masked_phoneNumber",
		"lastLoginTime":unix-timestamp,
		"lastLoginIP":"1.2.3.4",
		"birthday":unix-timestamp,
		"authority":0,
		"gender":3,
		"accountStatus":0,
		"followed":false,
		"mutual":false,
		"province":6_____,"city":6_____,
		"authStatus":0,"description":null,
		"detailDescription":null,
		"defaultAvatar":false,
		"expertTags":null,"djStatus":0,
		"locationStatus":0,"vipType":0,
		"allowRemoveHotComment":false,
		"authenticated":false,
		"accountType":1,
		"shortUserName":"masked_phone_number"
	}
}
"""
user_info_api: str = "discover/g/attr?csrf_token=" + private_token

"""
POST API
INP:
	{"songId":"","csrf_token":""}
RESP:
{
    "message": "提交成功",
    "data": {
        "songId": 2644531376,
        "songName": "モリヤスワコ (feat. Tracy × らっぷびと × miko)",
        "artistRepVos": [
            {
                "artistId": 149088,
                "artistName": "Tracy",
                "alias": null,
                "headPicUrl": null,
                "area": null,
                "type": null,
                "desc": null,
                "production": null,
                "avatarPicUrl": null,
                "transName": null
            },
            {
                "artistId": 61534939,
                "artistName": "みゅい",
                "alias": null,
                "headPicUrl": null,
                "area": null,
                "type": null,
                "desc": null,
                "production": null,
                "avatarPicUrl": null,
                "transName": null
            },
            {
                "artistId": 15245,
                "artistName": "らっぷびと",
                "alias": null,
                "headPicUrl": null,
                "area": null,
                "type": null,
                "desc": null,
                "production": null,
                "avatarPicUrl": null,
                "transName": null
            },
            {
                "artistId": 16114,
                "artistName": "Alternative ending",
                "alias": null,
                "headPicUrl": null,
                "area": null,
                "type": null,
                "desc": null,
                "production": null,
                "avatarPicUrl": null,
                "transName": null
            }
        ],
        "songSubTitle": "",
        "company": null,
        "publishTime": 0,
        "language": "日语",
        "originalCover": 0,
        "originalSong": null,
        "no": null,
        "disc": "01",
        "lyricArtists": [
            {
                "artistId": 96478188,
                "artistName": "まろん (IOSYS) / らっぷびと",
                "alias": null,
                "headPicUrl": null,
                "area": null,
                "type": null,
                "desc": null,
                "production": null,
                "avatarPicUrl": null,
                "transName": null
            }
        ],
        "composeArtists": [
            {
                "artistId": 735070,
                "artistName": "ZUN",
                "alias": null,
                "headPicUrl": null,
                "area": null,
                "type": null,
                "desc": null,
                "production": null,
                "avatarPicUrl": null,
                "transName": null
            }
        ],
        "arrangeArtists": [
            {
                "artistId": 149088,
                "artistName": "Tracy",
                "alias": null,
                "headPicUrl": null,
                "area": null,
                "type": null,
                "desc": null,
                "production": null,
                "avatarPicUrl": null,
                "transName": null
            }
        ],
        "roleArtists": null,
        "songTags": null,
        "albumRepVo": {
            "albumId": 253210138,
            "albumName": "THE ANTHEM",
            "artistRepVos": null,
            "albumPicUrl": null,
            "albumSubTitle": null,
            "company": null,
            "publishTime": null,
            "songRepVos": null,
            "songTags": null,
            "production": null,
            "language": null,
            "type": null,
            "transName": null
        },
        "transName": null,
        "mvIds": null,
        "lyricContent": null,
        "transLyricContent": null,
        "playUrl": "http://m701.music.126.net/20250620221625/8d601bf8f8f4d05c53cdc440f5d479c2/jdymusic/obj/wo3DlMOGwrbDjj7DisKw/57232603318/21da/7fd6/b5b0/6eaad182115363869e13e9131ed95e9c.mp3?vuutv=5qFa4yHj+CakNlBn3G428qcvSgEbNfr9XJ0d/tNfKCV4tTo7Jt13DpGxU02WOzv8iylNYSXKX0WZ5BJthxRKNfcJJXd02eAg32wcXk7jqoY=",
        "forTransLyric": 1,
        "noNeedLyric": 0,
        "lyricLock": 0,
        "transLyricLock": 0,
        "lyricIsEdited": 0,
        "duration": 173198
    },
    "code": 200
}
"""
reveal_song_api: str = "/weapi/rep/ugc/song/get?csrf_token=" + private_token

# POST API
wiki_editable_api: str = "/weapi/rep/ugc/user/privilege?csrf_token=" + private_token

# post-api
# weapi/w/user/safe/bindings/[userid]?csrf_token=?
