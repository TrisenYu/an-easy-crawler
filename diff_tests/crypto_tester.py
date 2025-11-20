#!/usr/bin/env python3
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
from loguru import logger

from misc_utils import *
from crypto_aux import *
from crypto_aux.unk_symm_cipher import unk_block
from configs.args_loader import PARSER

args = PARSER.parse_args()

logger.remove()
logger.add(GLOB_TEST_LOG_PATH, colorize=True, rotation='16MB', format=GLOB_LOG_FORMAT, compression='zip')


@eq_check_after_time_gauge(
	'24ef203783fa4da8ef6e5aaf2e200a0fe014febbe59c5f6e91dc90b1381c27b4a812e9b43882449c5745e'
	'2a68c1050dd1f8f297610687bc2897ea875938acd0f76894116907775f29474f23837354692c15038ebc8'
	'584cda38d0660447b84ecb039f0d8d584cb5f69b9a6ab2a430e27d89621fb6c45a56485581d142ed663d0d'
)
@get_interval
def evaluation1():
	return encSecKey_gen('e2yswfSf2Ac8CUpz')


@eq_check_after_time_gauge(
	'24ef203783fa4da8ef6e5aaf2e200a0fe014febbe59c5f6e91dc90b1381c27b4a812e9b43882449c5745e'
	'2a68c1050dd1f8f297610687bc2897ea875938acd0f76894116907775f29474f23837354692c15038ebc8'
	'584cda38d0660447b84ecb039f0d8d584cb5f69b9a6ab2a430e27d89621fb6c45a56485581d142ed663d0d'
)
@get_interval
def comp_eval1():
	return native_encSecKey_gen('e2yswfSf2Ac8CUpz')


@eq_check_after_time_gauge(
	'28a7a3b9ba4315fee97f4a1df3bd0a61f3d8bacb54a2850968b81ed37e877c625efb8a8f389ccfa8fa11d'
	'9b997c4f6bf310d20394026284784823dacdf909f60fd9d5837a556dcbe07c3eb215eef2b4c9c1586b4a5'
	'2c95f4f65740583b41d42537e95693b76ec51213cdaefbe435154a406c63afc53ef302a6a1fe0e9f7ba9a1'
)
@get_interval
def evaluation1_5():
	return encSecKey_gen('8l08fKqcmiaAHMok')


@eq_check_after_time_gauge(
	'28a7a3b9ba4315fee97f4a1df3bd0a61f3d8bacb54a2850968b81ed37e877c625efb8a8f389ccfa8fa11d'
	'9b997c4f6bf310d20394026284784823dacdf909f60fd9d5837a556dcbe07c3eb215eef2b4c9c1586b4a5'
	'2c95f4f65740583b41d42537e95693b76ec51213cdaefbe435154a406c63afc53ef302a6a1fe0e9f7ba9a1'
)
@get_interval
def comp_eval1_5():
	return native_encSecKey_gen('8l08fKqcmiaAHMok')


@get_interval
def evaluation2():
	return encText_gen(
		'e2yswfSf2Ac8CUpz',
		dic2ease_json_str({
			"csrf_token": f'"{PRIVATE_CONFIG[args.test_user]["csrf_token"]}'
		})
	)


@get_interval
# 每个人 token 都不一样，这里不比较了。
def comp_eval2():
	return native_encText_gen(
		'e2yswfSf2Ac8CUpz',
		dic2ease_json_str({
			"csrf_token": f'"{PRIVATE_CONFIG[args.test_user]["csrf_token"]}'
		})
	)

@eq_check_after_time_gauge(
	"vll81oCoAzW6zfyTcCgf9pOfUuS5cVTHAW8N7qWWve4hpfqL+DNTkahXA/+e/sNQBUWSaQbkdZriFLTBq1nxxoxPcgjl/"
	"tuSYy9DN2KbMlLB0wtCoJAo3iHI8mjIAjmEzQ6MZwdBo/HZgHxjziZcwg=="
)
@get_interval
def evaluation_dev_tk():
	return encText_gen(
		'sxShr7MV15sDLCYN',
		'{"browserType":1,"csrf_token":"8c78f0d158ec4a8b5cfbab02e4174e9e"}'
	)

@eq_check_after_time_gauge('WJmFWGo3WS13u8dKiWJNqzmB7Iq/b2Se3ENke5lpwZRL94gGgCBO9c5e1/THJI/v')
@get_interval
def evaluation2_5():
	return encText_gen('8l08fKqcmiaAHMok', '{"csrf_token":""}')


@eq_check_after_time_gauge('WJmFWGo3WS13u8dKiWJNqzmB7Iq/b2Se3ENke5lpwZRL94gGgCBO9c5e1/THJI/v')
@get_interval
def comp_eval2_5():
	return native_encText_gen('8l08fKqcmiaAHMok', dic2ease_json_str({"csrf_token":""}))


@eq_check_after_time_gauge(
	'noijREiPbpPLd+8eHCo9CJ6v08pl5JYNlwVhLvGtQkPRM0nT9O0wJearcacwMJ1F'
	'/Y0PWVa5RrGbrOxeTYMfi8WsoXofOJsxmrNdAGGS0g5zlV9enKPzzuEEWdKLuZ2w'
)
@get_interval
def evaluation2_9():
	return encText_gen('hahahahahahahaha', '{"ydDeviceType":"WebOnline","ydDeviceToken":"whatC4nISay?"}')


@eq_check_after_time_gauge(
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


@eq_check_after_time_gauge(
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

#
#
@eq_check_after_time_gauge(
	"19736feba8c544a5fe33b8a884a53212af3632efa03f58d7be37e524acd92164d42a0028dca71fd138"
    "74b69d8be2d936e13038670343ecaa86270463dab98b8b15613de33180163a69a798b6d0f688bee602"
    "9a760fd21efad33c4f665d6ab3ad0acaa92b24d2b812aa6ca9bae1aeeb1fe1d4900ab689ca0caec661"
    "a28dcf39176552d54f21e0659126205454a94b1abe"
)
@get_interval
def evaluation4_4():
	return sm4_encryptor(
		'{"pd":"music","pkid":"KGxdbOk","pkht":"music.163.com",'
		'"channel":0,"topURL":"https://music.163.com/",'
		'"rtid":"ekOrYjCyuif7N2pDF6pOSUgwhvtIpIht"}'
	)

@eq_check_after_time_gauge(
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


@eq_check_after_time_gauge('931d70e8')
@get_interval
def evaluation6():
	return netease_crc32("{'v':'v1.1','fp':'5735083394745,20364379824448',"
	                     "'u':'zgE1738765579303Jl3','h':'music.163.com'}")


@eq_check_after_time_gauge('20364379824448')
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
@eq_check_after_time_gauge('26870096765163')
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


@eq_check("QWSc1NeSGiHkuZOGViVFAtom5W37Axbdqzi7DQ+ojTxH5jA5V+VPnedcJlcIWBV3l/z+"
          "t5+kQFhHFBSmajwRDkosd9W55Uz3wOb+pcS2GdNPhhb5gCgekGCnikzsbH5F+9hc11MQ"
          "OHS\YYgRxXN8geVAfWw69gspKpCaApE39P/weKuZ")
def evaluation9():
	inp = "{'v':'v1.1','fp':'5735083394745,20364379824448'," \
	      "'u':'mV71738999513316FRV','h':'music.163.com'}"
	crc32 = netease_crc32(inp)
	return unk_block(f"{inp}{crc32}", [-19, -86, -29, 37])


@eq_check_after_time_gauge("f4d6d7596bcd931fc5b2480e7788b4f3")
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


@eq_check_after_time_gauge("f4d6d7596bcd931fc5b2480e7788b4f3")
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


@eq_check_after_time_gauge("6f255bfcd732eaf2d5fd55b52df7a12b")
@get_interval
def evaluation9_7():
	# function cc() 内最后的过程
	return netease_md5("104410450417d2275475c06b99150e11dAWsBhCqtOaNLLJ25hBzWbqWXwiK99Wd")


@eq_check("6f255bfcd732eaf2d5fd55b52df7a12b")
def comp_eval9_7():
	return native_md5("104410450417d2275475c06b99150e11dAWsBhCqtOaNLLJ25hBzWbqWXwiK99Wd")


@eq_check_after_time_gauge("b69f0e3afa15fb947efef61ec84603ce")
@get_interval
def evaluation10():
	return netease_mmh128(
		"PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf"
	)


@eq_check_after_time_gauge("b69f0e3afa15fb947efef61ec84603ce")
@get_interval
def comp_eval10():
	return raw_mmh3(
		"PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
		"WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf"
	)


@eq_check_after_time_gauge("eb3c874188f9cdbdb282af734adc465e")
@get_interval
def evaluation10_5():
	return netease_mmh128(
		"acos:1.4473588658278522,acosh:709.889355822726,acoshPf:355.291251501643,"
		"asin:0.12343746096704435,asinh:0.881373587019543,asinhPf:0.8813735870195429,"
		"atanh:0.5493061443340548,atanhPf:0.5493061443340548,atan:0.4636476090008061,"
		"sin:0.8178819121159085,sinh:1.1752011936438014,sinhPf:2.534342107873324,"
		"cos:-0.8390715290095377,cosh:1.5430806348152437,coshPf:1.5430806348152437,"
		"tan:-1.4214488238747245,tanh:0.7615941559557649,tanhPf:0.7615941559557649,"
		"exp:2.718281828459045,expm1:1.718281828459045,expm1Pf:1.718281828459045,"
		"log1p:2.3978952727983707,log1pPf:2.3978952727983707,powPI:1.9275814160560204e-50"
	)


@eq_check_after_time_gauge("a1374108a0bcc1626eeb20c4052da5f1")
@get_interval
def evaluation10_7():
	return netease_mmh128("extensions:ANGLE_instanced_arrays;EXT_blend_minmax;EXT_clip_control;"
	                      "EXT_color_buffer_half_float;EXT_depth_clamp;EXT_disjoint_timer_query;"
	                      "EXT_float_blend;EXT_frag_depth;EXT_polygon_offset_clamp;EXT_shader_texture_lod;"
	                      "EXT_texture_compression_bptc;EXT_texture_compression_rgtc;"
	                      "EXT_texture_filter_anisotropic;EXT_texture_mirror_clamp_to_edge;EXT_sRGB;"
	                      "KHR_parallel_shader_compile;OES_element_index_uint;OES_fbo_render_mipmap;"
	                      "OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;"
	                      "OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;"
	                      "WEBGL_blend_func_extended;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;"
	                      "WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;"
	                      "WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBGL_multi_draw;"
	                      "WEBGL_polygon_mode,webgl aliased line width range:[1, 1],"
	                      "webgl aliased point size range:[1, 1024],webgl alpha bits:8,"
	                      "webgl antialiasing:yes,webgl blue bits:8,webgl depth bits:24,"
	                      "webgl green bits:8,webgl max anisotropy:16,"
	                      "webgl max combined texture image units:32,webgl max cube map texture size:16384,"
	                      "webgl max fragment uniform vectors:1024,webgl max render buffer size:16384,"
	                      "webgl max texture image units:16,webgl max texture size:16384,"
	                      "webgl max varying vectors:30,webgl max vertex attribs:16,"
	                      "webgl max vertex texture image units:16,webgl max vertex uniform vectors:4096,"
	                      "webgl max viewport dims:[32767, 32767],webgl red bits:8,"
	                      "webgl renderer:WebKit WebGL,webgl shading language version:WebGL GLSL ES 1.0 "
	                      "(OpenGL ES GLSL ES 1.0 Chromium),webgl stencil bits:0,webgl vendor:WebKit,"
	                      "webgl version:WebGL 1.0 (OpenGL ES 2.0 Chromium),"
	                      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACWCAYAAABkW7XSAAAAAXNSR0IArs"
	                      "4c6QAABGhJREFUeF7t1IEJADAMAkG7/9AtdIuHywRyBs+2O0eAAIGAwDFYgZZEJEDgCxgsj0CAQEbAYG"
	                      "WqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpi"
	                      "pBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEp"
	                      "QAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCR"
	                      "AwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAY"
	                      "PlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH"
	                      "6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBw"
	                      "gQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAI"
	                      "GMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyA"
	                      "gYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgM"
	                      "HKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrE"
	                      "xVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVC"
	                      "UoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVgh"
	                      "IgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQ"
	                      "IGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYL"
	                      "D8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw"
	                      "8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AA"
	                      "ECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJ"
	                      "ARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIg8ADA2JYBN9"
	                      "/scgAAAABJRU5ErkJggg==")


@eq_check_after_time_gauge("8bdad2543f873b1d51afdc996c8ce5a1")
@get_interval
def evaluation10_9():
	return netease_mmh128(
		"Agency FB,Algerian,Baskerville Old Face,Bauhaus 93,Bell MT,Berlin Sans FB,"
		"Bernard MT Condensed,Blackadder ITC,Bodoni MT,Bodoni MT Black,"
		"Bodoni MT Condensed,Bookshelf Symbol 7,Bradley Hand ITC,Broadway,Brush Script MT,"
		"Californian FB,Calisto MT,Candara,Castellar,Centaur,Chiller,Colonna MT,Constantia,"
		"Cooper Black,Copperplate Gothic,Copperplate Gothic Light,Corbel,Curlz MT,Ebrima,"
		"Edwardian Script ITC,Elephant,Engravers MT,FangSong,Felix Titling,Footlight MT Light,"
		"Forte,Freestyle Script,French Script MT,Gabriola,Gigi,Gill Sans MT,"
		"Gill Sans MT Condensed,Goudy Old Style,Goudy Stout,Haettenschweiler,"
		"Harrington,High Tower Text,Imprint MT Shadow,Informal Roman,Jokerman,Juice ITC,"
		"KaiTi,Kristen ITC,Kunstler Script,Magneto,Maiandra GD,Malgun Gothic,Marlett,"
		"Matura MT Script Capitals,Meiryo,Meiryo UI,Microsoft Himalaya,Microsoft JhengHei,"
		"Microsoft New Tai Lue,Microsoft PhagsPa,Microsoft Tai Le,Microsoft YaHei,"
		"Microsoft Yi Baiti,MingLiU_HKSCS-ExtB,MingLiU-ExtB,Mistral,Modern No. 20,"
		"Mongolian Baiti,MS Mincho,MS PMincho,MS Reference Specialty,MS UI Gothic,MT Extra,"
		"MV Boli,Niagara Engraved,Niagara Solid,NSimSun,Old English Text MT,"
		"Onyx,Palace Script MT,Papyrus,Parchment,Perpetua,Perpetua Titling MT,Playbill,"
		"PMingLiU-ExtB,Poor Richard,Pristina,Ravie,Rockwell,Rockwell Condensed,"
		"Showcard Gothic,SimHei,SimSun,SimSun-ExtB,Snap ITC,Stencil,Sylfaen,Tempus Sans ITC,"
		"Tw Cen MT,Tw Cen MT Condensed,Viner Hand ITC,Vivaldi,Vladimir Script,Wide Latin,"
		"仿宋,华文中宋,华文仿宋,华文宋体,华文彩云,华文新魏,华文楷体,华文琥珀,华文细黑,华文行楷,华文隶书,"
		"宋体,幼圆,微软雅黑,新宋体,方正姚体,方正舒体,楷体,隶书,黑体"
	)


@eq_check_after_time_gauge("00fbfdf1d384fc93e658c32156de2275")
@get_interval
def evaluation10_99():
	return netease_mmh128(
		"Google Bahasa Indonesia, Google Bahasa Indonesia, id-ID, 0, 0,"
		"Google Deutsch, Google Deutsch, de-DE, 0, 0,Google Nederlands, Google Nederlands,"
		" nl-NL, 0, 0,Google UK English Female, Google UK English Female, en-GB, 0, 0,"
		"Google UK English Male, Google UK English Male, en-GB, 0, 0,"
		"Google US English, Google US English, en-US, 0, 0,Google español de Estados Unidos,"
		" Google español de Estados Unidos, es-US, 0, 0,Google español, Google español,"
		" es-ES, 0, 0,Google français, Google français, fr-FR, 0, 0,Google italiano,"
		" Google italiano, it-IT, 0, 0,Google polski, Google polski, pl-PL, 0, 0,"
		"Google português do Brasil, Google português do Brasil, pt-BR, 0, 0,"
		"Google русский, Google русский, ru-RU, 0, 0,Google हिन्दी, Google हिन्दी, hi-IN,"
		" 0, 0,Google 國語（臺灣）, Google 國語（臺灣）, zh-TW, 0, 0,"
		"Google 日本語, Google 日本語, ja-JP, 0, 0,Google 한국의, Google 한국의, ko-KR, 0,"
		" 0,Google 普通话（中国大陆）, Google 普通话（中国大陆）, zh-CN, 0, 0,"
		"Google 粤語（香港）, Google 粤語（香港）, zh-HK, 0, 0,"
		"Microsoft Huihui - Chinese (Simplified\, PRC),"
		" Microsoft Huihui - Chinese (Simplified\, PRC), zh-CN, 1, 1,"
		"Microsoft Kangkang - Chinese (Simplified\, PRC),"
		" Microsoft Kangkang - Chinese (Simplified\, PRC),"
		" zh-CN, 1, 0,Microsoft Yaoyao - Chinese (Simplified\, PRC),"
		" Microsoft Yaoyao - Chinese (Simplified\, PRC), zh-CN, 1, 0"
	)


@eq_check_after_time_gauge("7ae481c3234821b6649b434bed036ff0")
@get_interval
def evaluation10_999():
	return netease_mmh128(
		"1111111111111111111111111111111111111111112"
		"111111111111111111111111111121111111111111111111112"
		"1111111111111111111111111111111111111111111111111111111112"
		"111111111111111111111111111111111111111111111111112"
		"11111111111111111111111111211111111111111111"
	)


@eq_check("9ca17ae2e6ffcda170e2e6ee92f05cae8db8aff646a5ef8eb2c85f968b8fb0c742a3afbe8ce652"
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

	logger.info(
		f'{evaluation1()[1]}s, {comp_eval1()[1]}s\n\t'
		f'{evaluation1_5()[1]}s, {comp_eval1_5()[1]}s\n\t'
		f'{evaluation2()[1]}s, {comp_eval2()[1]}s\n\t'
		f'{evaluation2_5()[1]}s, {comp_eval2_5()[1]}s\n\t'
		f'{evaluation2_9()[1]}s, {comp_eval2_9()[1]}s'
	)
	tmp, pmt = evaluation3(), com_eval3()
	logger.info(
		f'{tmp[0]}\n\t{pmt[0]}\n\t'
		f'{tmp[1]}s, {pmt[1]}s'
	)
	del tmp, pmt
	logger.info(f'{evaluation4()[1]}s, {comp_eval4()[1]}s')
	logger.info(f'{evaluation4_4()[1]}')
	# '123' 经 PKCS1.5 标准 pad 后一般成
	# 0002||79aae568bcdb02fbe48070d3ba9ea6e1e0ecd830e52acaa91afbf1b7cc8147268b3702b7c4996
	# c57f88c2a9bceca69a538a756e41621c0ee0c12b2325be2845d77da9215dec90195ab31c320302a7bf050b65b5900||313233
	# 或者
	# 0002||94de5b1f4090b75916d957233d496d6cfaaa2f1b65190211dcb9e4ebf3c2b2ac69d230ee3dcaf
	# 911a48b8443fe209fe213c12a28df0712b9d6dde32586d3efbb3ae6a0b4a8638d94e83086da796f03e40a6d168500||313233
	# 即前接0002+{随机字符串}的形式。这导致加密结果不总是一致。从而只能看看。
	logger.info(f'{evaluation5()[1]}s, {comp_eval5()[1]}s')
	logger.info(f'{evaluation6()[1]}s')
	logger.info(f'{evaluation7()}')
	logger.info(f'{evaluation8()}')
	logger.info(f'{evaluation9()}')
	logger.info(f'{evaluation9_5()[1]}s, {comp_eval9_5()[1]}s\n\t'
	                  f'{evaluation10()[1]}s, {comp_eval10()[1]}s')
	logger.info(f'{evaluation9_7()}\n\t{comp_eval9_7()}')
	logger.info(f'{evaluation10_5()}\n\t{comp_eval11()}')
	logger.info(f'{evaluation_dev_tk()}')
