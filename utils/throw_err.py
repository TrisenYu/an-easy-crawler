#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
from utils.logger import DEBUG_LOGGER
from functools import wraps


def throw_err_if_exist(fn):
	@wraps(fn)
	def wrapper(*args, **kwargs):
		try:
			return fn(*args, **kwargs)
		except Exception as e:
			DEBUG_LOGGER.info(f'{e}')
			return None

	return wrapper


def throw_err_quietly(fn):
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
			DEBUG_LOGGER.error(f'{e}')
			exit(1)

	return error_dumper
