#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com> in 2025
# Created at 2025/09/03 星期三 00:24:10
# Last modified at 2025/10/25 星期六 19:41:50
"""
写着写着有种脑梗的"美感"
"""
import sqlite3
from threading import Semaphore
from typing import NoReturn, Optional

from misc_utils.wrappers.err_wrap import seize_err_if_any
from misc_utils.opts.db.sqlite_base import SQLiteTabMetaClass
# TODO: 数据库的表段、请求的字段应该抽象成编程语言中的结构，
# 		不然业务一变动，改起来就要爆炸了
#       另外这个看上去和x易的后端强相关，如果要做其它的表，这里的设计极其不理想
#       当同样的事情重复2遍以上的时候，可以考虑用更通用的结构简化表示
'''
如果后面还有需求要向表格增添新字段，可以用ALTER TABLE 语句
ALTER TABLE xxx ADD COLUMN email TEXT
'''

class DBfd:
	"""
	内部的几个函数如果暴露到公网，用不好就是教科书级别的SQL注入
	毕竟从用法上就是为了编程的方便而放弃了预编译的写法

	解决的办法可以用类似查表的方法，走固定而且写死的调用
	"""

	def __init__(
		self, db_path: str,
		sql_tabs: list[SQLiteTabMetaClass]
	) -> None:
		# 检查 db 是否存在，不存在则创建。
		self.path = db_path
		# 在这里拿到sql_tabs以后还不能直接拿去create，否则会有外键冲突的风险
		self.accept_tbls = self._topology_sort(dict([(v.table_name, v) for v in sql_tabs]))
		# TODO: 考虑将其cached，下次就不用计算了，但具体怎么做有点不知道
		self._conn = None
		self._lock = Semaphore(1)
		self._init_db()

	def close(self) -> None:
		self._lock.acquire()
		self._conn.close()
		self._lock.release()
		return

	def commit(self) -> None:
		self._lock.acquire()
		self._conn.commit()
		self._lock.release()
		return

	@staticmethod
	def _topology_sort(
		restrict_tbls: dict[str, SQLiteTabMetaClass]
	) -> dict[str, SQLiteTabMetaClass]:
		depend_graphy, in_degree = {}, {}
		for tab_name, tab in restrict_tbls.items():
			in_degree[tab_name] = 0
			for column in tab.field_info:
				if len(tab.field_info[column]['foreign']) != 2:
					continue
				depend_tab_name = tab.field_info[column]['foreign'][0]
				if depend_tab_name not in depend_graphy:
					depend_graphy[depend_tab_name] = set()
				depend_graphy[depend_tab_name].add(tab_name)
				in_degree[tab_name] += 1
		for tab_name in restrict_tbls:
			if tab_name not in depend_graphy:
				depend_graphy[tab_name] = set()
		map_root, st_list = [], list(filter(lambda x: in_degree[x] == 0, in_degree))
		while len(st_list) != 0:
			curr_choice = st_list.pop()
			map_root.append(curr_choice)
			for required in depend_graphy[curr_choice]:
				in_degree[required] -= 1
				if in_degree[required] == 0:
					st_list.insert(0, required)
		st_lsit = list(filter(lambda x: in_degree[x] != 0, in_degree))
		assert len(st_lsit) == 0, \
			   "there are still self-loops in given database tables' set after selecting"
		return dict([(restrict_tbls[x].table_name, restrict_tbls[x]) for x in map_root])


	@property
	def _is_table_empty(self) -> bool:
		cur = self._conn.cursor()
		ret = True
		for name in self.accept_tbls:
			cur.execute(
				"SELECT tbl_name FROM sqlite_master "
				"WHERE tbl_name = ? AND type = 'table';",
				(name,)
			)
			ret &= cur.fetchone() is None
		cur.close()
		return ret

	def _init_db(self) -> None:
		self._conn = sqlite3.connect(
			# 直接在变量内上锁
			self.path, check_same_thread=False,
			autocommit=False, isolation_level=None
		)
		self._conn.row_factory = sqlite3.Row
		self._conn.execute('PRAGMA foreign_keys = ON;')  # 外键约束
		self._conn.execute("PRAGMA cache_size = 10000;")  # 设置10MB缓存
		if self._is_table_empty:
			self._create_table()
		return

	def _create_table(self) -> None:
		once_payload = '\n'.join([v.cols_clause for _, v in self.accept_tbls.items()])
		curs = self._conn.cursor()
		curs.executescript(once_payload + 'COMMIT;')
		curs.execute("BEGIN;")
		curs.close()
		return None


	def is_col_name_in_tbl(
		self,
		table_name: str,
		collected_name: set[str]
	) -> bool:
		if table_name not in self.accept_tbls:
			return False
		return not any([
			col not in self.accept_tbls[table_name].field_info 
			for col in collected_name
		])

	# TODO: 在sqlite中删一个表中的字段比加一个字段更困难
	def _alter_columname_in_tbl(self, tbl_name: str, col_dict: dict[str, str]) -> None:
		lena, payload = len(col_dict), f"ALTER {tbl_name} "
		for name, attr in col_dict.items():
			lena -= 1
			payload += f'ADD COLUMN {name} {attr}'+ ',' if lena > 0 else ';'
		self._lock.acquire()
		cur = self._conn.cursor()
		cur.execute(payload)
		self._lock.release()

	@staticmethod
	def dict_unpacker(
		dom_dict: dict[str, int | str | bool | float]
	) -> tuple[list, tuple]:
		res_list, res_tupl = [], ()
		for k, v in dom_dict.items():
			res_list.append(k)
			res_tupl = (*res_tupl, v)
		return res_list, res_tupl

	@seize_err_if_any()
	def query_items_in_tbl(
		self,
		tbl_name: str,
		cond_dict: dict[str, int | str | bool | float],
		order_dom: dict[str, str] = {},
		choose_doms: Optional[list[str]] = None,
		limit_num: int = 0
	) -> list | NoReturn:
		cond_name, cond_val = self.dict_unpacker(cond_dict)
		_and_chain = '= ? AND '.join(cond_name) + ' = ?'
		order_body = ''
		for odd_name, order in order_dom.items():
			# TODO: 加入偏序关系的支持
			assert odd_name != '' and order in {'DESC', '', 'ASC'}
			order_body += f'{odd_name} {order}, '
			cond_name.append(odd_name)
		order_body = 'ORDER BY ' + order_body[:-2] if len(order_body) != 0 else ''
		limitation = f'LIMIT {limit_num}' if limit_num > 0 else ''
		choose_doms = [] if choose_doms is None else choose_doms
		assert self.is_col_name_in_tbl(tbl_name, set(cond_name+choose_doms)), \
			f'invalid column name{cond_name+choose_doms} was passed into ' \
			f'querying function for {tbl_name}'
		choose_domains = ', '.join(choose_doms)
		choose_domains = '*' if len(choose_domains) == 0 else choose_domains

		payload = f"SELECT {choose_domains} FROM {tbl_name} " \
		          f"WHERE {_and_chain} {order_body} {limitation};"
		del cond_name, tbl_name, order_dom, choose_domains, order_body

		self._lock.acquire()
		cur = self._conn.cursor()
		cur.execute(payload, cond_val)
		# TODO: 如果表格非常大，这里会要了整个系统的命
		# 不如返回游标，让应用自己去一个一个处理
		ret = cur.fetchall()
		cur.close()
		self._lock.release()
		return ret

	@seize_err_if_any()
	def query_null_items_in_tbl(
		self,
		tbl_name: str,
		domains: dict[str, int | str | bool | float],
		nil_doms: list[str],
		choose_doms: Optional[list[str]] = None
	) -> list:
		assert len(nil_doms) != 0 and len(domains) != 0

		cond_name, cond_val = DBfd.dict_unpacker(domains)
		and_chain = ' = ? AND '.join(cond_name) + ' = ? AND ' + \
		            ' IS NULL AND '.join(nil_doms) + ' IS NULL '
		choose_doms = [] if choose_doms is None else choose_doms

		assert self.is_col_name_in_tbl(tbl_name, set(cond_name+choose_doms)), \
			f'invalid column name{cond_name+choose_doms} was passed into ' \
			f'nullable querying function for {tbl_name}'

		choose_domains = ', '.join(choose_doms) if choose_doms is not None else ''
		choose_domains = '*' if len(choose_domains) == 0 else choose_domains
		payload = f'SELECT {choose_domains} FROM {tbl_name} WHERE {and_chain};'

		self._lock.acquire()
		cur = self._conn.cursor()
		cur.execute(payload, cond_val)
		ret = cur.fetchall()
		cur.close()
		self._lock.release()
		return ret

	@seize_err_if_any()
	def insert_to_tbl(
		self,
		tbl_name: str,
		dom_dict: dict[str, int | str | bool | float]
	) -> int:
		domains, dom_val = self.dict_unpacker(dom_dict)
		payload = f"INSERT OR IGNORE INTO {tbl_name} ({', '.join(domains)}) " \
				  f"VALUES ({'?, ' * (len(domains) - 1) + '?'});"
		assert self.is_col_name_in_tbl(tbl_name, set(domains)), \
			f'invalid column name{domains} was passed into inserting function for {tbl_name}'

		self._lock.acquire()
		cur = self._conn.cursor()
		cur.execute(payload, dom_val)
		ret = cur.lastrowid
		cur.close()
		self._lock.release()
		return ret

	@seize_err_if_any()
	def insert_multivals_to_tbl(
		self,
		tbl_name: str,
		domains: tuple,
		vals: list[tuple],
		confilct_key_ids: Optional[list[str]]=None
	) -> int:
		"""
		向数据库插入数据。
		如果有冲突，则改为更新
		"""
		# OR IGNORE
		assert len(domains) >= 1
		if len(vals) == 0:
			return 0
		payload = f"INSERT INTO {tbl_name} ({', '.join([*domains])}) " \
		          f"VALUES ({('?, ' * len(domains))[:-2]}) "
		flag = confilct_key_ids is not None and len(confilct_key_ids) > 0
		payload += '' if not flag else f"ON CONFLICT({', '.join(confilct_key_ids)}) DO UPDATE SET "
		for idx, v in enumerate(domains):
			# excluded 是语法内置的关键字，无需在表中定义，
			# 仅用于 ON CONFLICT 冲突处理中引用 “待插入的新数据”
			payload += f'{v}=excluded.{v}' if flag else ''
			payload += ';' if idx + 1 == len(domains) else (', ' if flag else '')

		self._lock.acquire()
		cur = self._conn.cursor()
		cur.executemany(payload, vals)
		ret = cur.lastrowid
		cur.close()
		self._lock.release()
		return ret

	@seize_err_if_any()
	def update_item_in_tbl(
		self,
		tbl_name: str,
		ids_dict: dict[str, int | str | bool | float],
		set_dict: dict[str, int | str | bool | float]
	) -> int:
		set_domains, set_domvals = DBfd.dict_unpacker(set_dict)
		del set_dict
		if len(set_domains) == 0:
			# 什么都没有就不更新，用-1表示这个含义
			return -1
		payload = ', '.join([_ + ' = ?' for _ in set_domains])
		set_domains = []
		for k, v in ids_dict.items():
			set_domains.append(k)
			set_domvals = (*set_domvals, v)
		and_chain = ' = ? AND '.join(set_domains) + ' = ?'
		del set_domains

		self._lock.acquire()
		cur = self._conn.cursor()
		cur.execute(
			f"UPDATE {tbl_name} SET {payload} WHERE {and_chain} ;",
			set_domvals
		)
		# self._conn.commit()
		ret = cur.rowcount  # > 0 就意味着更新成功
		cur.close()
		self._lock.release()
		return ret

	@seize_err_if_any()
	def renew_if_exist_else_insert(
		self,
		tbl_name: str,
		cond_dict: dict[str, int | str | bool | float],
		extra_insert_domains: dict[str, int | str | bool | float] = {}
	) -> any:
		ok_row = self.update_item_in_tbl(tbl_name, cond_dict, extra_insert_domains)
		if (isinstance(ok_row, int) and ok_row > 0) or len(extra_insert_domains) == 0:
			# TODO: ubid 出问题了，不好传id因为id本身就是要申请创建的对象
			#       另外就是cond_dict是复合insert来用的，
			#       如果传id就必须要传id对应的值，但insert哪里能分辨这个值已经存在？
			# choose_doms=[k for k in cond_dict],
			return self.query_items_in_tbl(tbl_name, cond_dict, limit_num=1)

		cond_dict.update(extra_insert_domains)
		return self.insert_to_tbl(tbl_name, cond_dict)

	def remove_item_in_tbl(
		self,
		tbl_name: str,
		cond_dict: dict[str, int | str | bool | float]
	) -> None:
		domains, dom_val = DBfd.dict_unpacker(cond_dict)
		and_chain = '= ? AND '.join(domains) + '= ?'

		self._lock.acquire()
		cur = self._conn.cursor()
		cur.execute(
			f"DELETE FROM {tbl_name} WHERE {and_chain} ;",
			dom_val
		)
		self._lock.release()

	@seize_err_if_any()
	def dump_table(self, tbl_name: str) -> any:
		self._lock.acquire()
		cur = self._conn.cursor()
		# 会超级慢
		cur.execute(f'SELECT * FROM {tbl_name}')
		ret = cur.fetchall()
		self._lock.release()
		return ret


def songslist_related_albums_counter() -> int:
	"""
	select DISTINCT albums.album_id from albums
	inner join songs on songs.album_id = albums.album_id
	inner join curr_songslists on curr_songslists.song_id = songs.song_id
	inner join songslists on songslists.songslist_id = curr_songslists.songslist_id;
	"""
	...

# 需要自己去手动控制database的释放
# 不考虑使用途中电脑突然关机导致更新失败的问题
# 需要检查是否真的有关于歌单数据库的配置
if __name__ == '__main__':
	# pass
	# from pathlib import Path
	# src_path = str(Path(__file__).parent / '..' / '..' / '..' / 'assets' / 'dyn' / 'somgs_test.db')
	# dst_path = str(Path(__file__).parent / '..' / '..' / '..' / 'assets' / 'dyn' / 'somgs.db')
	# print(src_path)
	# local_sync_db(src_path, dst_path, 'albums',['album_id'], ['cover'])
	
	from misc_utils.time_aux import dura_avg
	from configs.args_loader import PARSER
	from misc_utils import PRIVATE_CONFIG
	from datatypes.easynet.sqlite_types import netease_db_tbl_refs
	args = PARSER.parse_args()
	del PARSER
	database_fd = DBfd(args.database_path, netease_db_tbl_refs)

	ubid = database_fd.query_items_in_tbl(
		'user_behaviors',
		{'soid': 42, 'user_id': PRIVATE_CONFIG['netease'][args.songslist_author]['user-id']},
		{'ubid': 'DESC'},
		['ubid'],
		limit_num=1
	)
	print(ubid, type(ubid), len(ubid))
	song_id = database_fd.query_items_in_tbl(
		'curr_songslists',
		{'songslist_id': PRIVATE_CONFIG['netease'][args.songslist_author]['list-id']},
		choose_doms=['song_id']
		# limit_num=1
	)
	time_list = []
	for ssid in song_id:
		cur_time = database_fd.query_items_in_tbl(
			'songs',
			{'song_id': ssid[0]},
			choose_doms=['duration'],
			limit_num=1
		)
		time_list.append(cur_time[0]['duration'])
	print(dura_avg(time_list))
	# ubids = [
	# 	# select distinct soid from songslist_status where soid < {某个值}

