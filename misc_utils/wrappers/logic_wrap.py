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
from typing import Any

from loguru import logger

from misc_utils.logger import GLOB_LOG_FORMAT, GLOB_TEST_LOG_PATH

logger.remove()
logger.add(
	GLOB_TEST_LOG_PATH, colorize=True,
	rotation="16MB", format=GLOB_LOG_FORMAT,
	compression='zip', enqueue=True, encoding='utf-8'
)

def eq_check_after_time_gauge(payload):
	def dec(fn):
		def wrapper(*args, **kwargs):
			_ans, _spining = fn(*args, **kwargs)
			if _ans != payload:
				logger.warning('not eq!')
			return _ans, _spining
		return wrapper
	return dec


def eq_check(payload: Any):
	def dec(fn):
		def wrapper(*args, **kwargs):
			_ans: Any = fn(*args, **kwargs)
			if _ans != payload:
				logger.warning('not eq!')
			return _ans
		return wrapper
	return dec