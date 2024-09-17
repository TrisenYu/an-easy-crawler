#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY

"""
下次用 burpsuite 看可能会更快？
但是前端如果做参数加密，还是绕不开 js 逆向。
"""
import os.path, execjs

from utils.json_paser import PRIVATE_CONFIG

rsa_modulo = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
rsa_e = '010001'

_jstext = ''
_curr_dir = os.path.dirname(__file__)
with open(_curr_dir + '/./crypto_rsa.js', 'r', encoding='utf-8') as fd:
	while True:
		curr = fd.read()
		if curr is None or len(curr) <= 0:
			break
		_jstext += curr

# 此处需要配置 npm 路径。
CTX = execjs.compile(_jstext, cwd=PRIVATE_CONFIG['cloudmusic']['npm-path'])

def encSecKey_gen(ran_str: str):
	"""
	rsa_e 65537, 010001
    :return: 返回值作为 h { encSecKey }
	"""
	return CTX.call('c', ran_str, rsa_e, rsa_modulo)


if __name__ == '__main__':
	res = encSecKey_gen('e2yswfSf2Ac8CUpz')
	print(f'\n{res}')

# 参考答案：24ef203783fa4da8ef6e5aaf2e200a0fe014febbe59c5f6e91dc90b1381c27b4a812e9b43882449c5745e2a68c1050dd1f8f297610687bc2897ea875938acd0f76894116907775f29474f23837354692c15038ebc8584cda38d0660447b84ecb039f0d8d584cb5f69b9a6ab2a430e27d89621fb6c45a56485581d142ed663d0d
