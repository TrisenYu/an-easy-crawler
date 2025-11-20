from misc_utils.opts.db.sqlite_base import SQLiteTabMetaClass

class CommentTabDef(SQLiteTabMetaClass):
	table_structure = {
		"comments": {
			"comment_id": ('integer', 'primary'),
			"content": ('text', ),
			"useful_cnt": ('integer', ),
			"score": ("integer", ),
			"ip_addr": ('text', ),
			"publish_date": ('text', )
		}
	}

class ScenicSpotsTabDef(SQLiteTabMetaClass):
	table_structure = {
		"scenic_spots": {
			"ssid": ('integer', 'primary'),
			'name': ('text', )
		}
	}

class CommentsOnSpotsTabDef(SQLiteTabMetaClass):
	table_structure = {
		'comments_on_spots': {
			'spot_id': ('integer', ('scenic_spots', 'ssid'), 'primary'),
			'comment_id': ('integer', ('comments', 'comment_id'), 'primary'),
		}
	}

ctrip_tbl_refs = [
	CommentTabDef,
	CommentsOnSpotsTabDef,
	ScenicSpotsTabDef,
]