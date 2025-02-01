#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
"""
登出操作。
TODO: 实际测试以下正确性。
"""
from utils.json_paser import PRIVATE_CONFIG
from requests import post as rep
from crypto.manual_deobfuscation import cloud_music_encryptor
from args_loader import PARSER
from utils.logger import DEBUG_LOGGER
from file_operator import attempt_modify_json

PARSER.add_argument('targetAccount', type=str, help='登出账号')
PARSER.parse_args()

token = PRIVATE_CONFIG[PARSER.targetAccount]['csrf_token']
csrf_token = f'?csrf_token={token}'
suffix = '/weapi/logout' + csrf_token
host = 'music.163.com'
prefix = f'https://{host}'
header = {
	':authority:'       : host,
	':method:'          : 'POST',
	':path:'            : '/weapi/logout' + csrf_token,
	':scheme:'          : 'https',
	'accept'            : '*/*',
	'accept-language'   : 'zh-CN,zh-TW;q=0.9,zh;q=0.8,th;q=0.7',
	'cache-control'     : 'no-cache',
	'content-length'    : '410',
	'content-type'      : 'application/x-www-form-urlencoded',
	'cookie'            : PRIVATE_CONFIG[PARSER.targetAccount]['cookie'],  # cookie 内容有点多，需要调整。
	'nm-gcore-status'   : '1',
	'origin'            : prefix,
	"pragma"            : 'no-cache',
	'priority'          : "u=1, i",
	"referer"           : f"{prefix}/",
	"sec-ch-ua"         : '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
	"sec-ch-ua-mobile"  : '?0',
	"sec-ch-ua-platform": '"Windows"',
	"sec-fetch-dest"    : "empty",
	"sec-fetch-mode"    : "cors",
	"sec-fetch-site"    : "same-origin",
	"user-agent"        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
	                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

payload = f'{"{"}"csrf_token":"{token}"{"}"}'
resp = rep(prefix + suffix, headers=header, data=cloud_music_encryptor(payload))
# 做完以后 token 作废，相应地应该删除所提供的token
if resp.status_code != 200:
	DEBUG_LOGGER.error(f'{resp.status_code}, {resp.text}')
	exit(1)
else:
	DEBUG_LOGGER.info(f'{resp.text}')
	attempt_modify_json(
		'utils/config.json',
		[PARSER.targetAccount, PARSER.targetAccount],
		['csrf_token', 'cookie'],
		['', ''] # 置空就行
	)
