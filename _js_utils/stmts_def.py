#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com> in 2025
# Created at 2025年08月11日 星期一 22时17分36秒
# Last modified at 2025年08月24日 星期日 20时45分54秒
from typing import (
	TypeVar, # 创建泛型基类用
	Generic, # 继承泛型基类
	Optional
)
from typing_extensions import TypedDict
from _js_utils.tokens_def import JSTok, js_tk_lut
# 应该叫做泛型而非多态
# 好像写得有问题

unary_prefix: set = {
	js_tk_lut['typeof'], js_tk_lut['void'],
	js_tk_lut['delete'],
	js_tk_lut['--'], js_tk_lut['++'],
	js_tk_lut['!'], js_tk_lut['~'],
	js_tk_lut['-'], js_tk_lut['+']
}
unary_suffix: set = {
	js_tk_lut['--'], js_tk_lut['++']
}
"""
AssignmentOperator : one of
	*= /= %= += -= <<= >>= >>>= &= ^= |= **=
"""


class JSASTNode:
	ty: str
	loc_rang: str
	lin_rang: str

	def set_lxx(self, st: JSTok, ed: JSTok) -> 'JSASTNode':
		self.lin_rang = f'{st.line}-{ed.line}'
		self.loc_rang = f'{st.st_pos}-{ed.st_pos}'
		return self

class JSNull(JSASTNode):
	ty = 'null'

class JSStmt(JSASTNode):
	ty = 'stmt'

class JSExpr(JSASTNode):
	ty = 'expr'
	expr: list['JSExpr']

class JSPattern(JSASTNode):
	ty = 'pattern'

class JSIdenty(JSExpr):
	ty = "identy"
	name: str

class JSPemIdenty(JSASTNode):
	ty = 'pem_identy'
	name: str

class JSLiteral(JSExpr):
	ty = 'literal'
	val: Optional[str | bool | int]

class JSSrcFile(JSASTNode):
	ty = 'source'
	body: list[JSStmt]
	# script | module
	src_ty: str

class JSBlockStmt(JSStmt):
	ty = 'block_stmt'
	body: list[JSStmt]

class JSDeclVaror(JSASTNode):
	ty = 'decl_varor'
	identy: JSPattern
	init: Optional[JSExpr]

# 可作为declaration使用
class JSDeclVar(JSASTNode):
	ty = 'decl_var'
	decls: list[JSDeclVaror]
	# var let const using await using
	kind: str

class JSFunc(JSASTNode):
	ident: Optional[JSIdenty]
	args: list[JSPattern]
	body: list[JSBlockStmt | JSExpr]
	is_gen: bool
	is_async: bool
	is_expr: bool

class JSExprStmt(JSStmt):
	ty = 'expr_stmt'
	expr: JSExpr | JSLiteral
	is_direct: Optional[str]

class JSEmptStmt(JSStmt):
	ty = 'empt_stmt'

class JSDebuggerStmt(JSStmt):
	ty = 'debugger_stmt'

class JSWithStmt(JSStmt):
	ty = 'with_stmt'
	obj: JSExpr
	body: JSStmt

class JSRetnStmt(JSStmt):
	ty = 'retn_stmt'
	args: Optional[JSExpr]

class JSLabelStmt(JSStmt):
	ty = 'label_stmt'
	label: JSLiteral
	body: JSStmt

class JSCtrolFlowStmt(JSStmt):
	label: Optional[JSIdenty]

class JSBreakStmt(JSCtrolFlowStmt):
	ty = 'break_stmt'

class JSContinueStmt(JSCtrolFlowStmt):
	ty = 'continue_stmt'

class JSIfStmt(JSStmt):
	ty = 'if_stmt'
	cond: JSExpr
	then: JSStmt
	other: Optional[JSStmt]

class JSSwitchCases(JSASTNode):
	ty = 'switch_cases'
	cond: Optional[JSExpr]
	body: list[JSStmt]

class JSSwitchStmt(JSStmt):
	ty = 'switch_stmt'
	target: JSExpr
	cases: list[JSSwitchCases]

class JSThrowStmt(JSStmt):
	ty = 'throw_stmt'
	# 这东西有点抽象
	args: JSExpr

class JSCatcher(JSASTNode):
	ty = 'catch_except'
	arg: Optional[JSPattern]
	body: JSBlockStmt

class JSTryStmt(JSStmt):
	ty = 'try_stmt'
	block: JSBlockStmt
	handler: Optional[JSCatcher]
	final: Optional[JSBlockStmt]

class JSWhileStmt(JSStmt):
	ty = 'while_stmt'
	cond: JSExpr
	body: JSStmt

class JSDoWhileStmt(JSStmt):
	ty = 'do_while'
	body: JSStmt
	cond: JSExpr

class JSForStmt(JSStmt):
	ty = 'for_stmt'
	init: Optional[JSExpr | JSDeclVar]
	cond: Optional[JSExpr]
	update: Optional[JSExpr]
	body: JSStmt

class JSForInStmt(JSStmt):
	ty = 'for_in_stmt'
	lpart: JSPattern | JSDeclVar
	rpart: JSExpr
	body: JSStmt

class JSFuncDecl(JSFunc):
	ty = 'func_decl'
	ident: JSIdenty
	body: JSBlockStmt


class JSThisExpr(JSExpr):
	ty = 'this_expr'

class JSProperty(JSASTNode):
	ty = 'property'
	key: JSExpr
	val: JSExpr
	# init get set
	kind: str
	is_method: bool
	is_shorthand: bool
	is_computed: bool

class JSSpreadContent(JSASTNode):
	ty = 'spread_content'
	arg: JSExpr

class JSArrExpr(JSExpr):
	ty = 'arr_expr'
	contents: list[JSExpr | JSSpreadContent]

class JSObjExpr(JSExpr):
	ty = 'obj_expr'
	properties: list[JSProperty | JSSpreadContent]

class JSFuncExpr(JSExpr):
	ty = 'func_expr'
	body: JSBlockStmt

class JSUnaryExpr(JSExpr):
	ty = 'unary_expr'
	# +-!~ typeof void delete
	op: str
	is_pref: bool
	is_await: bool
	expr: JSExpr

class JSUpdateExpr(JSExpr):
	ty = 'update_expr'
	# ++ --
	op: str
	expr: JSExpr
	is_pref: bool

class JSBinExpr(JSExpr):
	ty = 'bin_expr'
	# == != === !=== < <= > >= << >> >>> + - * / % | ^
	# & in instanceof **
	op: str
	lpart: JSExpr | JSPemIdenty
	rpart: JSExpr

class JSAsgExpr(JSExpr):
	ty = 'asg_expr'
	# = += -= *= /= %= <<= >>= >>>=
	# != ^= |= &= **= ||= &&= ??=
	op: str
	lpart: JSPattern
	rpart: JSExpr

class JSlogicExpr(JSExpr):
	ty = 'logic_expr'
	# || && ??
	op: str
	lpart: JSExpr
	rpart: JSExpr

class JSSuper(JSASTNode):
	ty = 'super'

class JSMemExpr(JSExpr):
	ty = 'mem_expr'
	obj: JSExpr | JSSuper
	proper: JSExpr | JSPemIdenty
	is_computed: bool
	is_optional: bool

class JSCondExpr(JSExpr):
	ty = 'cond_expr'
	cond: JSExpr
	then: JSExpr
	other: JSExpr

class JSCallExpr(JSExpr):
	ty = 'call_expr'
	callee: JSExpr | JSSuper
	args: list[JSExpr | JSSpreadContent]
	is_optional: bool

class JSNewExpr(JSExpr):
	ty = 'new_expr'
	callee: JSExpr
	args: list[JSExpr | JSSpreadContent]

class JSThenExpr(JSExpr):
	ty = 'then_expr'
	exprs = list[JSExpr]

class JSForOfStmt(JSASTNode):
	ty = 'for_of_stmt'
	lpart: JSDeclVar | JSPattern
	rpart: JSExpr
	body: JSStmt
	is_await: bool

class JSArrowFuncExpr(JSExpr, JSFunc):
	ty = 'arrow_func_expr'

class JSYieldExpr(JSExpr):
	ty = 'yield_expr'
	expr: Optional[JSExpr]
	is_delegate: bool

class _js_tmpl_val(TypedDict):
	cooked: Optional[str]
	raw: str

class JSTmplContent(JSASTNode):
	ty = 'tmpl_content'
	is_tail: bool
	val: _js_tmpl_val

class JSTmplLiteral(JSExpr):
	ty = 'tmpl_literal'
	quasis: list[JSTmplContent]
	exprs: list[JSExpr]

class JSTaggedTmplExpr(JSExpr):
	ty = 'tagged_tmpl_expr'
	tag: JSExpr
	quasi: JSTmplLiteral

class JSAssignProperty(JSASTNode):
	ty = 'property'
	key: JSExpr
	val: JSPattern
	kind = 'init'
	meth = False
	is_shorthand: bool = False
	is_computed: bool = False

class JSRestContent(JSASTNode):
	ty = 'rest_content'
	arg: JSPattern

class JSObjPattern(JSASTNode):
	ty = 'obj_pattern'
	properties: list[JSAssignProperty | JSRestContent]

class JSArrPattern(JSASTNode):
	ty = 'arr_pattern'
	contents: list[Optional[JSPattern]]

class JSAssignPatterm(JSASTNode):
	ty = 'assign_pattern'
	lpart: JSPattern
	rpart: JSExpr

class JSMethDef(JSASTNode):
	ty = 'meth_def'
	key: JSExpr | JSPemIdenty
	val: JSFuncExpr
	# constructor method get set
	kind: str
	is_computed: bool
	is_static: bool

class JSPropertyDef(JSASTNode):
	ty = 'property_def'
	key: JSExpr | JSPemIdenty
	val: Optional[JSExpr]
	is_computed: bool
	is_static: bool

class JSStaticBlock(JSASTNode):
	ty = 'static_block'
	body: list[JSStmt]

class JSClassBody(JSASTNode):
	ty = 'class_body'
	body: list[JSMethDef | JSPropertyDef | JSStaticBlock]

class JSClass(JSASTNode):
	idt: Optional[JSIdenty]
	supre_class: Optional[JSExpr]
	body: JSClassBody

class JSClassDecl(JSClass):
	ty = 'class_decl'
	idt: JSIdenty

class JSClassExpr(JSExpr, JSClass):
	ty = 'class_expr'

class JSMetaProperty(JSExpr):
	ty = 'meta_property'
	meta: JSIdenty
	proper: JSIdenty

class JSImportSpecifier(JSASTNode):
	ty = 'import_specifier'
	imported: JSIdenty | JSLiteral
	local: JSIdenty

class JSImportDefault(JSASTNode):
	ty = 'import_default'
	local: JSIdenty

class JSImportNamespace(JSASTNode):
	ty = 'import_namespace'
	local: JSIdenty

class JSImportAttr(JSASTNode):
	ty = 'import_attr'
	key: JSIdenty | JSLiteral
	val: JSLiteral

class JSImportDecl(JSASTNode):
	ty = 'import_decl'
	specifiers: list[JSImportSpecifier | JSImportDefault | JSImportNamespace]
	src: JSLiteral
	attrs: list[JSImportAttr]

# 也可作为declaration使用
class JSAnonFuncDecl(JSFunc):
	ty = 'anon_func_decl'
	idt: Optional[str]
	body: JSBlockStmt

class JSAnonClassDecl(JSClass):
	ty = 'class_decl'
	idt: Optional[str]

class JSExportAllDecl(JSASTNode):
	ty = 'export_all_decl'
	src: JSLiteral
	is_exported: Optional[JSIdenty | JSLiteral]
	attrs: list[JSImportAttr]


class JSExportDefaultDecl(JSASTNode):
	ty = 'export_default_decl'
	decl: JSAnonFuncDecl | JSFuncDecl | \
		  JSAnonClassDecl | JSClassDecl | JSExpr


class JSExportNamedDecl(JSASTNode):
	ty = 'export_name_decl'
	# TODO: Declaration | null
	decl: Optional[str]
	src: Optional[JSLiteral]
	attrs: list[JSImportAttr]

class JSExportSpecifier(JSASTNode):
	ty = 'export_specifier'
	is_exported: JSIdenty | JSLiteral
	local: JSIdenty | JSLiteral

class JSAwaitExpr(JSExpr):
	ty = 'await_expr'
	arg: JSExpr

class JSChainExpr(JSExpr):
	ty = 'chain_expr'
	expr: JSMemExpr | JSCallExpr

class JSImportExpr(JSExpr):
	ty = 'import_expr'
	src: JSExpr
	opts: Optional[JSExpr]

class JSParenExpr(JSExpr):
	ty = 'paren_expr'
	expr: JSExpr


if __name__ == '__main__':
	pass
