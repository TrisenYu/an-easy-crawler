#! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2024,2025>
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
"""
b1x.cbO6I = function() {
    t1x.be1x("/api/web/qrcode/get", {
        method: "POST",
        type: "json",
        data: j1x.cr1x({
            url: window.location.href,
            size: 180
        }),
        onload: function(i1x) {
            if (i1x.code == 200) {
                this.cbG6A(i1x.qrcodeImageUrl)
            } else {
                alert("二维码获取失败")
            }
        }
        .f1x(this)
    })
}
"""