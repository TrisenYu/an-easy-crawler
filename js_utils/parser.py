#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025-06>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/03 星期五 00:13:56
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
WARN: 没写完没有测的半成品

Referer:
  	fla.cuijiacai.com
  	docs.python.org/zh-cn/3/library/ast.html
  	www.npmjs.com/package/acorn?activeTab=code
  	orn/dist/acorn.d.mts, acorn.d.ts
  	github.com/chaxus/ranlexer
  	github.com/v8/v8/blob/main/src/parsing/parser.cc
  	tc39.es/ecma262/multipage/ecmascript-language-lexical-grammar.html
  	github.com/estree/estree/blob/master/[es2015-es2025].md
  	0x3a0x29.github.io/p/contextfree/
  	raw.githubusercontent.com/PiotrDabkowski/pyjsparser/refs/heads/master/pyjsparser/parser.py
  	cs.nju.edu.cn/tiantan/courses/compiler-2025/lectures/4-syntax.pdf
	ecma262.com/#sec-ecmascript-language-functions-and-classes
	v8.dev/blog/understanding-ecmascript-part-4 part-3

语义分析？
相比字符流转token流更麻烦

做完这个后面就要将语句按条件拆解为dag作为基本块来用了
最多也只做到基本块这一步，同时精简原有结构

不过看上去整个编译器实际上就是超级庞大的、存在二义的代数替换？
原本想用LL(1)非预测分析表做掉这个问题但发现

new_expr、mem_expr、unary_expr和update_expr 就是彻彻底底的毒瘤

此外，发现要逆向的代码中用到了require语句来导入其他模块，而require在标准中是
没有的，这个只在CommonJS中用，所以写完以后还需要看CommonJS的标准

如果能顺利搞完这个，就要考虑怎么折腾标准块了
"""
from js_utils.stmts_def import (
	unary_prefix, unary_suffix,

	JSStmt, JSExpr,

	JSBlockStmt, JSExprStmt,
	# branch
	JSIfStmt,
	JSSwitchStmt,
	JSSwitchCases,
	# loop
	JSForStmt,
	JSForInStmt,
	JSForOfStmt,
	# -- loop --
	JSWhileStmt,
	JSDoWhileStmt,
	# error-ctrl
	JSTryStmt,
	JSThrowStmt,
	JSDebuggerStmt,

	JSWithStmt,
	# cfg
	JSCtrolFlowStmt,
	JSBreakStmt,
	JSContinueStmt,
	JSRetnStmt,

	# TODO: ? export 语句
	# 还得导入其他文件的定义
	JSImportDecl,

	JSAsgExpr,
	JSBinExpr,
	JSlogicExpr,
	JSCondExpr,
	JSNewExpr
)
from js_utils.lexer import JSLexer
from js_utils.tokens_def import (
	JSTok, JSTokTy
	js_tk_lut
)

from typing import Optional
from functools import partialmethod
from collections.abc import Callable
# from collections import deque
# from enum import Enum

class _identyInfo:
	name: str
	scope_stk: str
	# extern

class JSASTPaser:
	"""
	es2026
		12 ECMAScript Language: Lexical Grammar
		13 ECMAScript Language: Expressions

	写起来槽点特别多

	只检查src内的语义，
	noLineTerm:
		continue _ label;
		break _ label;
		return _ expr;
		throw _ expr;
		async _ function / MethNameInClass
		arrowParam _ =>
		yield _ Opt<*> assignment
		lpart _ ++/--
	"""
	lexer: JSLexer = JSLexer('')
	tok_cnt: int = 0

	# 直接用append和pop就行
	is_async: bool = False
	is_func: bool = False
	is_gen: bool = False
	is_loop: bool = False
	is_func_args: bool = False
	is_directive: bool = False

	known_labels = set()


	@property
	def _is_endl_ok(self) -> bool:
		return self._pre_tok.ty not in [
			JSTokTy.Continue, JSTokTy.Break,
			JSTokTy.Return, JSTokTy.throw,
			JSTokTy.Async, JSTokTy.Yield
		] and self._nxt_tok not in [
			js_tk_lut['=>'], js_tk_lut['++'],
			js_tk_lut['--']
		]

	@property
	def _is_new_line(self) -> bool:
		""" check whether current token is at a new line"""
		return self._cur_tok.line != self._pre_tok.line

	def set_src(self, src_abs_path: str) -> None:
		self.lexer.set_src(src_abs_path)

	@property
	def _cur_tok(self) -> JSTok:
		if self.tok_cnt >= len(self.lexer.res):
			return JSTok()
		return self.lexer.res[self.tok_cnt]

	@property
	def _nxt_tok(self) -> JSTok:
		if self.tok_cnt >= len(self.lexer.res) - 1:
			return JSTok()
		return self.lexer.res[self.tok_cnt + 1]

	@property
	def _pre_tok(self) -> JSTok:
		if self.tok_cnt == 0 or self.tok_cnt >= len(self.lexer.res):
			return JSTok()
		return self.lexer.res[self.tok_cnt - 1]

	@property
	def _pik_tok(self) -> JSTok:
		if len(self.lexer.res) == 0 or \
		   self.tok_cnt >= len(self.lexer.res):
			return JSTok()
		res = self._cur_tok
		self.tok_cnt += 1
		return res

	def _eat_tok(self, goal: JSTokTy) -> bool:
		if self._cur_tok.ty == goal:
			self._pik_tok
			return True
		return False

	def _expect_tok(self, sign: str) -> JSTok:
		expect = self._eat_tok(js_tk_lut[sign])
		if not expect:
			raise ValueError('expect `sign` but found {expect}')
		return expect

	@property
	def _can_insert_semi(self) -> bool:
		# TODO: return not options.strict and ...
		return self._cur_tok.ty in [
			js_tk_lut[';'], js_tk_lut['}'],
			JSTokTy.end_of_file,
		] or self._is_endl_ok or self._is_new_line

	@property
	def _check_semi(self) -> bool:
		return self._eat_tok(js_tk_lut[';']) or self._can_insert_semi

	@property
	def _try_add_semi(self) -> None:
		if self._check_semi: return
		raise ValueError(
			'unable to insert semicolon '
			f'after this token `{self._cur_tok}`!'
		)

	# 先从最简单的开始
	# start from the easist
	# ===================== debugger ==========================
	@property
	def _parse_debugger_stmt(self) -> JSDebuggerStmt:
		debugger = self._pik_tok
		self._try_add_semi
		return JSDebuggerStmt().set_lxx(debugger, self._cur_tok)

	# ===================== try ==========================
	@property
	def _parse_try_stmt(self) -> JSTryStmt:
		"""
		try { tryStmt }
		catch ( expr ) { catchStmt }
		finally { finalStmt }
		"""
		_try = self._pik_tok
		block = self._parse_block_stmt
		_catch, _fin = None, None
		# TODO
		if self._eat_tok(js_tk_lut['catch']):
			"""
			BindingIdentifier[?Yield, ?Await]
			BindingPattern[?Yield, ?Await]
			"""
			expr = self._parse_paren_expr
			_cat_block = self._parse_block_stmt

		if self._eat_tok(js_tk_lut['Finally']):
			_fin = self._parse_block_stmt

		if _catch is None and _fin is None:
			raise ValueError(
				'expect at least catch or finally statement to handle'
				'error, but got None of them!'
			)
		return JSTryStmt(
			handler=_catch, final=_fin
		).set_lxx(_try, self._cur_tok)

	# ===================== throw ==========================
	@property
	def _parse_throw_stmt(self) -> JSThrowStmt:
		"""
		 ThrowStatement[Yield, Await]
			throw [no LineTerminator here] Expression[+In, ?Yield, ?Await] ;
		"""
		_throw = self._pik_tok
		if self._is_new_line:
			raise ValueError(
				'no lineTerm rule of throw statement was violated!'
			)
		_expr = self._parse_expr
		self._try_add_semi
		return JSThrowStmt(args=_expr).set_lxx(_throw, self._cur_tok)

	# ===================== with ==========================
	@property
	def _parse_with_stmt(self) -> JSWithStmt:
		"""
		WithStatement[Yield, Await, Return] :
		with ( Expression[+In,?Yield,?Await] ) Statement[?Yield,?Await,?Return]
		"""
		_with = self._pik_tok
		cond = self._parse_paren_expr
		stmt = self._parse_stmt
		return JSWithStmt(
			obj=cond,
			body=stmt
		).set_lxx(_with, self._cur_tok)

	# ===================== return ==========================
	@property
	def _parse_return_stmt(self) -> JSRetnStmt:
		_ret = self._pik_tok
		val = None
		if not self._check_semi:
			self._try_add_semi
			val = self._parse_expr
		if not self.is_func:
			raise ValueError('return outside of function!')
		return JSRetnStmt(args=val).set_lxx(_ret, self._cur_tok)

	# ===================== break/continue ==========================
	@property
	def _parse_break_continue_stmt(self) -> JSCtrolFlowStmt:
		_is_break = self._cur_tok.ty == 'break'
		self._pik_tok
		label = None
		if not self._check_semi:
			label = self._parse_label_identy
			if label not in self.known_labels:
				raise ValueError(
					'unknow label was used without declaration!'
				)
			self.known_labels.add(
				# TODO: 检查标签是否有效并分配作用域
			)
		if not self.is_loop:
			raise ValueError(
				'break outside of loop or switch!'
			)
		self._try_add_semi
		return JSBreakStmt(label=label) if _is_break \
			else JSContinueStmt(label=label)

	# ===================== while ==========================
	@property
	def _parse_while_stmt(self) -> JSWhileStmt:
		_while = self._pik_tok
		cond = self._parse_paren_expr
		body = self._parse_stmt
		return JSWhileStmt(
			cond=cond, body=body
		).set_lxx(_while, self._cur_tok)

	# ===================== do-while ==========================
	@property
	def _parse_do_while_stmt(self) -> JSDoWhileStmt:
		_do = self._pik_tok
		body = self._parse_stmt
		self._expect_tok('while')
		cond = self._parse_paren_expr
		self._expect_tok(';')
		return JSDoWhileStmt(
			body=body, cond=cond
		).set_lxx(_do, self._cur_tok)

	# ===================== if ==========================
	@property
	def _parse_if_stmt(self) -> JSIfStmt:
		_if = self._pik_tok
		cond = self._parse_paren_expr
		then = self._parse_stmt('if')
		other = None
		if self._eat_tok(js_tk_lut['Else']):
			"""
			else -- {}
			else -- stmt
			else -- if ()
			"""
			other = self._parse_stmt('if')
		return JSIfStmt(
			cond=cond, then=then, other=other
		).set_lxx(_if, self._cur_tok)

	# ===================== switch ==========================
	def _check_cond_in_case(self, cond: JSExpr) -> bool:
		...

	def _calc_cases_body(self, ty: str) -> list:
		_colon = self._expect_tok(':')
		res = []
		while self._cur_tok.ty not in [
			js_tk_lut['}'], js_tk_lut['case'],
			js_tk_lut['default']
		]:
			res.append(self._parse_stmt(ty))
		return res

	@property
	def _handle_case_default(self, has_defaut: bool) -> JSSwitchCases:
		cond = None
		if self._cur_tok.ty == js_tk_lut['case']:
			_case = self._pik_tok
			cond = self._parse_expr
			if self._check_cond_in_case(cond):
				raise ValueError('double cond in current switch!')
			body = self._calc_cases_body('case')
		elif self._cur_tok.ty == js_tk_lut['default']:
			if has_default:
				raise ValueError('double default in current switch scope!')
			has_default = True
			_case = self._pik_tok
			body = self._calc_cases_body('default')
		else:
			raise ValueError('unexpected token in current scope of switch!')
		return JSSwitchCases(cond=cond, body=body), has_default

	@property
	def _parse_switch_stmt(self) -> JSSwitchStmt:
		"""
		switch ( target ) {
		case expr:
			stmt;
		default:
			stmt;
		}
		default 和 case 至少要存在一个
		"""
		_switch = self._pik_tok
		target = self._parse_paren_expr
		cases: list[JSSwitchCases] = []
		self._expect_tok('{')
		has_default = False
		while self._cur_tok.ty != js_tk_lut['}']:
			_case, has_default = self._handle_case_default(has_default)
			cases.append(_case)
		self._expect_tok('}')
		return JSSwitchStmt(
			target=target, cases=cases
		).set_lxx(_switch, self._cur_tok)

	# ===================== expr ==========================
	def _parse_args_in_expr(self):
		"""
		args[Yield, Await] :
			({<opt>(...) asg_expr ,}* )
			({<opt>(...) asg_expr ,}* <opt>(...)asg_expr )
		"""
		...

	def _parse_arr_in_asg(self):
		"""
		arr_literal =>
			[ <opt>(,)* ]
			[ <opt>(,)* asg_expr, <opt>(,)* <opt>(...) <opt>(asg_expr) <opt>(,) ]
			[]
			[,]
			[,,,,asg]
			[,,,,asg,]
			[,,,,asg,asg,,,asg]
			[,,,,asg,asg,,,asg,...asg,]
			[,,,,asg,asg,,,asg,...asg]
			[,,,,asg,asg,,,,...asg]
			[,,,,asg,...asg]
		"""
		self._expect_tok('[')
		while self._cur_tok.ty != js_tk_lut[']']:
			ty = self._cur_tok.ty
			if ty == js_tk_lut[',']:
				# 填入undefine
				_ = self._pik_tok

				continue
			elif ty == js_tk_lut['...']:
				# ... asg_expr
				self._pik_tok
				continue
			# else parse asg_expr
			expr = self._parse_assign_expr

		self._expect_tok(']')
		...

	def _parse_obj_in_asg(self):
		"""
		ObjectLiteral[Yield, Await] :
			{ (proper_def ,)* }
			{ (proper_def ,)* proper_def }

		proper_def[Yield, Await] :
			meth_def[?Yield, ?Await]
			id_ref
			id_ref = asg_expr
			identy : asg_expr[+In, ?Yield, ?Await]
			[ asg_expr ] : asg_expr[+In, ?Yield, ?Await]
			... asg_expr[+In, ?Yield, ?Await]
		LiteralPropertyName :
			id_name # id_start id_continue ~ identy
			string
			number

	meth_def[Yield, Await] :
		# meth
		<opt>(async)_n <opt>(*) class_elem_name[?Yield, ?Await] ( FormParams[~Yield, ~Await] ) { FuncBody[~Yield, ~Await] }
		get class_elem_name[?Yield, ?Await] ( ) { FuncBody[~Yield, ~Await] }
		set class_elem_name[?Yield, ?Await] ( FormalParameter[~Yield, ~Await] ) { FunctionBody[~Yield, ~Await] }

	ClassElementName[Yield, Await] :
		identy
		number
		string
		[ asg_expr ]
		# id_name ~ # identy
	form_params:
		[empty]
		FunctionRestParameter[?Yield, ?Await]
		FormalParameterList[?Yield, ?Await]
		FormalParameterList[?Yield, ?Await] ,
		FormalParameterList[?Yield, ?Await] , FunctionRestParameter[?Yield, ?Await]
		FormalParameterList[Yield, Await] :
		FormalParameter[?Yield, ?Await]
		FormalParameterList[?Yield, ?Await] , FormalParameter[?Yield, ?Await]
		FunctionRestParameter[Yield, Await] :
		BindingRestElement[?Yield, ?Await]
		FormalParameter[Yield, Await] :
		BindingElement[?Yield, ?Await]
		"""
		...

	def _parse_yield_expr(self):
		...

	# TODO: 下面函数的调用栈有点要命，最好改成非递归处理
	# 消除所有左递归，将其改为循环
	def _parse_prim_expr(self):
		"""
		数组元素可以在元素列表的开头、中间或末尾省略。
		当元素列表中的逗号前面没有
		AssignmentExpression（即开头的逗号或另一个逗号后面的逗号）时，
		缺失的数组元素会增加数组的长度并增加后续元素的索引。
		省略的数组元素未定义。如果在数组末尾省略了元素，该元素不会增加数组的长度。
		this
		identy_name | yield | await # 真逆天，后面这两个是什么鬼
		| null | boolean | integer | bigInt | Float
		' string+ '
		" string+ "
		args =>
			# 好像有直接留作的 ( expr )
			(  )
			( expr )
			( expr , )
			( ... binding_id )
			( ... binding_pattern )
			( expr , ... binding_id )
			( expr , ... binding_pattern )
		bind_pattern =>
			obj_bind_pattern[?Yield, ?Await] => { property : assign_expr,... }
			arr_bind_pattern[?Yield, ?Await] => [ ,bind_pattern,... ]
		property =>
			[ assign_expr ]
			IdentifierName
			StringLiteral
			NumericLiteral
		regex
		` tmpl_str `
		 # 内部有多个等待解析的串

		class binding_id extends LeftHandSideExpression { class_body } # static | [ computed_attr ] | pemId
		function <opt>(*) binding_id ( form_list ) { cond_stmts_list }
		async function <opt>(*) binding_id ( form_list ) { cond_stmts_list }

		"""
		ty = self._cur_tok.ty
		if ty == js_tk_lut['this']:
			this = self._pik_tok
			return JSThisExpr().set_lxx(this, self._cur_tok)
		elif ty == JSTokTy.identy:
			# 直接返回identy
			pass
		elif ty in [
			js_tk_lut['true'], js_tk_lut['false'],
			js_tk_lut['null'], JSTokTy.bigInt,
			JSTokTy.integer, JSTokTy.Float
		]:
			tk = self._pik_tok
			return JSLiteral(val=tk.literal).set_lxx(tk, self._cur_tok)
		elif ty in [js_tk_lut['"'], js_tk_lut["'"]]:
			tk = self._pik_tok
			cur_str = ''
			while self._cur_tok.ty == JSTokTy.string:
				char_arr = self._pik_tok
				cur_str += char_arr.literal
			self._expect_tok(ty.literal)
			return JSLiteral(

			)
		elif ty == js_tk_lut['`']:
			ty = self._pik_tok
			# TODO: parse tmpl_literal and return
			self._expect_tok('`')
			return
		elif ty == js_tk_lut['Async']:
			pass
		elif ty == js_tk_lut['function']:
			# function or gen
			pass
		elif ty == js_tk_lut['Class']:
			# class
			pass

	def process_tmpl(self, tmp: str):
		# 内部的 ${ xxx }
		# 可能是使用了已定义变量的表达式
		# 需要将结果填入到对应位置作为字符串使用
		# 但不可能提前算完，只能将其解析为字符串相加的表达式
		# 等到实际有值才能获取结果
		midd_strs: list[str] = []
		ids: list = []
		cnt, lena = 0, len(tmp)
		cur_str = ''
		need_close = False
		while cnt < lena:
			if tmp[cnt] != '$':
				cur_str += tmp[cnt]
				cnt += 1
				continue
			need_close = True
			if cnt + 1 < lena and tmp[cnt+1] == '{':
				# TODO: lexer 又要重新tokenize?
				# 我想是这样的
				# ${ expr }
				midd_strs.append(cur_str)
				cur_str = ''
			else:
				need_close = False
				cur_str += tmp[cnt]


	def _parse_lhs_expr(self):
		"""
		# 我到底是不是人啊！！
		# new_expr ：new多1~n个
		# mem_expr : 刚好够
		# call_expr : new 少
		# opt_expr: mem_expr 或 call_expr 后多一坨 ?. xxx
		# expr_first_tok:
			new super import ( [ { number id string regex tmpl class
		# context-free grammar
		LHS =>
			+ -------------------- new_expr
			|  new+ A cross_act{ (args)*, ( args | [ xpr ] | .id | tmpl )* }
			+		  数量一致
			+  +------------------+ mem_expr
			|  new* A cross_act{ (args)*, ( args | [ xpr ] | .id | tmpl )* }
			|
			+		  数量一致
			+  +------------------+ call_expr
				# mem_expr args
			| new* A cross_act{ (args)*, ( args | [ xpr ] | .id | tmpl )* } args ( args | [ xpr ] | .id | tmpl )*
			| super args ( args | [ xpr ] | .id | tmpl )*
			| import ( asg_expr <opt>(,) ) ( args | [ xpr ] | .id | tmpl )*
			| import ( asg_expr , asg_expr <opt>(,) ) ( args | [ xpr ] | .id | tmpl )*
			+
			+ --------------------  opt_expr
			| call_expr ?. ( args | '['expr']' | .(pem)identy | tmpl_literal)+
			| mem_expr ?. ( args | '['expr']' | .(pem)identy | tmpl_literal)+

		arr_literal =>
			[ <opt>(,) ]
			[ <opt>(,) asg_expr, ...asg_expr, ... ]
		obj_literal =>
			{ }
			... asg_expr[+In, ?Yield, ?Await]
			{ proper_def_list[?Yield, ?Await] }
			{ proper_def_list[?Yield, ?Await] , }

		"""
		decl_new = []
		while self._cur_tok.ty == js_tk_lut['new']:
			decl_new.append(self._pik_tok)
		decl_new = decl_new[::-1]
		ty = self._cur_tok.ty
		if ty == js_tk_lut['.']:
			# new.target
			cur_literal = self._pik_tok
			if len(decl_new) != 1 or cur_literal.ty != JSTokTy.identy or \
			   cur_literal.literal != 'target':
				raise ValueError(
					f'expect `new.target` but found `new.{cur_literal}`'
				)

		elif ty == js_tk_lut['this']:
			# this
			pass
		elif ty == js_tk_lut['`']:
			# tmpl_literal
			_tmpl = ''
			while self._cur_tok.ty != js_tk_lut['`']
				_tmpl += self._pik_tok.literal
			# TODO
			tmpl = self.process_tmpl(_tmpl)
			pass
		elif ty in [js_tk_lut['"'], js_tk_lut["'"]]:
			# string
			string = ""
			while self._cur_tok.ty != ty:
				string += self._pik_tok.literal
			quote = self._pik_tok
			# TODO: 检查 new
		elif ty in [JSTokTy.integer, JSTokTy.Float, JSTokTy.bigInt]:
			# number
			cur_literal = self._pik_tok
			# TODO: 检查 new
		elif ty == js_tk_lut['null']:
			# null
			pass
		elif ty == JSTokTy.boolean:
			# bool
			pass
		elif ty == JSTokTy.regex:
			# regex
			cur_regex = self._pik_tok
		elif ty == js_tk_lut['(']:
			# ( expr, ...bind_patt )
			pass
		elif ty == js_tk_lut['[']:
			# arr
			pass
		elif ty == js_tk_lut['{']:
			# obj
			pass
		elif ty == js_tk_lut['Async']:
			# async func or async gen
			# <opt>(async)_n function <opt>(*) <opt>(bind_id) ( form_list ) block_stmt
			pass
		elif ty == js_tk_lut['function']:
			# func or async gen
			# <opt>(async)_n function <opt>(*) <opt>(bind_id) ( form_list ) block_stmt
			pass
		elif ty == js_tk_lut['Class']:
			# class <opt>(bind_id) <opt>( extend asg_expr ) class_block
			pass
		elif ty == js_tk_lut['super']:
			# super idol 的笑容都没你的甜
			# super .id
			# super [ expr ]
			pass
		elif ty == js_tk_lut['import']:
			# import . meta
			pass
		else:
			raise ValueError('mismatched token during parsing mem_expr!')
		# . [ ` 检查是不是这三样
		# 检查new的args是否对应

	"""
		LHS =>
			+ -------------------- new_expr
			|  new+ A cross_act{ (args)*, ( args | [ xpr ] | .id | tmpl )* }
			+		  数量一致
			+  +------------------+ mem_expr
			|  new* A cross_act{ (args)*, ( args | [ xpr ] | .id | tmpl )* }
			|
			+		  数量一致
			+  +------------------+ call_expr
				# mem_expr args
			| new* A cross_act{ (args)*, ( args | [ xpr ] | .id | tmpl )* } args ( args | [ xpr ] | .id | tmpl )*
			| super args ( args | [ xpr ] | .id | tmpl )*
			| import ( asg_expr <opt>(,) ) ( args | [ xpr ] | .id | tmpl )*
			| import ( asg_expr , asg_expr <opt>(,) ) ( args | [ xpr ] | .id | tmpl )*
			+
			+ --------------------  opt_expr
			| call_expr ?. ( args | '['expr']' | .(pem)identy | tmpl_literal)+
			| mem_expr ?. ( args | '['expr']' | .(pem)identy | tmpl_literal)+

		A  ~ prim_expr
		  |~ super [ xpr ]
		  |~ super .identy
		  |~ import . meta

		prim_expr =>
			this | string | regex | number | identy
			` tmpl_literal` # result as_str_ref
			()
			(expr)
			(expr,)
			( expr, ...bind_patt )
			( expr, ...bind_id )
			arr_literal [<opt>(,)* asg <opt>(,)* ...asg <opt>(,) ]
			obj_literal
	-----------------------------------------------------------------------------------------
	It is easy to replace the equations designed for update_expr and
	unary_expr in the grammar by using Mathematical Induction in algebra.
	The result is as given below.

	let A = (delete | typeof | void | + | - | ~ | ! | await)*
	let B = (++|--)
	then
		update_expr = (BA)* LHS_n <opt>B
		unary_expr = (AB)* A LHS_n <opt>B = A(BA)* LHS_n <opt>B
	_n means no_line_terminator_here

	the form is not so easy to parse
	###############################
	una				= A(BA)* LHS_n <opt>B
	upd				= (BA)* LHS_n <opt>B
	################################
	exp				=> una (\\*\\* una)* => una A
	mul				=> exp (MOP exp)*	=> una A B => una A (MOP una A)*
	add				=> mul (AOP mul)*	=> una A B C
	shf				=> add (SOP add)*
	rel				=> shf (ROP shf)
					| pemId in shf # 最逆天的一集 malformed-algebra extension
	eq 				=> rel (EOP rel)*
	and				=> eq (& eq)*
	xor				=> and (^ and)*
	orr				=> xor (| xor)*
	lnd				=> orr (&& orr)*
	short_expr		=> orr (?? orr)*	# coal_expr
					| lnd (|| lnd)*		# lor
	"""
	@property
	def _parse_ops_in_expr(self):
		...

	def _parse_cond_expr(self) -> JSCondExpr:
		"""
		cond_expr => short_expr
				  | short_expr ? assign_expr : assign_expr
		"""
		cond = self._parse_short_expr
		then, other = None, None
		if self._cur_tok.ty == js_tk_lut['?']:
			then = self._parse_assign_expr
			self._expect_tok(':')
			other = self._parse_assign_expr
		return JSCondExpr(
			cond, then, other
		).set_lxx(cond, self._cur_tok)

	@property
	def _parse_assign_expr(self) -> JSAsgExpr:
		"""
		asg_expr[In, Yield, Await] :
			short_expr (? asg_expr : asg_expr){0, 1}
			##### arrow_expr
			: <opt>(async)_n bind_id_n	=> { func_body }
			| ( xxx )_n				   |  assig_expr [without beginning at '{']
			##### end_of arrow_expr
			mem_expr args_n
			yield unary_expr
			LHS ASG_OP assign_expr[?In, ?Yield, ?Await]
		ASG_OP:
			(*=, /=, %=, +=, -=, <<=, >>=, >>>=, &=, ^=, |=, **=, =, &&=, ||=, ??=)
		"""
		if self._cur_tok.ty == JSTokTy.Yield:
			_yield = self._pik_tok
			if self._is_new_line:
				return JSYieldExpr().set_lxx(_yield, self._cur_tok)
			if self._eat_tok(js_tk_lut['*']):
				# TODO: 何意味
				pass
			expr = self._parse_assign_expr
			return JSYieldExpr(expr=expr).set_lxx(_yield, self._cur_tok)
		elif self._cur_tok.ty == JSTokTy.Async:
			pass
		elif self._cur_tok.ty == JSTokTy.identy:
			pass
		# condition 和 LHS 的区别


	@property
	def _parse_expr(self):
		# expr => assign_expr C
		# c => , assign_expr C | eps
		res = [self._parse_assign_expr]
		while self._eat_tok(js_tk_lut[',']):
			res.append(self._parse_assign_expr)
		return JSExpr(expr=res)

	@property
	def _parse_expr_stmt(self) -> JSExprStmt:
		expr = self._parse_expr
		self._try_add_semi
		return JSExprStmt(
			lin_rang=expr.lin_rang,
			loc_rang=expr.loc_rang,
			expr=expr
		)

	def _parse_literal(self) -> str:
		if self._cur_tok.ty in [
			JSTokTy.integer, JSTokTy.Float,
			JSTokTy.string, JSTokTy.regex,
			JSTokTy.identy, JSTokTy.pemIdenty,
			JSTokTy.null, JSTokTy.boolean
		]:
			res = self._pik_tok
			return res.literal
		return ''

	@property
	def _parse_paren_expr(self) -> JSExpr:
		lparen = self._expect_tok('(')
		expr = self._parse_expr
		rparen = self._expect_tok(')')
		return JSExpr(expr=expr).set_lxx(lparen, self._cur_tok)
	# ================= param list ===================
	# [ a, b, c, ... ]
	# { a+b, c+d, ... }
	# { a+b: c+d, c+d: d+e, ... }
	# (a+b, c+d)
	# (a+b, ...)
	def _parse_comma_list(
		self,
		cloz_sign: str,
		enable_expr: bool=True # 如果False则理解为只能要标识符
	):
		...

	# ================= for ===================
	@property
	def _parse_for_of(self):
		...

	@property
	def _parse_for_in(self):
		...

	def _parse_norm_for(self, For_info: JSTok):
		self._expect_tok(';')
		cond = None if self._eat_tok(';') else self._parse_expr
		update = None if self._eat_tok(')') else self._parse_expr
		body = self._parse_stmt
		return JSForStmt(
			cond=cond,
			update=update,
			body=body
		).set_lxx(For_info, self._cur_tok)

	@property
	def _parse_for_(self): # -> JSForStmt:
		_for = self._pik_tok
		# TODO: 非常复杂
		# await_at = this.eatCtxtual("await")
		# lables.push(loopLabel)
		# enterScope(0)
		if self._cur_tok.ty == js_tk_lut['(']:
			self._pik_tok
			# for (let)
			# for (var)
			# for (const)
			# for (;;)
			pass
		elif self._cur_tok == js_tk_lut['Await']:
			# for await (variable of iterable)
			#	statement
			pass

	# ================= function <opt>(*) ===================
	# function
	# function*
	@property
	def _parse_func_(self):
		...

	def _parse_var_stmt(self, decl_kind, stmt_ctx):
		# decl_kind.is_lexial and stmt_ctx.is_single_stmt
		pass

	# ================= block ===================
	@property
	def _parse_block_stmt(self) -> JSBlockStmt:
		"""
		{ stmt_list }
		"""
		_lbrace = self._expect_tok('{')
		body = []
		# TODO: 创建作用域
		while not self._eat_tok(js_tk_lut['}']):
			body.append(self._parse_stmt)
		# TODO: 离开作用域
		return JSBlockStmt(body=body).set_lxx(_lbrace, self._cur_tok)

	# ================= import ===================
	@property
	def _parse_import_stmt(self):
		...

	# ================= export ===================
	@property
	def _parse_export_stmt(self):
		...

	# ================= async ===================
	# async function
	# async function*
	@property
	def _parse_async_stmt(self):
		_async = self._pik_tok
		_func = self._expect_tok('function')
		if self._cur_tok.ty == js_tk_lut['*']:
			self._pik_tok
			# TODO AST_async_gen
			# return self._parse_func_()
			return
		return self._parse_func_

	# ================= await ===================
	@property
	def _parse_await_stmt(self):
		pass

	# ================= class ====================
	@property
	def _parse_class_stmt(self):
		pass

	# ================= template ==================
	@property
	def _parse_tmpl(self):
		pass

	# ================= all stmts ===================
	@property
	def _parse_stmt(self) -> JSStmt:
		tk = self._cur_tok.ty
		if tk in [JSTokTy.end_of_file, js_tk_lut[';']]:
			self.is_directive = False
			return None
		elif tk == JSTokTy.lbrace:
			return self._parse_block_stmt
		elif tk == js_tk_lut['`']:
			return self._parse_tmpl
		elif tk in [js_tk_lut['"'], js_tk_lut["'"]]:
			return self._parse_string
		elif tk == JSTokTy.Import:
			# TopLevel!
			return self._parse_import_stmt
		elif tk == JSTokTy.export:
			# TopLevel!
			return self._parse_export_stmt
		elif tk == JSTokTy.require:
			# 这个看什么标准？
			# 这个怎么正确导入?
			pass
		elif tk == JSTokTy.super:
			pass
		elif tk == JSTokTy.Class:
			# TODO: 要看上下文合不合适
			# 如果是在函数、循环、分支内声明的，
			# 就要抛异常了
			return self._parse_class_stmt
		elif tk == JSTokTy.For:
			return self._parse_for_
		elif tk == JSTokTy.function:
			# function*
			# function
			return self._parse_func_
		elif tk in [JSTokTy.var, JSTokTy.const, JSTokTy.let]:
			pass
		elif tk == JSTokTy.Async:
			return self._parse_async_stmt
		elif tk == JSTokTy.Await:
			if self.is_async:
				return self._parse_await_stmt
			raise ValueError('invalid async scene!')
		elif tk == JSTokTy.Yield:
			if self.is_gen:
				return self._parse_yield_stmt

			# TODO: 上面写得都比较困难
		elif tk == JSTokTy.With:
			# use strict may not include a with statement!
			return self._parse_with_stmt
		elif tk == JSTokTy.If:
			return self._parse_if_stmt
		elif tk == JSTokTy.switch:
			return self._parse_switch_stmt
		elif tk == JSTokTy.While:
			return self._parse_while_stmt
		elif tk == JSTokTy.do:
			return self._parse_do_while_stmt
		elif tk == JSTokTy.debugger:
			return self._parse_debugger_stmt
		elif tk == JSTokTy.Try:
			return self._parse_try_stmt
		elif tk == JSTokTy.throw:
			return self._parse_throw_stmt
		elif tk == JSTokTy.Return:
			if not self.is_func:
				raise ValueError('return outside of function!')
			return self._parse_return_stmt
		elif tk in [JSTokTy.Continue, JSTokTy.Break]:
			return self._parse_break_continue_stmt
		# 剩下都交给解析表达式
		# 字符串、模板字符串、函数调用、类成员调用
		# 字面量等
		if self._nxt_tok.ty == js_tk_lut[':']:
			return self._parse_label_stmt
		return self._parse_expr_stmt

	def parse(self):
		_ = self.lexer.tokenize
		self.lexer.strip
		stmts: list[JSStmt] = []
		while self._cur_tok.ty != JSTokTy.end_of_file:
			cur = self._parse_stmt
			if cur is None:
				continue
			stmts.append(cur)
		return stmts

"""
tmd文法好像有问题，并不是LL(1)的文法

asg ::= lhs asg_op asg
asg ::= cond_expr
asg ::= arrow_expr
asg ::= async_arrow_expr

lhs ::= new_expr
lhs ::= call_expr
lhs ::= opt_expr

在遇到token的时候都还有问题
"""

