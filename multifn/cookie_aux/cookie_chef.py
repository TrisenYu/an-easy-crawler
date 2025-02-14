#! /usr/env/python3
# -*- coding: utf8 -*-
# (c) Author <kisfg@hotmail.com 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# 转 AI，这里相当不好做。
# TODO: 将实现转为提供可用cookie的接口。
#   能不能调用时即可能获知混淆代码中变量的值而无需人工干预？
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

import requests, time, random
from string import ascii_lowercase
from multifn.cookie_aux.session_gen import just_crack_cookie
from multifn.cookie_aux.unid_gen import fetch_vistor_hash
from multifn.cookie_aux.fp_gen import just_crack_fp_for_wmdev
from utils.header import HEADER
from crypto.unk_hash import netease_wmjsonp_guid
from crypto.native_js import native_wm_nike_gen

latent_targets = ["ac.dun.163yun.com/v3/d",
                  "ac.dun.163.com/v2/config/js",
                  "ac.dun.163yun.com/v3/b",
                  "ac.dun.163yun.com/v2/b",
                  "ac.dun.163yun.com/v2/d"]


def _unix_ts_gen() -> int:
	return int(time.time() * 1000)


def _gen_expired_time() -> int:
	return _unix_ts_gen() + 31536000


def gen_wnmcid() -> str:
	return "".join(random.choice(ascii_lowercase) for _ in range(6)) + f'.{_unix_ts_gen()}.01.0'


host = 'music.163.com'

resp = requests.get(f'https://{host}', headers=HEADER)  # place to fetch NMTID.
if resp.status_code != 200:
	print(f'{resp.status_code}: {resp.cookies} {resp.content}')
	exit(1)

ck = resp.cookies
ck.set(
	'JSESSIONID-WYYY', f'{just_crack_cookie()}',
	domain=f'.{host}', path='/', expires=f'{_gen_expired_time()}'
)
ck.set('_iuqxldmzr_', '32', domain=f'.{host}', path='/', expires=f'{_gen_expired_time()}')
_hash_val, _nnid_timeval = fetch_vistor_hash(ck.__str__()), f'{_gen_expired_time()}'
ck.set('_ntes_nuid', f'{_hash_val}', domain=f'{host}', path='/', expires=f'{_nnid_timeval}')
ck.set('_ntes_nnid', f'{_hash_val},{_unix_ts_gen()}',
       domain=f'{host}', path='/', expires=f'{_nnid_timeval}')
ck.set('WEVNSM', '1.0.0', domain=f'.{host}', path='/', expires=f'{_gen_expired_time()}')
ck.set('WNMCID', gen_wnmcid(), domain=f'.{host}', path='/', expires=f'{_gen_expired_time()}')
ck.set('__remember_me', 'true', domain=f'{host}', path='/', expires=f'{_gen_expired_time()}')
resp = requests.get(f'https://{host}', headers=HEADER, cookies=ck)

if resp.status_code != 200:
	print(f'{resp.status_code}: {resp.cookies} {resp.content}')
	exit(1)

print(ck.keys(), ck.values(), ck.__str__())
# __csrf: csrf_token from login.

dev_suffix = "weapi/middle/device-info/web/get"
what_we_got = just_crack_fp_for_wmdev()
dev_nuid_payload = f'{"{"}"p":"9d0ef7e0905d422cba1ecf7e73d77e67","v":"2.0.1",' \
                   f'"vk":"{"wait-a-minute"}","n":"{"wait-a-minute"}",' \
                   f'"d":"{what_we_got}"{"}"}'

# 貌似先去 GET，但实际测了一下感觉不需要。
curr_jsonp = f"__wmjsonp_{netease_wmjsonp_guid()[2:9]}"
# resp = requests.get(f"https://ac.dun.163.com/v2/config/js?pn=YD00000558929251&cvk=&cb={curr_jsonp}&t={_unix_ts_gen()}")
# if resp.status_code != 200:
# 	print(resp.status_code, resp.text)
# 	exit(1)
# print(resp.text)
# GET 正常结果形如：__wmjsonp_aaaaaaaa({"code":200,"msg":"ok","result":{
#   "s":"acstatic-dun.126.net",
#   "v":"2.7.5_602a5ad7",           # buildVersion
#   "luv":"2.7.5_af2952a4",         # latestVersion
#   "as":"ac.dun.163yun.com",       # apiServer
#   "ivp":300000,
#   "conf":"9ca170a1abeedba16ba1f2ac96ed26f3eafdcfe265aff1bad3ae70e2f4ee83e27fe2e6ee82e226a8aba2cfb43ef1 # configHash
#           f2ad90f025b6eee183a128e2bca4c3b92ae2f4ee8ee867e2e6fbd1af2aafbba7c3b939f4f0e4c3e26faffef6d3b328e2bdab
#           8aa132f1f000cda161a7b3eedbb43cf0fea586ec2afaed00d1af2aa6bba3c3b93af4f4ee87e863e2e6fdd1b328e2adab8ea1
#           32f2f0e4c3f26fabfef6d4b33cf0feab8be270e2e6aa82ef79a7f4ee86e579e2e6aa82ef79a7f4ee86f679e2e6aa82ef79a7
#           f4ee93e880e2e6ffcda169afb2eedbb128e2bda7c3b93bf4f0e4c3ee80a7b3eedbb83cf0fea195e863e2e6fdd1b328e2b3bc
#           86f02afaeb00cda167b8bba7c3b939f4f0e4c3f366e2e6eebac73cf4f000d1b83ffce7fedab13ff3fee4c3e870a1fef695f1
#           7fa7f4ee83ef2afafeeecda163b6b0eedbb23cf4f000d1af2aa8acba91a132fceafcd1b33cf4f0e4c3f780adfef6d3b33cf4
#           f4ee86e47fe2e6aa82ef79a7f4ee82e780e2e6fbd1af2aa7acadc3b96ea3b4bd86af2ab8bdbcc3b93cbf",
#   "ass":["ac.dun.163.com","ac.dun.163yun.com"],            # apiServers
#   "ss":["acstatic-dun.126.net","acstatic.dun.163yun.com"], # staticServers
#   "cvk":"bb1e322ecc385b9a43c6403050adbf87"}})

# 原本要用里头的信息。但是简单起见 ignore 掉。
wm_payload = {
	"d" : f"{just_crack_fp_for_wmdev()}",
	"v" : "602a5ad7", # TODO 从host解析之后要。
	"cb": f"{curr_jsonp}"
}
time.sleep(2)
HEADER['host'] = 'ac.dun.163.com'  # 不加这个是这个👎
wm_verifier = 'https://ac.dun.163.com/v3/d/'  # 获取 WM_NI, WM_NIKE, WM_TID

t_resp = requests.post(wm_verifier, headers=HEADER, cookies=ck, data=wm_payload)
if t_resp.status_code != 200:
	print(t_resp.status_code, t_resp.text)
	exit(1)
print(t_resp.text)
try:
	wm = t_resp.text.split(',')
	wm_tid, wm_did = wm[3].strip('"'), wm[4].strip('"')
	wm_ni = wm[5].strip('"')
	_curr = _gen_expired_time()
	ck.set('WM_NI', wm_ni, domain=f'{host}', path='/', expires=f'{_curr}')
	ck.set('WM_TID', wm_tid, domain=f'{host}', path='/', expires=f'{_curr}')
	ck.set('WM_NIKE', native_wm_nike_gen(f'{"{"}"r":1,"d":"{wm_did}","i":"{wm_ni}"{"}"}'),
	       domain=f'{host}', path='/', expires=f'{_curr}')
except Exception as e:
	print(e)
	exit(1)

# 乱劈风POST导致返回的不是 wm_jsonp({"code":200,...}) 的形式。
# 不过如果不乱劈风难道要写个前端出来吗？null([200,1739542802547,"aaa","aaa", null,"=aaa"])

"""

得到的结果可能会送往
https://ac.dun.163.com/v3/d
{
    d: xVqFdJesCGi.LO/iAnX...1v84
    v: af2952a4
    cb: __wmjsonp_7e4b460
}
	此处正常的格式形如 # 正常的格式形如 
		__wmjsonp_d380379([
		    200,
		    1739454502968, 时间
		    "aaaaa+a=a=",  WM_TID
		    "aaaa+",       WM_DID
		    null,
		    "aaaaa=aaaa/"  WM_NI
		])
	WM_NIKE = Na(JSON.stringfy({r:1, d:WM_DID, i:WM_NI}))

或者 fp-upload.dun.163.com/v2/js/d post 请求获取 sDeviceId 。
{
    d: "Jyvh0dABjlPawotO9Qg4v...rAI33H"    值 d 为unk_hash2 对 632 个块做摘要+自定义base64 得到的值。
    n: "3cfa3220cb054b168a4d2257394550f2"  md5?
    p: "9d0ef7e0905d422cba1ecf7e73d77e67"  值固定，发现为 appID。
    v: "2.0.1"                             应该为版本号
    vk: "d44593ca"                         好几天了暂时固定
}
	收到的正常参数中 {
	  "code":200,
	  "data":{
	      "dt":"Ky------------",      ydDeviceToken,
	      "st":1739194020259,         timestamp
	      "tid":"J2---------------"   作为 ntes_nuid 的 tid._.url_encode[data.tid]._.0出现。
	      },
	  "msg":"ok"
	}

然后按 {"ydDeviceType":"WebOnline","ydDeviceToken":"Ky-----------"}
加密后送去 /weapi/middle/device-info/web/get
响应报文中，报文头有 set-cookie: sDeviceId=YD-aaaa; Max-Age=315360000; Expires={DATE}; Path=/; Domain=.music.163.com
内容有 {"code":200,"data":{"sDeviceId":"YD-kxxxxxxxx","cached":false,
"correctDeviceId":null,"revertDeviceId":false,"initAppBySDeviceId":false},"message":""}
于是就应抽取 YD-kxxxxxxxx%2F 作为 cookie。不过通信完成，理论上 requests 自然会设置这个。
所以 SDeviceId 基本不用管。
"""


# ck.set('nets_nuid', f'', domain=f'{host}', path='/', expires=f'{_gen_expired_time()}')
# TODO:
#   MUSIC_U
#   __snaker__id
#   gdxidpyhxdE
#   __root_domain_v
