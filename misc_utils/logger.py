#!/usr/bin/env python3
# -*- coding: utf8 -*-
# Author: kisfg@hotmail.com
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/25 星期六 22:07:01
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
from pathlib import Path

import configs.args_loader

_args = configs.args_loader.PARSER.parse_args()

# https://app.readthedocs.org/projects/loguru/downloads/pdf/stable/
GLOB_LOG_FORMAT = '<green>{time}</green> [<yellow>{file}:{line}</yellow>' \
				  '|<level>{level}</level>] <level>{message}</level>'
# 用于主要爬取逻辑的记录
GLOB_MAIN_LOG_PATH = str(Path(_args.main_log_path))
# 用于测试文件
GLOB_TEST_LOG_PATH = str(Path(_args.test_log_path))
# 自动程序日志路径
GLOB_BOT_LOG_PATH = str(Path(_args.bot_log_path))


if __name__ == '__main__':
	import sys
	from loguru import logger
	logger.remove()
	logger.add(
		sys.stdout,
		format=GLOB_LOG_FORMAT,
		colorize=True
	)

	logger.info('Hello World!')
	logger.warning('Hello World!')
	logger.error('Hello World!')
	logger.critical('Hello World!')
	logger.debug('Hello World!')
	try:
		__1div0 = 1 / 0
	except ZeroDivisionError:
		logger.trace('hello world!!!')
		logger.exception('hello world!!')

