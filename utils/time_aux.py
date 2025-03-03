#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author <kisfg@hotmail.com 2025>
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
import time


def unix_time() -> float:
	return time.time()


def funix_us() -> float:
	return unix_time() * 1000_000


def unix_us() -> int:
	return int(funix_us())


def funix_ms() -> float:
	return unix_time() * 1000


def unix_ms() -> int:
	return int(funix_ms())


def unix_sec() -> int:
	return int(unix_time())


def unix_ms_of_next_year() -> int:
	return unix_ms() + 31536000


def unix_ts_to_time(unix_ts: int, time_format: str = "%Y-%m-%d %H:%M:%S") -> str:
	return time.strftime(time_format, time.localtime(unix_ts))


if __name__ == "__main__":
	print(unix_time(), unix_sec())
	print(unix_ms(), funix_ms())
	print(unix_us())
	print('\n', unix_ms(), unix_ms_of_next_year())
