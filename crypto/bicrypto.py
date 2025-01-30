#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64, random
from crypto.manual_deobfuscation import encSecKey_gen

# <简简单单> 打个 JavaScript 的断点。
# TODO: 有没有可能以后网易的前端不会用这种写死的办法了呢？
#       或者说后端接口全变了？
aes_cbc_iv = '0102030405060708'.encode('utf8')
cloud_music_aes_cbc_key = '0CoJUm6Qyw8W8jud'.encode('utf8')

def aes_cbc_encryptor(enc_key: bytes, payload: str) -> bytes:
	"""
	:param enc_key: 加密密钥
	:param payload: 待加密字符串
	"""
	binary_payload = pad(payload.encode('utf8'), 16)
	aes = AES.new(enc_key, AES.MODE_CBC, iv=aes_cbc_iv)
	return aes.encrypt(binary_payload)


def gen_base64_str(inp: bytes):
	"""转 base64 """
	return base64.b64encode(inp).decode('iso-8859-1')


def gen_random_16_str() -> str:
	"""
	function a(a: int) {
		var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
		for (d = 0; d < a; d ++)
			e = Math.random() * b.length,
			e = Math.floor(e),
			c += b.charAt(e);
		return c
	}
	:return: 伪随机生成的16个字节
	"""
	const_base_string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	res = ''
	for _ in range(16):
		e = random.randint(0, len(const_base_string) - 1)
		res += const_base_string[e]
	return res


def encText_gen(random_16_bytes: bytes, payload: str) -> str:
	global cloud_music_aes_cbc_key
	middle = gen_base64_str(aes_cbc_encryptor(cloud_music_aes_cbc_key, payload))
	raw_enc = aes_cbc_encryptor(random_16_bytes, middle)
	return gen_base64_str(raw_enc)


def cloud_music_encryptor(inp_string: str) -> tuple[dict, str]:
	"""
	:return: 加密后的 json payload 以及用于 rsa 的随机十六个字节。
	"""
	_for_Seckey = gen_random_16_str()
	_for_params = _for_Seckey.encode('iso-8859-1')
	res = {
		"params": encText_gen(_for_params, inp_string),
		"encSecKey": encSecKey_gen(_for_Seckey)
	}
	return res, _for_Seckey


if __name__ == "__main__":
	# 首先要求依靠登录获取到 token
	from utils.json_paser import PRIVATE_CONFIG
	csrf_token_json_deserializer = f'{"{"}"csrf_token":"{PRIVATE_CONFIG["cloudmusic"]["csrf_token"]}"{"}"}'
	# 应该由gen_random_16_str 生成
	ran_str_in_used = 'e2yswfSf2Ac8CUpz'
	binary_ran_str_in_used = ran_str_in_used.encode('utf8')
	# 生成 encText
	encText = encText_gen(binary_ran_str_in_used, csrf_token_json_deserializer)
	# 生成 encSecKey
	encSecKey = encSecKey_gen(ran_str_in_used)
	data = {
		"params"   : encText,
		"encSecKey": encSecKey
	}
	print(data)
