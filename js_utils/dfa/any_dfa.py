#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025-06>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025年08月24日 星期日 20时24分58秒
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
from typing import Any, runtime_checkable, Protocol

@runtime_checkable
class AbstractDFA(Protocol):
	"""抽象dfa定义，以供后续可以按同态{多态}的方式调用。"""
	def state_machine(self, inp: Any, state: Any) -> tuple[Any, bool, ...]:
		"""
		提供输入 inp 和当前所在状态 state
		返回次态以及是否可接受。
		"""
		...
