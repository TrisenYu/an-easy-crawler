# SPDX-LICENSE-IDENTIFIER: GPL2.0ONLY
# (c) author: <kisfg@hotmail.com 2025>

CC=gcc
flags=-shared -m64
ifeq ($(OS),Windows_NT)
	target=mmh3_x64_128_win.dll
    clang_test=-$(shell clang --version)
else
	target=mmh3_x64_128.so
    clang_test=$(shell clang --version 2>&1)
endif

ifdef clang_test
    CC=clang
else
    flags+=-fPIC
endif

dynamico:
	$(CC) $(flags) mmh3_x64_128.c -o $(target)
