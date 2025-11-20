#!/usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/25 星期六 20:51:47
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
from enum import Enum
from typing import TypeVar


class DiffOp(Enum):
	keep = 1
	insert = 2
	delete = 3


class _txtDiffInfo:
	def __init__(self, xv: int, ops_val: list) -> None:
		self.x = xv
		self.ops = ops_val


_T = TypeVar('_T')
def myers_diff_comparer(
	src: list[_T],
	dst: list[_T]
) -> list[tuple[DiffOp, tuple[_T, int]]]:
	"""
	Thanks to:
		https://github.com/nagaokayuji/diff3/blob/main/src/diff3/diff.py.
		https://chuquan.me/2023/09/13/myers-difference-algorithm/
	"""
	# TODO: 本来时间复杂度都不够好看了
	#       这里甚至还有表示意义下相同的空间复杂度？
	lena, lenb = len(src), len(dst)
	if lena == 0:
		return [(DiffOp.insert, (_, i)) for i, _ in enumerate(dst)]
	elif lenb == 0:
		return [(DiffOp.delete, (_, i)) for i, _ in enumerate(src)]

	bound, diff = lena + lenb, []
	mid_pos = { 1: _txtDiffInfo(0, []) }
	# myers algorithm
	# move_down  <=> insert
	# move_right <=> delete
	for d in range(bound+1):
		for k in range(-d, d+1, 2):
			move_down = k == -d or (k != d and mid_pos[k-1].x < mid_pos[k+1].x)
			prev_pos = mid_pos[k+1] if move_down else mid_pos[k-1]
			diff = prev_pos.ops[:]
			x, y = (prev_pos.x+int(not move_down), prev_pos.x-k+int(not move_down))

			if move_down and 1 <= y <= lenb:
				diff.append((DiffOp.insert, (dst[y-1], y-1)))
			elif not move_down and 1 <= x <= lena:
				diff.append((DiffOp.delete, (src[x-1], x-1)))

			while x < lena and y < lenb and src[x] == dst[y]:
				diff.append((DiffOp.keep, (src[x], x)))
				x, y = x+1, y+1

			mid_pos[k] = _txtDiffInfo(x, diff)
			if x >= lena and y >= lenb:
				return diff
	return []


if __name__ == '__main__':
	a = [123, 456, 789]
	b = [456, 456, 456, 456, 789, 123]
	print(myers_diff_comparer(a, b))
	a = [123, 456, 789]
	b = [789, 123, 456]
	print(myers_diff_comparer(a, b))

