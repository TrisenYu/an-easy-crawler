#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/09/28 星期日 16:51:59
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

import unittest
import random

from fake_useragent import UserAgent
from user_agents import parse


def fetch_browser_fp_from_ua(inp: str) -> str:
	return parse(inp).browser.family.lower().split(' ')[0]


def fetch_os_name(inp: str) -> str:
	name = parse(inp).get_os().split(' ')[0]
	if name in ['Ubuntu']:
		return 'Linux'
	elif name == 'Chrome':
		return random.choice(['Chrome OS', 'Chromium OS'])
	elif name == 'Mac':
		return random.choice(["macOS", "iOS"])
	return name


class MyTestCase(unittest.TestCase):
	def test_BROWSER(self):
		ua_obj = UserAgent(browsers=["Chrome", "Firefox", "Edge", 'Safari'])
		for _ in range(1_000):
			with self.subTest(i=_):
				self.assertIn(
					fetch_browser_fp_from_ua(ua_obj.random),
					["chrome", "safari", "edge", "firefox"],
					"bad browser choice"
				)

	def test_OSNAME(self):
		ua_obj = UserAgent(browsers=["Chrome", "Firefox", "Edge", 'Safari'])
		for _ in range(1_000):
			with self.subTest(i=_):
				self.assertIn(
					fetch_os_name(ua_obj.random),
					# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Sec-CH-UA-Platform
					["Android", "Chrome OS", "Chromium OS", "iOS", "Linux", "macOS", "Windows", "Unknown"],
					"bad os choice"
				)


# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15
# Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36
if __name__ == '__main__':
	unittest.main()
