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
from misc_utils.wrappers.err_wrap import (
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


@seize_err_if_any()
def write_in_given_mode(
	path: str,
	mode: str,
	payload: str,
	encoden: str = 'utf-8'
) -> None:
	with open(path, mode, encoding=encoden) as _fd:
		_fd.write(payload)


@seize_err_if_any()
def append_from_ro_file(
	src_path: str,
	dst_path: str,
	src_encd: str = 'utf-8',
	dst_encd: str = 'utf-8'
) -> None:
	with open(src_path, 'r', encoding=src_encd) as sd:
		with open(dst_path, 'a', encoding=dst_encd) as dd:
			while True:
				tmp = sd.read()
				if tmp is None or len(tmp) <= 0:
					break
				dd.write(tmp)


@seize_err_if_any()
def seek_to_remove_file(abspath: str) -> None:
	os.remove(abspath)


def unsafe_read(
	abspath: str,
	encoden: str='utf-8'
) -> str:
	res = ''
	with open(abspath, 'r', encoding=encoden) as fd:
		while True:
			tmp = fd.readline()
			if tmp is None or len(tmp) <= 0:
				break
			res += tmp
	return res


@die_if_err()
def load_txt_via_file_or_die(abspath: str) -> str:
	return unsafe_read(abspath)

