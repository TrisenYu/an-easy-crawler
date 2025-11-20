#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com> in 2025
from typing import Dict, Tuple, NoReturn

class SQLiteTabMeta(type):
	"""
	简化建表用的类，但填表看起来一九赤石
	https://liaoxuefeng.com/books/python/oop-adv/meta-class/index.html

	TODO: 加一个解析索引的逻辑，加快表的查询
	"""
	def __new__(cls, clsname, bases, attrs):
		if 'table_structure' in attrs:
			table_structure = attrs['table_structure']
			assert len(table_structure) == 1, 'only one table can be instanized'
			table_name = next(iter(table_structure))
			assert isinstance(table_name, str) and len(table_name) > 0, \
				'table name needs to be non-empty string type'
			attrs['table_name'] = table_name
			attrs['field_info']: Dict[str, Dict | Tuple[str, ...]] = {}
			attrs = cls._parse_columns_of_table(attrs, table_structure[table_name])

		return super().__new__(cls, clsname, bases, attrs)

	@staticmethod
	def _parse_columns_of_table(attrs: Dict, column_dict: Dict) -> Dict | NoReturn:
		"""
		comment TODO.
		"""
		foreign_cls, prim_cls, unique_vals = [], set(), set()
		cols_clause = f'CREATE TABLE IF NOT EXISTS {attrs["table_name"]} (\n'
		primary_clause, unique_clause = '', ''
		def column_type_check(tag, col_name: str, attr_check: set) -> tuple[set, bool] | NoReturn:
			"""判断tag类型，并将解析结果提供到attr_check中"""
			if isinstance(tag, tuple):
				# Foreign key
				assert len(tag) == 2 and isinstance(tag[0], str) and isinstance(tag[1], str) and \
						'FOREIGN' not in attr_check, f'reduplicate foreign keys constrain on {col_name}'
				foreign_cls.append(
					f'\tFOREIGN KEY ({col_name}) REFERENCES\n'
					f'\t\t{tag[0]}({tag[1]}) ON DELETE CASCADE,\n'
				)
				attrs['field_info'][col_name]['foreign'] = (tag[0], tag[1])
				return attr_check, True

			elif isinstance(tag, dict):
				# default assignment
				if 'DEFAULT' in attr_check:
					raise ValueError('reduplicate default assignment')
				assert len(tag) == 1
				default_val = f'{tag[next(iter(tag.keys()))]}'
				attr_check.add('DEFAULT')
				return attr_check, True

			elif not isinstance(tag, str):
				raise ValueError(
					f'unsupport data-format: {type(tag)} '
					f'when handler column name<{col_name}>'
				)
			return attr_check, False

		for col_name, col_xttrs in column_dict.items():
			if col_name in attrs:
				raise ValueError(
					f'reduplicate column name<{col_name}> already exists'
				)
			attrs[col_name] = col_name
			attrs['field_info'][col_name] = {
				'type'   : '',
				'attr'   : {},
				'foreign': (),
				'default': ''
			}
			default_val, attr_check = None, set()
			for tag in col_xttrs:
				attr_check, flag = column_type_check(tag, col_name, attr_check)
				if flag:
					continue
				tag = tag.strip(' ').upper()
				if tag in {'INTEGER', 'TEXT', 'BLOB', 'REAL', 'NULL'}:
					assert len(attrs['field_info'][col_name]['type']) == 0
					attrs['field_info'][col_name]['type'] = tag
				elif tag in {'AUTOINCREMENT', 'NOTNULL'}:
					tag = tag if tag != 'NOTNULL' else 'NOT NULL'
					attr_check.add(tag)
				elif tag == 'PRIMARY':
					# 多 primary key 统计
					prim_cls.add(col_name)
				elif tag == 'UNIQUE':
					# 多 unique 统计
					unique_vals.add(col_name)
				else:
					raise ValueError(
						f'unknown Tag<{tag}> on current column<{col_name}>'
					)
			if default_val is not None:
				attrs['field_info'][col_name]['default'] = default_val
			try:
				attr_check.remove('DEFAULT')
			except (ValueError, KeyError):
				# 不一定有，能删就删，不能删就消耗这个异常
				pass
			except Exception as e:
				assert 1 == 0, 'unrecognize exception happened, throw for manually handling: '+str(e)
			attrs['field_info'][col_name]['attr'] = attr_check

		if len(prim_cls) > 1:
			for p in prim_cls:
				attrs['field_info'][p]['attr'].add('NOT NULL')
			primary_clause = f'\tPRIMARY KEY ({", ".join(prim_cls)}),\n'
		elif len(prim_cls) == 1:
			attrs['field_info'][next(iter(prim_cls))]['attr'].add('PRIMARY KEY')
		else:
			raise ValueError(
				f'There must be a primary key for current table<{attrs["table_name"]}>'
			)

		if len(unique_vals) > 1:
			unique_clause = f'\tUNIQUE ({", ".join(unique_vals)}),\n'
		elif len(unique_vals) == 1:
			attrs['field_info'][next(iter(unique_vals))]['attr'].add('UNIQUE')

		for col_name, v in attrs['field_info'].items():
			cols_clause += f"\t{col_name} {v['type']} {' '.join([str(_) for _ in v['attr']])}"
			cols_clause += '' if len(v['default']) == 0 else f'DEFAULT {v["default"]}'
			cols_clause += ',\n'

		for f in foreign_cls:
			cols_clause += f
		if len(unique_clause) > 0:
			cols_clause += unique_clause
		if len(primary_clause) > 0:
			cols_clause += primary_clause
		attrs['cols_clause'] = cols_clause[:-2] + '\n) STRICT;'
		return attrs

class SQLiteTabMetaClass(metaclass=SQLiteTabMeta):
	"""
	@DynamicAttrs
	"""
	pass