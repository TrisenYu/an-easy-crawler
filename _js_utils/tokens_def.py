#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Last modified at 二  9/ 2 01:25:41 2025
delimiters: str = '()[]{},:;@'
js_operats: str = '+-*/%?&|^!<>=~'
decl_str: str = '\'"`'
repeatable: str = '+-*/&|<>='
twicenable: str = '*?&|<>=' # ** ?? && || >> << ==
commapsign: dict[str, str] = { # comment map sign
	'/': '*',
	'<': '!',
}
spacetab: str = '\t\f\v\x09\x0b\x0c\x20\xA0\u1680\u180E' \
		   '\u2000\u2001\u2002\u2003\u2004\u2005\u2006' \
		   '\u2007\u2008\u2009\u200A\u202F\u205F\u3000\uFEFF'
enter_set: str = '\r\n\u2028\u2029'
num_shape: str = '0123456789.eExXoObB_aAcCdDfF+-n'
pause_idt: str = delimiters + decl_str + js_operats + spacetab + enter_set + '.'


def get_escaped_ch_in_str(c: str) -> str:
	if c in ["'", '"', '`']:
		return c
	elif c == 't':
		return '\t'
	elif c == 'n':
		return '\n'
	elif c == 'r':
		return '\r'
	elif c == '\\':
		return '\\'
	elif c == 'b':
		return '\b'
	elif c == 'v':
		return '\v'
	elif c == 'f':
		return '\f'
	elif c == 'a':
		return '\a'
	elif len(c) > 1:
		return ''  # unable to handle, just return
	return c


from enum import Enum, auto

class JSTokTy(Enum):
	end_of_file = 1
	illegal = auto()
	identy = auto()
	bigInt = auto()
	integer = auto()
	Float = auto()
	string = auto()
	regex = auto()
	pemIdenty = auto()
	pemOp = auto()
	boolean = auto()
	null = auto()
	undefined = auto()
	comment = auto()
	line_comment_st_1 = auto()
	line_comment_st_2 = auto()
	block_comment_st = auto()
	block_comment_ed = auto()
	line_comment_ed = auto()
	endl = auto()
	mul = auto()
	div = auto()
	mod = auto()
	pow = auto()
	add = auto()
	sub = auto()
	And = auto()
	orr = auto()
	xor = auto()
	flp = auto()
	inc = auto()
	dec = auto()
	lsh = auto()
	srs = auto()
	urs = auto()
	lnd = auto()
	lor = auto()
	nil = auto()
	ato = auto()
	sto = auto()
	mto = auto()
	dto = auto()
	mdo = auto()
	nto = auto()
	oto = auto()
	xto = auto()
	lto = auto()
	sro = auto()
	uro = auto()
	pto = auto()
	eq_ = auto()
	eqq = auto()
	les = auto()
	leq = auto()
	ges = auto()
	geq = auto()
	nit = auto()
	asg = auto()
	Not = auto()
	neq = auto()
	nqq = auto()
	lnt = auto()
	lot = auto()
	lparen = auto()
	rparen = auto()
	lbrack = auto()
	rbrack = auto()
	lbrace = auto()
	rbrace = auto()
	semicolon = auto()
	colon = auto()
	comma = auto()
	qmask = auto()
	dot = auto()
	qdot = auto()
	omit = auto()
	arrow = auto()
	etouq = auto()
	quote = auto()
	quott = auto()
	backslash = auto()
	number = auto()
	symbol = auto()
	If = auto()
	In = auto()
	of = auto()
	do = auto()
	As = auto()
	var = auto()
	For = auto()
	new = auto()
	Try = auto()
	NaN = auto()
	this = auto()
	Else = auto()
	From = auto()
	case = auto()
	void = auto()
	With = auto()
	const = auto()
	While = auto()
	Break = auto()
	catch = auto()
	throw = auto()
	Class = auto()
	super = auto()
	Return = auto()
	typeof = auto()
	Delete = auto()
	switch = auto()
	Import = auto()
	export = auto()
	default = auto()
	Finally = auto()
	extends = auto()
	type = auto()
	function = auto()
	Continue = auto()
	debugger = auto()
	require = auto()
	instanceof = auto()
	interface = auto()
	expands = auto()
	let = auto()
	Async = auto()
	Await = auto()
	Yield = auto()
	static = auto()
	at = auto()
	sharp = auto()
	dollar = auto()
	protected = auto()
	private = auto()
	public = auto()
	Set = auto()
	get = auto()
	implements = auto()
	package = auto()
	using = auto()
	accessor = auto()


# javascript token_look_up_table
# javascript token 速查表
js_tk_lut: dict[str, JSTokTy] = {
	'('			: JSTokTy.lparen,
	')'			: JSTokTy.rparen,
	'['			: JSTokTy.lbrack,
	']'			: JSTokTy.rbrack,
	'{'			: JSTokTy.lbrace,
	'}'			: JSTokTy.rbrace,
	'+'			: JSTokTy.add,
	'-'			: JSTokTy.sub,
	'*'			: JSTokTy.mul,
	'/'			: JSTokTy.div,
	'%'			: JSTokTy.mod,
	'&'			: JSTokTy.And,
	'|'			: JSTokTy.orr,
	'^'			: JSTokTy.xor,
	'~'			: JSTokTy.flp,
	'!'			: JSTokTy.Not,
	'?'			: JSTokTy.qmask,
	':'			: JSTokTy.colon,
	';'			: JSTokTy.semicolon,
	','			: JSTokTy.comma,
	'.'			: JSTokTy.dot,
	"'"			: JSTokTy.quote,
	'"'			: JSTokTy.quott,
	'`'			: JSTokTy.etouq,
	'\\'		: JSTokTy.backslash,
	'@'			: JSTokTy.at,
	'#'			: JSTokTy.sharp,
	'$'			: JSTokTy.dollar,
	'<'			: JSTokTy.les,
	'>'			: JSTokTy.ges,
	'>>'		: JSTokTy.srs,
	'>>>'		: JSTokTy.urs,
	'<<'		: JSTokTy.lsh,
	'>='		: JSTokTy.geq,
	'<='		: JSTokTy.leq,
	'+='		: JSTokTy.ato,
	'-='		: JSTokTy.sto,
	'*='		: JSTokTy.mto,
	'**'		: JSTokTy.pow,
	'/='		: JSTokTy.dto,
	'%='		: JSTokTy.mdo,
	'&='		: JSTokTy.nto,
	'|='		: JSTokTy.oto,
	'^='		: JSTokTy.xto,
	'&&='		: JSTokTy.lnt,
	'||='		: JSTokTy.lot,
	'??='		: JSTokTy.nit,
	'<<='		: JSTokTy.lto,
	'>>='		: JSTokTy.sro,
	'>>>='		: JSTokTy.uro,
	'**='		: JSTokTy.pto,
	'=='		: JSTokTy.eq_,
	'==='		: JSTokTy.eqq,
	'!='		: JSTokTy.neq,
	'!=='		: JSTokTy.nqq,
	'='			: JSTokTy.asg,
	'=>'		: JSTokTy.arrow,
	'&&'		: JSTokTy.lnd,
	'||'		: JSTokTy.lor,
	'??'		: JSTokTy.nil,
	'++'		: JSTokTy.inc,
	'--'		: JSTokTy.dec,
	'?.'		: JSTokTy.qdot,
	'...'		: JSTokTy.omit,
	'//'		: JSTokTy.line_comment_st_1,
	'<!--'		: JSTokTy.line_comment_st_2,
	'-->'		: JSTokTy.line_comment_ed,
	'/*'		: JSTokTy.block_comment_st,
	'*/'		: JSTokTy.block_comment_ed,
	# keywords
	'Number'	: JSTokTy.number,
	'Symbol'	: JSTokTy.symbol,
	'if'		: JSTokTy.If,
	'as'		: JSTokTy.As,
	'in'		: JSTokTy.In,
	'do'		: JSTokTy.do,
	'var'		: JSTokTy.var,
	'for'		: JSTokTy.For,
	'new'		: JSTokTy.new,
	'try'		: JSTokTy.Try,
	'this'		: JSTokTy.this,
	'else'		: JSTokTy.Else,
	'from'		: JSTokTy.From,
	'case'		: JSTokTy.case,
	'void'		: JSTokTy.void,
	'with'		: JSTokTy.With,
	'type'		: JSTokTy.type,
	'async'		: JSTokTy.Async,
	'await'		: JSTokTy.Await,
	'while'		: JSTokTy.While,
	'break'		: JSTokTy.Break,
	'catch'		: JSTokTy.catch,
	'throw'		: JSTokTy.throw,
	'yield'		: JSTokTy.Yield,
	'return'	: JSTokTy.Return,
	'typeof'	: JSTokTy.typeof,
	'delete'	: JSTokTy.Delete,
	'switch'	: JSTokTy.switch,
	'default'   : JSTokTy.default,
	'finally'   : JSTokTy.Finally,
	'function'  : JSTokTy.function,
	'continue'  : JSTokTy.Continue,
	'debugger'  : JSTokTy.debugger,
	'undefined' : JSTokTy.undefined,
	'instanceof': JSTokTy.instanceof,
	'interface' : JSTokTy.interface,
	'const'		: JSTokTy.const,
	'class'		: JSTokTy.Class,
	'true'		: JSTokTy.boolean,
	'false'		: JSTokTy.boolean,
	'null'		: JSTokTy.null,
	"super"		: JSTokTy.super,
	"extends"   : JSTokTy.extends,
	"import"	: JSTokTy.Import,  # 可能的方向是记录到集合中让tokenizer去找
	"export"	: JSTokTy.export,  # 这个导出就相当于提供信息了
	"require"   : JSTokTy.require, # 也有点怪怪的
	# TODO: let 不是关键词，yield 和 await 也不是
	"let"		: JSTokTy.let,
	"static"	: JSTokTy.static,
	"protected" : JSTokTy.protected,
	"private"   : JSTokTy.private,
	"public"	: JSTokTy.public,
	"Set"		: JSTokTy.Set,
	"get"		: JSTokTy.get,
	"implements": JSTokTy.implements,
	"package"   : JSTokTy.package,
	"using"		: JSTokTy.using,
	"accessor"  : JSTokTy.accessor
	# meta?
}
# 先不做外部导入和内部导出的实现，先做单个文件内的解析工作
# 外部导入和内部导出后面再说

from pydantic import BaseModel

class JSTok(BaseModel):
	"""
	token类，内置字符流解析出的token值、所在行以及行内的位置。
	块注释的所在行仅为块内第一个换行内的所在行。
	"""
	ty: JSTokTy = JSTokTy.illegal
	literal: str = ''
	line: int = 0
	st_pos: int = 1
	ed_pos: int = 0

	def __str__(self):
		res = f'line-{self.line:05d} ' \
			  f'rang-{self.st_pos:05d}:{self.ed_pos:05d} <{self.ty.name:^18}>'
		if self.ty in [JSTokTy.endl, JSTokTy.end_of_file]: return res
		elif self.ty in [JSTokTy.comment, JSTokTy.string]:
			fn = lambda x: ''.join([_ if _ not in enter_set else '\\n' for _ in x])
			gn = lambda x: ''.join([
				f'\\u{hex(ord(_))[2:]}' if 0xd800 <= ord(_) <= 0xdFFF \
				else _ for _ in x
			])
			self.literal = fn(self.literal)
			self.literal = gn(self.literal)
		res += f': {self.literal}'
		return res

