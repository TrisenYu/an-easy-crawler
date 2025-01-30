#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY


import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")  # 不加等着被 execjs 抛出的 gbdk 编码失效锤。

import os.path, execjs
from utils.json_paser import PRIVATE_CONFIG
from file_operator import load_readable_txt_from_file
rsa_modulo = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17' \
             'a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c9387011' \
             '4af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef5' \
             '2741d546b8e289dc6935b3ece0462db0a22b8e7'

_CURR_DIR = os.path.dirname(__file__)
try:
	crypto_sm4 = execjs.compile(load_readable_txt_from_file(_CURR_DIR + '/./crypto_sm4.js'))
	crypto_rsa = execjs.compile(load_readable_txt_from_file(_CURR_DIR + '/./crypto_rsa.js'),
	                            cwd=PRIVATE_CONFIG['cloudmusic']['npm-path'])
	crypto_rsa2 = execjs.compile(load_readable_txt_from_file(_CURR_DIR + '/./crypto_rsa2.js'))
except Exception as e:
	print(e)
	exit(1)

def encSecKey_gen(ran_str: str):
	"""
	rsa_e 65537, 0x010001
	:return: 返回值作为 h { encSecKey }
	"""
	global crypto_rsa, rsa_modulo
	# 此处需要配置 npm 路径。
	return crypto_rsa.call('c', ran_str, '010001', rsa_modulo)

def sm4_encryptor(payload: str):
	"""
	:return: 返回网易云前端 sm4 加密后的值
	"""
	global crypto_sm4
	return crypto_sm4.call('cloudmusic_sm4_encrypt', payload)

def rsa_encrypt_without_token(payload: str):
	global crypto_rsa2
	return crypto_rsa2.call('pwd_encrypt_wrapper', payload)


if __name__ == '__main__':
	# import sys
	# print(sys.getsizeof(crypto_rsa), sys.getsizeof(crypto_rsa2), sys.getsizeof(crypto_sm4))
	# 疑似指针，三者均为 56 字节

	res = encSecKey_gen('e2yswfSf2Ac8CUpz')
	print(f'\n{res}')
	# 参考答案：24ef203783fa4da8ef6e5aaf2e200a0fe014febbe59c5f6e91dc90b1381c27b4a812e9b4
	# 3882449c5745e2a68c1050dd1f8f297610687bc2897ea875938acd0f76894116907775f29474f238
	# 37354692c15038ebc8584cda38d0660447b84ecb039f0d8d584cb5f69b9a6ab2a430e27d89621fb6c45a56485581d142ed663d0d

	res = sm4_encryptor('{"un":"whatCanIsay123haha@163.com","pkid":"KGxdbOk","pd":"music",'
	                    '"channel":0,"topURL":"https://music.163.com/",'
	                    '"rtid":"ivai2ozLZcH3MH9GfTtLK2e8Lf5cHL2z"}')
	print(res)
	# 参考 '{"encParams":"6bf50cfdbac1dbd512f8f01a7851c8a9df78bafaa05a057770d33fdfb74109
	# e8de41cd3f56c9f809b37b06fa8e05b2f88dacbdca0dccc5e22774eeb3b913071bd7e88947977e27a
	# 85753ff75b15ed7042a285436209c6c5453e1faf244ce8f6a36c627daad5ffcc62536bc9cebf3a026
	# 16f594768f38c4f35db46cf5645e5f319c5b232dfe7cce39a7b81d9da746fe2c2dc1f34cc4394a5605be29b684763195"}'

	res = rsa_encrypt_without_token("123456abcdhahaha")
	print(res)
