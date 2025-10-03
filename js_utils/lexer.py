#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com, 2025-06>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/03 星期五 00:12:36
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
# Acknowledgement: https://github.com/BVolt/NumericLiterals/blob/main/DecIntDFA.py
#				  Thank you very much, BVolt.
# Referer: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Lexical_grammar
#		  https://github.com/PiotrDabkowski/pyjsparser/blob/master/pyjsparser/parser.py
"""
A javascript lexer written in python
以 python 写成的javascript的词法分析器

	- It is better to use the famous project ``babel`` because the total workload is overwhelming.
	-	This lexer should support for es6 standard in expectation but not sure
	-	whether it works definitely right.
	预期应支持es6但如果要全部做一遍，工作量其实非常大，所以不保证完全正确。
	不如直接调 babel

	- core design: 带回溯的向前看1~5个字符
	核心设计：Look Ahead 1~5 chars with Rewinding Operation for Identifying RegExpression
"""
from functools import reduce, partialmethod
from typing import Optional, TypedDict, NoReturn
from copy import deepcopy

from js_utils.dfa.numeric_dfa import (
	decable, octable,
	ch_in_hex,
	JS_num_literal_DFA
)
from js_utils.tokens_def import (
	JSTokTy, JSTok, js_tk_lut,
	delimiters, js_operats, decl_str,
	spacetab, enter_set, num_shape, pause_idt,
	repeatable, twicenable, commapsign,

	get_escaped_ch_in_str
)

from js_utils.regex_def import (
	assume_regex,
	regex_deter_chars,
	regex_flag_chars
)

from js_utils.unicode_aux import (
	is_id_start,
	is_id_continue
)

from misc_utils.file_operator import unsafe_read_text

_num_dfa = JS_num_literal_DFA()


class _peek_token_cond(TypedDict):
	repeat_ok: bool
	peek_twice: bool
	qmask_type: bool
	assign_ty: bool
	other_char: str
	peek_more: bool


class _BlockCommentInfo:
	literal: str = ''
	linum: int = 0
	st: int = 0
	ed: int = 0
	tail_enter: bool = False

	def __init__(self, line: int = 1, st: int = 1) -> None:
		self.linum = line
		self.st = st


class JSLexer:
	_tot_read: int = 0
	_buf: str = ''
	_linum: int = 1			# line-number
	_stp: int = 0			# start_recording_position
	_edp: int = 0  			# end_recording_position
	_stp_fix: bool = False	# fix for correcting start recording position
	_cur_type: JSTokTy = JSTokTy.illegal
	_cur_literal: str = ''
	_cur_sign: str = ''
	res: list[JSTok] = []
	_block_comments: list[_BlockCommentInfo] = []

	def __init__(self, src_abs_path: str) -> None:
		self.src_abs_path: str = src_abs_path

	@property
	def yet_to_init(self) -> bool:
		return len(self._buf) == 0 or self.src_abs_path == ''

	def _reset_pos(self) -> None:
		self._edp = 0
		self._stp = 1

	def _if_enter(self, c: str) -> bool:
		if c not in enter_set:
			return False
		self._linum += 1
		self._reset_pos()
		return True

	def cln_res(self, res_needed: bool = True) -> None:
		if res_needed:
			self.res.clear()
		self._edp = self._stp = self._tot_read = 0
		self._linum = 1
		self._cur_type = JSTokTy.illegal
		self._cur_literal = self._cur_sign = ''

	def set_src(self, src_abs_path: str) -> None:
		self.src_abs_path = src_abs_path
		self.cln_res()
		self._buf = ''

	def _pik_ch(self, ed: int = 1) -> str:
		if self.yet_to_init or self._tot_read >= len(self._buf):
			return ''
		choice = min(self._tot_read+ed, len(self._buf))
		res = self._buf[self._tot_read:choice]
		self._edp += choice - self._tot_read
		self._tot_read = choice
		return res

	def _ret_chs(self, ret: int = 1) -> None:
		if self.yet_to_init or ret == 0:
			return None
		elif self._tot_read <= 0:
			return self.cln_res(False)
		self._edp -= ret
		self._tot_read -= ret
		return None

	def _set_buf_via_src(
		self,
		encoden: str = 'utf-8'
	) -> None | NoReturn:
		""" 给定文件路径，通过读取函数来重置缓冲区，最后清空原先持有的统计数据"""
		if not self.yet_to_init:
			return
		if self.src_abs_path == '':
			raise ValueError(
				'the lexer do not hold `src_abs_path` yet!'
			)
		self._buf = unsafe_read_text(self.src_abs_path, encoden)
		return self.cln_res()

	def _unset_buf(self) -> None:
		if self.yet_to_init:
			return
		self._buf = ''
		self.cln_res(False)

	def _activate_exception(self, err: str) -> NoReturn:
		dumper = f'\nDUMP##COLLECTED##TOKEN##OF##{self.src_abs_path}\n'
		for tok in self.res:
			dumper += tok.__str__() + '\n'
		dumper += 'END##OF##DUMPING##COLLECTED##TOKEN\n\n'
		ve = ValueError(
			dumper +
			f'in {self.src_abs_path}\n'
			f'(line-{self._linum} '
			f'rang-{self._stp:05d}#{self._edp:05d})\n' +
			err
		)
		self._buf = ''
		self._cur_type = JSTokTy.illegal
		self._cur_literal = self._cur_sign = ''
		self.res = []
		raise ve

	def _mal_(
		self,
		ty: JSTokTy,
		reason: str = '',
		tok_name: str = ''
	) -> NoReturn:
		"""抛出错误不会返回"""
		self._activate_exception(
			f'found invalid {tok_name} behind `{ty}`'
			f'{reason}\n'
			f'current literal: {self._cur_literal}'
		)

	_mal_eof_ = partialmethod(_mal_, tok_name='eof')
	_mal_endl = partialmethod(_mal_, tok_name='endl')

	def _push2res(
		self,
		ty: JSTokTy,
		ch: str,
		linum: Optional[int] = None,
		pos: Optional[list[int]] = None
	) -> None:
		self.res.append(
			JSTok(
				ty=ty, literal=ch,
				line=self._linum if linum is None else linum,
				st_pos=self._stp if pos is None else pos[0],
				ed_pos=self._edp if pos is None else pos[1]
			)
		)

	def _cancel_state_and_push(
		self,
		ty: JSTokTy,
		linum: Optional[int] = None,
		pos: Optional[list[int]] = None
	) -> None:
		self._cur_type = JSTokTy.illegal
		self._cur_sign = ''
		self._push2res(ty, self._cur_literal, linum, pos)
		self._cur_literal = ''

	def _asg_aux(self, cur: str, nxt: str) -> tuple[None, None]:
		"""
		'!=' 或者 '!==' 或者 '!=(' 或者 '!=＿'
			 或者 '!=a'bc 或者 !=\r\n接入下一行
		"""
		fut = self._pik_ch()
		res = cur + nxt
		if fut == '':
			self._mal_eof(js_tk_lut[res])
		elif fut == '=':
			res += nxt
		else:
			self._ret_chs()
		return self._push2res(js_tk_lut[res], res), None

	def _multi_asg_op_aux(self, cur: str, fut: str) -> tuple[None, None]:
		res = cur * 2 + fut
		# >>= <<= === ??=
		if fut == '=':
			return self._push2res(js_tk_lut[res], res), None
		if cur != fut or fut != '>':
			res = res[:-1]
			ty = js_tk_lut[res]
			return self._ret_chs(), self._push2res(ty, res)
		# >>> >>>=
		now = self._pik_ch()
		if now == '': self._mal_eof(js_tk_lut[res])
		elif now == '=': res += '=' # >>>=
		else: self._ret_chs()
		return self._push2res(js_tk_lut[res], res), None

	def _handle_enter_in_regex(
		self,
		inp: str,
		has_close: bool
	) -> str:
		if len(inp) == 1 and inp in '/*':
			self._ret_chs()
			return 'c'
		elif len(inp) == 0:
			self._ret_chs()
			return 'd'
			# if not has_close:
			# /=123/.test()
			# /=123/;
			# /=123;
			# 但是这个分支被判掉了
		self._activate_exception(
			'does not close slash but invalid endline!'
		)
		# self._ret_chs()
		# return 'r'

	@property
	def _handler_escape_char_in_regex(self) -> str:
		# 这里不能用字符串的处理方式? 这里还有 \W \S \w \s 没有处理
		nxt = self._pik_ch()
		if nxt == '':
			self._activate_exception(
				'invalid end_of_file during parsing regex_obj!'
			)
		elif nxt in enter_set:
			self._activate_exception(
				'invalid enter char left regex undone'
			)
		# 可选的字符有
		# \dDwWsStfvrnux0[](){}*/\$^.
		# 直接连同nxt一起记录
		elif nxt not in regex_deter_chars:
			# self._activate_exception(f'invalid escape for char {ch}')
			# 理解为无效转义，拿走\只留下nxt
			# return '\0'
			return nxt
		elif nxt == 'x':
			digit = self._pik_ch(2)
			self._is_valid_hexeq(digit, 'x')
			return bytes.fromhex(digit).decode('iso-8859-1')
		elif nxt == 'u':
			tmp, _ = self._unicode_represent_in_chars(
				flag=False,
				need_id_checker=False
			)
			return tmp
		# 不然全部保留字面量
		return '\\' + nxt

	@property
	def _handle_regex_flags(self) -> str:
		flags_rec = ''
		while True:
			maybe_flag = self._pik_ch()
			if maybe_flag not in regex_flag_chars:
				self._ret_chs()
				break
			elif maybe_flag in flags_rec:
				self._activate_exception('reduplicate flags in regex!')
			flags_rec += maybe_flag
		return flags_rec

	def _regex_handler(self) -> tuple[str, str]:
		"""
		开局一个 /
		注意到/gugugaga/mygdiu[Symbol.split]; 这个是valid的
		保留字面量并留给regex引擎来分析

		regex 和 /, /=, // 之流存在二义性
		但
			/= 前面一定有数字或者identy
			/ 前面一定有数字或者 identy
		而 regex 前面一定不能是这两个token

		https://eighthundreds.github.io/es6/es6-ch.html#sec-literals-regular-expression-literals
		https://tc39.es/ecma262/multipage/text-processing.html#sec-get-regexp.prototype.flags
		"""
		res = ''
		estimator = ''
		inside_class = False
		while True:
			ch = self._pik_ch()
			if ch in enter_set:
				# 有可能完全构不成regex, 但已经换行了，必须要退出
				estimator = self._handle_enter_in_regex(res)
				break
			elif ch == '\\':
				# 并判断是否是第一个字符
				res += self._handler_escape_char_in_regex
				continue
			elif ch in '[]':
				# [ RegularExpressionClassChars ]
				inside_class = ch == '[' or not ch == ']'
				res += ch
				continue
			elif len(res) == 0 and ch in '/*':
				estimator = 'c' # block-comment
				res = ch
				break
			elif ch != '/':
				res += ch
				continue
			res += ch
			if inside_class:
				continue
			estimator = 'r' # regex object
			res += self._handle_regex_flags
			break
			# 反例：/[(`.[+\-*/%<>=,?^&]/my;
			# 多个flags但不允许重复
		return res, estimator

	@property
	def _handle_id_continue(self) -> str:
		cont = ''
		while True:
			tmp = self._pik_ch()
			if is_id_continue(tmp):
				cont += tmp
				continue
			self._ret_chs()
			break
		return cont

	def _non_id_peeker(
		self,
		cur: str,
		cond: _peek_token_cond,
	) -> tuple[Optional[str], Optional[JSTokTy]]:
		nxt = self._pik_ch()
		sig = '.' if cond['qmask_type'] else '='
		res = cur + nxt
		if nxt == '':
			self._mal_eof(js_tk_lut[cur])
		elif nxt == sig and cond['assign_ty']:
			# != ==
			return self._asg_aux(cur, sig)
		elif nxt == sig and not cond['assign_ty']:
			# /=的反例：/=123/.test(r)
			# 好在能回头看token而筛出来
			# tm 哪个天才想的拿 / 做js regex分隔符？
			#					 做行块注释
			#					 做除号
			# += -= *= /= %= &= |= ^= ?.
			if cur != '/' or self.res[-1].ty == JSTokTy.identy:
				return None, self._push2res(js_tk_lut[res], res)
			self._ret_chs()
			# 否则就只会是正则表达式或者错误的情况
			tmp, _ = self._regex_handler()
			return None, self._push2res(JSTokTy.regex, cur+tmp)
		elif cond['repeat_ok'] and nxt == cur:  # ++ -- //
			if not cond['peek_twice']:
				res_ty = js_tk_lut[res]
				self._push2res(res_ty, res)
				return (res, res_ty) if cur == '/' else (None, None)
			# ** && || ?? == >> <<
			fut = self._pik_ch()
			if fut == '':
				self._mal_eof(js_tk_lut[res])
			elif cond['peek_more']:
				return self._multi_asg_op_aux(cur, fut)
			return self._ret_chs(), \
				   self._push2res(js_tk_lut[res], res)
		elif cond['other_char'] != '' and \
			 nxt == cond['other_char']:  # /* <!--
			if res == '/*':
				self._push2res(js_tk_lut['/*'], res)
				return res, js_tk_lut[res]
			dashline = self._pik_ch(2)
			if dashline == '--':
				self._push2res(js_tk_lut['<!--'], res + dashline)
				self._stp = self._edp
				return res + dashline, js_tk_lut['<!--']
			# 否则有可能按照 <!(123 + 123) 这种奇怪的表达式来理解
			#				<!-(123 + 123)
			# 反例: let g = /<!--*/
			return self._ret_chs(3), \
				   self._push2res(js_tk_lut['<'], '<')
		elif cur == '/' and len(self.res) > 0 and \
			assume_regex(self.res[-1].ty):
			# 否则就理解为单纯的除号
			# 这个时候 nxt 都匹配不上那只能是潜在的正则表达式或者单纯的 / 了
			self._ret_chs()
			tmp, sug_type = self._regex_handler()
			if sug_type == 'r': # regex
				self._push2res(JSTokTy.regex, cur + tmp)
			elif sug_type == 'd': # div
				self._push2res(js_tk_lut['/'], '/')
			return None, None
		elif cur == '#' and is_id_start(nxt):
			return None, self._push2res(
				JSTokTy.pemIdenty,
				nxt+self._handle_id_continue
			)
		else:
			res = cur
		return self._ret_chs(), \
			   self._push2res(js_tk_lut[res], res)

	def _unicode_id_checker(
		self,
		inp: str,
		start_flag: bool
	) -> bool:
		if len(inp) > 1:
			self._activate_exception(
				f'illegal operation caused by {inp}!'
			)
		if not start_flag and not is_id_start(inp):
			self._activate_exception(
				'invalid unicode start char'
			)
		elif not start_flag:
			start_flag = True
		elif not is_id_continue(inp):
			self._activate_exception(
				'invalid unicode continue char'
			)
		return start_flag

	def _unicode_represent_in_chars(
		self,
		flag: bool,
		need_id_checker: bool=True
	) -> tuple[str, bool]:
		maybe_digit = self._pik_ch()
		if maybe_digit != '{':
			maybe_digit += self._pik_ch(3)
			self._is_valid_hexeq(maybe_digit, 'u')
			res = chr(int(maybe_digit, 16))
		else:
			res = self._codepoint_2_char(self._uni_lbr_form.zfill(6))
		if need_id_checker:
			flag = self._unicode_id_checker(res, flag)
		return res, flag

	def _concat_identy(self, started: bool) -> tuple[bool, bool]:
		c = self._pik_ch()
		if c not in pause_idt and c not in ['', '\\']:
			if not started:
				started = True
			self._literal_add(c)
			return True, started
		elif c == '\\':
			if self._pik_ch() == 'u':
				tmp, started = self._unicode_represent_in_chars(started)
				self._literal_add(tmp)
				return True, started
			self._activate_exception(
				"invalid representation for identy "
				"violated against es6's rule of identifier!"
			)

		# 得判断 _cur_literal 是不是关键字
		token_type = JSTokTy.identy
		if self._cur_literal in js_tk_lut:
			token_type = js_tk_lut[self._cur_literal]
		if c != '':
			self._ret_chs()
		self._push2res(token_type, self._cur_literal)
		self._cur_literal = ''
		return False, started

	def _identy_extractor(self, intro: str) -> None:
		# \u1234, uni_id uni_continue 也能作为标识符使用
		# 没有单独处理转义，直接到这里还是可行的
		self._cur_literal = intro
		has_start: bool = False
		while True:
			state, has_start = self._concat_identy(has_start)
			if not state:
				break

	def _num_pass(
		self,
		state: JSTokTy,
		cut: int,
		buf_pos: int
	) -> bool:
		if state == JSTokTy.illegal:
			return False
		self._ret_chs(buf_pos)
		self._push2res(state, self._cur_literal[:cut])
		self._cur_literal = ''
		return True

	def _calc_state(self, sign: str, sign_pos: int = 0) -> bool:
		# cacl_state-1:  -1 + 2 1+
		lena = len(self._cur_literal)-1
		step = self._cur_literal.find(sign, min(sign_pos, lena))
		cut_literal = step
		part = self._cur_literal[:step]
		step = len(self._cur_literal) - step + 1
		state = _num_dfa.validator(part)
		# 1 JSTokTy.integer -1 4
		return self._num_pass(state, cut_literal, step)

	def _check_sign(self, sign: str) -> bool:
		cnt = self._cur_literal.count(sign)
		if cnt == 0: return False

		valid = self._calc_state(sign, self._cur_literal.index(sign) + 1)
		return self._calc_state(sign) if not valid else True

	def _number_extractor(self, intro: str) -> None:
		"""
		354 +
		355 1
		check_sign:  1+ 1 +
		cacl_state:  -1 + 2
		cacl_state:  1 4 JSTokTy.integer
		"""
		# 读到运算符或者分隔符为止
		self._cur_literal = intro
		while True:
			c = self._pik_ch()
			if c in num_shape:
				# TODO: 1 + 1 + 2 + 3
				# 这种反而就识别不了了
				self._literal_add(c)
				continue
			# 放过了一些奇怪的东西 eg: 12var
			final_state = _num_dfa.validator(self._cur_literal)
			if self._num_pass(final_state, len(self._cur_literal), 1) or \
				self._check_sign('+') or self._check_sign('-'):
				return
			# 不然就异常，加减号拿掉了都不行
			self._activate_exception(
				f'as if the given literal is invalid: `{self._cur_literal}`'
			)

	def _nonstandard_oct(self, nxt: str) -> tuple[str, int]:
		_digit_ch_2num = lambda xx: ord(xx) - ord('0')
		_oct_fn = lambda xx: xx * 8
		_oct_base = lambda xx: _oct_fn(_digit_ch_2num(xx))

		# 入口：\[0-9]?$
		# 最多可能读2次
		pik = self._pik_ch(2)
		if pik[0] not in octable:
			fnxt, ofs = f'0{nxt}', 2
		elif pik[1] not in octable:  # \34 := 4 + 3 * 8
			x = _oct_base(nxt) + _digit_ch_2num(pik[0])
			fnxt, ofs = f'{hex(x)[2:]}', 1
		else:
			x = _oct_base(nxt) * 8 + _oct_base(pik[0]) + \
				_digit_ch_2num(pik[1])
			ofs = 1 if x >= 256 else 0
			x = (x - _digit_ch_2num(pik[1])) >> 3 if x >= 256 else x
			fnxt = f'{hex(x)[2:]}'
		self._ret_chs(ofs)
		return bytes.fromhex(fnxt).decode(), 2 - ofs

	def _check_unicode_in_range(self, inp: str) -> None:
		if 0 <= int('0x'+inp, 16) <= 0x10FFFF: return
		self._activate_exception(
			'invalid unicode due to out of range!'
		)

	@staticmethod
	def _codepoint_2_char(inp: str) -> str:
		return chr(int(inp, 16))

	@property
	def _uni_lbr_form(self) -> str:
		"""只保证了在0x0-0x10FFFF里面"""
		unicode, cnt, closure = '', 0, False
		# 最多读7次
		# 10FFFF}
		while cnt <= 6:
			uni = self._pik_ch()
			if uni == '':
				self._activate_exception(
					"unexpected null during parsing "
					"unicode in escaped char handler!"
				)
			elif uni == '}':
				closure = True
				break
			cnt += self._is_valid_hexeq(uni, 'u')
			unicode += uni

		if not closure:
			self._activate_exception(
				"found regex string without closure	`/` !"
			)
		self._check_unicode_in_range(unicode)
		return unicode

	def _is_valid_hexeq(self, inp: str, kind: str) -> int:
		if reduce(lambda x, y: x & y, map(ch_in_hex, inp)):
			return len(inp)
		self._activate_exception(
			f'invalid unicode representation in \\{kind}{inp}!'
		)

	def _escaped_char_handler(self) -> tuple[str, int]:
		pik = 1
		nxt = self._pik_ch()
		if nxt == 'u':
			# https://ziglang.org/documentation/0.14.1/#toc-Escape-Sequences
			# Unicode可以最多编码1114112个字符(也即 U+0000 ~ U+10FFFF).
			# 常用的都在 U+0000 ~ U+FFFF，第0分区. 总共有 17 个分区
			# 用的时候如果只是 \u 而非 \u{} 时，就只有 4 个
			# 否则就有1-6个hex-digit(s), 读到}为止
			exam = self._pik_ch()
			if exam == '{':
				seq = self._uni_lbr_form
				pik += len(seq)
				fnxt = self._codepoint_2_char(seq.zfill(6))
				return fnxt, pik
			else:
				self._ret_chs()
			seq = self._pik_ch(4)
			pik += self._is_valid_hexeq(seq, nxt)
			fnxt = chr(int(seq, 16))
		elif nxt == 'x':
			seq = self._pik_ch(2)
			pik += self._is_valid_hexeq(seq, nxt)
			fnxt = bytes.fromhex(f'{seq}').decode('iso-8859-1')
		elif nxt in octable:
			fnxt, sup = self._nonstandard_oct(nxt)
			pik += sup
		else:
			fnxt = get_escaped_ch_in_str(nxt)
		return (fnxt, pik) if fnxt != '' else (nxt, pik)

	def _literal_add(self, c: str) -> bool:
		self._cur_literal += c
		return True

	def _block_comment_ed_aux(self, c: str) -> bool:
		def _endl_aux(inp: str) -> bool:
			self._literal_add(inp)
			if inp not in enter_set:
				return True
			self._push2res(
				JSTokTy.comment, self._cur_literal,
				self._linum, [self._stp, self._edp]
			)
			self._linum += 1
			self._reset_pos()
			self._cur_literal = ''
			return True

		if c != '*': return _endl_aux(c)
		nxt = self._pik_ch()
		if nxt == '/':
			# 块注释结束
			if self._cur_literal != '':
				self._push2res(
					JSTokTy.comment, self._cur_literal,
					pos=[self._stp, self._edp-2]
				)
			self._cur_literal = '*/'
			self._cancel_state_and_push(
				JSTokTy.block_comment_ed,
				pos=[self._edp-1, self._edp]
			)
			return True
		elif nxt == '':
			self._mal_eof(
				JSTokTy.comment,
				' and without `block_comment_ed`!'
			)
		self._literal_add(c)
		return _endl_aux(nxt)

	def _line_comment_ed_aux(self, c: str) -> bool:
		guess = self._pik_ch(2)
		if c + guess != '-->':
			self._ret_chs(2)
			return self._literal_add(c)
		ch = self._pik_ch()
		if ch not in enter_set and ch != '':
			# 必须是换行或终结符
			# TODO: 好像不完全是这样
			# var a = <!-- 123 --> "a";
			# 但是这样子以后后面测试发现上面这条语句的后一句就不能再声明变量
			# 没在实战遇到暂时先不管了
			self._activate_exception(
				f'invalid char `{ch}` after token `-->`!'
			)
		self._cur_literal += ch
		edp = self._edp
		self._edp -= 3 # */\n总共是3，2就挪到*的位置
		self._cancel_state_and_push(JSTokTy.comment)
		self._edp = edp
		self._stp = edp - 2
		self._push2res(JSTokTy.line_comment_ed, f'{c}{guess}')
		return self._if_enter('\n')

	def _comment_or_str_aux(self, c: str) -> bool:
		def split_via_endl(inp: str = c) -> bool:
			self._literal_add(inp)
			self._push2res(JSTokTy.string, self._cur_literal)
			self._cur_literal = ''
			self._if_enter('\n')
			return True

		if self._cur_type == JSTokTy.string:
			# \" \' \` \t \n \\
			if c == '\\':
				calc, _ = self._escaped_char_handler()
				return split_via_endl(calc) \
					if calc in enter_set \
					else self._literal_add(calc)
			elif c != self._cur_sign:
				return self._literal_add(c) \
					if c not in enter_set \
					else split_via_endl()
			self._push2res(
				JSTokTy.string, self._cur_literal,
				self._linum, [self._stp, self._edp-1]
			)
			self._cur_literal = c
			self._stp = self._edp
			self._cancel_state_and_push(js_tk_lut[c])
			return True
		elif self._cur_type in [
				JSTokTy.line_comment_st_1,
				JSTokTy.line_comment_st_2
			]:
			if self._stp_fix:
				self._stp_fix = False
				self._stp = self._edp
			if self._cur_sign == '//':
				if c not in enter_set:
					return self._literal_add(c)
				self._literal_add(c)
				self._cancel_state_and_push(JSTokTy.comment)
				return self._if_enter('\n')
			if c == '-':
				return self._line_comment_ed_aux(c)
			elif c not in enter_set:
				return self._literal_add(c)
			self._mal_endl(
				JSTokTy.comment,
				' end before `line_comment_ed`'
			)
		elif self._cur_type == JSTokTy.block_comment_st:
			if self._stp_fix:
				self._stp_fix = False
				self._stp = self._edp
			return self._block_comment_ed_aux(c)
		return False

	def _binop_aux(self, c: str) -> bool:
		self._stp = self._edp
		cond: _peek_token_cond = {
			"repeat_ok" : c in repeatable, # ++ -- // **
			"peek_twice": c in twicenable, # >>>= &&= ||= **= ===
			"qmask_type": c == '?',
			"assign_ty" : c in '!=',
			"other_char": commapsign[c] if c in '/<' else '',
			"peek_more" : c in '>?'
		}
		ans, ty = self._non_id_peeker(c, cond)
		if ty in [
			JSTokTy.block_comment_st,
			JSTokTy.line_comment_st_1,
			JSTokTy.line_comment_st_2
		]:
			self._cur_sign = ans
			self._cur_type = ty
			self._stp_fix = True
			return True
		return ty is None

	def _dot_aux(self, c: str) -> None:
		# 成员变量或者 ... 或者小数 .535 这样的
		nxt = self._pik_ch()
		if nxt in decable:
			if self._cur_literal == '':
				return self._number_extractor(c + nxt)
			self._activate_exception(
				'invalid member started with digit!'
			)
		fut = self._pik_ch()
		if nxt == fut and nxt == c:
			return self._push2res(JSTokTy.omit, '...')
		self._ret_chs(2)
		return self._push2res(JSTokTy.dot, '.')

	@property
	def _internal_tokenizer(self) -> int:
		c = self._pik_ch()
		if c == '':
			if self._cur_type == JSTokTy.illegal \
			or self._cur_sign == '':
				self._edp += 1
				self._stp = self._edp
				self._push2res(JSTokTy.end_of_file, '')
				return 0
			self._mal_eof(
				self._cur_type,
				f'unexpected given input {self._cur_type.name}'
			)
		elif self._comment_or_str_aux(c) or c in spacetab or \
			(c in js_operats+'#' and self._binop_aux(c)) or \
			self._if_enter(c):
			# 注释、空格或者++ -- ** // ?? && || << >> ==或者换行
			return 1

		self._stp = self._edp
		if c in decl_str:
			# 语法分析器去管括号匹配的事情
			# 字符串引号也留给语法分析器分析
			self._cur_type = JSTokTy.string
			self._cur_sign = c
			self._push2res(js_tk_lut[c], c)
			self._stp = self._edp + 1
		elif c in delimiters:
			self._push2res(js_tk_lut[c], c)
			self._stp = self._edp + 1
		elif c == '.':
			self._dot_aux(c)
		elif c in decable:
			self._number_extractor(c)
		# identy和保留字一直读到换行或者空白或者其它运算符为止
		else:
			self._identy_extractor(c)
		return 1

	@property
	def tokenize(
		self,
		encoden: str='utf-8',
		custom_buff: Optional[str]=None
	) -> list[JSTok]:
		"""
			只负责读某个文件里的源码并顺序生成源文件包含的所有token。
			对应的dfa转为代码实现极其琐碎。

			目前并不是生成器类型的，需要解析完整个源码才能执行
		"""
		if custom_buff is None:
			self._set_buf_via_src(encoden=encoden)
		else:
			self.src_abs_path = ''
			self._buf = custom_buff
			self.cln_res()
		while True:
			# 浏览器环境下不需要 hashbang
			# 但倒是有 'use strict';
			# #! /usr/bin/env node
			# // js code...
			if self._internal_tokenizer == 0:
				break
		self._unset_buf()
		return self.res

	@property
	def strip(self) -> None:
		alter, lenr = [], len(self.res)
		for i in range(0, lenr):
			t = self.res[i].ty
			if t not in [
				js_tk_lut['//'], js_tk_lut['<!--'],
				js_tk_lut['-->'], js_tk_lut['/*'],
				js_tk_lut['*/'], JSTokTy.comment
			]:
				alter.append(t)
				continue
				# elif t == JSTokTy.endl:
				# 	i += 1
			if t == js_tk_lut['//']:
				# a; // 123
				i += 2
			elif t == js_tk_lut['<!--']:
				# TODO: 这个尖括号做的话就要写一堆有的没的
				# a;<!-- only permit -->
				i += 3
			elif t == js_tk_lut['/*']:
				j = i
				while j < lenr and self.res[j].ty != js_tk_lut['*/']:
					j += 1
				i += j - i
		self.res = deepcopy(alter)
		alter.clear()

