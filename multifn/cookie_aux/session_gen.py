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
import time
import random

from crypto_aux.manual_deobfus import (
	netease_crc32,
	netease_mmh32_checksum
)
from crypto_aux.unk_symm_cipher import unk_block


_inject_str = "aZbY0cXdW1eVf2Ug3Th4SiR5jQk6PlO7mNn8MoL9pKqJrIsHtGuFvEwDxCyBzA"
_f = lambda x: ''.join([x[random.randint(0, len(x) - 1)] for _ in range(3)])

def just_crack_cookie() -> str:
	a, b = random.getrandbits(32), random.getrandbits(32)
	inpt = f"{'{'}'v':'v1.1','" \
	       f"fp':'{a}{netease_mmh32_checksum(f'{a}')},{b}{netease_mmh32_checksum(f'{b}')}'," \
	       f"'u':'{_f(_inject_str)}{int(time.time() * 1000)}{_f(_inject_str)}','h':'music.163.com'{'}'}"
	return unk_block(f'{inpt}{netease_crc32(inpt)}')


if __name__ == "__main__":
	payload = just_crack_cookie()
	print(f'dec(JSESSIONID-WYYY)={payload}; _iuqxldmzr_=32')
	print(unk_block(payload))
