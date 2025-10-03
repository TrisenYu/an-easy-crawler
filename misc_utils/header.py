#!/usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/09/11 星期四 21:13:52
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
"""
http header
"""
import random

from fake_useragent import UserAgent
from user_agents import parse

_ua = UserAgent(browsers=["Chrome", "Firefox", "Edge", 'Safari']).random


def _fetch_browser_fp_from_ua(inp: str) -> str:
	return parse(inp).browser.family.lower().split(' ')[0]


def _fetch_os_name(inp: str) -> str:
	name = parse(inp).get_os().split(' ')[0]
	if name in ['Ubuntu']:
		return 'Linux'
	elif name == 'Chrome':
		return random.choice(['Chrome OS', 'Chromium OS'])
	elif name == 'Mac':
		return random.choice(["macOS", "iOS"])
	return name


# 不同进程的内存空间互相隔离，不会影响。除了其它程序的读写文件操作。
BROWSER: str = _fetch_browser_fp_from_ua(_ua)
HEADER: dict[str, str] = {
	"Accept"			: "text/html,application/xhtml+xml,application/xml,"
						  "application/json,text/javascript;"
						  "q=0.9,image/avif,image/webp,image/apng,*/*;"
						  "q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Accept-Language"   : "zh-CN,zh-TW,en-US;q=0.9,zh;q=0.8,th;q=0.7",
	"Cache-Control"		: "no-cache",
	"Connection"		: "keep-alive",
	# TODO: 后面不一定要用这个网站了, 或者说需要用一个更通用的方法来
	# 同等对待所有网站
	"Host"				: "music.163.com",
	"Pragma"			: "no-cache",
	"Sec-Fetch-Dest"	: "iframe",
	"Sec-Fetch-Mode"	: "navigate",
	"Sec-Fetch-Site"	: "same-origin",
	"User-Agent"		: f"{_ua}",
	"Sec-Ch-Ua-Platform": _fetch_os_name(_ua)
}

def alter_header(inp: dict[str, str]) -> None:
	"""增添不存在的项或者修改已存在的项"""
	for k in inp:
		HEADER[k] = inp[k]


if __name__ == "__main__":
	print(HEADER["User-Agent"])
	print(BROWSER, type(BROWSER))
