#!/usr/bin/env python3
# -*- coding: utf8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/02 星期四 23:34:31
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
import logging
import os
from misc_utils.time_aux import (
	LOG_TIME_FORMAT,
	curr_time_formatter
)

class _CustomFormatter(logging.Formatter):
	"""
	Logging colored formatter, adapted from and thanks to:
		- stackoverflow.com/a/56944256/3638629
		- alexandra-zaharia.github.io/posts/make-your-own-custom-color-formatter-with-python-logging/
	"""

	grey = '\x1b[38;21m'
	blue = '\x1b[38;5;39m'
	yellow = '\x1b[38;5;226m'
	red = '\x1b[38;5;196m'
	bold_red = '\x1b[31;1m'
	reset = '\x1b[0m'

	def __init__(self, fmt: str):
		super().__init__()
		self.fmt = fmt
		self.FORMATS = {
			logging.DEBUG   : self.grey + self.fmt + self.reset,
			logging.INFO    : self.blue + self.fmt + self.reset,
			logging.WARNING : self.yellow + self.fmt + self.reset,
			logging.ERROR   : self.red + self.fmt + self.reset,
			logging.CRITICAL: self.bold_red + self.fmt + self.reset
		}

	def format(self, record):
		log_fmt = self.FORMATS.get(record.levelno)
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)


_format = '%(asctime)s [%(filename)s|%(funcName)s|line%(lineno)d]-%(levelname)s: %(message)s'
_logfiles_handler = logging.FileHandler(
	filename=''+
		os.path.join(os.path.dirname(__file__), '../assets/stat/logs/')+
		curr_time_formatter(LOG_TIME_FORMAT)+"-debug.log"
)
_logfiles_handler.setFormatter(_CustomFormatter(_format))

DEBUG_LOGGER = logging.getLogger(__name__)
DEBUG_LOGGER.setLevel(logging.DEBUG)
DEBUG_LOGGER.addHandler(_logfiles_handler)

if __name__ == "__main__":
	DEBUG_LOGGER.info('hello world')
