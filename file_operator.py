#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY

"""
文件操作简化函数。
"""
import os, json
from utils.throw_err import (
	throw_err_if_exist,
	die_if_err
)
from utils.json_paser import load_config


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


@throw_err_if_exist
def attempt_modify_json(
	path: str,
	target_name: list[str],
	specific_member: list[str],
	payload: list
) -> None:
	"""
	在 `O(n)` 的复杂度下完成对文件的修改。
	"""
	if len(target_name) != len(specific_member) and len(target_name) != len(payload):
		raise ValueError('invalid parameters')
	if len(target_name) == 0:
		raise ValueError('Empty parameter')

	_for_match_1, _for_match_2 = [f'{t}' for t in target_name], [f'{s}' for s in specific_member]
	pattern = load_config(path)
	for idx, m1 in enumerate(_for_match_1):
		pattern[m1][_for_match_2[idx]] = payload[idx]
	del _for_match_1, _for_match_2
	with open(path, 'w+', encoding='utf-8') as fd:
		json.dump(pattern, fd, indent=4, ensure_ascii=False)


if __name__ == "__main__":
	attempt_modify_json('utils/example.json', ['user2', 'user2'], ['user-id', 'password'], [123, "321"])