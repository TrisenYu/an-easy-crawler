#! /usr/bin/env python3
# -*- coding: utf8 -*-
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
import logging


class CustomFormatter(logging.Formatter):
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


_format = '\n%(asctime)s [%(filename)s/%(funcName)s/line%(lineno)d]-%(levelname)s: \n\t%(message)s'
_stdout_handler = logging.StreamHandler()
_stdout_handler.setLevel(logging.DEBUG)
_stdout_handler.setFormatter(CustomFormatter(_format))

DEBUG_LOGGER = logging.getLogger(__name__)
DEBUG_LOGGER.setLevel(logging.DEBUG)
DEBUG_LOGGER.addHandler(_stdout_handler)

if __name__ == "__main__":
	DEBUG_LOGGER.info('hello world')
