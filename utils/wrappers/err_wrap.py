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
from functools import wraps


def throw_err_if_any(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		try:
			return fn(*args, **kwargs)
		except Exception as e:
			DEBUG_LOGGER.error(f'{e}')
			return None

	return wrapper


def throw_quietly(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		try:
			return fn(*args, **kwargs)
		finally:
			return None

	return wrapper


def die_if_err(fn):
	@wraps(fn)
	def error_dumper(*args, **kwargs):
		try:
			return fn(*args, **kwargs)
		except Exception as e:
			DEBUG_LOGGER.critical(f'{e}')
			exit(1)

	return error_dumper
