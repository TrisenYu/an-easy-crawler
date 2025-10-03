#!/usr/bin/env python3
# Last modified at 2025/10/04 星期六 19:19:41
from misc_utils.args_loader import PARSER
from misc_utils.logger import DEBUG_LOGGER
from misc_utils.opts.json.conf_reader import PRIVATE_CONFIG
from misc_utils.http_meths.man import getter

_args = PARSER.parse_args()
csrf_token = PRIVATE_CONFIG[_args.login_dummy]['csrf_token']

host_root = 'music.163.com'
hostname = f"https://interface.{host_root}"
cdns_api = f"{hostname}/weapi/cdns" + csrf_token

resp = getter(url=cdns_api)
if resp is None:
	exit(0)

# TODO: 主站内嵌 js？这怎么搞？
print(resp.status_code, resp.text, resp.content, resp.cookies)
