# Last modified at 2025年08月24日 星期日 18时31分28秒
#!/usr/bin/env python3
from js_utils.lexer import JSLexer
# TODO: test 得不够规范
import os

_file_dir=os.path.dirname(__file__)
print(_file_dir)

_repl_dir=os.path.join(_file_dir, '../js_src_testcase')
lexer = JSLexer(f'{_repl_dir}/ez1.js')
print()
for token in lexer.tokenize:
	print(token)
print()

lexer.strip
print('after stripping...')
for token in lexer.res:
	print(token)
print()

print(f'{_repl_dir}/ez2.js')
lexer.set_src(f'{_repl_dir}/ez2.js')
for token in lexer.tokenize:
	print(token)
print()

print(f'{_repl_dir}/ez3.js')
lexer.set_src(f'{_repl_dir}/ez3.js')
for token in lexer.tokenize:
	print(token)
print()

print(f'{_repl_dir}/mal1.js')
lexer.set_src(f'{_repl_dir}/mal1.js')
for token in lexer.tokenize:
	print(token)
print()

print(f'{_repl_dir}/mal2.js')
lexer.set_src(f'{_repl_dir}/mal2.js')
for token in lexer.tokenize:
	print(token)
print()

print(f'{_repl_dir}/mal3.js')
lexer.set_src(f'{_repl_dir}/mal3.js')
# print(f'{_repl_dir}/mal3.js')
try:
	for token in lexer.tokenize:
		print(token)
	print('panic...')
except Exception as e:
	print(f'# ----------- ok with e: {e}')
	lexer.cln_res()
	pass

print(f'{_repl_dir}/mal4.js')
lexer.set_src(f'{_repl_dir}/mal4.js')
for token in lexer.tokenize:
	print(token)
print()

# 包含 import export 的测试用例
lexer.set_src(f'{_repl_dir}/test.ts')
print(f'{_repl_dir}/test.ts')
for token in lexer.tokenize:
	print(token)

# 尝试对混淆文件分词
_repl_dir=os.path.join(_file_dir, '../../crypto_aux/obfus-js/')
lexer.set_src(f'{_repl_dir}/wmlike_gen.js')
with open('output-wmlike-gen.log', 'w', encoding='utf-8') as fd:
	for c in lexer.tokenize:
		fd.write(c.__str__()+'\n')

