# !/usr/bin/env/python3
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.
import math, os

from utils.args_loader import PARSER
from utils.json_conf_reader import PRIVATE_CONFIG

args = PARSER.parse_args()
backup_dir = PRIVATE_CONFIG[args.songlist_author]['backup-dir']


if __name__ == "__main__":
	content, st = '', False
	with open(os.path.join(backup_dir, 'songs-list.txt'), 'r', encoding='utf-8') as fd:
		while True:
			tmp = fd.readline()
			if not st :
				if tmp == '# songs:\n':
					st = True
				continue
			elif st and len(tmp) > 1:
				content += tmp
			else:
				break

	content = content[:-1].split('\n')

	# 最好是转义之后再转义回来，机器这样就不会有 bug 了。但对人来说不行——太别扭了。
	lena, tot_time = len(content), 0
	calc_t = lambda x, y, z: x * 60_000 + y * 1_000 + z
	t_clac = lambda s: f'{s//60_000:02d}:{((s-s%1_000)//1_000)%60:02d}.{s%1_000:03d}'
	author_set = set()
	for v in content:
		curr = v.split('--')
		author = curr[2].strip('[').strip(']').lower().split(',')
		now = curr[1].strip('-')
		arr, clr = [], ''
		for c in now:
			if c == ':' or c == '.':
				arr.append(int(clr))
				clr = ''
			else:
				clr += c
		arr.append(int(clr))
		tot_time += calc_t(arr[0], arr[1], arr[2])
		author = [_.strip(' ') for _ in author]
		for a in author:
			author_set.add(a)

	# 看有多少个不同的作者，歌单总时长以及平均时间。
	print(
		f'\nexpected-diff-author:{len(author_set)}, '
        f'tot: {tot_time / 1000}s, '
        f'avg: {t_clac(math.floor(tot_time / lena))}'
	)
