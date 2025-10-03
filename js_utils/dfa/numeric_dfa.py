#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025-06>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025年08月24日 星期日 20时28分42秒
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

bitable = '01'
octable = f'{bitable}234567'
decable = f'{octable}89'
hexable = f'{decable}abcdefABCDEF'

from functools import partial
from typing import Callable
from js_utils.dfa.any_dfa import AbstractDFA
from js_utils.tokens_def import JSTokTy

def _ch_in_table(ch: str, tab: str) -> bool: return ch in tab

ch_in_hex = partial(_ch_in_table, tab=hexable)
ch_in_oct = partial(_ch_in_table, tab=octable)
ch_in_dec = partial(_ch_in_table, tab=decable)
ch_in_bin = partial(_ch_in_table, tab=bitable)

def _num_curry1(ch: str):
	"""upper态对应curry2中的转移。lower则为0x$或0o$或0B$等状态"""
	lower, upper = ch.lower(), ch.upper()

	def set_table(table: str):
		return lambda _: upper if _ in table else ('d' if _ != '' else lower)

	return set_table


def _num_curry2(loop_state: str):
	def set_table(table: str, hang_state: str) -> Callable[[str], str]:
		def inp(c: str) -> str:
			if c in table or c == '':
				return loop_state
			elif c == '_':
				return hang_state
			return 'E' if c == 'n' else 'd'

		return inp

	return set_table


def _num_curry3(loop_state: str):
	def nxt(nxt_state: str) -> Callable[[str], Callable[[str], str]]:
		def set_id(det: str) -> Callable[[str], str]:
			def inp(_c: str) -> str:
				if _c in decable or _c == '':
					return loop_state
				elif _c in det:
					return nxt_state
				return 'd'

			return inp

		return set_id

	return nxt


def _num_curry_dot_state(loop_state: str):
	def nxt(nxt_state: str):
		def fn(inp: str) -> str:
			if inp in decable:
				# .1? .0?
				return nxt_state
			# .$
			return loop_state if inp == '' else 'd'
		return fn

	return nxt


def _fn_of_fn(loop_state: str, under_state: str, expn_state: str):
	def inp(c: str) -> str:
		if c in decable or c == '':
			# .1$
			# .12?
			# .12$
			return loop_state  # 也属于可以接受的状态
		elif c == '_':
			# .123_?
			return under_state
		elif c in 'eE':
			# .12e?
			# .123E?
			return expn_state
		return 'd'

	return inp


def _1_(_c: str) -> str:
	if _c == '':
		return '1'
	elif _c == '0':
		# 0?
		return '2'
	elif _c in decable[1:]:
		# 123?
		return '3'
	elif _c == '.':
		# .?
		return '4'
	return 'd'


def _2_(_c: str) -> str:
	"""已经读取到0*，要对*构建跳转边的状态"""
	if _c == '':
		return '2'
	elif _c == '.':
		# 0.?
		return '5'
	elif _c == '0':
		# 0$
		return 'z'
	elif _c in decable[1:]:
		# 02?
		return 'l'
	elif _c in 'xX':
		return 'x'
	elif _c in 'oO':
		return 'o'
	elif _c in 'bB':
		return 'b'
	elif _c in 'eE':
		# 0e?或0E
		return '6'
	# 前导零不得接 _ 且不得出现于浮点数表示中
	return 'd'

# 不允许前导零使用类似 0001n 的表示。
_l_ = lambda _: 'l' if _ in decable or _ == '' else 'd'

_b_ = _num_curry1('B')(bitable)
_B_ = _num_curry2('B')(bitable, 'b')
_o_ = _num_curry1('O')(octable)
_O_ = _num_curry2('O')(octable, 'o')
_x_ = _num_curry1('X')(hexable)
_X_ = _num_curry2('X')(hexable, 'x')
_E_ = lambda _: 'd' if _ != '' else 'E'  # 最后用n修饰的bigNumber


def _3_(_c: str) -> str:
	if _c in decable or _c == '':
		# 123? 132_1?
		return '3'
	elif _c == '.':
		# 123.?
		# 1_23.?
		return '5'
	elif _c == '_':
		# 123_?
		return '7'
	elif _c in 'eE':
		# 123e?
		# 1_23E?
		return '6'
	elif _c == 'n':
		# 123n?
		return 'E'
	return 'd'


"""
7 -> 3 123_3?
7 -> 7 123_$
"""
_7_ = _num_curry_dot_state('7')('3')


def _z_(_c: str) -> str:
	if _c == '0' or _c == '':  # 00...0?
		return 'z'
	if _c in decable[1:]:
		return 'l'
	# 000...01?
	return 'd'


"""
4 -> 8 .1?
4 -> 4 .$
"""
_4_ = _num_curry_dot_state('4')('8')
"""
状态本身可接受
8 -> 8 .1$
	 | .12?
	 | .12$
8 -> c .123_?
8 -> 6 .12e?
	 | .123E?
"""
_8_ = _fn_of_fn('8', 'c', '6')
""" 如果拿走状态 5，则状态 9 会匹配上 123._3 这样的意外结果
5 -> 9 123.$
	 | 123.1?

5 -> 6 123.e?
	 | 0.E?
"""
_5_ = _num_curry3('9')('6')('eE')
_d_ = lambda _: 'd'  # 拒绝态

"""
c -> 9 .345_3?
c -> c .345_$
"""
_c_ = _num_curry_dot_state('c')('9')
"""
这一状态本身也可以接受
9 -> 9 123.$
	 | 123.3$
	 | 123.3?
9 -> f 123.3_?
9 -> 6 123.3e?
	 | 3.1_4_15E?
"""
_9_ = _fn_of_fn('9', 'f', '6')
"""
f -> 9 123.3_2?
f -> f 123.3_$
"""
_f_ = _num_curry_dot_state('f')('9')


def _6_(_c: str) -> str:
	if _c == '':
		return '6'
	elif _c in '+-':
		# .4e+?
		# 123.e-?
		# 0E+?
		# 12E-?
		return 'a'
	elif _c in decable:
		# specification不care指数上面的前导零了
		# 123.e0
		# 123e1
		# 1.23E2
		# .3e1
		return 'g'  # 这个时候可以接受了
	return 'd'


"""
a -> a
	 | 1.2e-$
	 | 1.3e+$
a -> g
	 | 1.23e+1?
	 | 1.2e-0?
	 | 1.23e+100?
"""
_a_ = _num_curry_dot_state('a')('g')
"""
g -> e 1.23e+1_?
g -> g 1.23?
"""
_g_ = _num_curry3('g')('e')('_')
"""
e -> g 1.23e+1_2?
e -> e 1.23e+1_$
"""
_e_ = _num_curry_dot_state('e')('g')


class JS_num_literal_DFA(AbstractDFA):
	"""
	JavaScript中，正浮点数、整数的字面量对应的DFA
	构造上尽量不用其它状态污染过的值，然后大多数是按照位次顺序来给定状态编号的。
	因为十六进制之类的数的DFA解析规则是后加进来的，所以命名上看起来比较抽象
	如果要理解这些状态，就把 if 条件上给的值当成跳转边，函数自身作为状态。
	只保证通过单测。如果修改了 JS_num_literal_DFA 的状态转换，
	`ac4int`、`ac4float`也需要视情况更改。

	Won't do: 画状态图严格化论证状态自动机的正确性。
	TODO: 难道不能搞成自动生成？
	"""
	ac4int = '2Bz3OXE'  # 整数终态
	ac4bigInt = 'l' # 大整数终态
	ac4float = '589g' # 浮点数终态
	def __init__(self):
		self.trans = {
			'1': _1_, '2': _2_, '3': _3_,
			'4': _4_, '5': _5_, '6': _6_,
			'7': _7_, '8': _8_, '9': _9_,
			'e': _e_, 'a': _a_, 'g': _g_,
			'c': _c_, 'E': _E_, 'f': _f_,
			'z': _z_, 'l': _l_,
			'x': _x_, 'X': _X_,
			'o': _o_, 'O': _O_,
			'B': _B_, 'b': _b_, 'd': _d_,
		}
	def state_machine(self, inp: str, state: str) -> tuple[str, bool]:
		nxt_state = self.trans[state](inp)
		return nxt_state, nxt_state in self.ac4int + self.ac4float + self.ac4bigInt
	def explain_state(self, state: str) -> JSTokTy:
		if state in self.ac4int:
			return JSTokTy.integer
		elif state in self.ac4float:
			return JSTokTy.Float
		elif state in self.ac4bigInt:
			return JSTokTy.bigInt
		return JSTokTy.illegal
	def validator(self, inp: str) -> JSTokTy:
		cur = '1'
		for i in inp:
			cur = self.trans[cur](i)
		return self.explain_state(cur)
