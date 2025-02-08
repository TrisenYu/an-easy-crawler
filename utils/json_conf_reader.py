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
from typing import Optional
from utils.wrappers.err_wrap import (
	die_if_err,
	throw_err_if_any
)
from utils.args_loader import PARSER


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
	""" 解析传回的 json 为 python 可处理的内存对象 """
	return json.loads(inp) if key is None else json.loads(inp)[key]


@throw_err_if_any
def load_json_from_str(inp: str) -> dict:
	return json.loads(inp)


ARGS = PARSER.parse_args()
PRIVATE_CONFIG = load_config(os.path.join(ARGS.config_dir, "config.json"))

if __name__ == "__main__":
	print(PRIVATE_CONFIG)
