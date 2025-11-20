#!/usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/03 星期五 18:52:17
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
#
# TODO: 命令行可能得按照某个具体的网站来配相应的接口才行
#       另外就是这样子配太别扭了，有冇被广泛使用的开源第三方维护性强的参数解析库？
"""
	解析命令行/给定的选择参数
"""
import argparse
from pathlib import Path

PARSER = argparse.ArgumentParser(
	description='逆向解析web-js obfuscated by netease',
	allow_abbrev=True,
	usage='视需求为对应模块传参或者直接在 args_loader.py 配置选用参数。'
)
# HTTP请求上的配置
PARSER.add_argument(
	'-rtimes', '--retry-times',
	type=int,
	default=3 # 事不过三
)
# -=-=-=-=-=-=-=-= misc_utils/logger.py -=-=-=-=--=-=-=-=-=-=-=-
PARSER.add_argument(
	'-blogp', '--bot-log-path',
	type=str,
	default=str(Path(__file__).parent.joinpath('../assets/stat/logs/test.log').absolute()),
)
PARSER.add_argument(
	'-mlogp', '--main-log-path',
	type=str,
	default=str(Path(__file__).parent.joinpath('../assets/stat/logs/main.log').absolute())
)
PARSER.add_argument(
	'-tlogp', '--test-log-path',
	type=str,
	default=str(Path(__file__).parent.joinpath('../assets/stat/logs/test.log').absolute())
)
# ================  misc_utils/ops/json/conf_reader.py  ===================
PARSER.add_argument(
	'-cdir', '--config-dir',
	type=str,
	default=str(Path(__file__).parent.absolute()),
	help="配置文件所在的绝对目录。"
)
# ================ misc_utils/opts/db/sqlite.py =================
## 数据库配置参数
# TODO: 怎么对数据库文件做备份？
PARSER.add_argument(
	'-dbpath', '--database-path',
	type=str,
	default=str(Path(__file__).parent.joinpath('../assets/dyn/somgs.db').absolute()),
	help='本地数据库的路径。'
)

### 凡涉及到用户的，默认给 user1
## diff_tests
# ================  diff_tests/crypto_tester.py =================
PARSER.add_argument(
	'-tuser', '--test-user',
	type=str, default='user1',
	help='用于 `diff_tests/` 中测试的用户。'
)
## multtp
# ================  multtp/songslist_hit_bot.py ================
PARSER.add_argument(
	'--author',
	type=str, default='user1',
	help='歌单作者，更新hit专用。'
)
PARSER.add_argument(
	'--dummy',
	type=str, default='user1',
	help='指定傀儡，更新hit用。'
)
# 此处用相对路径归功于project的组织结构和python解释器。
PARSER.add_argument(
	'-bsp', '--bot-sh-path',
	type=str,
	default=str(Path(__file__).parent.joinpath('../bot_hits.sh').absolute()),
	help='bot_hits.sh的绝对路径。'
)
# ================ multtp/_login_test.py =========================
PARSER.add_argument(
	'--applicant',
	type=str, default='user1',
	help="要求登录的账号。"
)
# ================  multtp/logout.py ============================
PARSER.add_argument(
	'-eu', '--exit-user',
	type=str, default='user1',
	help='对应到配置文件config.json的登出账户。'
)
# ================  multtp/refresh_token.py =====================
PARSER.add_argument(
	'-rd', '--refresh-dummy',
	type=str, default='user1',
	help='待刷新token的dummy。'
)
# ================ multtp/indistinct_search.py(Feature in the future) =============
PARSER.add_argument(
	'-sfn', '--songslist-fuzzy-name',
	type=str, default='',
	help="(yet to impl)歌单的模糊名，用于模糊搜索获取其id。"
)
## root-dir
# ================  fetch_songslist_info.py ======================
PARSER.add_argument(
	'-sa', '--songslist-author',
	type=str, default='user1',
	help="歌单作者名，以从json中读取相关约定信息。"
)
PARSER.add_argument(
	'-ld', '--login-dummy',
	type=str, default='user1',
	help="登录过的dummy，用于抽取cookie和token。"
)
PARSER.add_argument(
	'-tps', '--threadpool-size',
	type=int, default=8,
	help="给定线程池大小。"
)
PARSER.add_argument(
	'-nd', '--need-download',
	type=bool, default=True,
	help="需要将歌单内的所有歌及其封面尽力而为地保存到本地。"
)
PARSER.add_argument(
	'-cvp', '--covers-path',
	type=str, default=str(Path(__file__).parent.joinpath('../assets/stat/covers').absolute()),
	help="本地保存封面的路径。"
)
PARSER.add_argument(
	'-trp', '--tracks-path',
	type=str, default=str(Path(__file__).parent.joinpath('../assets/stat/tracks').absolute()),
	help="本地保存音轨的路径。"
)


# 解析命令行参数示例
if __name__ == "__main__":
	args = PARSER.parse_args()
	print(args)
	print(PARSER.__str__())
	print(PARSER.print_help())
