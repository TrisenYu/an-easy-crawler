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
from utils.logger import DEBUG_LOGGER


def check_eq_after_time_gauge(payload):
	def dec(fn):
		def wrapper(*args, **kwargs):
			_ans, _spining = fn(*args, **kwargs)
			if _ans != payload:
				DEBUG_LOGGER.warn('not eq!')
			return _ans, _spining
		return wrapper
	return dec


def check_eq(payload):
	def dec(fn):
		def wrapper(*args, **kwargs):
			_ans = fn(*args, **kwargs)
			if _ans != payload:
				DEBUG_LOGGER.warn('not eq!')
			return _ans
		return wrapper
	return dec