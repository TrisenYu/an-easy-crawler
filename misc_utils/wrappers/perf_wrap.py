#!/usr/bin/env python3
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
from time import perf_counter
from functools import wraps

def get_interval(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		# TODO: perf_counter 有个问题，时间如果超过半分钟，内存就会被计算占满
		# 		如果是类似临界区的场景用，这个是没问题的
		# 但是cpu密集型任务在不需要太精确的情况下最好换成unix_time相减算
		st = perf_counter()
		ans = fn(*args, **kwargs)
		ed = perf_counter()
		return ans, ed - st
	return wrapper

