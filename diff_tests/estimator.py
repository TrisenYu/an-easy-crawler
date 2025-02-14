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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.

"""
测试用例兼执行速度评估。
"""
from utils.args_loader import PARSER
from utils.wrappers.perf_wrap import get_interval
from utils.wrappers.logic_wrap import (
	check_eq_after_time_gauge,
	check_eq
)
from utils.logger import DEBUG_LOGGER
from utils.json_conf_reader import PRIVATE_CONFIG
from crypto.manual_deobfuscation import (
	encSecKey_gen,
	encText_gen,
	netease_encryptor,
	sm4_encryptor,
	rsa_encrypt_without_token,
	netease_crc32,  # 不提供混淆脚本解释执行，只检查是否构成对应。
	netease_mmh32,
	netease_md5
)
from crypto.mmh3_x64_128 import mmh3_x64_128
from crypto.native_js import (
	native_encSecKey_gen,
	native_encText_gen,
	native_netease_encryptor,
	native_sm4_encryptor,
	native_md5,
	native_rsa_encrypt_without_token,
	raw_mmh3,
	native_wm_nike_gen,
)
from crypto.unk_hash import unk_hash

args = PARSER.parse_args()


@check_eq_after_time_gauge(
	'24ef203783fa4da8ef6e5aaf2e200a0fe014febbe59c5f6e91dc90b1381c27b4a812e9b43882449c5745e'
	'2a68c1050dd1f8f297610687bc2897ea875938acd0f76894116907775f29474f23837354692c15038ebc8'
	'584cda38d0660447b84ecb039f0d8d584cb5f69b9a6ab2a430e27d89621fb6c45a56485581d142ed663d0d'
)
@get_interval
def evaluation1():
	return encSecKey_gen('e2yswfSf2Ac8CUpz')


@check_eq_after_time_gauge(
	'24ef203783fa4da8ef6e5aaf2e200a0fe014febbe59c5f6e91dc90b1381c27b4a812e9b43882449c5745e'
	'2a68c1050dd1f8f297610687bc2897ea875938acd0f76894116907775f29474f23837354692c15038ebc8'
	'584cda38d0660447b84ecb039f0d8d584cb5f69b9a6ab2a430e27d89621fb6c45a56485581d142ed663d0d')
@get_interval
def comp_eval1():
	return native_encSecKey_gen('e2yswfSf2Ac8CUpz')


@check_eq_after_time_gauge(
	'28a7a3b9ba4315fee97f4a1df3bd0a61f3d8bacb54a2850968b81ed37e877c625efb8a8f389ccfa8fa11d'
	'9b997c4f6bf310d20394026284784823dacdf909f60fd9d5837a556dcbe07c3eb215eef2b4c9c1586b4a5'
	'2c95f4f65740583b41d42537e95693b76ec51213cdaefbe435154a406c63afc53ef302a6a1fe0e9f7ba9a1'
)
@get_interval
def evaluation1_5():
	return encSecKey_gen('8l08fKqcmiaAHMok')


@check_eq_after_time_gauge(
	'28a7a3b9ba4315fee97f4a1df3bd0a61f3d8bacb54a2850968b81ed37e877c625efb8a8f389ccfa8fa11d'
	'9b997c4f6bf310d20394026284784823dacdf909f60fd9d5837a556dcbe07c3eb215eef2b4c9c1586b4a5'
	'2c95f4f65740583b41d42537e95693b76ec51213cdaefbe435154a406c63afc53ef302a6a1fe0e9f7ba9a1')
@get_interval
def comp_eval1_5():
	return native_encSecKey_gen('8l08fKqcmiaAHMok')


@get_interval
def evaluation2():
	return encText_gen(
		'e2yswfSf2Ac8CUpz',
		f'{"{"}"csrf_token":"{PRIVATE_CONFIG[args.test_user]["csrf_token"]}{"}"}'
	)


@get_interval
# 每个人 token 都不一样，这里不比较了。
def comp_eval2():
	return native_encText_gen(
		'e2yswfSf2Ac8CUpz',
		f'{"{"}"csrf_token":"{PRIVATE_CONFIG[args.test_user]["csrf_token"]}{"}"}'
	)


@check_eq_after_time_gauge('WJmFWGo3WS13u8dKiWJNqzmB7Iq/b2Se3ENke5lpwZRL94gGgCBO9c5e1/THJI/v')
@get_interval
def evaluation2_5():
	return encText_gen('8l08fKqcmiaAHMok', '{"csrf_token":""}')


@check_eq_after_time_gauge('WJmFWGo3WS13u8dKiWJNqzmB7Iq/b2Se3ENke5lpwZRL94gGgCBO9c5e1/THJI/v')
@get_interval
def comp_eval2_5():
	return native_encText_gen('8l08fKqcmiaAHMok', '{"csrf_token":""}')


@check_eq_after_time_gauge(
	'noijREiPbpPLd+8eHCo9CJ6v08pl5JYNlwVhLvGtQkPRM0nT9O0wJearcacwMJ1F'
	'/Y0PWVa5RrGbrOxeTYMfi8WsoXofOJsxmrNdAGGS0g5zlV9enKPzzuEEWdKLuZ2w'
)
@get_interval
def evaluation2_9():
	return encText_gen('hahahahahahahaha', '{"ydDeviceType":"WebOnline","ydDeviceToken":"whatC4nISay?"}')


@check_eq_after_time_gauge(
	'noijREiPbpPLd+8eHCo9CJ6v08pl5JYNlwVhLvGtQkPRM0nT9O0wJearcacwMJ1F'
	'/Y0PWVa5RrGbrOxeTYMfi8WsoXofOJsxmrNdAGGS0g5zlV9enKPzzuEEWdKLuZ2w'
)
@get_interval
def comp_eval2_9():
	return native_encText_gen('hahahahahahahaha', '{"ydDeviceType":"WebOnline","ydDeviceToken":"whatC4nISay?"}')


@get_interval
def evaluation3():
	return netease_encryptor('{"csrf_token":""}')[0]


@get_interval
def com_eval3():
	return native_netease_encryptor('{"csrf_token":""}')


@check_eq_after_time_gauge(
	'6bf50cfdbac1dbd512f8f01a7851c8a9df78bafaa05a057770d33fdfb74109e8de41cd3f56c9f809b37b06fa8e05b2f88dacbdca0d'
	'ccc5e22774eeb3b913071bd7e88947977e27a85753ff75b15ed7042a285436209c6c5453e1faf244ce8f6a36c627daad5ffcc62536'
	'bc9cebf3a02616f594768f38c4f35db46cf5645e5f319c5b232dfe7cce39a7b81d9da746fe2c2dc1f34cc4394a5605be29b684763195'
)
@get_interval
def evaluation4():
	return sm4_encryptor(
		'{"un":"whatCanIsay123haha@163.com","pkid":"KGxdbOk","pd":"music",'
		'"channel":0,"topURL":"https://music.163.com/",'
		'"rtid":"ivai2ozLZcH3MH9GfTtLK2e8Lf5cHL2z"}'
	)


@check_eq_after_time_gauge(
	'6bf50cfdbac1dbd512f8f01a7851c8a9df78bafaa05a057770d33fdfb74109e8de41cd3f56c9f809b37b06fa8e05b2f88dacbdca0d'
	'ccc5e22774eeb3b913071bd7e88947977e27a85753ff75b15ed7042a285436209c6c5453e1faf244ce8f6a36c627daad5ffcc62536'
	'bc9cebf3a02616f594768f38c4f35db46cf5645e5f319c5b232dfe7cce39a7b81d9da746fe2c2dc1f34cc4394a5605be29b684763195'
)
@get_interval
def comp_eval4():
	return native_sm4_encryptor(
		'{"un":"whatCanIsay123haha@163.com","pkid":"KGxdbOk","pd":"music",'
		'"channel":0,"topURL":"https://music.163.com/",'
		'"rtid":"ivai2ozLZcH3MH9GfTtLK2e8Lf5cHL2z"}'
	)


@get_interval
def evaluation5():
	return rsa_encrypt_without_token('123')


@get_interval
def comp_eval5():
	return native_rsa_encrypt_without_token('123')


@check_eq_after_time_gauge('931d70e8')
@get_interval
def evaluation6():
	return netease_crc32("{'v':'v1.1','fp':'5735083394745,20364379824448',"
	                     "'u':'zgE1738765579303Jl3','h':'music.163.com'}")


@check_eq_after_time_gauge('20364379824448')
@get_interval
def evaluation7():
	return netease_mmh32(
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
		'Chrome/132.0.0.0 Safari/537.36###zh-CN###24###864x1536###-480######PDF Viewer::'
		'Portable Document Format::application/pdf~pdf,text/pdf~pdf$Chrome PDF Viewer::'
		'Portable Document Format::application/pdf~pdf,text/pdf~pdf$Chromium PDF Viewer::'
		'Portable Document Format::application/pdf~pdf,text/pdf~pdf$Microsoft Edge PDF Viewer::'
		'Portable Document Format::application/pdf~pdf,text/pdf~pdf$WebKit built-in '
		'PDF::Portable Document Format::'
		'application/pdf~pdf,text/pdf~pdf'
		';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
		';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
	)


# 12123839674255 文本太大了，不打算测
@check_eq_after_time_gauge('26870096765163')
@get_interval
def evaluation8():
	return netease_mmh32(
		'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0'
		'###zh-CN###24###1080x1920###-480###1###'
		'PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf$Chrome PDF Viewer::'
		'Portable Document Format::application/pdf~pdf,text/pdf~pdf$Chromium PDF Viewer::'
		'Portable Document Format::application/pdf~pdf,text/pdf~pdf$Microsoft Edge PDF Viewer::'
		'Portable Document Format::application/pdf~pdf,text/pdf~pdf$WebKit built-in PDF::'
		'Portable Document Format::application/pdf~pdf,text/pdf~pdf'
		';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
		';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;'
	)


@check_eq("QWSc1NeSGiHkuZOGViVFAtom5W37Axbdqzi7DQ+ojTxH5jA5V+VPnedcJlcIWBV3l/z+"
          "t5+kQFhHFBSmajwRDkosd9W55Uz3wOb+pcS2GdNPhhb5gCgekGCnikzsbH5F+9hc11MQ"
          "OHS\YYgRxXN8geVAfWw69gspKpCaApE39P/weKuZ")
def evaluation9():
	inp = "{'v':'v1.1','fp':'5735083394745,20364379824448'," \
	      "'u':'mV71738999513316FRV','h':'music.163.com'}"
	crc32 = netease_crc32(inp)
	return unk_hash(f"{inp}{crc32}", [-19, -86, -29, 37])


@check_eq_after_time_gauge("f4d6d7596bcd931fc5b2480e7788b4f3")
@get_interval
def evaluation9_5():
	return netease_md5(
		"1739039009597.8303https://music.163.com/1536864Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
		"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
		"NMTID=00OfA_VKxVftZ-MU0hfmHTPRgIyHQUAAAGU5s09aA; "
		"JSESSIONID-WYYY=e8EwXjZnGHUIz9e35HjBAgfOkgTVFopsa9NGCnl1Cc7"
		"%5CkZSmJWbuK%5C6v5h0lQ76GpAw6O7ECZBqWWjGd0KEDuF0nTzgrWFmhGaa8UoRhNTHF1tyGHTVNN"
		"%5Cm460bFGnf04g5q1YOr5EIrfskf%2BefCMhBVv8g4eK"
		"%2FR7MSQPmF%2FmpX2uWEx%3A1739040809575; _iuqxldmzr_=321536:747"
	)


@check_eq_after_time_gauge("f4d6d7596bcd931fc5b2480e7788b4f3")
@get_interval
def comp_eval9_5():
	return native_md5(
		"1739039009597.8303https://music.163.com/1536864Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
		"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
		"NMTID=00OfA_VKxVftZ-MU0hfmHTPRgIyHQUAAAGU5s09aA; "
		"JSESSIONID-WYYY=e8EwXjZnGHUIz9e35HjBAgfOkgTVFopsa9NGCnl1Cc7"
		"%5CkZSmJWbuK%5C6v5h0lQ76GpAw6O7ECZBqWWjGd0KEDuF0nTzgrWFmhGaa8UoRhNTHF1tyGHTVNN"
		"%5Cm460bFGnf04g5q1YOr5EIrfskf%2BefCMhBVv8g4eK"
		"%2FR7MSQPmF%2FmpX2uWEx%3A1739040809575; _iuqxldmzr_=321536:747"
	)


@check_eq_after_time_gauge("6f255bfcd732eaf2d5fd55b52df7a12b")
@get_interval
def evaluation9_7():
	# function cc() 内最后的过程
	return netease_md5("104410450417d2275475c06b99150e11dAWsBhCqtOaNLLJ25hBzWbqWXwiK99Wd")

@check_eq("6f255bfcd732eaf2d5fd55b52df7a12b")
def comp_eval9_7():
	return native_md5("104410450417d2275475c06b99150e11dAWsBhCqtOaNLLJ25hBzWbqWXwiK99Wd")

@check_eq_after_time_gauge("b69f0e3afa15fb947efef61ec84603ce")
@get_interval
def evaluation10():
	return mmh3_x64_128(
		"PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf"
	)


@check_eq_after_time_gauge("b69f0e3afa15fb947efef61ec84603ce")
@get_interval
def comp_eval10():
	return raw_mmh3(
		"PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf"
	)

# try:
# 	from crypto.mmh3_x64_128 import dll
# 	@check_eq_after_time_gauge("b69f0e3afa15fb947efef61ec84603ce")
# 	@get_interval
# 	def o_comp_eval10():
# 		mmh3_obj = dll.mmh3_x64_128(b"PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf", 394, 0)
# 		return f'{mmh3_obj.h1:08x}{mmh3_obj.h2:08x}'
# 	DEBUG_LOGGER.info(f'{o_comp_eval10()}')
# except Exception as e:
# 	DEBUG_LOGGER.warning(e)
# 	pass
"""
以上代码执行结果: 
b69f0e3afa15fb947efef61ec84603ce

2025-02-12 02:24:38,082 [estimator.py/<module>/line296]-INFO:
        ('b69f0e3afa15fb947efef61ec84603ce', 1.1600001016631722e-05)
"""

@check_eq("9ca17ae2e6ffcda170e2e6ee92f05cae8db8aff646a5ef8eb2c85f968b8fb0c742a3afbe8ce652"
          "afb59f95aa2af0fea7c3b92aa5f09dadf454aebdb7a8ee7ea8bba2a2d27b8a8c9e91e47da89e9d"
          "9bb64298b7ac8dd560f7efa3b0cb5994bab9a6e25398939aa3d47daa88f988e4618287a5d8eb73"
          "82ad9788f75bae97b7d9ea60edf599b3b867a29ca9afc4399292bda3f87d8596a4a8f23ca8b7ba"
          "d5b44888b6feccf533a5a7feb5e267f8a9a4b4d25c85ba9ad3cc37e2a3")
def comp_eval11():
	return native_wm_nike_gen('{"r":1,'
	                          '"d":"qmPnSxNwNg1BQEUVUAODJaqrkgZmkQt+",'
	                          '"i":"g0SLqXncyGovdenASqJTRpawdBSz7JTidlVT51mOHSPfwEcYTMVBQwjX7gakBYk7hyBsYgtQnIy8kT'
	                          '/+WR5mbDgNA3RNsBuwGJlGs0div41LDj2+v9gy2Tcm4wlSSPGfV2I="}')

if __name__ == "__main__":
	# 不计划做差分分析，只比较混淆造成的额外开销。
	# 鉴定为，直接跑快很多，就以上两者来看，10到1000个数量级。

	DEBUG_LOGGER.info(
		f'{evaluation1()[1]}s, {comp_eval1()[1]}s\n\t'
		f'{evaluation1_5()[1]}s, {comp_eval1_5()[1]}s\n\t'
		f'{evaluation2()[1]}s, {comp_eval2()[1]}s\n\t'
		f'{evaluation2_5()[1]}s, {comp_eval2_5()[1]}s\n\t'
		f'{evaluation2_9()[1]}s, {comp_eval2_9()[1]}s'
	)
	tmp, pmt = evaluation3(), com_eval3()
	DEBUG_LOGGER.info(
		f'{tmp[0]}\n\t{pmt[0]}\n\t'
		f'{tmp[1]}s, {pmt[1]}s'
	)
	del tmp, pmt
	DEBUG_LOGGER.info(f'{evaluation4()[1]}s, {comp_eval4()[1]}s')
	# '123' 经 PKCS1.5 标准 pad 后一般成
	# 0002||79aae568bcdb02fbe48070d3ba9ea6e1e0ecd830e52acaa91afbf1b7cc8147268b3702b7c4996
	# c57f88c2a9bceca69a538a756e41621c0ee0c12b2325be2845d77da9215dec90195ab31c320302a7bf050b65b5900||313233
	# 或者
	# 0002||94de5b1f4090b75916d957233d496d6cfaaa2f1b65190211dcb9e4ebf3c2b2ac69d230ee3dcaf
	# 911a48b8443fe209fe213c12a28df0712b9d6dde32586d3efbb3ae6a0b4a8638d94e83086da796f03e40a6d168500||313233
	# 即前接0002+{随机字符串}的形式。这导致加密结果不总是一致。从而只能看看。
	DEBUG_LOGGER.info(f'{evaluation5()[1]}s, {comp_eval5()[1]}s')
	DEBUG_LOGGER.info(f'{evaluation6()[1]}s')
	DEBUG_LOGGER.info(f'{evaluation7()}')
	DEBUG_LOGGER.info(f'{evaluation8()}')
	DEBUG_LOGGER.info(f'{evaluation9()}')
	DEBUG_LOGGER.info(f'{evaluation9_5()[1]}s, {comp_eval9_5()[1]}s\n\t'
	                  f'{evaluation10()[1]}s, {comp_eval10()[1]}s')
	DEBUG_LOGGER.info(f'{evaluation9_7()}\n\t{comp_eval9_7()}')
	DEBUG_LOGGER.info(f'{comp_eval11()}')
