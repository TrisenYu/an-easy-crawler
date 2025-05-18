#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
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
from typing import TypedDict


## 先实现可能有用的部分
### 歌单部分
class ArtistInfo(TypedDict):
	name: str
	id: int
	picId: int
	picUrl: str


class AlbumInfo(TypedDict):
	id: int
	name: str
	type: str
	size: int               # 专辑内歌曲数量
	blurPicUrl: str
	picUrl: str
	pic: int                # 实际为 pidID
	tags: str
	artist: ArtistInfo
	publishTime: int
	description: str
	commentThreadId: str
	company: str            # 发行公司 / 展会
	subType: str


class SongDetails(TypedDict):
	name: str
	id: int
	position: int
	alias: list[str]        # 原曲名之类的。
	artists: list[ArtistInfo]
	album: AlbumInfo
	duration: int


class SongsResp(TypedDict):
	"""
	单首歌的 response 结构
	"""
	songs: list[SongDetails]
	code: int
	equalizers: dict


class PlaylistTrackInfo(TypedDict):
	id: int
	v: int
	t: int
	at: int
	uid: int
	rcmdReasonTitle: str
	# sc, f, sr, dpr, alg: null


class PlaylistDetail(TypedDict):
	id: int
	name: str
	coverImgId: int
	coverImgUrl: str
	userId: int
	createTime: int
	updateTime: int
	trackCount: int
	trackUpdateTime: int
	playCount: int
	subscribedCount: int
	description: str
	tags: list[str]
	commentThreadId: str
	trackIds: list[PlaylistTrackInfo]


class PlaylistInfo(TypedDict):
	"""歌单 response 结构"""
	code: int
	playlist: PlaylistDetail

### 登录部分
class LoginInit(TypedDict):
	pass