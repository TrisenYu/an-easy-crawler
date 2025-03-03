#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
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

"""
文件操作简化函数。
"""
import os
from utils.wrappers.err_wrap import (
	seize_err_if_any,
	die_if_err
)


def dir2file(dirname: str, filename: str) -> str:
	"""
	:param dirname: 给定目录。
	:param filename: 给定文件名。
	:return: 各操作系统下到文件的绝对路径
	"""
	return os.path.join(dirname, filename)


@seize_err_if_any
def write_in_given_mode(path: str, mode: str, payload: str) -> None:
	with open(path, mode, encoding='utf-8') as _fd:
		_fd.write(payload)


@seize_err_if_any
def append_from_read_only_file(src_path: str, dst_path: str) -> None:
	with open(src_path, 'r', encoding='utf-8') as sd:
		with open(dst_path, 'a', encoding='utf-8') as dd:
			while True:
				tmp = sd.read()
				if tmp is None or len(tmp) <= 0:
					break
				dd.write(tmp)


@seize_err_if_any
def remove_file(abspath: str) -> None:
	os.remove(abspath)


@die_if_err
def load_readable_txt_from_file(abspath: str) -> str:
	res = ''
	with open(abspath, 'r', encoding='utf-8') as fd:
		while True:
			tmp = fd.readline()
			if tmp is None or len(tmp) <= 0:
				break
			res += tmp
	return res
