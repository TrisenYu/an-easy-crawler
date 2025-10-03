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

from misc_utils.logger import DEBUG_LOGGER
from misc_utils.header import (
	HEADER, BROWSER, alter_header
)


def _http_meth_gen(
	func: Callable[..., any],
	url: str,
	payload: Optional[str]=None,
	err_info: str='',
	alter_map: Optional[dict[str, str]]=None,
	turnoff_tls_fingerprint: bool=False
) -> any:

	if alter_map is not None:
		alter_header(alter_map)
	person = BROWSER if not turnoff_tls_fingerprint else None
	try:
		resp = func(
			url, data=payload,
			headers=HEADER, impersonate=person
		)
	except Exception as e:
		DEBUG_LOGGER.error(
			f'During interaction with {url} and payload {payload}, ' \
			f'an error emerged:' + err_info + str(e)
		)
		return None
	return resp


poster = partial(_http_meth_gen, func=postman)
getter = partial(_http_meth_gen, func=messger)


if __name__ == '__main__':
	print(
		getter(
			url='https://interface.music.163.com' \
			'/api/song/detail?ids=[687374,22826700,1414030855]'
		).text
	)
