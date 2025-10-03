# !/usr/bin/env/python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025-06>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/01 星期三 20:13:06
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

def dic2json_str(_dict: dict) -> str:
	"""将dict的字符串表示替换为浏览器中的规范"""
	res = ''
	for _ in _dict.__str__():
		if _ == '\'':
			res += '"'
			continue
		elif _ == ' ':
			continue
		res += _
	return res

from functools import partial

def _strip_x(inp: str, x: str) -> str:
	res: str = ''
	for c in inp:
		if c == x:
			continue
		res += c
	return res

strip_underscore = partial(_strip_x, x='_')
strip_space = partial(_strip_x, x=' ')
