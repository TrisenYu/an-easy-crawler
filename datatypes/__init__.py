__author__ = 'kisfg@hotmail.com'
__date__ = '2025/11 - '
__license__ = 'GPL2.0-ONLY'
# easynet = netease，之所以这样子是因为懂得抖动
__all__ = [
	# ref_types
	"SongsResp",
	"SongDetails",
	"SongDatum",
	"PlaylistInfo",
	"PlaylistDetail",
	"PlaylistTrackInfo",
	"BotHitsParam",
	"JsonUserConf",
]
from .easynet.ref_types import (
	SongsResp, SongDetails,
	SongDatum, PlaylistInfo,
	PlaylistDetail, PlaylistTrackInfo,
	BotHitsParam, JsonUserConf
)