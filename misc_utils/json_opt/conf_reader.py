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
from typing import (
	Optional,
	Union,
	TypedDict
)
from typing_extensions import NotRequired

from misc_utils.wrappers.err_wrap import (
	die_if_err,
	seize_err_if_any
)
from misc_utils.file_operator import dir2file
from misc_utils.args_loader import PARSER
from misc_utils.time_aux import curr_time_formatter
_args = PARSER.parse_args()


@die_if_err()
def load_config(inp: str) -> dict[str, Union[str, dict[str, str]]]:
	payload_str: str = ''
	with open(inp, 'r') as fd:
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
	keyval: dict = None
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
	global _args
	if keyval is None or len(keyval) == 0:
		raise ValueError('empty parameters')
	pattern = load_config(dir2file(_args.config_dir, filename))
	# 留个备份，以防毁灭性修改。以后要删，自己评估完了删。
	# TODO: 选数据库来读写。直接写到某个文件夹就像是拉了一样
	#       分布式还是？一个人自用？
	date = curr_time_formatter("-%Y-%m-%d-%H-%M-%S-")
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


# See https://docs.python.org/zh-cn/3.10/library/typing.html#typing.TypedDict
_PerUserConf = TypedDict(
	'_PerUserConf',
	{
		"cookie": str,      # cookie
		"user-id": str,     # 用户 id 非必选
		"list-id": str,     # 歌单 id
		"email": str,       # 登录邮箱号
		"password": str,    # 明文
		"backup-dir": str,  # 备份目录
		"csrf_token": str   # 跨域 token
	}
)
ConfJson = TypedDict(
	'ConfJson',
	{
		"npm-path": str,    # npm 路径
		# TODO: 疑似可用用户池来？user1如果想要最大程度的
		#  自定义就可能需要延拓一下定义了。
		"user1": NotRequired[_PerUserConf]
	},
	total=False
)

PRIVATE_CONFIG: dict[str, Union[str, dict[str, str]]] = load_config(dir2file(_args.config_dir, "config.json"))

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
