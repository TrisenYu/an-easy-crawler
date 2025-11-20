# Last modified at 2025/10/25 星期六 21:06:39
#!/usr/bin/env python3
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com, 2025>
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
import sys

from loguru import logger

from _js_utils.dfa.any_dfa import AbstractDFA
from _js_utils.dfa.numeric_dfa import JS_num_literal_DFA
from misc_utils.logger import GLOB_LOG_FORMAT, GLOB_MAIN_LOG_PATH

logger.remove()
logger.add(
	GLOB_MAIN_LOG_PATH,
	format=GLOB_LOG_FORMAT,
	colorize=True,
	rotation='16MB',
	compression='zip'
)
logger.add(
	sys.stdout,
	format=GLOB_LOG_FORMAT,
	colorize=True
)

def dfa_test(
	inp: str,
	dfa: AbstractDFA,
	exp_res: bool=True,
	debug: bool=True
) -> str:
	cur_state: str = '1'
	ok: bool = False
	for idx, c in enumerate(inp):
		cur_state, ok = dfa.state_machine(c, cur_state)
		if debug:
			logger.debug(f'{cur_state}: {ok}')
	if ok != exp_res:
		logger.warning(f'{inp}, {cur_state}')
	return cur_state


if __name__ == '__main__':
	fjudger = JS_num_literal_DFA()
	print()
	dfa_test('0_00_12_3_4', fjudger, False)
	dfa_test('01234554', fjudger)
	dfa_test('abcd', fjudger, False)
	dfa_test('0x123_45_6a_B_cn', fjudger)
	dfa_test('0X123_45_6a_B_c', fjudger)
	dfa_test('0X1_23_45_6a_B_cn', fjudger)
	dfa_test('0X0_23_45_6a_BdE_Fcn', fjudger)
	dfa_test('0X_23_45_6a_BdE_Fcn', fjudger, False)
	dfa_test('_23_45_6a_BdE_Fcn', fjudger, False)
	dfa_test('0x00', fjudger)
	dfa_test('0X00', fjudger)
	dfa_test('0X001', fjudger)
	dfa_test('0_23_45_6a_BdE_Fcn', fjudger, False)
	dfa_test('0x', fjudger, False)
	dfa_test('0x0', fjudger)
	dfa_test('0O', fjudger, False)
	dfa_test('0B0', fjudger)
	dfa_test('0B0001', fjudger)
	dfa_test('0Babcd1', fjudger, False)
	dfa_test('0b', fjudger, False)
	dfa_test('0b_', fjudger, False)
	dfa_test('0b_1', fjudger, False)
	dfa_test('0b0', fjudger)
	dfa_test('0o0', fjudger)
	dfa_test('0O0', fjudger)
	dfa_test('0000', fjudger)
	dfa_test('0b11_01', fjudger)
	dfa_test('0b11_01n', fjudger)
	dfa_test('0b001_11_01n', fjudger)
	dfa_test('00001_23n', fjudger, False)
	dfa_test('001_2_3n', fjudger, False)
	dfa_test('123n', fjudger)
	dfa_test('123', fjudger)
	dfa_test('1234566677_1231346_120000000n', fjudger)
	# 浮点数字面量测试
	dfa_test('1_34.2_34e+3_3_4_5', fjudger)
	dfa_test('.33_30_2e-3_5', fjudger)
	dfa_test('.33302e+3__5', fjudger, False)
	dfa_test('._03302e+35', fjudger, False)
	dfa_test('.a0002e+35', fjudger, False)
	dfa_test('00123', fjudger)
	dfa_test('9.1_2_3_42e-1_134', fjudger)
	dfa_test('1_29.1_2_3_42e-1_134', fjudger)
	dfa_test('1.23E1_34_5', fjudger)
	dfa_test('1.23E.1_34_5', fjudger, False)
	dfa_test('1.23.E1_34_5', fjudger, False)
	dfa_test('1.23.1_3.4_5', fjudger, False)
	dfa_test('.1_3.4_5', fjudger, False)
	dfa_test('.1_30.4_5', fjudger, False)
	dfa_test('1.e1_34_5', fjudger)
	dfa_test('.5e+00001_3', fjudger)
	dfa_test('0.00e+00001_3', fjudger)
	dfa_test('0.e+00001_3', fjudger)
	dfa_test('0.0_0_0e+00001_3', fjudger)
	dfa_test('.e00001_34_5', fjudger, False)
	dfa_test('.2e00001_34_5', fjudger)
	dfa_test('0.00000000000023e+1_3_1', fjudger)
	dfa_test('.00000000000023e+1_3_1_', fjudger, False)
	dfa_test('.000_000_00_000023e+1_3_1', fjudger)
	dfa_test('000_000_00_0001.23e+1_3_1', fjudger, False)
	dfa_test('000_000_00_0002.23e+1_3_1', fjudger, False)
	dfa_test('000_000_00_0003.23113e12', fjudger, False)
	dfa_test('000_000_00_0004.23113e-12', fjudger, False)
	dfa_test('100_000_00_0004.23113e-12', fjudger)
	dfa_test('200_000_00_000423113.3e-12', fjudger)
	dfa_test('200_000_00_000423113.3e-1_000_00_0004231132', fjudger)
	dfa_test('200_000_00_000423113.3e-1_000_00_0004231132.123e+123', fjudger, False)
	dfa_test('200_000_00_000423113.e-12', fjudger)
	dfa_test('-000_000_00_0002.23113e-12', fjudger, False)
	dfa_test('+000_000_00_0001.23113e-12', fjudger, False)
	dfa_test('1000_000_00_0001e.23113e-12', fjudger, False)
	dfa_test('1000_000_1.0_0001e231_13e-12', fjudger, False)
	dfa_test('.0_0001231.1312', fjudger, False)
	dfa_test('.0_00012311312', fjudger)
	dfa_test('.0_00012311312_', fjudger, False)
	dfa_test('.0e-12311312_1', fjudger)
	dfa_test('.0E+12311312_1', fjudger)
	dfa_test('.0E+123.11312_1', fjudger, False)
	dfa_test('.0E+123.e11312_1', fjudger, False)
	dfa_test('.0E+123e-11312_1', fjudger, False)
	dfa_test('1.0E+123.11312_1', fjudger, False)
	dfa_test('1_0_1.0_02_1e-2_0_0e-12', fjudger, False)
	dfa_test('11.2e-23113e-12', fjudger, False)
	dfa_test('11.223.11312', fjudger, False)
	dfa_test('11.2e+23.11312', fjudger, False)
	dfa_test('11.2e+2311312', fjudger)
	dfa_test('11.2ee2311.312', fjudger, False)
	dfa_test('11..312', fjudger, False)
	dfa_test('12', fjudger)
	dfa_test('12.', fjudger)
	dfa_test('1.2_33_3e1_2', fjudger)
	dfa_test('.5E-4', fjudger)
	dfa_test('.5e3', fjudger)
	dfa_test('1e', fjudger, False)
	dfa_test('1e+', fjudger, False)
	dfa_test('1E-', fjudger, False)
	dfa_test('1.', fjudger)
	dfa_test('.5', fjudger)
	dfa_test('.e5', fjudger, False)
	dfa_test('1.e5', fjudger)
	dfa_test('.4e5', fjudger)
	dfa_test('__', fjudger, False)
	dfa_test('ab', fjudger, False)
	dfa_test('xeabcd', fjudger, False)
	dfa_test('12eabcd', fjudger, False)
	dfa_test('12.eabcd', fjudger, False)
	dfa_test('12.e+abcd', fjudger, False)
	dfa_test('1.e+10000', fjudger)
	dfa_test('1.e+1123.e+123', fjudger, False)
	dfa_test('1.2.e+abcd', fjudger, False)
	dfa_test('123', fjudger)
	dfa_test('12_23_443', fjudger)
	dfa_test('12_23_44_3n', fjudger)
	dfa_test('0x12_23_443', fjudger)
	dfa_test('0O12_23_443', fjudger)
	dfa_test('0o12_23_448', fjudger, False)
	dfa_test('0x12_23_448', fjudger)
	dfa_test('0xo12_23_448', fjudger, False)
	dfa_test('0xoe12_23_448', fjudger, False)
	dfa_test('0xoe+12_23_448', fjudger, False)
	dfa_test('0x0e012_23_448', fjudger)
	dfa_test('0X12_23_443', fjudger)
	dfa_test('0X12_23_443n', fjudger)
	dfa_test('0x12_23_44_3n', fjudger)
	dfa_test('0b1_1', fjudger)
	dfa_test('0B01001', fjudger)
	dfa_test('0b010_01', fjudger)
	dfa_test('0b010_01n', fjudger)
	dfa_test('0b1234', fjudger, False)
	dfa_test('0_b1234', fjudger, False)
	dfa_test('0_x1234', fjudger, False)
	dfa_test('0_10x1234', fjudger, False)
	dfa_test('1_10x1234', fjudger, False)
	dfa_test('0_O1234', fjudger, False)
	dfa_test('123._3', fjudger, False)
	dfa_test('0b1_234', fjudger, False)
	dfa_test('0o1234', fjudger)
	dfa_test('0o12_34', fjudger)
	dfa_test('0o1_2_3_4n', fjudger)
	dfa_test('0oa_b_c_dn', fjudger, False)
	dfa_test('00000000n', fjudger, False)
	dfa_test('00000000', fjudger)
	dfa_test('0', fjudger)
	dfa_test('1', fjudger)
	dfa_test('.2', fjudger)

