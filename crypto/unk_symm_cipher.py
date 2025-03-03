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

import random
import copy
import binascii
import uuid

_f = lambda x: ''.join([x[random.randint(0, len(x) - 1)] for _ in range(3)])
_s_box_ka = [
	0xe7, 0x4f, 0xab, 0x9b, 0xbb, 0xbe, 0xe8, 0xa5, 0x44, 0x03, 0x40, 0x9d, 0x52, 0xda, 0xf9, 0xde,
	0x32, 0xcd, 0x6f, 0xb0, 0x0f, 0x14, 0x7e, 0x78, 0x1c, 0x2a, 0x8e, 0x73, 0xb5, 0x7a, 0xe2, 0x5f,
	0x63, 0x22, 0x45, 0x46, 0x50, 0x64, 0x13, 0x7c, 0xbd, 0xea, 0x3f, 0x6b, 0x5a, 0x0b, 0xb8, 0x97,
	0xc7, 0xe4, 0xed, 0x27, 0x3e, 0x37, 0xad, 0x58, 0x3a, 0x08, 0x79, 0xf5, 0xd3, 0x8a, 0x15, 0x35,
	0xd7, 0x68, 0x6a, 0xa0, 0x36, 0x16, 0xcc, 0xc5, 0x33, 0x4c, 0x11, 0xf6, 0x83, 0xd2, 0x76, 0x17,
	0xe0, 0xfe, 0x8c, 0xac, 0xe9, 0xd0, 0xba, 0xd5, 0xca, 0x2d, 0x69, 0x88, 0xdb, 0x5e, 0x18, 0x05,
	0x31, 0x7f, 0xfb, 0xcb, 0x71, 0x7d, 0xfa, 0xa4, 0x6c, 0xf7, 0xdd, 0xe6, 0x04, 0x42, 0xb6, 0xb4,
	0x6e, 0xaa, 0x2f, 0x62, 0x12, 0x02, 0x6d, 0xf0, 0x0c, 0x9f, 0x3c, 0xce, 0xd4, 0x80, 0xbc, 0x29,
	0xdc, 0x99, 0x1e, 0x34, 0x96, 0x59, 0x1d, 0x65, 0xae, 0x70, 0x20, 0x72, 0xdf, 0xa8, 0x24, 0x1b,
	0x8d, 0x89, 0x2b, 0x4d, 0xa1, 0x1a, 0x30, 0x74, 0xd9, 0x2e, 0x4b, 0xfd, 0x90, 0x3d, 0xef, 0x19,
	0xc1, 0x07, 0xc3, 0xcf, 0xe1, 0x5d, 0x25, 0x94, 0xd6, 0xc8, 0xd1, 0xa2, 0x7b, 0xb1, 0x92, 0x49,
	0x56, 0x98, 0x28, 0xb2, 0xe5, 0x2c, 0xf4, 0x54, 0x06, 0x8f, 0x75, 0x39, 0x8b, 0xa6, 0xc9, 0xf3,
	0xa3, 0x1f, 0xd8, 0x5c, 0x38, 0x66, 0xf2, 0x23, 0x77, 0x82, 0x01, 0x9e, 0x95, 0xc6, 0xee, 0x86,
	0xec, 0x93, 0x41, 0x00, 0xff, 0x5b, 0x55, 0xa7, 0x4e, 0x48, 0x51, 0x10, 0x60, 0x84, 0x9a, 0x0e,
	0x87, 0xc0, 0x0d, 0xc2, 0x81, 0xeb, 0xaf, 0x4a, 0x85, 0xc4, 0x21, 0x61, 0xb7, 0xf8, 0xe3, 0x9c,
	0x26, 0xfc, 0x91, 0xb9, 0xb3, 0x09, 0x53, 0xf1, 0xbf, 0x43, 0x57, 0x67, 0x47, 0xa9, 0x3b, 0x0a
]

_s_box_xc = [
	0x07, 0xda, 0xe4, 0x21, 0xf9, 0x42, 0x0e, 0xd0, 0x83, 0x8d, 0x8b, 0xd2, 0xf7, 0xf3, 0x5e, 0x19,
	0x9d, 0xaf, 0x24, 0xa7, 0x86, 0xc6, 0x41, 0xfa, 0xeb, 0xbb, 0x27, 0xc9, 0x17, 0xef, 0x55, 0x8a,
	0x23, 0x54, 0x82, 0x6f, 0xbc, 0xc1, 0xfb, 0xd8, 0x85, 0xf1, 0xbf, 0xf8, 0x69, 0xdf, 0x05, 0x4c,
	0x61, 0x6a, 0xea, 0x9f, 0x15, 0x18, 0xad, 0x3c, 0x29, 0x28, 0x79, 0x50, 0x2f, 0x71, 0x62, 0xac,
	0xc8, 0x2d, 0x34, 0xba, 0xd4, 0x14, 0x97, 0x36, 0x31, 0x06, 0x60, 0x47, 0x1e, 0x4f, 0xa5, 0x4d,
	0x48, 0x04, 0xee, 0x0b, 0xcd, 0x6c, 0x44, 0x74, 0x8f, 0xf2, 0x98, 0x3d, 0xca, 0xf0, 0xcc, 0x1d,
	0x16, 0xa0, 0x6e, 0x89, 0xfc, 0x01, 0xc5, 0x46, 0x70, 0x58, 0x76, 0x80, 0xd9, 0x9b, 0x91, 0x5d,
	0xc0, 0xa4, 0x38, 0xd3, 0xf6, 0x8e, 0x11, 0xa9, 0xe2, 0x1b, 0x78, 0xdb, 0x03, 0x09, 0x72, 0xb5,
	0x93, 0xb0, 0xfd, 0xed, 0xcb, 0xd6, 0xa1, 0xbd, 0x3a, 0xfe, 0xb9, 0xe6, 0xce, 0xe9, 0xe1, 0x96,
	0x77, 0xab, 0x51, 0xe8, 0x94, 0x00, 0xe3, 0xf5, 0x4a, 0x5c, 0xb2, 0x26, 0xdc, 0x2b, 0x13, 0x63,
	0x12, 0x65, 0x66, 0x52, 0x3b, 0x92, 0xb6, 0xc4, 0x90, 0xae, 0x75, 0xe5, 0x32, 0xde, 0x8c, 0x0f,
	0x84, 0xc3, 0x7d, 0x43, 0x6d, 0x56, 0xb1, 0x2e, 0xc7, 0x49, 0x67, 0x30, 0x39, 0x68, 0x1c, 0x4b,
	0xff, 0xe7, 0xd5, 0x88, 0x59, 0x37, 0x0d, 0x64, 0x57, 0xb3, 0x6b, 0x22, 0x99, 0xc2, 0x7a, 0x7e,
	0x3e, 0x4e, 0x2a, 0xa3, 0xa6, 0x9e, 0x95, 0x2c, 0x20, 0xcf, 0x0a, 0x53, 0xe0, 0x9a, 0x0c, 0xdd,
	0x33, 0x5a, 0x87, 0xd7, 0x40, 0x7f, 0x5b, 0x9c, 0x25, 0x02, 0xb8, 0x5f, 0x08, 0x3f, 0x1a, 0xec,
	0x45, 0xbe, 0x10, 0x7b, 0xd1, 0xaa, 0xa2, 0xb4, 0xf4, 0x73, 0x35, 0xa8, 0x7c, 0xb7, 0x81, 0x1f
]

_k1 = "IUoKOfRm31Ck\e/EdVbz6XNHt5W+24P9i7Gc80xuFshSyYnDgZvljaABwrTQpJqM"  # 缺 L

# TODO: k2, c2 这两个换得很频繁，在后端架构没有太大变动的情况下，需要通过自动化的方法来获取。否则需要一直人工干预更新。
k2_1 = "icB3gaKm8J4fkrF9.2ZI651Wqw+xCDLMRbQYotu0/dXzjT7hnSspGyvleOVEUHNA" # 缺 P
k2_2 = "NiYht0P.fcLyE8RH2dZXj1GCMFpWqvlAQT/4sw7amebBk6nUxKIJr5zuOV+SogD9" # 缺 3
k2_3 = "qXNSC3WT67dGu4IsraKFn50Q/fotxypA2Oi.gmU+MbJjLkvZYRw81eh9BVPHEzcD" # 缺 l
k2_d = "MB.CfHUzEeJpsuGkgNwhqiSaI4Fd9L6jYKZAxn1/Vml0c5rbXRP+8tD3QTO2vWyo" # 缺 7
c2_1 = "87d2d49c491940d1ad3b8fcf7c295567"
c2_2 = "77c41e1486ec4773a35957f68abc7e33"
c2_3 = "ef8c9f09464240e5974d364643e19e27"
c2_d = "fd6a43ae25f74398b61c03c83be37449"


_aux_arr_ka = [
	0xf2, 0xf1, 0xf0, 0xef, 0xee, 0xed, 0xec, 0xeb, 0xea, 0xe9, 0xe8, 0xe7, 0xe6, 0xe5, 0xe4, 0xe3,
	0xe2, 0xe1, 0xe0, 0xdf, 0xde, 0xdd, 0xdc, 0xdb, 0xda, 0xd9, 0xd8, 0xd7, 0xd6, 0xd5, 0xd4, 0xd3,
	0xd2, 0xd1, 0xd0, 0xcf, 0xce, 0xcd, 0xcc, 0xcb, 0xca, 0xc9, 0xc8, 0xc7, 0xc6, 0xc5, 0xc4, 0xc3,
	0xc2, 0xc1, 0xc0, 0x3f, 0x3e, 0x3d, 0x3c, 0x3b, 0x3a, 0xb9, 0xb8, 0xb7, 0xb6, 0xb5, 0xb4, 0xb3
]


def _fet_via_sbox(arr: list[int], sb: list[int]):
	res = []
	for a in arr:
		res.append(sb[(a >> 4 & 0xF) * 0x10 + (a & 0xF)])
	return res


def _necessary_pad(inp: str) -> list[int]:
	lenp, _for_pad = len(inp), 60
	if lenp & 0x3F > 60:
		_for_pad = 124
	choice = _for_pad - (lenp & 0x3F)
	res = [ord(_) for _ in inp]
	for _ in range(choice):
		res.append(0)
	for _ in range(3, -1, -1):  # 大端序
		res.append((lenp >> (_ << 3)) & 0xFF)
	if len(res) & 0x3F != 0:
		raise ValueError('unable to pad in the multiples of 64')
	return res


# decode 有点费脑
def custom_encode(inp_list: list[int], key: str, pad: str):
	def _3_2_4(i: int, j: int):
		if j == 1:
			return f"{key[(inp_list[i] >> 2) & 0x3F]}{key[(inp_list[i] << 4) & 0x30]}{pad * 2}"
		elif j == 2:
			return f'{key[(inp_list[i] >> 2) & 0x3F]}' \
			       f'{key[((inp_list[i] << 4) & 0x30) + ((inp_list[i + 1] >> 4) & 0x0F)]}' \
			       f'{key[((inp_list[i + 1] << 2) & 0x3C)]}{pad}'
		return f'{key[(inp_list[i] >> 2) & 0x3F]}' \
		       f'{key[((inp_list[i] << 4) & 0x30) + ((inp_list[i + 1] >> 4) & 0x0F)]}' \
		       f'{key[((inp_list[i + 1] << 2) & 0x3C) + ((inp_list[i + 2] >> 6) & 0x03)]}' \
		       f'{key[(inp_list[i + 2]) & 0x3F]}'

	res, lena = '', len(inp_list)
	jdx, remain = 0, lena % 3
	for idx in range(0, len(inp_list), 3):
		res += _3_2_4(idx, min(lena, idx + 3) - idx)
		jdx = idx
	if remain == 0:
		return res
	return res + _3_2_4(jdx, remain)


def unk_block(inp: str, assign: list[int] = None) -> str:
	"""
	core.js JSESSIONID-WYYY
	:param inp: inp 带有 crc32 后缀的字典。
	:param assign: 4 个随机数
	:return: 编码后的 base64
	"""
	tt, ext_y = "14744d95383cd3075DA42C93cDaAe7465CFA5fC0B93B1", []

	if assign is None or len(assign) < 4:
		y = [random.randint(0, 255) for _ in range(4)]
	else:
		y = [assign[_] for _ in range(4)]

	fet = lambda x: (x & 0xFF)
	for _ in range(64):
		ext_y.append(fet(ord(tt[_ % 45])) ^ fet(y[_ & 0x3]))
	E = copy.deepcopy(ext_y)

	parr = _necessary_pad(inp)

	for i in range(0, len(parr), 64):
		v0 = -39
		for j in range(64):
			parr[i + j] = fet(parr[i + j] + v0) ^ _aux_arr_ka[j] ^ ext_y[j]
			parr[i + j] = fet(E[j] + parr[i + j]) ^ E[j]
			v0 = v0 + 1
		E = _fet_via_sbox(_fet_via_sbox(parr[i:i + 64], _s_box_ka), _s_box_ka)
		for _ in E:
			y.append(_)
	del ext_y, parr, E
	return custom_encode(y, _k1, 'L')


def unk_block2(inp: str, assign: list[int] = None, ck: str = c2_3, enck: str = k2_3, padk: str = 'l') -> str:
	""" watchman.js ? """
	if assign is None or len(assign) < 4:
		y = [random.randint(0, 255) for _ in range(4)]
	else:
		y = [assign[_] for _ in range(4)]
	fet = lambda x: (x & 0xFF)
	parr = _necessary_pad(inp + hex(binascii.crc32(inp.encode('iso-8859-1')))[2:])

	ext_y = []
	for _ in range(64):
		ext_y.append(fet(ord(ck[_ & 0x1F])) ^ fet(y[_ & 0x3]))
	d = copy.deepcopy(ext_y)

	for i in range(0, len(parr), 64):
		v2, v3 = -54, 32
		for j in range(64):
			parr[i + j] = fet(parr[i + j] - 128)
			parr[i + j] = fet(parr[i + j] ^ v2)
			parr[i + j] = fet(parr[i + j] + v3) ^ ext_y[j]
			parr[i + j] = fet((parr[i + j] + d[j]) ^ d[j])
			v2, v3 = v2 + 1, v3 + 1
		d = _fet_via_sbox(_fet_via_sbox(parr[i:i + 64], _s_box_xc), _s_box_xc)
		for _ in d:
			y.append(_)
	del ext_y, parr, d
	return custom_encode(y, enck, padk)


def netease_wmjsonp_guid() -> str:
	return uuid.uuid4().bytes.hex()[2:]


if __name__ == "__main__":
	payload = b'\x00\x09\x00\x10\x59\x44\x30\x30\x30\x30\x30\x35\x35\x38\x39\x32\x39\x32\x35\x31\x00' \
	          b'\x01\x00\x0e\x32\x2e\x37\x2e\x35\x5f\x61\x66\x32\x39\x35\x32\x61\x34\x03\x24\x00\x08' \
	          b'\x31\x35\x36\x39\x64\x36\x35\x65\x03\x20\x00\x08\x66\x35\x30\x37\x31\x64\x32\x63\x00' \
	          b'\x05\x00\x04\x67\xa9\x98\xe9\x00\x06\x00\x01\x01\x03\x21\x00\x08\x30\x63\x30\x32\x30' \
	          b'\x39\x66\x38\x00\x00\x00\x03\x32\x30\x30\x00\x08\x00\x00\x00\x07\x00\x00\x00\x04\x00' \
	          b'\x20\x36\x61\x61\x39\x30\x38\x65\x34\x63\x34\x63\x39\x34\x35\x31\x33\x39\x62\x34\x39' \
	          b'\x34\x39\x62\x36\x38\x34\x63\x66\x63\x35\x38\x61\x00\xd6\x00\x07\x75\x6e\x6b\x6e\x6f' \
	          b'\x77\x6e\x00\xce\x00\x01\x14\x00\xe4\x00\x01\x01\x00\xdf\x00\x01\x02\x00\xc9\x00\x05' \
	          b'\x7a\x68\x2d\x43\x4e\x00\xee\x00\x00\x00\xe1\x00\x01\x02\x00\xe9\x00\x67\x35\x2e\x30' \
	          b'\x20\x28\x57\x69\x6e\x64\x6f\x77\x73\x20\x4e\x54\x20\x31\x30\x2e\x30\x3b\x20\x57\x69' \
	          b'\x6e\x36\x34\x3b\x20\x78\x36\x34\x29\x20\x41\x70\x70\x6c\x65\x57\x65\x62\x4b\x69\x74' \
	          b'\x2f\x35\x33\x37\x2e\x33\x36\x20\x28\x4b\x48\x54\x4d\x4c\x2c\x20\x6c\x69\x6b\x65\x20' \
	          b'\x47\x65\x63\x6b\x6f\x29\x20\x43\x68\x72\x6f\x6d\x65\x2f\x31\x33\x32\x2e\x30\x2e\x30' \
	          b'\x2e\x30\x20\x53\x61\x66\x61\x72\x69\x2f\x35\x33\x37\x2e\x33\x36\x00\xcb\x00\x01\x01' \
	          b'\x00\xda\x00\x01\x02\x00\xd3\x00\x01\x02\x00\xde\x00\x01\x02\x00\xe5\x00\x01\x02\x00' \
	          b'\xdd\x00\x01\x01\x00\xf2\x00\x08\x06\x00\x03\x60\x06\x00\x03\x42\x00\xd4\x00\x00\x00' \
	          b'\xef\x00\x0a\x43\x53\x53\x31\x43\x6f\x6d\x70\x61\x74\x00\xd0\x00\x01\x01\x00\xec\x00' \
	          b'\x00\x00\xd1\x00\x01\x01\x00\xe7\x00\x00\x00\xc8\x00\x6f\x4d\x6f\x7a\x69\x6c\x6c\x61' \
	          b'\x2f\x35\x2e\x30\x20\x28\x57\x69\x6e\x64\x6f\x77\x73\x20\x4e\x54\x20\x31\x30\x2e\x30' \
	          b'\x3b\x20\x57\x69\x6e\x36\x34\x3b\x20\x78\x36\x34\x29\x20\x41\x70\x70\x6c\x65\x57\x65' \
	          b'\x62\x4b\x69\x74\x2f\x35\x33\x37\x2e\x33\x36\x20\x28\x4b\x48\x54\x4d\x4c\x2c\x20\x6c' \
	          b'\x69\x6b\x65\x20\x47\x65\x63\x6b\x6f\x29\x20\x43\x68\x72\x6f\x6d\x65\x2f\x31\x33\x32' \
	          b'\x2e\x30\x2e\x30\x2e\x30\x20\x53\x61\x66\x61\x72\x69\x2f\x35\x33\x37\x2e\x33\x36\x00' \
	          b'\xcf\x00\x01\x01\x00\xca\x00\x01\x18\x00\xd2\x00\x01\x02\x01\x47\x00\x00\x00\xe6\x00' \
	          b'\x07\x4d\x6f\x7a\x69\x6c\x6c\x61\x00\xed\x00\x00\x00\xeb\x00\x00\x00\xd8\x00\x10\xcc' \
	          b'\x22\x8f\xb5\xac\x6a\x41\xd0\x8d\xbf\x55\x40\x5b\xb3\xd6\xae\x00\xd7\x00\x10\xb6\x9f' \
	          b'\x0e\x3a\xfa\x15\xfb\x94\x7e\xfe\xf6\x1e\xc8\x46\x03\xce\x00\xd5\x00\x05\x57\x69\x6e' \
	          b'\x33\x32\x00\xea\x00\x11\x7a\x68\x2d\x43\x4e\x2c\x7a\x68\x2d\x54\x57\x2c\x7a\x68\x2c' \
	          b'\x74\x68\x00\xe8\x00\x08\x4e\x65\x74\x73\x63\x61\x70\x65\x00\xf3\x00\x01\x08\x01\xc3' \
	          b'\x00\x01\x01\x01\x91\x00\x01\x01\x01\x93\x00\x01\x00\x01\x94\x00\x01\x00\x01\xc2\x00' \
	          b'\x01\x07\x01\x92\x00\x00'.decode('iso-8859-1')
	print(len(payload))
	_tmp = unk_block2(payload, [-11, -12, 83, 87], c2_1, k2_1, 'P')
	print(_tmp, len(_tmp))
	print(netease_wmjsonp_guid())
	"""
	预期：HM2I5nqo12VFAGpsyIdqdmRY8lFEOoYmui/HGlRs19asuEG0BK4v3dVMHjg7jHvoCTp7UZXOFN9rox24+zmFpYm/
		 itTAvGu0z06OL8+ilZAa5GHi54aWNVNGUStl7yMVnOFomOLVGs9hLYtO+i6TFpMCgQvEk+EndQd4LcBnZCweZpAt
		 6sp79bNhv6AhypoMy+yFGFpL4ucTpkqf12i4lYGl0TK1J12NfddqFN5AFRUvGKyuSZRtOOaWeYYSSSYc7mKy1.
		 0et6aFQz2+D/XO.iRS2dfJ7lFI3fFitEiNKfssogUO1hkQR7ymxvGi4k.YseitazubvFJrUSqm9G/2JHyjntyRmn7vtEK7mwKm75xOS.4
		 gMxcwi1O.RTFwJ1kYjQa514bptA2FHfYuw6U9a0+3./fxFjwt788iaxwLs0alHh15o3+WvzXSZd74s4JKUO2NVh8ROnkQx6ddlshUsd+
		 C82sF0DOrw2WdqDMRqtn3VGm+AYQRNajaG3NrVRNBJIcekJcI/QCtqC939tWhVpx40uf7ZuYOZzRicc+0CmhZZS+ZmcV4ZHvC.gvc.
		 aLnj6WWv7cq9viViKJJ98zxcHbW8l/NxwC77JmXHBkVhZ9EfZzdik6Sk23HZV.UXvozG/vfSSvTac7QjJZSVlsW0.YIl3ObUv7n77M5VzhOQFIrgsR7aMz.
		 8JtlIMK7T+aQHkcY6fzUdfelL1ns7xCWeDEK3bdxvF8uEg8ZBnWA+4w+BH6ccjZ1h.K4ptKzLCR7DqSouJhzD2KM+.SU8chcpKNkYNWv2/ZglK.
		 GnvKcl7HAarpVBRetlxhGAkO5tZDuAWT3AQSD20LJaaRbkh7sCnO68exLx2RbTtOjO+ApOiEnU5H8TxhdBm2Jj92iYD./dhWUsD8UEtHvsLosxtDh9hpf.
		 7nu2in30p2qHsCifAiIHONFQ
	"""
