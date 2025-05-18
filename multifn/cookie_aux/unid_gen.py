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
import time, random
from crypto_aux.manual_deobfus import netease_md5

def _get_val(v: str) -> str:
	"""
	function str_to_ent(e) {
		var a = "";
		for (var d = 0; d < e.length; d++) {
			var f = e.charCodeAt(d), b = "";
			if (f < 256) {
				a += e.charAt(d);
				continue;
			}
			while (f >= 1) {
				b = "0123456789".charAt(f % 10) + b;
				f = f / 10
			}
			if (b == "") {
				b = "0"
			}
			a += "#&" + b + ";";
		}
		return a
	}
	"""
	val = int.from_bytes(v.encode('utf-16-LE'), 'little')
	return f'&#{val};' if val > 255 else f'{val}'

def _convertor(v: str) -> str:
	res = ''
	for a in v:
		res += _get_val(a)
	return res


def crack_vistor_hash(cookie_siz_salt: str = '') -> str:
	"""
	str_to_ent("卧槽马绝杀") = "&#21351;&#27133;&#39532;&#32477;&#26432;"

	>>> 'function str2binl(d) {'                                \
		'var c = new Array;'                                    \
		'var a = (1 << 8) - 1;'                                 \
		'for (var b = 0; b < d.length * 8; b += 8) {'           \
			'c[b >> 5] |= (d.charCodeAt(b / 8) & a) << b % 32'  \
		'}'                                                     \
		'return c'                                              \
	'}'                                                         \
	'function binl2hex(c) {'                                    \
		'var b = "0123456789abcdef";'                           \
		'var d = "";'                                           \
		'for (var a = 0; a < c.length * 4; a++) {'              \
			'd += b.charAt(c[a >> 2] >> a % 4 * 8 + 4 & 15) + ' \
			'b.charAt(c[a >> 2] >> a % 4 * 8 & 15)'             \
		'}'                                                     \
		'return d'                                              \
	'}'                                                         \
	'function fetch_visitor_hash() {'                           \
		'var c = new Date;'                                     \
		'# referer: https://music.163.com/'                     \
		'# location: "https://music.163.com/discove"'           \
		'var a = str_to_ent('                                   \
			'c.getTime() + Math.random() + document.location +' \
			'document.referrer + screen.width + screen.height +'\
			'navigator.userAgent + document.cookie +'           \
			'document.body.clientWidth + ":" + '                \
			'document.body.clientHeight'                        \
		');'                                                    \
		'return ntes_hex_md5(a)'                                \
	'}'
	"""
	return netease_md5(_convertor(f"{'卧槽马绝杀'}{int(time.time() * 1000) + random.random()}{cookie_siz_salt}"))


if __name__ == "__main__":
	print(crack_vistor_hash())
