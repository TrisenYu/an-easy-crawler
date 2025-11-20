# !/usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# Last modified at 2025/10/02 星期四 20:41:55
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
from typing import Optional, TypedDict

## 先实现可能有用的部分，后续应该会把这些类型定义丢到types文件夹里
### 歌单部分
## TODO: 以后结构多了就像一大坨一样。
class ArtistInfo(TypedDict):
	name: str
	id: int
	picId: int
	picUrl: str


class AlbumInfo(TypedDict):
	id: int
	name: str
	type: str
	size: int  # 专辑内歌曲数量
	blurPicUrl: str
	picUrl: str
	pic: int  # 实际为 pidID
	tags: str
	artist: ArtistInfo
	publishTime: int
	description: str
	commentThreadId: str
	company: str  # 发行公司 / 展会
	subType: str


class SongDetails(TypedDict):
	name: str
	id: int
	no: int  # number in dics
	alias: list[str]  # 原曲名之类的。
	artists: list[ArtistInfo]
	album: AlbumInfo
	duration: int
	position: int  # track_pos，但有时候抽风要用no
	publishTime: int
	copyright: int


class SongsResp(TypedDict):
	""" 单首歌的 response 结构 """
	songs: list[SongDetails]
	code: int
	equalizers: dict


class PlaylistTrackInfo(TypedDict):
	id: int
	v: int
	t: int
	at: int  # 加入到歌单的时间
	uid: int  # 加歌进来的用户
	rcmdReasonTitle: str
# sc, f, sr, dpr, alg: null


class CreatorDetail(TypedDict):
	userId: int
	nickname: str
	signature: str


class PlaylistDetail(TypedDict):
	id: int
	name: str
	coverImgId: int
	coverImgUrl: str
	userId: int
	createTime: int
	updateTime: int
	trackCount: int
	shareCount: int
	creator: CreatorDetail
	trackUpdateTime: int
	playCount: int
	subscribedCount: int
	description: str
	tags: list[str]
	commentThreadId: str
	trackIds: list[PlaylistTrackInfo]


class PlaylistInfo(TypedDict):
	""" 歌单 response 结构 """
	code: int
	playlist: PlaylistDetail


### 单曲部分
class SongDatum(TypedDict):
	songName: str
#


class aSong(TypedDict):
	code: int
	data: SongDatum
	message: str


### 机器人部分

class BotHitsParam(TypedDict):
	shell_path: str
	author_idx: str
	dummy_idx: str


### 配置部分

class JsonUserConf(TypedDict):
	csrf_token: str
	cookie: str
	email: Optional[str]
	user_id: Optional[str]
	backup_dir: Optional[str]

