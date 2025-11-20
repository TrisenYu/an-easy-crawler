#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com> in 2025
# Created at 2025年08月14日 星期四 17时33分32秒
# Last modified at 2025年08月15日 星期五 00时03分26秒
from _js_utils.unicode_aux import (
	is_id_start,
	is_id_continue
)

def check_char() -> None:
	for i in range(0, 0x10FFFF):
		c = chr(i)
		# 累计 144541 个字符可以作为标识符
		if is_id_start(c) or is_id_continue(c):
			continue
		# UnicodeEncodeError: 'utf-8' codec can't
		# encode character '\ud800' in position 0:
		# surrogates not allowed
		if 0xd800 <= i <= 0xdFFF:
			print(hex(i), f'skip due to UTF16-surrogation')
			continue
		# 总共有969570个字符不能作为标识符
		print(hex(i), chr(i))

check_char()

