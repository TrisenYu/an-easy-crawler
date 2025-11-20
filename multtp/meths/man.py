#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com> in 2025
# Created at 2025/10/01 星期三 20:37:54
# Last modified at 2025/10/04 星期六 20:01:27
from typing import Optional, Callable
from functools import partial

from curl_cffi.requests import post as postman
from curl_cffi.requests import get  as messger
from curl_cffi import Response

from loguru import logger

from misc_utils.logger import GLOB_MAIN_LOG_PATH, GLOB_LOG_FORMAT
from configs.args_loader import PARSER
from multtp.meths.header import (
	alter_header, gen_fake_browser_and_http_header
)

logger.remove()
logger.add(
	GLOB_MAIN_LOG_PATH,
	format=GLOB_LOG_FORMAT,
	colorize=True,
	rotation='16MB',
	compression='zip'
)
_args = PARSER.parse_args()
RETRY_TIMES = _args.retry_times


def _http_meth_gen(
	func: Callable[..., any],
	url: str,
	payload: Optional[str]=None,
	err_info: str='',
	alter_dict: Optional[dict[str, str]]=None,
	no_header: bool=False
) -> Optional[Response]:
	"""
	:param func: http method function
	:param url: url for interaction
	:param payload: 载荷
	:param err_info: 额外错误信息
	:param alter_dict: header内需要修改的域
	:param no_header: 不需要header
	"""
	global RETRY_TIMES
	cnt = 0
	browser, prev_header = gen_fake_browser_and_http_header()
	if alter_dict is not None:
		prev_header = alter_header(alter_dict, prev_header)
	headers = prev_header if not no_header else None
	while cnt < RETRY_TIMES:
		try:
			resp = func(
				url, data=payload,
				headers=headers, 
				impersonate=browser
			)
			break
		except Exception as e:
			logger.error(
				f'During interaction with {url} and payload {payload}, an error emerged:' +
				err_info + str(e)
			)
			if cnt < RETRY_TIMES:
				cnt += 1
				continue
			return None
	if resp.status_code != 200:
		logger.warning(
			f'{url} responses with {resp.status_code}, '
			'and its detail with boundary restrain is '
			f'\n{resp.text if len(resp.text) < 512 else resp.text[:512]}'
		)
	return resp


poster = partial(_http_meth_gen, func=postman)
getter = partial(_http_meth_gen, func=messger)


if __name__ == '__main__':
	pass