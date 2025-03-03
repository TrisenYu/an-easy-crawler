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
import json, os
from datetime import datetime
from typing import Optional
from utils.wrappers.err_wrap import (
	die_if_err,
	seize_err_if_any
)
from utils.file_operator import dir2file
from utils.args_loader import PARSER

_args = PARSER.parse_args()


@die_if_err
def load_config(inp: str) -> dict:
	payload_str: str = ''
	with open(inp, 'r') as fd:
		while True:
			flows: str = fd.read()
			if flows is None or len(flows) == 0:
				break
			payload_str += flows
	payload = json.loads(payload_str)
	return payload


@die_if_err
def json2dict_via_str_or_die(inp: str, key: Optional[str] = None) -> dict:
	"""
	ascii意义下，尝试将 json 字符串反序列化为 python 可处理的 dict
	"""
	return json.loads(inp) if key is None else json.loads(inp)[key]


@seize_err_if_any
def load_json_from_str(inp: str) -> dict:
	return json.loads(inp)


@seize_err_if_any
def attempt_modify_json(filename: str = 'config.json', keyval: dict = None) -> None:
	"""
	在 `O(n)` 的复杂度下完成对 path 指向文件的修改。

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
	global _args
	if len(keyval) == 0:
		raise ValueError('empty parameters')
	pattern = load_config(dir2file(_args.config_dir, filename))
	# 留个备份，以防毁灭性修改。以后要删，自己评估完了删。
	# TODO: 选数据库来读写。直接写到某个文件夹就像是拉了一样
	date = datetime.now().strftime('-%Y-%m-%d-%H-%M-%S-')
	pmt = dir2file(_args.config_dir, 'before' + date + filename + '.tmp')
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

	with open(dir2file(_args.config_dir, filename), 'w+', encoding='utf-8') as fd:
		json.dump(pattern, fd, indent=4, ensure_ascii=False)


PRIVATE_CONFIG = load_config(dir2file(_args.config_dir, "config.json"))

if __name__ == "__main__":
	print(PRIVATE_CONFIG)
	attempt_modify_json(
		'example.json',
		{
			"user2": {
				'user-id' : 123,
				'password': "321"
			}
		}
	)
