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
from misc_utils.logger import DEBUG_LOGGER
import traceback

def seize_err_if_any(logger_enable: bool = True):
	def dec(fn_with_ret_val):
		def wrapper(*args, **kwargs):
			try:
				return fn_with_ret_val(*args, **kwargs)
			except Exception as e:
				if logger_enable:
					dump_stk = traceback.format_exc()
					DEBUG_LOGGER.error(f'{e}\n{dump_stk}')
			return None
		return wrapper
	return dec


def die_if_err(logger_enable: bool = True):
	def dec(fn):
		def error_dumper(*args, **kwargs):
			try:
				return fn(*args, **kwargs)
			except Exception as e:
				dump_stk = traceback.format_exc()
				if logger_enable:
					DEBUG_LOGGER.critical(f'{e}\n{fn}\n{dump_stk}')
				exit(1)
		return error_dumper
	return dec
