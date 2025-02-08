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
import os, json
from datetime import datetime
from utils.wrappers.err_wrap import (
	throw_err_if_any,
	die_if_err
)
from utils.json_conf_reader import load_config, ARGS


@throw_err_if_any
def write_in_assigned_mode(path: str, attr: str, payload: str) -> None:
	with open(path, attr, encoding='utf-8') as _fd:
		_fd.write(payload)


@throw_err_if_any
def append_from_read_only_file(src_path: str, dst_path: str) -> None:
	with open(src_path, 'r', encoding='utf-8') as sd:
		with open(dst_path, 'a', encoding='utf-8') as dd:
			while True:
				tmp = sd.read()
				if tmp is None or len(tmp) <= 0:
					break
				dd.write(tmp)


@throw_err_if_any
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


@throw_err_if_any
def attempt_modify_json(filename: str = 'config.json', keyval: dict = None) -> None:
	"""
	在 `O(n)` 的复杂度下完成对path指向文件的修改。

	keyval 格式形如：
	{
	...."user1": {
	........"attr1" : "",
	........"attr2" : 123,
	....}
	}

	必须与 config.json 对应。否则删除中间文件并抛出ValueError。

	- path 配置名。其父目录写死为 args_loader.py 中 PARSER 解析得来的参数。
	- keyval 待修改的键值对。
	"""
	if len(keyval) == 0:
		raise ValueError('empty parameters')
	pattern = load_config(os.path.join(ARGS.config_dir, filename))
	# 留个备份，以防毁灭性修改。以后要删，自己评估完了删。
	date = datetime.now().strftime('-%Y-%m-%d-%H-%M-%S-')
	pmt = os.path.join(ARGS.config_dir, 'before' + date + filename + '.tmp')
	with open(pmt, 'w+', encoding='utf-8') as fd:
		json.dump(pattern, fd, indent=4, ensure_ascii=False)
	for attr in keyval:
		if attr not in pattern:
			os.remove(pmt)
			raise ValueError('invalid member-record')
		for val in keyval[attr]:
			if val not in pattern[attr]:
				os.remove(pmt)
				raise ValueError('invalid key-field')
			pattern[attr][val] = keyval[attr][val]

	with open(os.path.join(ARGS.config_dir, filename), 'w+', encoding='utf-8') as fd:
		json.dump(pattern, fd, indent=4, ensure_ascii=False)


if __name__ == "__main__":
	print(ARGS.config_dir)
	attempt_modify_json(
		'example.json',
		{
			"user2": {
				'user-id': 123,
				'password': "321"
			}
		}
	)