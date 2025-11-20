#!/usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author <kisfg@hotmail.com 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/26 星期日 21:23:15
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
import time
from datetime import datetime

__BASIC_TIME_FORMAT__: str = "%Y-%m-%d %H:%M:%S"# 形如 2025-03-14 11:45:14
US_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f"
UNDERSCORE_FORMAT: str = "%Y_%m_%d_%H_%M_%S_%f" # 到微秒
LOG_TIME_FORMAT: str = "%Y-%m-%d"

def unix_time() -> float:
	""" 返回 unix 时间戳。结果形如 1741964349.3201044。 """
	return time.time()


def funix_us() -> float:
	""" 返回 us 精度的 unix 时间戳。"""
	return unix_time() * 1_000_000


def unix_us() -> int:
	""" 返回 us 精度的 unix 时间戳。"""
	return int(funix_us())


def funix_ms() -> float:
	""" 返回 ms 精度的 unix 时间戳。"""
	return unix_time() * 1000


def unix_ms() -> int:
	""" 返回 ms 精度的 unix 时间戳。"""
	return int(funix_ms())


def unix_sec() -> int:
	""" 返回 sec 精度的 unix 时间戳。"""
	return int(unix_time())


def unix_ms_of_next_year() -> int:
	""" 计算从此刻 unix 时间戳起经过了一年的对应时间戳。"""
	return unix_ms() + 31536000


def unix_ts_to_time(
	unix_ts: int | float,
	format_str: str=__BASIC_TIME_FORMAT__
) -> str:
	""" 将 unix 时间戳按格式转为易于人类读取的时间。"""
	return datetime.fromtimestamp(unix_ts).strftime(format_str)


def curr_time_formatter(
	format_str: str=UNDERSCORE_FORMAT
) -> str:
	"""
	按给定格式字符串解析当前时间。
	"""
	# TODO: 有点过于简陋了
	if format_str == UNDERSCORE_FORMAT:
		return datetime.now().strftime(format_str)[:-3]
	return datetime.now().strftime(format_str)


def dura_avg(dura_list: list[str]) -> str:
	""" 提供形如 xx:xx.xxx 的时长列表，返回列表的均值 """
	mins, sec = 0, 0
	for dura in dura_list:
		d = dura.split(':')
		mins += int(d[0])
		sec += int(float(d[1])*1000)
	sec += mins * 60_000
	return f'{sec/(len(dura_list)*1000)}'


if __name__ == "__main__":
	print(unix_time(), unix_sec())
	print(unix_ms(), funix_ms())
	print(unix_us())
	print('\n', unix_ms(), unix_ms_of_next_year())
	print(unix_ts_to_time(1759325083.902, US_TIME_FORMAT))