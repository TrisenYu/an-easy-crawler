#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
import json, os.path
from typing import Optional
from utils.throw_err import (
	die_if_err,
	throw_err_if_exist
)


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


@throw_err_if_exist
def load_json_from_str(inp: str) -> dict:
	return json.loads(inp)


CURR_DIR = os.path.dirname(__file__)
PRIVATE_CONFIG = load_config(CURR_DIR + '/./config.json')

if __name__ == "__main__":
	print(PRIVATE_CONFIG)
