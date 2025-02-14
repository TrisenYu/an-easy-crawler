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
"""
	diff_tests/estimator.py 下粗略比较了native和非native函数的执行用时，结果表明混淆后造成性能下降10~100倍。
	需特别注意混淆js脚本出入字符串的大小写以及格式要求。
"""
import subprocess
from functools import partial

import mmh3, math, os

if os.name == 'nt':
	_Popen = subprocess.Popen
	subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
	from Crypto.Cipher import (
		AES,
		PKCS1_v1_5
	)
	from Crypto.PublicKey import RSA
	from Crypto.Util.Padding import pad
	from Crypto.Util.number import bytes_to_long
	subprocess.Popen = _Popen
	del _Popen
else:
	from Crypto.Cipher import (
		AES,
		PKCS1_v1_5
	)
	from Crypto.PublicKey import RSA
	from Crypto.Util.Padding import pad
	from Crypto.Util.number import bytes_to_long

import hashlib, base64, random, binascii
from gmssl import sm4

# <简简单单> 打个 JavaScript 的断点。
_rsa_modulo = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17' \
              'a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c9387011' \
              '4af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef5' \
              '2741d546b8e289dc6935b3ece0462db0a22b8e7'
_rsa_pub2 = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4" \
            "XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfr" \
            "RxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0S" \
            "a4R4qhPO3I2MQIDAQAB\n-----END PUBLIC KEY-----"

_rsa_enc2 = PKCS1_v1_5.new(RSA.importKey(_rsa_pub2))
_sm4_enc = sm4.CryptSM4(padding_mode=sm4.PKCS7)  # PKCS7 在实现上和 PKCS5 一致。
# 下一行写法调了很久才调出来。属于是难绷了
_sm4_enc.set_key(0xbc60b8b9e4ffeffa219e5ad77f11f9e2.to_bytes(16, 'big'), sm4.SM4_ENCRYPT)
_aes_cbc_iv = b'0102030405060708'
_cloud_music_aes_cbc_key = b'0CoJUm6Qyw8W8jud'



def encSecKey_gen(ran_str: str) -> str:
	# 1. 直接 powmod
	# 2. 翻转
	global _rsa_modulo
	cur = bytes_to_long(ran_str[::-1].encode('utf-8'))
	encur = pow(cur, 0x010001, int(_rsa_modulo, 16))
	return hex(encur)[2:]


def base64_str_gen(inp: bytes) -> str:
	"""转 base64 """
	return base64.b64encode(inp).decode('iso-8859-1')


def random_16_str_gen() -> str:
	"""
	function a(a: int) {
	....var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
	....for (d = 0; d < a; d ++)
	........e = Math.random() * b.length,
	........e = Math.floor(e),
	........c += b.charAt(e);
	....return c
	}

	- function return val: 伪随机生成的16个字节
	"""
	const_base_string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	ans = ''
	for _ in range(16):
		ee = random.randint(0, len(const_base_string) - 1)
		ans += const_base_string[ee]
	return ans


def encText_gen(random_16_bytes: str, payload: str) -> str:
	def aes_cbc_encryptor(enc_key: bytes, inpt: str) -> bytes:
		"""
		:param enc_key: 加密密钥
		:param inpt: 待加密字符串
		"""
		binary_payload = pad(inpt.encode('utf8'), 16)
		aes = AES.new(enc_key, AES.MODE_CBC, iv=_aes_cbc_iv)
		return aes.encrypt(binary_payload)

	global _cloud_music_aes_cbc_key
	middle = base64_str_gen(aes_cbc_encryptor(_cloud_music_aes_cbc_key, payload))
	raw_enc = aes_cbc_encryptor(random_16_bytes.encode('iso-8859-1'), middle)
	return base64_str_gen(raw_enc)


def netease_encryptor(inp_string: str) -> tuple[dict, str]:
	"""
	:return: 加密后的 json payload 以及用于 rsa 的随机十六个字节。
	"""
	_for_Seckey = random_16_str_gen()
	ans = {
		"params"   : encText_gen(_for_Seckey, inp_string),
		"encSecKey": encSecKey_gen(_for_Seckey)
	}
	return ans, _for_Seckey


def sm4_encryptor(payload: str) -> str:
	global _sm4_enc
	return _sm4_enc.crypt_ecb(payload.encode('utf-8')).hex()



def rsa_encrypt_without_token(payload: str) -> str:
	global _rsa_enc2
	pmt = _rsa_enc2.encrypt(payload.encode('utf-8'))
	return base64_str_gen(pmt)


def netease_md5(content: str) -> str:
	return hashlib.md5(content.encode('iso-8859-1')).hexdigest()


def netease_crc32(content: str) -> str:
	return hex(binascii.crc32(content.encode('iso-8859-1')))[2:]


def netease_mmh32_checksum(mmh32: str) -> str:
	p, dig = 0, 0
	for c in mmh32:
		p += ord(c) - ord('0')
	dig, l, lt, g, gt = math.floor(p / len(mmh32)), 0, 0, 0, 0
	for c in mmh32:
		cur = ord(c) - ord('0')
		if cur < dig:
			l += cur
			lt += 1
		else:
			g += cur
			gt += 1
	lt = 1 if lt == 0 else lt
	gt = 1 if gt == 0 else gt
	cur = int((g / gt - l / lt) * 10)
	if cur < 0 or cur >= 99:
		return f'----'
	return f'{p:02d}{cur:02d}'


def netease_mmh32(content: str) -> str:
	ans = f"{mmh3.hash(content, seed=31, signed=False)}"
	return ans + netease_mmh32_checksum(ans)


def netease_mmh128(payload: str) -> str:
	_tmp = mmh3.hash128(payload.encode('iso-8859-1'), 0)
	res = _tmp.to_bytes(16, byteorder='little', signed=False).hex()
	return res


if __name__ == '__main__':
	# import sys
	# print(sys.getsizeof(crypto_rsa), sys.getsizeof(crypto_rsa2), sys.getsizeof(crypto_sm4))
	# 疑似指针，三者均为 56 字节
	from utils.json_conf_reader import PRIVATE_CONFIG
	csrf_token_json_deserializer = f'{"{"}"csrf_token":"{PRIVATE_CONFIG["user1"]["csrf_token"]}"{"}"}'
	# 应由 random_16_str_gen 生成

	# 生成 encText
	encText = encText_gen('e2yswfSf2Ac8CUpz', csrf_token_json_deserializer)
	# 生成 encSecKey
	print(netease_encryptor(csrf_token_json_deserializer)[0])
