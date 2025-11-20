#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com> in 2025
# Created at 2025年08月13日 星期三 16时59分42秒
# Last modified at 2025/10/03 星期五 00:08:26
from _js_utils.tokens_def import (
	js_tk_lut,
	JSTokTy
)
regex_deter_chars: str = 'bBdDwWsStfvrnux0[](){}*\\/$^?.+-\'"'
regex_flag_chars: str = 'mygdisuv'

def assume_regex(pre_token: JSTokTy) -> bool:
	"""
	/[/+]/mygusiv.test();/123/;
	[/123/, /456/]
	{/123/.test('hahah'): false}
	(/\/(?=121212121212121212121212)[?=111111111111]/g)

	var a = /123/, b += /123/.test('');
	var c = 1 === 2 ? /123/ : /258/;
	/endl/;
	"""
	res = JSTokTy.endl.value <= pre_token.value <= JSTokTy.lparen.value \
		and pre_token not in [js_tk_lut['++'], js_tk_lut['--']]
	res |= pre_token in [
		JSTokTy.lbrack, JSTokTy.lbrace,
		JSTokTy.semicolon, JSTokTy.colon,
		JSTokTy.qmask, JSTokTy.comma,
		JSTokTy.line_comment_ed,
		JSTokTy.comment,
		JSTokTy.block_comment_ed
		# 如果有继续加
	]
	return res

class JSReg:
	"""
	组一辈子regex好吗？

	既然要从字符流识别出 regex、/、/=、//、/*，
	就顺便调研一下化简regex吧?
	"""
	pattern: str = ''
	flags: str = ''
	is_global: bool = False
	is_sticky: bool = False
	is_unicode: bool = False
	is_ignore: bool = False
	is_multi_line: bool = False
	is_has_indices: bool = False

	is_in_match: bool # ()
	is_in_choice: bool # []
	is_repeated: bool # {}
	# TODO: 将 js regex 转为判定程序？
	def __init__(self):
		pass

