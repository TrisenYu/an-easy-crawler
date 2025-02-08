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
from crypto.manual_deobfuscation import netease_md5

def get_val(v: str) -> str:
    res = ''
    val = int.from_bytes(v.encode('utf-16-LE'), 'little')
    if val > 255:
        res += f'&#{val};'
    else:
        res += f'{val}'
    return res

def convertor(v: str) -> str:
    res = ''
    for a in v:
        res += get_val(a)
    return res


def fetch_vistor_hash(ref_url: str, loc_url: str, cookie_siz_salt: str):
	"""
    function str2binl(d) {
        var c = new Array;
        var a = (1 << 8) - 1;
        for (var b = 0; b < d.length * 8; b += 8) {
            c[b >> 5] |= (d.charCodeAt(b / 8) & a) << b % 32
        }
        return c
    }
    function binl2hex(c) {
        var b = "0123456789abcdef";
        var d = "";
        for (var a = 0; a < c.length * 4; a++) {
            d += b.charAt(c[a >> 2] >> a % 4 * 8 + 4 & 15) + b.charAt(c[a >> 2] >> a % 4 * 8 & 15)
        }
        return d
    }
    function str_to_ent(e) {
        var a = "";
        var d;
        for (d = 0; d < e.length; d++) {
            var f = e.charCodeAt(d);
            var b = "";
            if (f > 255) {
                while (f >= 1) {
                    b = "0123456789".charAt(f % 10) + b;
                    f = f / 10
                }
                if (b == "") {
                    b = "0"
                }
                b = "#" + b;
                b = "&" + b;
                b = b + ";";
                a += b
            } else {
                a += e.charAt(d)
            }
        }
        return a
    }
	function fetch_visitor_hash() {
        var c = new Date;
        # referer: https://music.163.com/
        # location: "https://music.163.com/discove"
        var a = str_to_ent(
            c.getTime() + Math.random() + document.location + document.referrer +
            screen.width + screen.height + navigator.userAgent + document.cookie +
            document.body.clientWidth + ":" + document.body.clientHeight
        );
        return ntes_hex_md5(a)
    }
    str_to_ent("卧槽马绝杀") = "&#21351;&#27133;&#39532;&#32477;&#26432;"
	"""
	return netease_md5(convertor(f"{int(time.time() * 1000) + random.random()}{loc_url}{ref_url}{cookie_siz_salt}"))


if __name__ == "__main__":
	fetch_vistor_hash()
