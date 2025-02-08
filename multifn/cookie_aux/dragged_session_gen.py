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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.
# TODO: 检验 session_gen 算的 cookie 是否不能取代这种大量计算得出的值
import re, random, time

from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent

from multifn.cookie_aux.draw_canvas import gen_fp_png_base64str
from crypto.manual_deobfuscation import (
	netease_mmh32,
	netease_crc32
)

_sdk_s = [
	SoftwareName.CHROME.value,
	SoftwareName.YANDEX.value,
	SoftwareName.EDGE.value,
	SoftwareName.FIREFOX.value,
	SoftwareName.SAFARI.value
]
_os_s = [
	OperatingSystem.WINDOWS.value,
	OperatingSystem.WINDOWS_PHONE.value,
	OperatingSystem.LINUX.value,
	OperatingSystem.ANDROID.value,
	OperatingSystem.DARWIN.value,
	OperatingSystem.IOS.value,
	OperatingSystem.MACOS.value,
	OperatingSystem.UNIX.value,
	OperatingSystem.OPENBSD.value
]
inject_str = "aZbY0cXdW1eVf2Ug3Th4SiR5jQk6PlO7mNn8MoL9pKqJrIsHtGuFvEwDxCyBzA"
r2_const_suffix = "PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf" \
                  "$Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf" \
                  "$Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf" \
                  "$Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf" \
                  "$WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf" \
                  ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;" \
                  ";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;"
_f = lambda x: ''.join([x[random.randint(0, len(x) - 1)] for _ in range(3)])

def cloud_music_gen_session_id():
	def anony_rand() -> int:
		return random.randint(0, 255)

	def rand_rgb() -> tuple[int, int, int]:
		return anony_rand(), anony_rand(), anony_rand()

	user_agent_rotator = UserAgent(operating_systems=_os_s, software_names=_sdk_s)
	ua = user_agent_rotator.get_random_user_agent()
	try:
		# 事实上 Navigator.platform 理应被弃用了。不过为什么要纠结这个呢？ua里头有啊——
		# 如果想搞特殊可以看 https://stackoverflow.com/a/19883965
		match_plantform = re.search(r'\([^;]+;\s([^;]+);\s[^)]+\)', ua).group(1)
	except AttributeError:
		match_plantform = ''

	css_sys_col = f"ActiveBorder:rgb{rand_rgb()}:ActiveCaption:rgb{rand_rgb()}:AppWorkspace:rgb{rand_rgb()}:" \
	              f"Background:rgb{rand_rgb()}:ButtonFace:rgb{rand_rgb()}:ButtonHighlight:rgb{rand_rgb()}:" \
	              f"ButtonShadow:rgb{rand_rgb()}:ButtonText:rgb{rand_rgb()}:CaptionText:rgb{rand_rgb()}:" \
	              f"GrayText:rgb{rand_rgb()}:InactiveBorder:rgb{rand_rgb()}:Highlight:rgb{rand_rgb()}:" \
	              f"HighlightText:rgb{rand_rgb()}:InactiveBorder:rgb{rand_rgb()}:InactiveCaption:rgb{rand_rgb()}:" \
	              f"InactiveCaptionText:rgb{rand_rgb()}:InfoBackground:rgb{rand_rgb()}:InfoText:rgb{rand_rgb()}:" \
	              f"Menu:rgb{rand_rgb()}:MenuText:rgb{rand_rgb()}:Scrollbar:rgb{rand_rgb()}:" \
	              f"ThreeDDarkShadow:rgb{rand_rgb()}:ThreeDFace:rgb{rand_rgb()}:ThreeDHighlight:rgb{rand_rgb()}:" \
	              f"ThreeDLightShadow:rgb{rand_rgb()}:ThreeDShadow:rgb{rand_rgb()}:Window:rgb{rand_rgb()}:" \
	              f"WindowFrame:rgb{rand_rgb()}:WindowText:rgb{rand_rgb()}"
	# 除了 IE 才有 cpuClass，其它都要不了。写死算了……？
	raw_str1 = f"true###true###true###undefine###undefine###undefine###{match_plantform}###" \
	           f"{gen_fp_png_base64str(rect_col=rand_rgb(), txt_col1=rand_rgb(), txt_col2=rand_rgb())}###{css_sys_col}"
	# 语言和时区暂时保留不动。
	raw_str2 = f"{ua}###zh-CN###24###-480###{['1', ''][random.randint(0, 1)]}###{r2_const_suffix}"

	# 版本, 浏览器指纹, 随机三字符串||时间戳||随机三字符串, 主站
	inp = f"{'{'}'v':'v1.1'," \
	      f"'fp':'{netease_mmh32(raw_str1)},{netease_mmh32(raw_str2)}'," \
	      f"'u':'{_f(inject_str)}{int(time.time() * 1000)}{_f(inject_str)}'," \
	      f"'h':'music.163.com'{'}'}"
	del raw_str1, raw_str2
	return f'{inp}{netease_crc32(inp)}'
