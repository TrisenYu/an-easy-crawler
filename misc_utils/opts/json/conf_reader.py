#!/usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/04 星期六 21:07:49
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
from typing import (
	Optional,
	Union
)
from pathlib import Path

from misc_utils.wrappers.err_wrap import (
	die_if_err,
	seize_err_if_any
)
from configs.args_loader import PARSER
from misc_utils.time_aux import curr_time_formatter

# TODO: 配置与功能函数分开
@die_if_err()
def _load_config(inp: str) -> dict[str, Union[str, dict[str, str]]]:
	payload_str: str = ''
	with open(inp, 'r', encoding='utf-8') as fd:
		while True:
			flows: str = fd.read()
			if flows is None or len(flows) == 0:
				break
			payload_str += flows
	payload = json.loads(payload_str)
	return payload

@die_if_err()
def deserialize_json_or_die(inp: str, key: Optional[str] = None) -> dict:
	"""
	ascii意义下，尝试将 json 字符串反序列化为 python 可处理的 dict
	:param inp: inp 为序列化为字符串的 json。
	:param key: inp 内存在的键值。
	:return: 返回反序列化对象。
	"""
	return json.loads(inp) if key is None else json.loads(inp)[key]


@seize_err_if_any()
def load_json_from_str(inp: str) -> dict:
	return json.loads(inp)


@seize_err_if_any()
def attempt_modify_json(
	filename: str = 'config.json',
	keyval: Optional[dict] = None
) -> None:
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
	global _conf_gopher
	if keyval is None or len(keyval) == 0:
		raise ValueError('empty parameters')
	pattern = _load_config(_conf_gopher(filename))
	# 留个备份，以防毁灭性修改。以后要删，自己评估完了删。
	# TODO: 选数据库来读写。直接写到某个文件夹就像是拉了一样
	#       分布式还是？一个人自用？
	# 		有点抽象了，数据库来存配置？改还要写sql或者找sql-gui？
	# 或者开发一个类似于git的版本控制系统？
	date = curr_time_formatter("-%Y-%m-%d-%H-%M-%S-")
	pmt = _conf_gopher('before' + date + filename + '.tmp')

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

	with open(_conf_gopher(filename), 'w+', encoding='utf-8') as fd:
		json.dump(pattern, fd, indent=4, ensure_ascii=False)


_args = PARSER.parse_args()
_conf_gopher = lambda _x: str(Path(_args.config_dir).joinpath(_x))
PRIVATE_CONFIG = _load_config(_conf_gopher("config.json"))

if __name__ == "__main__":
	print(PRIVATE_CONFIG)
