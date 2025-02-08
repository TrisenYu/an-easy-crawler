#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
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
import subprocess
from functools import partial

import os

# 很离谱，这里需要根据操作系统来处理。
if os.name != 'nt':
	_Popen = subprocess.Popen
	subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")  # 不加等着被 execjs 抛出的 gbk 编码失效锤。
	import execjs
	subprocess.Popen = _Popen  # 不加等着被操作系统兼容性锤。
	del _Popen
else:
	subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
	import execjs

from utils.file_operator import load_readable_txt_from_file
from utils.json_conf_reader import PRIVATE_CONFIG
from utils.logger import DEBUG_LOGGER

_curr_dir = os.path.dirname(__file__)
obfus_dir = os.path.join(_curr_dir, 'obfus')
defus_dir = os.path.join(_curr_dir, 'deobfus')

try:
	_crypto_sm4 = execjs.compile(load_readable_txt_from_file(os.path.join(obfus_dir, 'crypto_sm4.js')))
	_crypto_rsa = execjs.compile(load_readable_txt_from_file(os.path.join(obfus_dir, 'crypto_rsa.js')),
	                             cwd=PRIVATE_CONFIG['npm-path'])
	_crypto2rsa = execjs.compile(load_readable_txt_from_file(os.path.join(obfus_dir, 'crypto2rsa.js')))
	_crypto_md5 = execjs.compile(load_readable_txt_from_file(os.path.join(defus_dir, 'crypto_md5.js')))
	_cryptommhx64_128 = execjs.compile(load_readable_txt_from_file(os.path.join(defus_dir, 'mmh3.js')))
except Exception as e:
	DEBUG_LOGGER.critical(e)
	exit(1)

_rsa_modulo = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17' \
              'a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c9387011' \
              '4af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef5' \
              '2741d546b8e289dc6935b3ece0462db0a22b8e7'
_rsa_pub2 = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4" \
            "XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfr" \
            "RxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0S" \
            "a4R4qhPO3I2MQIDAQAB\n-----END PUBLIC KEY-----"


def native_encSecKey_gen(ran_str: str) -> str:
	"""
	rsa_e 65537, 0x010001
	:return: 返回值作为 h { encSecKey }
	"""
	global _crypto_rsa, _rsa_modulo
	# 此处需要配置 npm 路径。
	return _crypto_rsa.call('c', ran_str, '010001', _rsa_modulo)

def native_encText_gen(ran_16_str: str, payload: str) -> str:
	global _crypto_rsa
	return _crypto_rsa.call('b', _crypto_rsa.call('b', payload, "0CoJUm6Qyw8W8jud"), ran_16_str)


def native_netease_encryptor(inp_string: str):
	""" 用法同 cloud_music_encryptor, 只不过走的是调用混淆后的 js。 """
	global _crypto_rsa
	return _crypto_rsa.call('get_sign', inp_string)


def native_sm4_encryptor(payload: str) -> str:
	"""
	:return: 返回网易云前端 sm4 加密后的值
	"""
	global _crypto_sm4
	return _crypto_sm4.call('cloudmusic_sm4_encrypt', payload)


def native_rsa_encrypt_without_token(payload: str) -> str:
	global _crypto2rsa
	return _crypto2rsa.call('pwd_encrypt_wrapper', payload)


def native_md5(payload: str) -> str:
	global _crypto_md5
	return _crypto_md5.call('ntes_hex_md5', payload)


def raw_mmh3(payload: str) -> str:
	global _cryptommhx64_128
	return _cryptommhx64_128.call('mmh3_x64_128', payload, 0)


if __name__ == "main":
	encSecKey = native_encSecKey_gen('e2yswfSf2Ac8CUpz')
	csrf_token_json_deserializer = f'{"{"}"csrf_token":"{PRIVATE_CONFIG["user1"]["csrf_token"]}"{"}"}'
	data = {
		"params"   : native_encText_gen('e2yswfSf2Ac8CUpz', csrf_token_json_deserializer),
		"encSecKey": encSecKey
	}
	print(data)
	print(native_netease_encryptor(csrf_token_json_deserializer))