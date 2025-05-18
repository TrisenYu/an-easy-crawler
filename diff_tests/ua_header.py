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

import unittest

from fake_useragent import UserAgent
from misc_utils.header import (
	fetch_browser_fp_from_ua, 
	fetch_os_name
)


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


if __name__ == '__main__':
	unittest.main()
