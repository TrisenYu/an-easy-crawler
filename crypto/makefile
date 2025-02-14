# SPDX-LICENSE-IDENTIFIER: GPL2.0ONLY
# (c) author: <kisfg@hotmail.com 2025>

ifeq ($(OS),Windows_NT)
	target=mmh3_x64_128_win.dll
else
	target=mmh3_x64_128.so
endif

dynamico:
	gcc -fPIC -shared -m64 mmh3_x64_128.c -o $(target)
