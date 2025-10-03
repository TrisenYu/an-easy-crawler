# SPDX-LICENSE-IDENTIFIER: GPL2.0ONLY
# (c) author: <kisfg@hotmail.com 2025>

CC=gcc
flags=-shared -m64 -O3
target=mmh3_x64_128_win
ifeq ($(OS),Windows_NT)
	target+=.dll
    clang_test=-$(shell clang --version)
else
	target+=.so
    clang_test=$(shell clang --version &> /dev/null)
endif

ifdef clang_test
    CC=clang
else
    flags+=-fPIC
endif

dynamico:
	$(CC) $(flags) mmh3_x64_128.c -o $(target)
