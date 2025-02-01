# ! /usr/bin/env python3
# -*- coding: utf8 -*-
# (c) Author: <kisfg@hotmail.com in 2025>
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
import argparse

PARSER = argparse.ArgumentParser(description='命令行参数解析器')

# 解析命令行参数
if __name__ == "__main__":
	args = PARSER.parse_args()
	print(args)
