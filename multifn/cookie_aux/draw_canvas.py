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
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from base64 import b64encode
from utils.wrappers.err_wrap import throw_err_if_any

"""
canvas 生成过程：
	创建一个大小为 300 × 150 的空白画布调整待显示文字的基线，然后上色画出（文字可以超出边界）
	再在两个不同位置(？)涂上不同颜色的色块。
	okk = getContext('2d')
	okk.fontsize: 70px Arial
	okk.textbaseline: alphabetic
	okk.fillRect (125, 1, 62, 20) # 长方形填充。
	okk.fillstype: #069
	okk.fillText(2, 15)           # 两次文本填充上不同颜色而形成层次。
	okk.fillstyle: rgba(102, 204, 0, 0.7)
	okk.fillText(4, 17)
	canvas.toDataURL()
"""


@throw_err_if_any
def gen_fp_png_base64str(
	rect_pos: tuple[int, int, int, int] = (125, 1, 187, 20),
	rect_col: tuple[int, int, int] = (0xFF, 0x66, 0x00),
	txt_col1: tuple[int, int, int] = (0, 0x66, 0x99),
	txt_col2: tuple[int, int, int] = (0x66, 0xCC, 0)
) -> str:
	"""
	TODO: 看后面随机数取代原生实现的检测。
	:param rect_pos: (x0, y0, x1, y1) 四个点确定矩形在图中的位置。
	:param rect_col: 矩形颜色。
	:param txt_col1: 文本首次上色的颜色。
	:param txt_col2: 文本第二次上色的颜色。
	"""
	txt = 'mwC nkbafjord phsgly exvt zqiu, ὠ tphst/:/uhbgtic.mo/levva'
	img = Image.new(mode="RGB", size=(300, 150), color='white')
	draw_canvas = ImageDraw.Draw(img, mode='RGB')
	font = ImageFont.truetype('arial', 70, encoding='utf-8')
	draw_canvas.rectangle(((rect_pos[0], rect_pos[1]), (rect_pos[2], rect_pos[3])), fill=rect_col, outline=rect_col)
	# -65，我也不清楚为什么要变成这样。一定是没有调好 alphabetic 所导致的。
	draw_canvas.text((2, 15 - 65), txt, font=font, fill=txt_col1)
	draw_canvas.text((4, 17 - 65), txt, font=font, fill=txt_col2)
	del draw_canvas
	mem_obj = BytesIO()
	img.save(mem_obj, format='png')
	del img
	img_str = b64encode(mem_obj.getvalue()).decode('iso-8859-1')
	return f'data:image/png;base64,' + img_str


if __name__ == "__main__":
	print(gen_fp_png_base64str())
