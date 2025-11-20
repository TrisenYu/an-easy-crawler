#!/usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/26 星期日 14:51:47
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
伪装 http header
"""
import random

from fake_useragent import UserAgent
from user_agents import parse


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


def gen_fake_browser_and_http_header() -> tuple[str, dict[str, str]]:
	"""
	:return: 浏览器字符串, http header
	"""
	ua = UserAgent(browsers=["Chrome", "Firefox", "Edge", 'Safari']).random
	browser = _fetch_browser_fp_from_ua(ua)
	header = {
		"Accept"			: "text/html,application/xhtml+xml,application/xml,"
							  "application/json,text/javascript;"
							  "q=0.9,image/avif,image/webp,image/apng,*/*;"
							  "q=0.8,application/signed-exchange;v=b3;q=0.7",
		"Accept-Language"   : "zh-CN,zh-TW,en-US;q=0.9,zh;q=0.8,th;q=0.7",
		"Cache-Control"		: "no-cache",
		"Connection"		: "keep-alive",
		"Pragma"			: "no-cache",
		"Sec-Fetch-Dest"	: "iframe",
		"Sec-Fetch-Mode"	: "navigate",
		"Sec-Fetch-Site"	: "same-origin",
		"User-Agent"		: f"{ua}",
		"Sec-Ch-Ua-Platform": _fetch_os_name(ua)
	}
	return browser, header

def alter_header(
	inject: dict[str, str],
	orig_header: dict[str, str]
) -> dict[str, str]:
	"""增添不存在的项或者修改已存在的项"""
	for k in inject:
		orig_header[k] = inject[k]
	return orig_header


if __name__ == "__main__":
	pass