#!/usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/09/29 星期一 16:40:46
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
from pathlib import Path
from typing import Optional

from misc_utils.wrappers.err_wrap import (
	seize_err_if_any,
	die_if_err
)


def unsafe_read_text(
	abspath: str,
	encoden: Optional[str]='utf-8'
) -> str:
	"""按行**只读**掉人类可读文本的不安全函数"""
	res = ''
	with open(abspath, 'r', encoding=encoden) as fd:
		while True:
			tmp = fd.readline()
			if tmp is None or len(tmp) <= 0:
				break
			res += tmp
	return res


def is_fpath(path: str) -> bool:
	return Path(path).is_file()


def is_path_ok(path: str) -> bool:
	return Path(path).exists()


@seize_err_if_any()
def write_in_given_mode(
	path: str,
	mode: str,
	payload: str,
	encoden: Optional[str] = 'utf-8'
) -> None:

	if encoden is None:
		encoden = 'utf-8'
	if 'b' in mode:
		encoden = None
	with open(path, mode, encoding=encoden) as _fd:
		_fd.write(payload)
	


@seize_err_if_any()
def append_from_ro_file(
	src_path: str, dst_path: str,
	src_encd: str = 'utf-8',
	dst_encd: str = 'utf-8'
) -> None:
	with (open(src_path, 'r', encoding=src_encd) as sd,
	      open(dst_path, 'a', encoding=dst_encd) as dd):
		while True:
			tmp = sd.read()
			if tmp is None or len(tmp) <= 0:
				break
			dd.write(tmp)


@seize_err_if_any()
def seek_to_remove_file(abspath: str) -> None:
	Path(abspath).unlink()


@die_if_err()
def load_txt_via_file_or_die(abspath: str) -> str:
	"""
	这个函数最好只在导入库时定义某些重要的常量出现失败时使用。
	"""
	return unsafe_read_text(abspath)

