#!/usr/bin/env zsh
# -*- coding: utf-8 -*-
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# (c) Author: <kisfg@hotmail.com, 2025>
# Last modified at 2025/10/04 星期六 21:56:20
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

# 单行最大字符数不超过100

# 这里每次动一下会影响 songslist_hit_bot.py 的执行
# 有没有为了防止AI用源代码训练而直接加不可见字符又不影响人阅读的可能？
# 需要测试该脚本
set -e
sh_name="$0"
hash_val=$(sha256sum "$sh_name" | awk -F' ' '{ print $1 }') # 不care成功与否
version_numno="bot_hits.sh v1.0.3-$hash_val"

function deps_check() {
	py3=$(which python3)
	# shellcheck disable=SC2181
	if [[ $? != 0 ]]; then
		cat <<END_OF_LINE
系统似乎没有python，建议是
对于windows
	下载uv以方便python的版本管理
对于linux发行版
	debian系
		sudo apt install python3 python3-dev
	arch系
		sudo pacman -Sy python3 python3-dev
	其余系类似
对于mac
	brew install python3
END_OF_LINE
		exit 1
	fi
	uv_check=$(which uv)
	if [[ $? != 0 ]]; then
		cat << END_OF_LINE
似乎没有下载uv以管理环境。
END_OF_LINE
		exit 1
	fi
}


### 默认参数 ======================================================
"deps_check"
curr_dir=$(readlink -f $0)
curr_dir=$(dirname $curr_dir)
bot_src_dir="$curr_dir/multifn"
init_logdir="$curr_dir/assets/stat"

# TODO: 建议多dummy执行时对应存放或改用数据库
logging_path="$init_logdir/bot_hits.log"
refresh_path="$init_logdir/bot_refr.log"
func_name=''
dummy=''
refr_dummy=''
songslist=''

ggetopt="getopt"
gsed="sed"
ggrep='grep'
if [[ "`uname -o`" == "Darwin" ]]; then
	# 还是假定用这个脚本的人至少是懂装brew的
	brew install gnu-getopt gnu-sed
	ggetopt="/opt/homebrew/opt/gnu-getopt/bin/getopt"
	gsed="gsed"
	ggrep='ggrep'
fi


opts=`\
	$ggetopt -o h::f::l::r::s::d::n::v::b:: \
	--long help::,func-name::,logg-path::,refr-path::,songslist::,dummy::,refr-dummy::,version::,bot-src-dir:: \
	-- "$@" \
`
# shellcheck disable=SC2181
[[ $? != 0 ]] && {
	echo '意外！解析选项失败！'
	exit 1
}

### 函数声明 ======================================================
# TODO: 加入检查。检查必要的函数，缺乏则尝试下载。首先需要检查不同发行版下使用的包管理器
# "check_cmd"

# 帮助
function help() {
	# >&2  标准输出定向到标准错误输出
	cat << END_OF_INFO
usages   := $sh_name -f<函数名> <可选入参: -l,-r,-s,-d,-n>(附带对应值)
          | $sh_name -h
          | $sh_name -v

func-name:= write2crontab
          | boot
          | refresh_token
          | clean_crontab
          | help
          | self_validate

examples := $sh_name -fboot -suser1 -duser1
          | $sh_name -frefresh_token -nuser1 -r /abs/path/to/ref/file
          | $sh_name -fclean_crontab -suser1 -duser1
          | $sh_name -fself_validate
          | $sh_name -fhelp
          | $sh_name -h
          | $sh_name -v
          | $sh_name --func-name=boot --songslist=user1 --dummy=user1
          | $sh_name --func-name=refresh_token -l/abs/path/to/log/file
          | $sh_name --func-name=clean_crontab --songslist=user1 --dummy=user1
          | $sh_name --func-name=self_validate
          | $sh_name --func-name=help
          | $sh_name --help
          | $sh_name --version

details  := write2crontab <-s, songslist-refname> <-d, dummy-refname>: 将定时脚本写入crontab
          | boot          <-s, songslist-refname> <-d, dummy-refname>: 运行bot
          | refresh_token <-n, dummy-for-refreshing-refname>:          更新dummy的token
          | self_validate:                                             计算此脚本的sha256值
          | help:                                                      帮助
          | clean_crontab:                                             清除crontab
          |
          | refresh-path(refresh-path) 默认指向  ./assets/stat/bot_refr.log
          | logging-path(hit-logg-path) 默认指向 ./assets/stat/bot_hits.log
          |
          | 因该脚本协同multifn/songslist_hit_bot.py一起使用，且脚本自身的sha256为
          | songslist_hit_bot.py所硬编码。因此脚本内假定脚本与songslist_hit_bot.py的相对位置不变。
          | 一旦脚本本身出现任何修改，则会直接影响到songslist_hit_bot.py中remedy_for_post_crash的执行。
          | 相对位置关系具体以 bot_src_dir 变量保持。如果需要变更，则必须要提供 -b 参数。
          | 如仍不理解，建议阅读本脚本源码中的函数self_validate。
END_OF_INFO
}

function parse_options() {
	eval set -- "$opts"
	while true; do
		case "$1" in
		-f|--func-name)
			func_name=$2
			shift 2
			;;
		-s|--songslist)
			songslist=$2
			shift 2
			;;
		-d|--dummy)
			dummy=$2
			shift 2
			;;
		-n|--refr-dummy)
			refr_dummy=$2
			shift 2
			;;
		-b|--bot-src-dir)
			bot_src_dir=$2
			shift 2
			;;
		-l|--logg-path)
			logging_path=$2
			shift 2
			;;
		-r|--refr-path)
			refresh_path=$2
			shift 2
			;;
		-h|--help)
			"help"
			exit 0
			;;
		-v|--version)
			echo "$version_numno"
			shift 2
			exit 0
			;;
		--)
			break
			;;
		*)
			echo ''
			"help"
			exit 1
			;;
		esac
	done
}

# TODO: sync information in certain songslist
# deps: grasp the whole logic for generating cookie...
#		and corresponding counteractive methods

function validator() {
	trusted_list=(
		'write2crontab'
		'refresh_token'
		'boot'
		'help'
		'self_validate'
	)
	terminated=true
	for a in "${trusted_list[@]}"; do
		[[ "$func_name" != "$a" ]] && continue
		terminated=false
		break
	done
	# 检查 bot-src-dir 一定包含 songslist_hit_bot.py和refresh_token且内部存在bot_hit函数。

	[[ $terminated = false ]] && return
	echo '参数有误'
	"help"
	exit 1
}

function boot() {
	given_path=${logging_path%/*}
	[[ ! -d "$given_path" ]] && mkdir -p "$given_path"
	if [[ "$songslist" = '' || "$dummy" = '' ]]; then
		echo '参数 songslist 或 dummy 缺失' | tee -a "$logging_path"
		return
	fi
	# shellcheck disable=SC2086
	$py3 -m multifn.songslist_hit_bot \
		--author="$songslist" \
		--dummy="$dummy" \
		&>> "$logging_path"
}

# TODO: 好像不管用，还是需要换 cookie
function refresh_token() {
	given_path=${refresh_path%/*}
	[[ ! -d "$given_path" ]] && mkdir -p "$given_path"
	if [[ "$refr_dummy" = '' ]]; then
		echo '参数 refr_dummy 缺失' | tee -a "$refresh_path"
		return
	fi
	$py3 -m multifn.refresh_token \
		--refresh-dummy="$refr_dummy" \
		&>> "$refresh_path"
}

function clean_crontab() {
	# shellcheck disable=SC2046
	[[ $(crontab -l | $ggrep -c 'bot_hits' || echo '0') -ne '0' ]] && \
	crontab -l | $gsed "/-fboot -s$songslist -d$dummy/,+2d" | crontab
	# sed: 筛掉 -f boot -s $1 -d $2 以及底下两行。
}

# echo 所做操作：
# 	每隔一天，在执行脚本的当天中每隔6分钟执行 boot.
# 	每隔5天，在0点1分清除bot记录
# 	每周日凌晨2点32更新token。
# TODO: 考虑把时间选项抽取出来供配置使用
#		不然每次都要到crontab里改还是比较繁琐的
function write2crontab() {
	echo -e "\
*/6 * */2 * * cd $curr_dir && /usr/bin/zsh $curr_dir/${0##*/}\
 -fboot -s$songslist -d$dummy\n\
1   0 */5 * * /usr/bin/cat /dev/null > $logging_path\n\
32  2  *  * 0 cd $curr_dir && /usr/bin/zsh $curr_dir/${0##*/}\
 -frefresh_token -n$dummy" | tee -a a.txt # crontab
	crontab -l
}

function self_validate() {
	echo "$hash_val"
	bot_src='songslist_hit_bot.py'
	bot_src_path="$bot_src_dir/$bot_src"
	if [[ ! -f "$bot_src_path" ]]; then
		echo "$bot_src_path 疑似无效"
		exit 1
	fi
	# 这里和自动点击程序的实现逻辑绑定
	py_code_seg='flag = len\(inp\) != 0 and sha256\(inp'
	src_hash=$(
		awk "/$py_code_seg/{ getline; print }" "$bot_src_path" |
		awk -F'"' '{ print $2 }'
	)
	if [[ "$src_hash" = '' ]]; then
		echo "所提供的 $bot_src_dir 疑似无效"
		exit 1
	fi
	[[ "$hash_val" = "$src_hash" ]] && return
	# 直接替换
	$gsed -i "s/$src_hash/$hash_val/g" "$bot_src_path"
	exit 0
}

### shell入口 ===================================================
"parse_options" "$@"
"validator"

# 目前调的都是multifn模块，所以只需将 bot_hits.sh 所在目录提供给sys.path
# export PYTHONPATH="$bot_src_dir:$PYTHONPATH"
# 先检查有没有虚拟环境
[ ! -f "$curr_dir/.venv/bin/python" ] && uv venv
source "$curr_dir/.venv/bin/activate"
uv sync
py3="$curr_dir/.venv/bin/python"
set -u
"$func_name"
