#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
#
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
import time
from requests import post as req_post

from crypto.manual_deobfuscation import (
	ran_str_gen,
	sm4_encryptor,
	netease_mmh32,
	dilphabet_32_str_gen,
	rsa_encrypt_without_token
)
from utils.json_conf_reader import (
	PRIVATE_CONFIG,
	load_json_from_str
)
from utils.time_aux import (
	unix_ms,
	funix_ms,
	unix_ms_of_next_year
)
from utils.header import HEADER
from utils.args_loader import PARSER
from utils.wrappers.err_wrap import seize_err_if_any
from multifn.cookie_aux.unid_gen import crack_vistor_hash


# config of config.
args = PARSER.parse_args()

# config init payload
user = PRIVATE_CONFIG[args.applicant]
e_mail, passwd = user['email'], rsa_encrypt_without_token(user['password'])

# config backend
_https = "https://"
_authName = "dl.reg.163.com"
reg_host = f"{_https}{_authName}"           # 认证站

_link_to_referer = "/webzj/v1.0.1/pub/index_dl2_new.html"

init_api = "/dl/zj/mail/ini/"              # 初始化准备，此处会要求设置 cookie: l_s_musicKGxdbOk=，如果响应成功的话。
modp_api = "/dl/zj/mail/powGetP/"          # 模数 p
cstk_api = "/dl/zj/mail/gt"                # 跨域 token
accs_api = "/dl/zj/mail/l"                 # 登录入口

## config header
# init-part:
HEADER["Origin"] = f"{_authName}"
_hash_val, _nnid_timeval = crack_vistor_hash("just_crack"), f'{unix_ms_of_next_year()}'
HEADER["cookie"] = f"_ntes_nnid={_hash_val},{_nnid_timeval}; _ntes_nuid={_hash_val}; " \
                   f"utid={dilphabet_32_str_gen()};"
# 2025-03-03 验
HEADER["refer"] = _link_to_referer + f"?MGID={funix_ms()}&wdaId=&pkid=KGxdbOk&product=music"


# payload preparation.
init_inp = f'{"{"}'                                       \
		   f'"pkid":"KGxdbOk",'                           \
		   f'"pd":"music",'                               \
		   f'"un":"{e_mail}",'                            \
		   f'"channel":0,'                                \
		   f'"topURL":"https://music.163.com/",'          \
		   f'"rtid":"aaaa"'                               \
		   f'{"}"}'
modp_inp = f'{"{"}'                                       \
		   f'"un":"{e_mail}",'                            \
		   f'"pkid":"KGxdbOk",'                           \
		   f'"pd":"music",'                               \
		   f'"channel":0,'                                \
		   f'"topURL": "https://music.163.com/",'         \
		   f'"rtid": "bbbb"'                              \
		   f'{"}"}'
cstk_inp = f'{"{"}"un":"{e_mail}",'                       \
		   f'"pw":"{passwd}",'                            \
		   f'"pd":"music",'                               \
		   f'"l":0,"d":10,'                               \
		   f'"t":{time.time_ns() / 1000},'                \
		   f'"pkid": "KGxdbOk"'                           \
		   f'{"}"}'

@seize_err_if_any
def login_in_netease_music() -> None:
	"""
	此处代码仅作为实现参考，未经过测试，不要调用！！！
	后续计划从二维码和安卓逆向入手。
	"""
	global reg_host, init_api, modp_api, cstk_api
	global accs_api, cstk_inp, modp_inp, init_inp

	init_obs = sm4_encryptor(init_inp)
	resp = req_post(init_api, data={"encParams": f"{init_obs}"}, headers=HEADER)
	if resp.status_code != 200:
		return
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
	modp_obs = sm4_encryptor(modp_inp)
	HEADER["cookie"] += f" NTES_WEB_FP={crack_vistor_hash('FakeBrowserPayload'+ran_str_gen(2))};"
	resp = req_post(reg_host + modp_api, data={"encParams":f"{modp_obs}"}, headers=HEADER)
	if resp.status_code != 200:
		return
	modp_info = load_json_from_str(resp.text)
	puzzle, sid = modp_info['pVParam']['puzzle'], modp_info['pVParam']['sid']
	mod, hash_fn = modp_info['pVParam']['mod'], modp_info['pVParam']['hashFunc']
	_9_hex = modp_info['pVParam']['x']

	# 200-resp-of-cstk: {"ret":"201","tk":"before_starting_logining_token"}
	cstk_obs = sm4_encryptor(cstk_inp)
	resp = req_post(reg_host + cstk_api, data={"encParams": f"{cstk_obs}"}, headers=HEADER)
	if resp.status_code != 200:
		return
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
	    "un": f"{e_mail}","pw": f"{passwd}",
	    "pd":"music","l":0,"d":10,
		"t": unix_ms(),
		"pkid":"KGxdbOk",
		"domains": "",
		"tk": f"{token}",
	    "pwdKeyUp": 1,
	    "pVParam": {
			"puzzle": f"{puzzle}",
	        "spendTime": 1000,
		    "runTimes": interval,
		    "sid": f"{sid}",
	        "args": f'{"{"}"x":"{_9_hex}","t":{cnt},"sign":{netease_mmh32(challenge, cnt)}{"}"}'
		},
	    "channel": 0,
	    "topURL": "https://music.163.com/",
	    "rtid": f"{dilphabet_32_str_gen()}"
	}
	resp = req_post(reg_host + accs_api, data={"encParams": f"{accs_inp}"}, headers=HEADER)
	if resp.status_code != 200:
		return
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


if __name__ == '__main__':
	login_in_netease_music()
