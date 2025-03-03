#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
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

from fake_useragent import UserAgent
from user_agents import parse

_ua = UserAgent().random
_ua_obj = parse(_ua)
# 不同进程的内存空间互相隔离，不会影响。除了其它程序的读写文件操作。
HEADER = {
	"Accept"                   : "text/html,application/xhtml+xml,application/xml;"
	                             "q=0.9,image/avif,image/webp,image/apng,*/*;"
	                             "q=0.8,application/signed-exchange;v=b3;q=0.7",
	"Accept-Language"          : "zh-CN,zh-TW,en-US;q=0.9,zh;q=0.8,th;q=0.7",
	"Cache-Control"            : "no-cache",
	"Connection"               : "keep-alive",
	"Host"                     : "music.163.com",
	"Pragma"                   : "no-cache",
	"Sec-Fetch-Dest"           : "iframe",
	"Sec-Fetch-Mode"           : "navigate",
	"Sec-Fetch-Site"           : "same-origin",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent"               : f"{_ua}",
}

if __name__ == "__main__":
	print(HEADER["User-Agent"])
