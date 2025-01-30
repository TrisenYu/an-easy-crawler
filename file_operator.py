#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY

"""
文件操作简化函数。
"""
import os
from utils.throw_err import throw_err_if_exist, die_if_err


@throw_err_if_exist
def write_to_file_in_a_way(path: str, attr: str, payload: str) -> None:
	with open(path, attr, encoding='utf-8') as _fd:
		_fd.write(payload)


@throw_err_if_exist
def write_from_file(src_path: str, dst_path: str) -> None:
	with open(src_path, 'r', encoding='utf-8') as sd:
		with open(dst_path, 'a', encoding='utf-8') as dd:
			while True:
				tmp = sd.read()
				if tmp is None or len(tmp) <= 0:
					break
				dd.write(tmp)


@throw_err_if_exist
def remove_file(path: str) -> None:
	os.remove(path)


@die_if_err
def load_readable_txt_from_file(path: str) -> str:
	res = ''
	with open(path, 'r', encoding='utf-8') as fd:
		while True:
			tmp = fd.readline()
			if tmp is None or len(tmp) <= 0:
				break
			res += tmp
	return res