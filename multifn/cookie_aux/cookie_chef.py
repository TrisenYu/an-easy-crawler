#! /usr/env/python3
# -*- coding: utf8 -*-
# (c) Author <kisfg@hotmail.com 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
#
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

import requests, time, random
from string import ascii_lowercase

from multifn.cookie_aux.session_gen import just_crack_cookie
from multifn.cookie_aux.unid_gen import crack_vistor_hash
from multifn.cookie_aux.fp_gen import (
	just_crack_fp_for_wmdev,
	crack_fp_payload_gen,

)
from utils.header import HEADER
from utils.time_aux import unix_ms, unix_ms_of_next_year
from crypto.unk_symm_cipher import (
	netease_wmjsonp_guid,
	unk_block2, c2_d, k2_d # 如果暂时不能利用好 unk_block2.unk_block，那就走前端获取混淆脚本执行的路。
	# 再不行就用户自己扒下来。不可能为了一个网站写个浏览器出来。
)
from crypto.native_js import native_wm_nike_gen

def gen_wnmcid() -> str:
	return "".join(random.choice(ascii_lowercase) for _ in range(6)) + f'.{unix_ms()}.01.0'


host = 'music.163.com'

resp = requests.get(f'https://{host}', headers=HEADER)  # place to fetch NMTID.
if resp.status_code != 200:
	print(f'{resp.status_code}: {resp.cookies} {resp.content}')
	exit(1)

ck = resp.cookies
ck.set(
	'JSESSIONID-WYYY', f'{just_crack_cookie()}',
	domain=f'.{host}', path='/', expires=f'{unix_ms_of_next_year()}'
)
ck.set('_iuqxldmzr_', '32', domain=f'.{host}', path='/', expires=f'{unix_ms_of_next_year()}')
_hash_val, _nnid_timeval = crack_vistor_hash(ck.__str__()), f'{unix_ms_of_next_year()}'
ck.set('_ntes_nuid', f'{_hash_val}', domain=f'{host}', path='/', expires=f'{_nnid_timeval}')
ck.set('_ntes_nnid', f'{_hash_val},{unix_ms()}',
       domain=f'{host}', path='/', expires=f'{_nnid_timeval}')
ck.set('WEVNSM', '1.0.0', domain=f'.{host}', path='/', expires=f'{unix_ms_of_next_year()}')
ck.set('WNMCID', gen_wnmcid(), domain=f'.{host}', path='/', expires=f'{unix_ms_of_next_year()}')
ck.set('__remember_me', 'true', domain=f'{host}', path='/', expires=f'{unix_ms_of_next_year()}')
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
	ck.set('WM_NI', wm_ni, domain=f'{host}', path='/', expires=f'{_curr}')
	ck.set('WM_TID', wm_tid, domain=f'{host}', path='/', expires=f'{_curr}')
	ck.set('WM_NIKE', native_wm_nike_gen(f'{"{"}"r":1,"d":"{wm_did}","i":"{wm_ni}"{"}"}'),
	       domain=f'{host}', path='/', expires=f'{_curr}')
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

"""
\x01\xff\x00\x04
-102
\x02\x04\x00\x04\x00\x00N!\x02\x00\x00\x01\x02\x00\xd9\x00\x10\xa17A\x08\xa0\xbc\xc1bn\xeb \xc4\x05-\xa5\xf1\x00\x02\x00
 9d0ef7e0905d422cba1ecf7e73d77e67
 \x01\xfc\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x01\x05\x00\x01\x02\x00\xdf\x00\x01\x02\x00\xfb\x00\x01\x00\x01\x0d\x00\x020\xb9\x00\xcf\x00\x01\x01\x01
\x08\x00\x01\x00\x00\xef\x00\x0a
CSS1Compat
\x00\xd5\x00\x05
Win32
\x01\x19\x00\x10
z
\xe4\x81\xc3#
H!\xb6d\x9bCK\xed\x03o\xf0\x01\x04\x00\x04\x00?\xff\x00\x00\xea\x00\x11
zh-CN,zh-TW,zh,th
\x00\xfe\x00\x01\x01\x00\xf0\x00\x10\x8b\xda\xd2T?\x87;\x1dQ\xaf\xdc\x99l\x8c\xe5\xa1\x02\xbc\x00\x16
https://music.163.com/
\x01\x02\x00\x01\x08\x03 \x00\x08
5bf1626b
\x02\x03\x00\x04\x00\x00T\xe1\x01\x0e\x00\x18
application/pdf,text/pdf
\x01\xfa\x00\x01\x01\x01\x11\x00\x10%t\x95G\xc0\x85z&\x9a/V\xbd\xf6\x1fh\x03\x86\x00\x10\x01-\x97\xc4G\xe3\xd74\xb1\x90\xd1\xd3[\x82\x1f\xf5\x00\xe1\x00\x01\x02\x01\xf9\x00\x03
222
\x00\xca\x00\x01\x18\x01\x16\x00\x04\x00\x04\xfaP\x00\xfc\x00\x1f
48000,2,1,0,2,explicit,speakers
\x03$\x00\x08
89e7c489
\x00\xfa\x00\x01\x02\x00\xf1\x00\x02\x00\x82\x00\xd1\x00\x01\x01\x03\x84\x00\x10\x12\x90C\xd88\xd2\xdf0\xee\xdc
3<S\x1c\xd5\xda\x00\xd6\x00\x07unknown\x01\x09\x00
'audioinput__,videoinput__,audiooutput__
\x01\x1a\x00\x00\x00\xd2\x00\x01\x02\x01\x01\x00\x00\x00\xc8\x00o
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36
\x01\x07\x00\x08\x01\x03\x00\x01\x00\x02\x01\x02\x01\x0b\x00\x01\x18\x00\x04\x00\x05
2.0.1
\x01\xf5\x00\x01\x00\x01\xf4\x00\x13
2222222222222222222
\x01\x1b\x00\xdb
PDF Viewer_application/pdf,text/pdf,Chrome PDF Viewer_application/
pdf,text/pdf,Chromium PDF Viewer_application/pdf,text/pdf,
Microsoft Edge PDF Viewer_application/pdf,text/pdf,
WebKit built-in PDF_application/pdf,text/pdf
\x01\xfb\x00\x00\x00\xf3\x00\x01\x08\x01\x17\x00\x05
22221
\x00\xee\x00\x00\x03!\x00\x00\x00\xe5\x00\x01\x02\x01\x1c\x00\x97
x86,Not(A:Brand_99,Google Chrome_133,Chromium_133,Not(A:Brand_99.0.0.0,Google Chrome_133.0.6943.127,Chromium_133.0.6943.127,false,false,,Windows,10.0.0
\x00\xd8\x00\x10\xfc\xff\xe7\x8e+H\xd9\xf4\x1e[\xa9\x11\xcf\xfb%.\x01\x0c\x00\xff
255_255_255,240_240_240,0_0_0,0_0_0,128_128_128,255_255_255,255_255_255,0_0_0,0_0_0,0_0_0,0_0_0,109_109_109,0_0_0,0_120_215,0_0_0,255_255_255,240_240
_240,240_240_240,0_0_0,0_0_0,0_0_0,255_255_255,255_255_255,255_255_255,255_255_255,0_0_0,240_240_240,0_0_0
\x01\x10\x00\x04\x00\x0a\x00\x13\x00\xce\x00\x01\x14\x00\xe9\x00g
5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36
\x03#\x00\x08
a4c622e1
\x00\x05\x00 
 8344a875d3fb4ad4820a67ad24a60738
 \x03\x88\x00\x10\xf8\xb5&\x8cH\xf7\xc8r\xc3M\x1dQq\xee\x1fX\x02\x01\x00\x0f\xe7\xbd\x91\xe6\x98\x93\xe4\xba\x91\xe9\x9f\xb3\xe4\xb9\x90\x00\x03\x00\x00\
x03"\x00\x08
e5cd4de6
\x00\xc9\x00\x05
zh-CN
\x00\xd3\x00\x01\x02\x00\xfd\x00\x07
0.0.0.0
\x00\xda\x00\x01\x02\x01\xf7\x00\x08
22222222
\x01\x06\x00\x07
0.0.0.0
\x00\xe4\x00\x01\x01\x03\x85\x00l
Google Inc. (Intel):ANGLE (Intel, Intel(R) Iris(R) Xe Graphics (0x00009A49) Direct3D11 vs_5_0 ps_5_0, D3D11)
\x02\xc9\x00\x08\x00\x00\x06\x00\x00
\x00\x02\xeb\x01\x0f\x00\x04\x00\x1d
@H
\x00\xcb\x00\x01\x01\x01\xfd\x00\x0d
object Window
\x01\x18\x00\x01!\x00\x06\x00\x0d
1740142294116
\x00\xff\x00\x05
UTF-8
\x00\xf2\x00\x08\x06\x00\x03`\x06
\x00\x03B\x01\xfe\x00\x04
-102
\x01\xf6\x00\x0ac\x01\xff\xff\xff\xff\xff\xff\xff\xff\x00\xd0\x00\x01\x01"""

# 事实确实不行。
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