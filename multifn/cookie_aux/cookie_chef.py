#! /usr/env/python3
# -*- coding: utf8 -*-
# (c) Author <kisfg@hotmail.com 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
#
# 施工现场。
# 益言定真，鉴定为转人工 paste 更好。除非前后端都不更新，不然这里不确定性太大，相当不稳定。
#   感觉过于困难。只能说连同 unk_block2 提供出来作为参考。
#   后续会尝试先从此处获取 cookie，如果失败，再去文件中读预置的。如果还失败，则不会往后做任何实现并抛出错误。
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

import time, random
from string import ascii_lowercase

from curl_cffi import requests

from multifn.cookie_aux.session_gen import just_crack_cookie
from multifn.cookie_aux.unid_gen import crack_vistor_hash
from multifn.cookie_aux.fp_gen import (
	just_crack_fp_for_wmdev,
	crack_fp_payload_gen,

)
from misc_utils.header import HEADER
from misc_utils.time_aux import unix_ms, unix_ms_of_next_year
from crypto_aux.unk_symm_cipher import (
	netease_wmjsonp_guid,
	unk_block2, c2_d, k2_d # 如果暂时不能利用好 unk_block2.unk_block，那就走前端获取混淆脚本执行的路。
	# 再不行就用户自己扒下来。不可能为了一个网站写个浏览器出来。
)
from crypto_aux.native_js import native_wm_nike_gen

def gen_wnmcid() -> str:
	return "".join(random.choice(ascii_lowercase) for _ in range(6)) + f'.{unix_ms()}.01.0'


host = 'music.163.com'

resp = requests.get(f'https://{host}', headers=HEADER)  # place to fetch NMTID.
if resp.status_code != 200:
	print(f'{resp.status_code}: {resp.cookies} {resp.content}')
	exit(1)

# TODO: 用合理的数据结构取控制下面的结构
ck = resp.cookies
ck.set(
	'JSESSIONID-WYYY', f'{just_crack_cookie()}',
	domain=f'.{host}', path='/'
)
ck.set('_iuqxldmzr_', '32', domain=f'.{host}', path='/')
_hash_val, _nnid_timeval = crack_vistor_hash(ck.__str__()), f'{unix_ms_of_next_year()}'
ck.set('_ntes_nuid', f'{_hash_val}', domain=f'{host}', path='/')
ck.set('_ntes_nnid', f'{_hash_val},{unix_ms()}', domain=f'{host}', path='/')
ck.set('WEVNSM', '1.0.0', domain=f'.{host}', path='/')
ck.set('WNMCID', gen_wnmcid(), domain=f'.{host}', path='/')
ck.set('__remember_me', 'true', domain=f'{host}', path='/')
resp = requests.get(f'https://{host}', headers=HEADER, cookies=ck)

if resp.status_code != 200:
	print(f'{resp.status_code}: {resp.cookies} {resp.content}')
	exit(1)

print(ck.keys(), ck.values(), ck.__str__())
# __csrf: csrf_token from login.

curr_jsonp = f"__wmjsonp_{netease_wmjsonp_guid()[2:9]}"
"""
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
"""
wm_payload = {
	"d" : f"{just_crack_fp_for_wmdev()}",
	"v" : "e2891084",  # TODO 到底能不能从host解析后要。变 e2891084 了
	"cb": f"{curr_jsonp}"
}
time.sleep(2)
HEADER['host'] = 'ac.dun.163.com'
wm_verifier = 'https://ac.dun.163.com/v3/d/'  # 获取 WM_NI, WM_NIKE, WM_TID
t_resp = requests.post(wm_verifier, headers=HEADER, cookies=ck, data=wm_payload)
if t_resp.status_code != 200:
	print('wm_failed', t_resp.status_code, t_resp.text)
	exit(1)
print(t_resp.text)
try:
	wm = t_resp.text.split(',')
	wm_tid, wm_did = wm[3].strip('"'), wm[4].strip('"')
	wm_ni = wm[5].strip('"')
	_curr = unix_ms_of_next_year()
	ck.set('WM_NI', wm_ni, domain=f'{host}', path='/')
	ck.set('WM_TID', wm_tid, domain=f'{host}', path='/')
	ck.set('WM_NIKE', native_wm_nike_gen(f'{"{"}"r":1,"d":"{wm_did}","i":"{wm_ni}"{"}"}'),
	       domain=f'{host}', path='/')
except Exception as e:
	print(e)
	exit(1)

HEADER['host'] = "fp-upload.dun.163.com" # host 设置不要多也不要少
tmp = crack_fp_payload_gen(1876)
dev_nuid_payload = {
	"p": "9d0ef7e0905d422cba1ecf7e73d77e67",    # appID
	"v": "2.0.1",                               # versionKey
	"vk": "d44593ca",                           # sdkVersion
	"n": f"{netease_wmjsonp_guid()}",           # uuid
	"d": f"{unk_block2(tmp, None, c2_d, k2_d, '7')}"   #   问题在于输入是什么现在都不清楚。TODO: 只要搞清楚这里，后面登录就能拿来用了。
}

# DeviceID 上扒下来的脚本得了？

# 事实确实不行。被资本做局了
dev_resp = requests.post('https://fp-upload.dun.163.com/v2/js/d',
                         headers=HEADER, data=dev_nuid_payload)
if dev_resp.status_code != 200:
	print(dev_nuid_payload, dev_resp.text)
	exit(1)
print(dev_resp.text)
dev_suffix = "weapi/middle/device-info/web/get"

"""
fp-upload.dun.163.com/v2/js/d post 请求获取 sDeviceId 。
{
    d: "Jyvh0dABjlPawotO9Qg4v...rAI33H"    值 d 为 unk_block2 对 632 个简单加密后得到的值。
    n: "3cfa3220cb054b168a4d2257394550f2"  md5?没找到事实上的计算结果，分发器太过魔鬼。又没有空出来的时间。
    p: "9d0ef7e0905d422cba1ecf7e73d77e67"  值固定，发现为 appID。
    v: "2.0.1"                             应该为版本号
    vk: "d44593ca"                         TODO: 同上需求
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

# ck.set('nets_nuid', f'', domain=f'{host}', path='/', expires=f'{unix_ms_of_next_year()}')