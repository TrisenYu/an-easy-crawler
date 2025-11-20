# !/usr/bin/env/python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025-06>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/26 星期日 21:22:46
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
from typing import Optional
from functools import partial


def dic2ease_json_str(dic: dict) -> str:
	"""将dict的字符串表示替换为浏览器中javascript的规范"""
	res = ''
	for _ in dic.__str__():
		if _ == "'":
			res += '"'
			continue
		elif _ == ' ':
			continue
		res += _
	return res


def _strip_x(inp: str, x: str) -> str:
	res: str = ''
	for c in inp:
		if c == x:
			continue
		res += c
	return res


strip_underscore = partial(_strip_x, x='_')
strip_space = partial(_strip_x, x=' ')


def streplacer(
	inp: str,
	unwant: Optional[list[str]]=None, # TODO: set 可能会更高效一点？
	ch: str='_'
) -> str:
	"""
	将输入字符串(inp)中不想要(unwant)的字符列表替换为给定的字符(ch)
	然后作为结果返回
	"""
	if unwant is None:
		unwant = [
			'~', ',', ';', ' ', ':', '\\', '|', '/', '<', '>', '$',
            '%', '^', '&', '*', '(', ')', '[', ']', '{', '}',
            '!', '@', '#', '"', '\'', '?'
		]
	return ''.join([_ if _ not in unwant else ch for _ in inp])
