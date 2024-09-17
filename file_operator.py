#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY

"""
之前这里的逻辑没有直接用网易的后端，而是通过解析冗长的前端来完成任务。
编程效率相对比较快但是运行效率有点 low。所以已经全部清掉了。
"""
import os
from utils.throw_err import throw_err_if_exist


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

# 删除提交 6f549e8f3e31c1b3cf8aaa250308ed9f7978f208 在此文件下的注释
