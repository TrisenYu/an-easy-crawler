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

_x64 = lambda x: x & 0xFFFF_FFFF_FFFF_FFFF
_x32 = lambda x: x & 0xFFFF_FFFF
_add = lambda x, y: _x64(x + y)
_mul = lambda x, y: _x64(x * y)
_xor = lambda x, y: _x64(x ^ y)


def _group_s(x: str, st: int, s: int) -> int:
	res = 0
	for i in range(4):
		res |= ord(x[i + st + s]) << (i << 3)
	return res


def _rot_l(m: int, x: int) -> int:
	x &= 0x3F
	if x == 0:
		return m
	temp = bin(_x64(m))[2:].zfill(64)
	return int(temp[x:] + temp[:x], 2)


def _ari_l(m: int, x: int) -> int:
	return int(bin(_x64(m))[2:].zfill(64)[x:] + '0' * x, 2) if 0 <= x < 64 else 0


def _f_mix(x: int) -> int:
	x = _xor(x, x >> 33)
	x = _mul(x, 0xff51afd7_ed558ccd)
	x = _xor(x, x >> 33)
	x = _mul(x, 0xc4ceb9fe_1a85ec53)
	return _xor(x, x >> 33)


def mmh3_x64_128(key: str = '', seed: int = 0) -> str:
	lena = len(key)
	remainder = lena & 0xF
	divable = lena - remainder
	h1, h2 = _x64(seed), _x64(seed)
	c1, c2 = 0x87c37b91_114253d5, 0x4cf5ad43_2745937f
	for i in range(0, divable, 16):
		k1 = (_x32(_group_s(key, i, 0x4)) << 32) | _x32(_group_s(key, i, 0x0))
		k2 = (_x32(_group_s(key, i, 0xC)) << 32) | _x32(_group_s(key, i, 0x8))

		k1 = _mul(_rot_l(_mul(k1, c1), 31), c2)
		h1 = _add(_mul(_add(_rot_l(_xor(h1, k1), 27), h2), 5), 0x52dce729)

		k2 = _mul(_rot_l(_mul(k2, c2), 33), c1)
		h2 = _add(_mul(_add(_rot_l(_xor(h2, k2), 31), h1), 5), 0x38495ab5)

	k1, k2 = 0, 0
	while remainder != 0:
		cur = _x32(ord(key[remainder - 1 + divable]))
		if 9 < remainder < 16:
			k2 = _xor(k2, _ari_l(cur, (remainder - 9) * 8))
			remainder -= 1
			continue
		elif 1 < remainder < 9:
			k1 = _xor(k1, _ari_l(cur, (remainder - 1) * 8))
			remainder -= 1
			continue
		elif remainder == 9:
			k2 = _mul(_rot_l(_mul(_xor(k2, cur), c2), 33), c1)
			h2 = _xor(h2, k2)
			remainder -= 1
			continue
		elif remainder == 1:
			k1 = _mul(_rot_l(_mul(_xor(k1, cur), c1), 31), c2)
			h1 = _xor(h1, k1)
			break

	h1 = _xor(h1, lena)
	h2 = _xor(h2, lena)
	h1 = _add(h1, h2)
	h2 = _add(h2, h1)
	h1 = _f_mix(h1)
	h2 = _f_mix(h2)
	h1 = _add(h1, h2)
	h2 = _add(h2, h1)
	return f'{h1:08x}{h2:08x}'


# try:
# 	from ctypes import cdll, Structure, c_ulonglong
# 	import os
# 	if os.name == 'nt':
# 		# mmh3_x64_128_win.dll
# 		p = os.path.join(os.path.dirname(__file__), 'mmh3_x64_128_win.dll')
# 	else:
# 		p = os.path.join(os.path.dirname(__file__), 'mmh3_x64_128.so')
# 	dll = cdll.LoadLibrary(p)
# 	class x128(Structure):
# 		_fields_ = [("h1", c_ulonglong),
# 					("h2", c_ulonglong)]
# 	dll.mmh3_x64_128.restype = x128
# 	# 直接在这里用字节串，避免错误。
# 	h = dll.mmh3_x64_128(b"PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf", 394, 0)
# 	print(f'{h.h1:08x}{h.h2:08x}')
# except Exception as e:
# 	print(e)
# 	pass


if __name__ == "__main__":
	print(mmh3_x64_128("PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
	                   "Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
	                   "Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
	                   "Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
	                   "WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf"))
	print(mmh3_x64_128("卧槽马绝杀"))