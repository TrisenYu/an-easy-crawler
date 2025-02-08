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
	usage='视需求为对应模块传参或者直接在 utils/args_loader.py 配置选用参数。'
)
# ================  utils/json_parser.py  ===================
## 因为 utils/args_loader.py 和 utils/json_parser.py 同在一个文件夹下所以才没有影响。
PARSER.add_argument(
	'--config-dir', '-dir',
	type=str, default=os.path.join(os.path.dirname(__file__), 'configs'),
	help="配置文件config.json所在的绝对目录。"
)
### 默认都给 user1
# ================  multifn/update_song_list_cnt.py =========
PARSER.add_argument('--author', type=str, default='user1', help='歌单作者，更新cnt专用。')
PARSER.add_argument('--dummy', type=str, default='user1', help='指定傀儡，更新cnt用。')

# ================  multifn/logout.py =======================
PARSER.add_argument('--exit-user', type=str, default='user1', help='对应到配置文件config.json的登出账户。')

# ================  song_list_info.py =======================
PARSER.add_argument('--songlist-author', type=str, default='user1', help="歌单作者名，以从 json 中读取相关约定信息。")
PARSER.add_argument('--login-dummy', type=str, default='user1', help="登录过的 dummy，用于抽取 cookie 和 token。")

# ================  suffixes.py =======================
PARSER.add_argument('--poc-user', type=str, default='user1', help="用于验证某种设计的用户。")

# ================  diff_tests/estimator.py =================
PARSER.add_argument('--test-user', type=str, default='user1', help='用于 diff_tests/ 中测试的用户。')

# 解析命令行参数
if __name__ == "__main__":
	args = PARSER.parse_args()
	print(args)
