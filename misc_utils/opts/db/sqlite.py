#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0
# (C) All rights reserved. Author: <kisfg@hotmail.com> in 2025
# Created at 2025/09/03 星期三 00:24:10
# Last modified at 2025/10/04 星期六 02:37:04
"""
写着写着有种脑梗的"美感"
"""
import sqlite3, ast, os, copy

from typing import Optional
from misc_utils.file_operator import (
	unsafe_read_text,
	is_fpath,
	dir2file
)
from misc_utils.time_aux import (
	unix_ts_to_time,
	US_TIME_FORMAT
)
from misc_utils.logger import DEBUG_LOGGER
from threading import Semaphore

'''
如果后面还有需求要向表格增添新字段，可以用ALTER TABLE 语句
ALTER TABLE xxx ADD COLUMN email TEXT

但是怎么整合是一个需要好好考虑的问题
'''

_SONGSLISTS_PAYLOAD: str = """-- 歌单表
CREATE TABLE IF NOT EXISTS songslists (
	songslist_id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	-- 不能在定义时起别名真的是虾头，
	-- 这里只作为创建者来使用
	birthday TEXT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES
		users(user_id) ON DELETE CASCADE
) STRICT; CREATE UNIQUE INDEX IF NOT EXISTS slidx ON songslists(songslist_id, user_id);"""


def _gen_database_table(
	tbl_name: str,
	comment: str='',
	field_attr: str='INTEGER'
) -> str:
	'''
	给定输入生成创建数据表的函数
	'''
	return ""													\
	f"-- {comment}\n"											\
	f"CREATE TABLE IF NOT EXISTS {tbl_name}_rec  (\n"			\
	"	soid INTEGER NOT NULL,			-- 观测记录作为外键\n" 	  \
	f"	{tbl_name} {field_attr} NOT NULL,\n"					\
	"	FOREIGN KEY (soid) REFERENCES\n"					 	\
	"		songslists_observation(soid) ON DELETE CASCADE,\n"	\
	"	PRIMARY KEY (soid) "									\
	") STRICT;"													\
	f"CREATE UNIQUE INDEX IF NOT EXISTS {tbl_name}_rec_idx ON {tbl_name}_rec(soid); "

_TITLE_PAYLOAD: str = _gen_database_table("titles", "歌单名称表", 'TEXT')

_LIKER_PAYLOAD: str = _gen_database_table("likers", "收藏歌单观测统计表")

_DESCRIPTION_PAYLOAD: str = _gen_database_table(
	"description", "歌单简介记录观测表", 'TEXT'
)
_REF_HITS_PAYLOAD: str = _gen_database_table(
	"ref_hits", "歌单参考点击量观测表"
)
_SHARE_CNT_PAYLOAD: str = _gen_database_table(
	"share_cnt", "分享量观测统计表"
)

_USERS_BEHAVIORS_PAYLOAD: str = """-- 歌单中用户行为观测表
CREATE TABLE IF NOT EXISTS users_behaviors (
	ubid INTEGER PRIMARY KEY AUTOINCREMENT,
	soid INTEGER NOT NULL, 					-- 观测到的歌单记录
	user_id INTEGER NOT NULL,	   			-- 对歌单有编辑权限的用户
	FOREIGN KEY (soid) REFERENCES
		songslists_observation(soid) ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES
		users(user_id) ON DELETE CASCADE,
	UNIQUE (ubid, soid, user_id)
) STRICT; CREATE UNIQUE INDEX IF NOT EXISTS usu_idx ON users_behaviors(ubid, soid, user_id); """

_SONGS_STATUS_PAYLOAD: str = """-- 歌单中editor(s)对歌曲操作的差分观测记录表
CREATE TABLE IF NOT EXISTS songs_status_in_songslists (
	song_id INTEGER NOT NULL,
	ubid INTEGER NOT NULL,   				 -- 操作者行为表中的某项记录
	op_time TEXT DEFAULT current_timestamp,	 -- 删除是不好知道的，顶多只能给范围
	-- 还是要记一记哪里删减增加
	insert_pos INTEGER,
	delete_pos INTEGER,
	-- 外键定义
	FOREIGN KEY (song_id) REFERENCES
		songs(song_id) ON DELETE CASCADE,
	FOREIGN KEY (ubid) REFERENCES
		users_behaviors(ubid) ON DELETE CASCADE,
	UNIQUE (song_id, ubid),
	PRIMARY KEY (song_id, ubid)
) STRICT; CREATE UNIQUE INDEX IF NOT EXISTS ssis_idx ON songs_status_in_songslists(song_id, ubid); """

_CURR_SONGSLIST_PAYLOAD: str = """-- 当前歌单表
CREATE TABLE IF NOT EXISTS curr_songslists (
	song_id INTEGER NOT NULL,			-- song_id 是会变动的
	songslist_id INTEGER NOT NULL,
	pos_val INTEGER NOT NULL,			-- 只维护，不记录更新，反而这个值和歌单一起做主键比较合适
	FOREIGN KEY (songslist_id) REFERENCES
		songslists(songslist_id) ON DELETE CASCADE,
	FOREIGN KEY (song_id) REFERENCES
		songs(song_id) ON DELETE CASCADE,
	PRIMARY KEY (songslist_id, pos_val)
) STRICT; CREATE INDEX IF NOT EXISTS cur_ssid ON curr_songslists(songslist_id, song_id, pos_val); """

_OBSERVATIONS_PAYLOAD: str = """-- 歌单观测记录表
CREATE TABLE IF NOT EXISTS songslists_observation (
	soid INTEGER PRIMARY KEY AUTOINCREMENT,
	songslist_id INTEGER NOT NULL,		-- 歌单id外键
	user_id INTEGER NOT NULL,			-- 观测者id外键
	observation_time TEXT,
	FOREIGN KEY (songslist_id) REFERENCES
		songslists(songslist_id) ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES
		users(user_id) ON DELETE CASCADE,
	UNIQUE (songslist_id, user_id, observation_time)
) STRICT; """

_SONGS_PAYLOAD: str = """-- 歌曲数据表
CREATE TABLE IF NOT EXISTS songs (
	song_id INTEGER PRIMARY KEY,
	name TEXT,
	duration TEXT,
	album_id INTEGER,
	tr_pos INTEGER,						-- tr 在 album 中的位置
	-- 有种情况是专辑由多张光盘保存
	-- 导致歌曲需要细分为 第 i 个光盘中的第 j 轨
	-- 但是为了方便，这里只记录按顺序数的位次
	download_path TEXT,					-- 本地下载位置，如果可能
	lyrics  TEXT,						-- 不一定有但是要留
	translatext  TEXT,					-- 翻译也是一样的道理
	-- 存在一首有多个作者的情况，这里用类似list的结构会更好
	-- 业内似乎是用序列化的方式来存储多义的字段
	arrangers TEXT,						-- 编曲
	composers TEXT,						-- 作曲
	lyricists TEXT,						-- 作词
	vocals TEXT,						-- 献唱域
	mastering TEXT,						-- 母带，暂时还不知道怎么填？
	subtitle TEXT,						-- 可能有子标题
	styles_tags TEXT,					-- 风格，后面再说
	-- 不建议将音频文件存到数据库，即使有些是确实可以下载的
	-- 最多就留个路径指向本地的文件
	-- 但是如果删了本地的这个文件，那这里的数据域还有用吗？
	fetchable INTEGER DEFAULT 1,-- 是否有效
	-- other information
	FOREIGN KEY (album_id) REFERENCES
		albums(album_id) ON DELETE CASCADE
) STRICT; """

_ALBUM_PAYLOAD: str = """-- 专辑表
CREATE TABLE IF NOT EXISTS albums (
	album_id INTEGER PRIMARY KEY,
	name TEXT,
	cover  TEXT,			 			-- 专辑封面
	company TEXT,		 				-- 发行方
	publish_time TEXT 					-- 发行时间
) STRICT; """

_USERS_PAYLOAD: str = """-- 可能会涉及到的用户
CREATE TABLE IF NOT EXISTS users (
	user_id INTEGER NOT NULL PRIMARY KEY,
	name TEXT,			 				-- 生产环境下不关心名字修改与否
	brief TEXT, 		 				-- 包括简介也是一样
	avatar TEXT
) STRICT; """


class DBfd:
	"""
	内部的几个函数用不好就是妥妥的SQL注入
	毕竟从用法上就是为了编程的方便而放弃了预编译

	解决的办法可以用类似查表的方法，走固定而且写死的调用
	但是还是要一定工作量的，正好假期也结束了，等后面有空再做。
	"""
	def __init__(self, db_path: str) -> None:
		# 检查 db 是否存在，不存在则创建。
		self.path = db_path
		self._conn = None
		self.lock = Semaphore(1)
		self._init_db

	@property
	def close(self) -> None:
		self.lock.acquire()
		self._conn.close()
		self.lock.release()

	@property
	def _is_table_empty(self) -> bool:
		# TODO: 指出哪一个是空的
		cur = self._conn.cursor()
		ret = True
		targets = [
			'songs', 'users', 'songslists', 'albums',
			'songslists_observation',
			'songs_status_in_songslists', 'users_behaviors'
			"titles_rec", "likers_rec",
			"curr_songslists",
			"descrtiption_rec",
			"ref_hits_rec", "share_cnt_rec",
		]
		for item in targets:
			self.lock.acquire()
			cur.execute(
				"SELECT tbl_name FROM sqlite_master "
				"WHERE tbl_name = ? AND type = 'table';",
				(item,)
			)
			ret &= cur.fetchone() is None
			self.lock.release()
		cur.close()
		return ret

	@property
	def _init_db(self) -> None:
		self._conn = sqlite3.connect(
			# 直接在变量内上锁
			self.path, check_same_thread=False
		)
		self._conn.row_factory = sqlite3.Row
		self._conn.execute('PRAGMA foreign_keys = ON')
		if self._is_table_empty:
			self._create_table

	@property
	def _create_table(self) -> None:
		global _USERS_PAYLOAD, _SONGSLISTS_PAYLOAD
		global _SONGS_PAYLOAD, _SONGS_STATUS_PAYLOAD
		global _OBSERVATIONS_PAYLOAD, _REF_HITS_PAYLOAD
		global _LIKER_PAYLOAD, _TITLE_PAYLOAD, _ALBUM_PAYLOAD
		global _SHARE_CNT_PAYLOAD, _DESCRIPTION_PAYLOAD
		global _USERS_BEHAVIORS_PAYLOAD, _CURR_SONGSLIST_PAYLOAD
		curs = self._conn.cursor()
		curs.execute("BEGIN")
		curs.execute(_USERS_PAYLOAD)
		curs.execute(_ALBUM_PAYLOAD)
		curs.execute(_SONGS_PAYLOAD)
		curs.executescript(_SONGSLISTS_PAYLOAD)
		curs.execute(_OBSERVATIONS_PAYLOAD)
		curs.executescript(_USERS_BEHAVIORS_PAYLOAD)
		curs.executescript(_SONGS_STATUS_PAYLOAD)
		curs.executescript(_CURR_SONGSLIST_PAYLOAD)
		curs.executescript(_DESCRIPTION_PAYLOAD)
		curs.executescript(_LIKER_PAYLOAD)
		curs.executescript(_REF_HITS_PAYLOAD)
		curs.executescript(_SHARE_CNT_PAYLOAD)
		curs.executescript(_TITLE_PAYLOAD)
		curs.close()
		self._conn.commit()
		return None


	def check_domain_in_tbl(self): pass
	def check_type_in_tbl(self): pass

	@staticmethod
	def dict_unpacker(
		dom_dict: dict[str, int | str | bool | float]
	) -> tuple[list, tuple]:
		reslist, restupl = [], ()
		for k, v in dom_dict.items():
			reslist.append(k)
			restupl = (*restupl, v)
		return reslist, restupl

	def query_items_in_tbl(
		self,
		tbl_name: str,
		cond_dict: dict[str, int | str | bool | float],
		# TODO: ORDER 也整个字典，然后提供desc和limit
		order_dom: str='',
		need_desc: bool=False
	) -> any:
		cond_name, cond_val = DBfd.dict_unpacker(cond_dict)
		_and_chain = '= ? AND '.join(cond_name) + ' = ?'
		_need_desc = 'DESC' if need_desc else ''
		order_dom = f'ORDER BY {order_dom} {_need_desc}' if order_dom != '' else ''
		payload = f"SELECT * FROM {tbl_name} WHERE {_and_chain} {order_dom};"
		del cond_name, tbl_name, order_dom
		self.lock.acquire()
		cur = self._conn.cursor()
		cur.execute(payload, cond_val)
		ret = cur.fetchall()
		cur.close()
		self.lock.release()
		return ret


	def query_null_items_in_tbl(
		self,
		tbl_name: str,
		domains: dict[str, int | str | bool | float],
		nil_doms: list[str]
	) -> any:
		assert len(nil_doms) != 0 and len(domains) != 0
		cond_name, cond_val = DBfd.dict_unpacker(domains)
		and_chain = ' = ? AND '.join(cond_name) + ' = ? AND ' + \
					' IS NULL AND '.join(nil_doms) + ' IS NULL '
		payload = f'SELECT * FROM {tbl_name} WHERE {and_chain};'
		self.lock.acquire()
		cur = self._conn.cursor()
		cur.execute(payload, cond_val)
		ret = cur.fetchall()
		cur.close()
		self.lock.release()
		return ret


	def insert_to_tbl(
		self,
		tbl_name: str,
		dom_dict: dict[str, int | str | bool | float]
	) -> any:
		domains, dom_val = DBfd.dict_unpacker(dom_dict)
		payload = '' \
			f"INSERT OR IGNORE INTO {tbl_name} " \
			f"({', '.join(domains)}) VALUES ({'?, '*(len(domains)-1)+'?'});"
		self.lock.acquire()
		cur = self._conn.cursor()
		cur.execute(payload, dom_val)
		self._conn.commit()
		ret = cur.lastrowid
		cur.close()
		self.lock.release()
		return ret


	def update_item_in_tbl(
		self,
		tbl_name: str,
		ids_dict: dict[str, int | str | bool | float],
		dom_dict: dict[str, int | str | bool | float]
	) -> None:
		domains, domval = DBfd.dict_unpacker(dom_dict)
		del dom_dict
		if len(domains) == 0:
			# 什么都没有就不更新
			return
		payload = ', '.join([_+' = ?' for _ in domains])
		domains = []
		for k, v in ids_dict.items():
			domains.append(k)
			domval = (*domval, v)
		and_chain = '= ? AND '.join(domains) + '= ?'
		del domains

		self.lock.acquire()
		cur = self._conn.cursor()
		cur.execute(
			f"UPDATE {tbl_name} "
			f"SET {payload} "
			f"WHERE {and_chain} ;",
			domval
		)
		self._conn.commit()
		self.lock.release()


	def insert_if_not_exist_else_renew(
		self,
		tbl_name: str,
		dom_dict: dict[str, int | str | bool | float],
		extra_insert_domains: dict[str, int | str | bool | float]={}
	) -> any:
		last_obj = self.query_items_in_tbl(tbl_name, dom_dict)
		if last_obj is None or len(last_obj) == 0:
			for k, v in extra_insert_domains.items():
				dom_dict[k] = v
			return self.insert_to_tbl(tbl_name, dom_dict)
		return self.update_item_in_tbl(tbl_name, dom_dict, extra_insert_domains)


	def remove_item_in_tbl(
		self, 
		tbl_name: str,
		dom_dict: dict[str, int | str | bool | float]
	) -> None:
		domains, dom_val = DBfd.dict_unpacker(dom_dict)
		and_chain = '= ? AND '.join(domains) + '= ?'

		self.lock.acquire()
		cur = self._conn.cursor()
		cur.execute('BEGIN')
		cur.execute(
			f"DELETE FROM {tbl_name} WHERE {and_chain} ;",
			dom_val
		)
		self._conn.commit()
		self.lock.release()


	def is_item_in_tbl(
		self,
		IDs: tuple,
		keys: tuple,
		tbl_name: str
	) -> tuple[bool, any]:
		self.lock.acquire()
		cur = self._conn.cursor()
		listr = ' AND '.join([_+'= ?' for _ in [*IDs]])
		cur.execute(
			f"SELECT * FROM {tbl_name} WHERE {listr} ;", keys
		)
		ret = cur.fetchone()
		cur.close()
		self.lock.release()
		return ret is not None, ret


# 需要自己去手动控制database的释放
# 不考虑使用途中电脑突然关机导致更新失败的问题
# 需要检查是否真的有关于歌单数据库的配置
if __name__ == '__main__':
	import os
	from typing import Optional
	from misc_utils.args_loader import PARSER
	_args = PARSER.parse_args()

	database_fd: Optional[DBfd] = DBfd(_args.database_path)
	if database_fd is None:
		exit(0)
	# rows = database_fd.query_items_in_tbl('songs_status_in_songslists', {'ubid': 1})
	# print([_['song_id'] for _ in rows])
	# print(len(upd_list))
	rows = database_fd.query_null_items_in_tbl(
		'songs_status_in_songslists', {
			'ubid': 1
		}, ['delete_pos']
	)
	print([_['song_id'] for _ in rows])