#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
#
# 施工现场，定义变动+逻辑缺失=>仍不能运行
# TODO: 没写好的大概率需要验证码或者扫二维码
#       考虑拦截二维码然后看它想做甚。
#       如果有 root 的安卓设备，intercept 请求应该好做吧？
#       纯粹和知识垄断是同样逻辑的东西。
#       虽说行不通，但至少先实现再说。行不通去找 qrcode 方向的内容。
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
assert 1 == 0, 'should not use this program'

from crypto_aux import *
from misc_utils import *
from configs.args_loader import PARSER
from multtp._cookie_aux.unid_gen import crack_vistor_hash

# config of config.
args = PARSER.parse_args()

# config init payload
user = PRIVATE_CONFIG[args.applicant]
e_mail, passwd = user['email'], rsa_encrypt_without_token(user['password'])

# config backend
_https = "https://"
_authName = "dl.reg.163.com"
reg_host = f"{_https}{_authName}"  # 认证站

_link_to_referer = "/webzj/v1.0.1/pub/index_dl2_new.html"

init_api = "/dl/zj/mail/ini/"  		# 初始化准备，此处会要求设置 cookie: l_s_musicKGxdbOk=，如果响应成功的话。
modp_api = "/dl/zj/mail/powGetP/"  	# 模数 p
cstk_api = "/dl/zj/mail/gt"  		# 跨域 token
accs_api = "/dl/zj/mail/l"  		# 登录入口

## config header
# init-part:
# 2025-03-03 验
"""
_p._$addUtid = function() {
    var e = function() {
        var e = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
          , t = 32
          , n = [];
        for (; t-- > 0; )
            n[t] = e.charAt(Math.random() * e.length);
        return n.join("")
    };
    return function() {
        var t = _cookie._$cookie("utid");
        if (!t) {
            t = e();
            _cookie._$cookie("utid", {
                value: t,
                expires: 3650,
                path: "/"
            })
        }
        return t
    }
}();
"""
# payload preparation.
_rtid = dilphabet_32_str_gen()
host = "music.163.com"
init_inp = {
	"pd": "music",  # 猜测义为product
	"pkid": "KGxdbOk",
	"pkht": "music.163.com",
	"channel": 0,
	"topURL": f"https://{host}/",
	"rtid": f"{_rtid}"
}
modp_inp = {
	"un": f'{e_mail}',
	"pkid": "KGxdbOk",
	"pd": "music",
	"channel": 0,
	"topURL": f"https://{host}/",
	"rtid": f"{_rtid}"
}
cstk_inp = {
	"un": f'{e_mail}',
	"pw": f"{passwd}",
	"pd": "music",
	"l": 0,
	"d": 10,
	"t": f"{funix_ms()}",
	"pkid": "KGxdbOk",
}


# TODO: 拆这个函数为三个子函数的组合
@seize_err_if_any()
def login_in_netease_music() -> None:
	"""
	后续计划从二维码和安卓逆向入手。
	"""
	global reg_host, init_api, modp_api, cstk_api
	global accs_api, cstk_inp, modp_inp, init_inp
	"""
	"https://dl.reg.163.com/webzj/v1.0.1/pub/index_dl2_new.html?MGID=1749748386926.861&wdaId=&pkid=KGxdbOk&product=music"
	"""
	# resp = requests.get(f'https://{host}', headers=HEADER)  # place to fetch NMTID.
	# if resp.status_code != 200:
	# 	print(f'{resp.status_code}: {resp.cookies} {resp.content}')
	# 	exit(1)
	# ck = resp.cookies
	HEADER["Origin"] = f"{reg_host}"
	HEADER["Host"] = f"{_authName}"
	HEADER["Referer"] = reg_host + _link_to_referer + f"?MGID={funix_ms()}&wdaId=&pkid=KGxdbOk&product=music"
	HEADER["Sec-Fetch-Mode"] = 'cors'
	HEADER["Sec-Fetch-Dest"] = 'empty'
	HEADER["Sec-Ch-Ua-Mobile"] = '?0'
	HEADER["Content-Type"] = 'application/json'
	# sec-ch-ua-mobile: ?0
	# https://dl.reg.163.com/webzj/v1.0.1/pub/index_dl2_new.html?
	# MGID=1742125340512.4631&wdaId=&pkid=KGxdbOk&product=music
	_hash_val = crack_vistor_hash("just_crack")
	HEADER["Cookie"] = f"_ntes_nnid={_hash_val},{unix_ms()}; " \
	                   f"_ntes_nuid={_hash_val}; "             \
	                   f"utid={dilphabet_32_str_gen()};"
	# ck.set('_ntes_nuid', f'{_hash_val}', domain=f'{host}', path='/')
	# ck.set('_ntes_nnid', f'{_hash_val},{unix_ms()}', domain=f'{host}', path='/')
	# ck.set('utid', f'{dilphabet_32_str_gen()}', domain=f'{host}', path='/')
	## init_obs = sm4_encryptor(init_inp)
	## init_payload = {"encParams": f"{init_obs}"}
	# init_lena = len(f'{"{"}"encParams":"{init_obs}"{"} "}')
	# HEADER['Content-Length'] = f'{init_lena-1}'
	# 包含 Content-Length 超时？
	# 不包含有反馈 400.
	## resp = requests.post(
	## 	reg_host + init_api,
	## 	data=init_payload,
	## 	headers=HEADER, # cookies=ck,
	## 	impersonate=BROWSER
	## )

	## if resp.status_code != 200:
	## 	# 难绷之第一关都没过。
	## 	# 疑似缺了步骤/内容，导致结果总是 415/400
	## 	print(init_inp)
	## 	print(reg_host + init_api, init_obs, HEADER)
	## 	print(resp.status_code, resp.text)
	## 	return
	## print(resp.status_code, resp.text)

	# 200-resp-of-init: {"ret":"201","capFlag":0,"pv":true,"capId":"#MD5#"}
	# cap_id = load_json_from_str(resp.text)["capId"]

	"""
	200-resp-of-modp:
	{
	    "ret": "201",
	    "pVInfo": {
	        "needCheck": true,
	        "sid": "xxxxxxxx-xx7d-437d-xx4c-xxxxxxxxxxxx",
	        "hashFunc": "VDF_FUNCTION",
	        "maxTime": 2050,
	        "minTime": 2000,
	        "args": {
	            "mod": "32-hex",
	            "t": 300000,
	            "puzzle": "????\r\n????\r\n????\r\n????==",
	            "x": "2c53c4dfbd"
	        }
	    }
	}
	"""
	modp_obs = sm4_encryptor(dic2ease_json_str(modp_inp))
	HEADER["Cookie"] += f" NTES_WEB_FP={crack_vistor_hash('FakeBrowserPayload' + ran_str_gen(2))};"
	resp = requests.post(
		reg_host + modp_api,
		data={ "encParams": f"{modp_obs}" },
		headers=HEADER,
		impersonate=BROWSER
	)
	if resp.status_code != 200:
		print(f'{resp.status_code}, {resp.text}')
		return
	print(resp.status_code, resp.text)

	modp_info = load_json_from_str(resp.text)
	puzzle, sid = modp_info['pVParam']['puzzle'], modp_info['pVParam']['sid']
	mod, hash_fn = modp_info['pVParam']['mod'], modp_info['pVParam']['hashFunc']
	_9_hex = modp_info['pVParam']['x']

	# 200-resp-of-cstk: {"ret":"201","tk":"before_starting_logining_token"}
	cstk_obs = sm4_encryptor(dic2ease_json_str(cstk_inp))
	resp = requests.post(
		reg_host + cstk_api,
		data={ "encParams": f"{cstk_obs}" },
		headers=HEADER, impersonate=BROWSER
	)
	if resp.status_code != 200:
		print(f'{resp.status_code}, {resp.text}')
		return
	print(f'{resp.status_code}, {resp.text}')
	token = load_json_from_str(resp.text)['tk']

	## TMD 填个表单这么沟槽
	cnt, st_time = 0, unix_ms()
	# 小于 2s 或仍小于 300000 次。
	while cnt < 300000 or unix_ms() - st_time < 2000:
		_9_hex = _9_hex * _9_hex % mod
		cnt += 1
	interval = unix_ms() - st_time
	challenge = f"runTimes={cnt}&spendTime={interval}&t={cnt}&x={_9_hex}"
	accs_inp = {
		"un"      : f"{e_mail}", "pw": f"{passwd}",
		"pd"      : "music", "l": 0, "d": 10,
		"t"       : unix_ms(),
		"pkid"    : "KGxdbOk",
		"domains" : "",
		"tk"      : f"{token}",
		"pwdKeyUp": 1,
		"pVParam" : {
			"puzzle"   : f"{puzzle}",
			"spendTime": 1000,
			"runTimes" : interval,
			"sid"      : f"{sid}",
			"args"     : f'{"{"}"x":"{_9_hex}","t":{cnt},"sign":{netease_mmh32(challenge, cnt)}{"}"}'
		},
		"channel" : 0,
		"topURL"  : "https://music.163.com/",
		"rtid"    : f"{dilphabet_32_str_gen()}"
	}
	resp = requests.post(
		reg_host + accs_api,
		data={"encParams": f"{accs_inp}"},
		headers=HEADER, impersonate=BROWSER
	)
	if resp.status_code != 200:
		print(f'{resp.status_code}, {resp.text}')
		return
	print(resp.ststatus_codeatus, resp.text)
	# 对于 cookie，底下 4 个在成功后由 /l 设置：
	# NTES_P_UTID={utid}|1741010805;
	# NTES_SESS=00O61Taaaaaaaaa7.a5aaa3aaaaaaKsU_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaIaaaaaaaaaaaaaaaaaaaaaaAAAAA_
	#           00O61Taaaaaaaaa72a5aaa3aaaaaaKsUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa_aaaaaaaaaaaaaaaaaaaaaaAAAAAAAAAAAAA.
	#           00O61Taaaaaaaaa72a5aaa3.aa_;
	# S_INFO=1741010805|0|3&80##|{prefix before @};
	# P_INFO={email}|1741010805|0|music|00&99|gux&1738436884&music#hun&430100#10#0#0|189430&0||{email};

	"""
	返回200，就登录成功？
	{
	    "code": 8830,
	    "message": "需要进行二次验证",
	    "debugInfo": null,
	    "data": {
	        "MUSIC_TU": "xxxxxxxx-xx7d-xx7d-xx4c-xxxxxxxxxxxx"
	    },
	    "failData": null
	}
	No, 这种情况还需要拼图！滑动对齐！
	对齐完发给 

	拼图完了还要扫码，码的内容 be like：
	orpheus://rnpage?
	      component=rn-account-verify
	      &isTheme=true
	      &immersiveMode=true
	      &route=confirmOldDevice
	      &pollingToken="unknown-how-to-gen-such-md5-shape-token"
	post to https://music.163.com/weapi/middle/account/sns/weblogin

	询问扫码情况的 api：/weapi/login/origin-device/scan-apply/check
	{"code":200,"message":null,"data":{"intervalMillis":1002}} 扫了
	{"code":802,"message":null,"data":{"intervalMillis":1002}} 没有扫
	
	手机做了什么，目前不知道。
	"""
	# 简单来看就是安卓内可用的Url Scheme，一种页面内跳转协议，通过定义自己的URL Scheme协议，
	# 可以从一个APP中打开另外一个APP指定的页面。与远程服务器的交互逻辑由APP内部实现
	# orpheus姑且理解为冈难的包名。
	# 似乎本地下载了冈难的应用后，可以直接在浏览器内用"orpheus://"唤起。

if __name__ == '__main__':
	login_in_netease_music()
