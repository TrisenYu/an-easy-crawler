#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
import logging


class CustomFormatter(logging.Formatter):
	"""
	Logging colored formatter, adapted from:
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


# Define format for logs
_format = ' %(asctime)s [%(levelname)s]: %(message)s'

_stdout_handler = logging.StreamHandler()
_stdout_handler.setLevel(logging.DEBUG)
_stdout_handler.setFormatter(CustomFormatter(_format))

DEBUG_LOGGER = logging.getLogger(__name__)
DEBUG_LOGGER.setLevel(logging.DEBUG)
DEBUG_LOGGER.addHandler(_stdout_handler)

if __name__ == "__main__":
	DEBUG_LOGGER.info('hello world')
