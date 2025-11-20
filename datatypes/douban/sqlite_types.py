from misc_utils.opts.db.sqlite_base import SQLiteTabMetaClass

class MoviesTabDef(SQLiteTabMetaClass):
	table_structure = {
		"movies": {
			"movie_id": ('integer', 'primary', 'unique'),
			'name': ('text', )
		}
	}

class CommentsTabDef(SQLiteTabMetaClass):
	table_structure = {
		"comments": {
			"comment_id": ('integer', 'primary', 'unique'),
			"content": ('text', ),
			"publish_date": ('text', ),
			'votes': ('integer', ),
			'ip_addr': ('text',),
			'rating': ('text', ) # 4/5, 1/5, 5/5 这样子
		}
	}

class CommentsOnMoviesTabDef(SQLiteTabMetaClass):
	table_structure = {
		"comment_on_movies": {
			"comment_id": ('integer', ('comments', 'comment_id'), 'primary'),
			"movie_id": ('integer', ('movies', 'movie_id'), 'primary'),
		}
	}

douban_tbl_refs = [
	CommentsOnMoviesTabDef,
	MoviesTabDef,
	CommentsTabDef,
]