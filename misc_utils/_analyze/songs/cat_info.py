# !/usr/bin/env/python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
#
# 施工中。
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.
# from misc_utils.args_loader import PARSER
# from misc_utils.opts.json.conf_reader import PRIVATE_CONFIG
from pathlib import Path

import ffmpeg

# from misc_utils.opts.db.sqlite import DBfd


def avg_duration_evalator(slid: int) -> str:
	return ''


def dump_audio_info(audio_fpath: Path) -> None:
	for audio_path in audio_fpath.rglob('*.mp3'):
		"""
		"""
		probe = ffmpeg.probe(audio_path)
		print(probe)
		break


if __name__ == '__main__':
	ref_path = Path(__file__).parent/'..'/'..'/'..'/'assets'/'stat'/'tracks'
	dump_audio_info(ref_path.resolve())