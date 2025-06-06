# ! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
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
"""
	解析命令行/给定的选择参数
"""
import argparse, os.path

PARSER = argparse.ArgumentParser(
	description='对网易云web混淆js的一个逆',
	allow_abbrev=True,
	usage='视需求为对应模块传参或者直接在 misc_utils/args_loader.py 配置选用参数。'
)
# ================  misc_utils/json_parser.py  ===================
## 因为 misc_utils/args_loader.py 和 misc_utils/json_parser.py 同在一个文件夹下所以才没有影响。
PARSER.add_argument(
	'--config-dir', '-dir',
	type=str, default=os.path.join(os.path.dirname(__file__), 'configs'),
	help="配置文件config.json所在的绝对目录。"
)

### 凡涉及到用户的，默认给 user1。
## diff_tests
# ================  diff_tests/estimator.py =================
PARSER.add_argument('-tu', '--test-user', type=str, default='user1', help='用于 diff_tests/ 中测试的用户。')
## multifn
# ================  multifn/songlist_hit_bot.py =========
PARSER.add_argument('-a', '--author', type=str, default='user1', help='歌单作者，更新cnt专用。')
PARSER.add_argument('-d', '--dummy', type=str, default='user1', help='指定傀儡，更新cnt用。')
# 此处用相对路径归功于project的组织结构和python解释器。
PARSER.add_argument('-bsp', '--bot-sh-path', type=str, default='../bot_hits.sh', help='bot_hits.sh的绝对路径。')
# ================ multifn/login_test.py =========================
PARSER.add_argument('--applicant', type=str, default='user1', help="要求登录的账号")
# ================  multifn/logout.py =======================
PARSER.add_argument('-eu', '--exit-user', type=str, default='user1', help='对应到配置文件config.json的登出账户。')
# ================  multifn/refresh_token.py ================
PARSER.add_argument('-rd', '--refresh-dummy', type=str, default='user1', help='待刷新token的dummy。')
# ================ multifn/indistinct_search.py(Feature in the future) =============
PARSER.add_argument('-sfn', '--songlist-fuzzy-name', type=str, default='', help="歌单的模糊名，用于模糊搜索获取其id")
## root-dir
# ================  fetch_songlist_info.py =======================
PARSER.add_argument('-sa', '--songlist-author', type=str, default='user1', help="歌单作者名，以从 json 中读取相关约定信息。")
PARSER.add_argument('-ld', '--login-dummy', type=str, default='user1', help="登录过的 dummy，用于抽取 cookie 和 token。")
PARSER.add_argument('-tps', '--threadpool-size', type=int, default=8, help="给定线程池大小")
# ================  suffixes.py =============================
PARSER.add_argument('-pu', '--poc-user', type=str, default='user1', help="用于验证某种设计的用户。")


# 解析命令行参数
if __name__ == "__main__":
	args = PARSER.parse_args()
	print(args)
	print(PARSER.__str__())
	print(PARSER.print_help())
