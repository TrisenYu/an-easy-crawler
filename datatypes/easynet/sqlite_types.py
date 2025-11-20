from typing import Dict

from misc_utils.opts.db.sqlite_base import SQLiteTabMetaClass

class SongslistTabDef(SQLiteTabMetaClass):
	table_structure = {
		'songslists': {
			'songslist_id': ('INTEGER', 'PRIMARY', 'AUTOINCREMENT'),
			'creator_id'  : ('INTEGER', ('users', 'user_id')),
			'birthday'    : ('TEXT', 'NOTNULL'),
		}
	}


class UserBehaviorsTabDef(SQLiteTabMetaClass):
	table_structure = {
		'user_behaviors': {
			"ubid"   : ('INTEGER', 'PRIMARY', 'AUTOINCREMENT', 'UNIQUE'),
			'soid'   : ('INTEGER', ('songslists_observations', 'soid'), 'UNIQUE'),
			'user_id': ('INTEGER', ('users', 'user_id'), 'UNIQUE')
		}
	}


class SongstatusTabDef(SQLiteTabMetaClass):
	table_structure = {
		'songs_status_in_songslists': {
			'song_id'       : ('integer', 'primary', 'unique', ('songs', 'song_id')),
			'ubid'      : ('integer', 'primary', 'unique', ('user_behaviors', 'ubid')),
			'op_time'   : ('text', {'default': 'current_timestamp'}),
			'insert_pos': ('integer',),
			'delete_pos': ('integer',)
		}
	}


class CurrSongslistTabDef(SQLiteTabMetaClass):
	table_structure = {
		'curr_songslists': {
			'song_id'    : ('INTEGER', 'NOTNULL', ('songs', 'song_id')),
			'songslist_id'   : ('INTEGER', ('songslists', 'songslist_id'), 'PRIMARY'),
			'pos_val': ('INTEGER', 'PRIMARY')
		}
	}


class SongslistsObservationsTabDef(SQLiteTabMetaClass):
	table_structure = {
		'songslists_observations': {
			'soid'            : ('integer', 'primary', 'autoincrement'),
			'songslist_id'    : ('integer', ('songslists', 'songslist_id'), 'unique'),
			'observer_id'     : ('integer', ('users', 'user_id'), 'unique'),
			'observation_time': ('text', 'unique'),
		}
	}


class SongsTabDef(SQLiteTabMetaClass):
	table_structure = {
		'songs': {
			'song_id'      : ('integer', 'primary'),
			'name'         : ('text',),
			'duration'     : ('text',),
			'album_id'     : ('integer', ('albums', 'album_id')),
			'tr_pos'       : ('integer',),
			'download_path': ('text',),
			'lyrics'       : ('text',),
			'translatext'  : ('text',),
			'arrangers'    : ('text',),
			'vocals'       : ('text',),
			'mastering'    : ('text',),
			'subtitle'     : ('text',),
			'styles_tags'  : ('text',),
			'fetchable'    : ('integer', {'default': 1}),
			'being_liked'  : ('integer',)
		}
	}


class AlbumsTabDef(SQLiteTabMetaClass):
	table_structure = {
		'albums': {
			'album_id'    : ('integer', 'primary'),
			'name'        : ('text',),
			'cover'       : ('text',),
			'company'     : ('text',),
			'publish_time': ('text',),
			'being_liked' : ('integer',)
		}
	}



class UsersTabDef(SQLiteTabMetaClass):
	table_structure = {
		'users': {
			'user_id': ('integer', 'primary', 'notnull'),
			'name'   : ('text',),
			'brief'  : ('text',),
			'avatar' : ('text',)
		}
	}


class ArtistTabDef(SQLiteTabMetaClass):
	table_structure = {
		'artists': {
			'artist_id'   : ('integer', 'notnull', 'primary', 'autoincrement'),
			'name'        : ("text",),
			'social_media': ('text',)
		}
	}


class SongsRelatedArtistsTabDef(SQLiteTabMetaClass):
	table_structure = {
		'songs_related_artists': {
			'artist_id': ('integer', ('artists', 'artist_id'), 'primary'),
			'song_id'  : ("integer", ('songs', 'song_id'), 'primary'),
		}
	}

def _songslists_observation_tab_def_helper(name: str, field_ty: str) -> Dict:
	return {
		f'{name}_rec': {
			'soid'   : ('integer', ('songslists_observations', 'soid'), 'primary'),
			f'{name}': (f'{field_ty}', 'notnull')
		}
	}

class TitleTabDef(SQLiteTabMetaClass):
	table_structure = _songslists_observation_tab_def_helper('title', 'text')

class LikerTabDef(SQLiteTabMetaClass):
	table_structure = _songslists_observation_tab_def_helper('liker', 'INTEGER')

class DescriptionTabDef(SQLiteTabMetaClass):
	table_structure = _songslists_observation_tab_def_helper('description', 'TEXT')


class ShareCntTabDef(SQLiteTabMetaClass):
	table_structure = _songslists_observation_tab_def_helper('share_cnt', 'integer')

class RefHitsTabDef(SQLiteTabMetaClass):
	table_structure = _songslists_observation_tab_def_helper('ref_hit', 'INTEGER')


netease_db_tbl_refs = [
	SongslistTabDef,
	UserBehaviorsTabDef,
	SongstatusTabDef,
	CurrSongslistTabDef,
	SongslistsObservationsTabDef,
	SongsTabDef,
	AlbumsTabDef,
	UsersTabDef,
	ArtistTabDef,
	SongsRelatedArtistsTabDef,
	TitleTabDef,
	LikerTabDef,
	DescriptionTabDef,
	ShareCntTabDef,
	RefHitsTabDef,
]
