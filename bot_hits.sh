#!/usr/bin/env zsh
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# (c) Author: <kisfg@hotmail.com>
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
# 这里动一下会影响 songlist_hit_bot.py 的执行
#
set -ue
py3=`which python3`
sh_name="$0"

# shellcheck disable=SC2181
[[ $? != 0 ]] && { echo "系统似乎没有python"; exit 1; }

curr_dir=`pwd`
log_path="$curr_dir/static_assets/bot_hits.log"
ref_path="$curr_dir/static_assets/bot_refs.log"
func_name=""
dummy=""
renew_dummy=""
songlist=""

function help() {
	cat >&2 << END_OF_INFO
usages    := $sh_name -f <func-name> optional-for-specific-func<-l||-r||-s||-d||-n>(corresponding-value)
           | $sh_name -h

func-name := modify_crontab 
           | run_bot 
           | update_config
           | clean_crontab
           | help
           | self_validate

examples  := $sh_name -f run_bot -s user1 -d user1
           | $sh_name -h

# modify_crontab <target-songslist-refname> <dummy-refname>: 将定时脚本写入crontab
# run_bot <-s, target-songslist-refname> <-d, dummy-refname>: 运行bot
# update_config <-n, dummy-for-renew-refname>: 更新dummy的token
# self_validate: 计算此脚本的sha256值
# help: 帮助
# clean_crontab: 清除crontab
END_OF_INFO
}

opts=`\
getopt \
-o h::f:l::r::s::d::n:: \
--long help::,func-name:,log-path::,ref-path::,songslist::,dummy::,renew-dummy::, \
-- "$@"
`
# shellcheck disable=SC2181
if [[ $? != 0 ]]; then
	echo "意外！解析选项失败！"
	exit 1
fi

function parse_options() {
	eval set -- "$opts"
	while true; do
		case "$1" in
		-d|--dummy)
			dummy=$2
			shift 2
			;;
		-s|--songlist)
			songlist=$2
			shift 2
			;;
		-f|--func-name)
			func_name=$2
			shift 2
			;;
		-l|--log-path)
			log_path=$2
			shift 2
			;;
		-r|--ref-path)
			ref_path=$2
			shift 2
			;;
		-h|--help)
			"help"
			exit 0
			;;
		-n|--renew-dummy)
			renew_dummy=$2
			shift 2
			;;
		--)
			break
			;;
		*)
			echo ""
			"help"
			exit 1
			;;
		esac
	done
}

function validator() {
	trusted_list=(
		'modify_crontab'
		'update_config'
		'run_bot'
		'help'
		'self_validate'
	)
	terminated=true
	for a in "${trusted_list[@]}"; do
		[[ "$func_name" != "$a" ]] && continue
		terminated=false
		break
	done
	[ $terminated = false ] && return
	echo "参数有误"
	"help"
	exit 1
}

function run_bot() {
	# shellcheck disable=SC2086
	$py3 -m multifn.songlist_hit_bot \
		 --author="$songlist" \
		 --dummy="$dummy" \
	&>> "$log_path"
}

# TODO: 好像不管用，还是需要换 cookie
function update_config() {
	$py3 -m multifn.refresh_token \
		 --refresh-dummy="$renew_dummy" \
	&>>"$ref_path"
}

# $1: songslist-refname
# $2: dummy-refname
function clean_crontab() {
	# shellcheck disable=SC2046
	[ `crontab -l | grep -c "bot_hits" || echo '0'` -ne '0' ] && \
	crontab -l | sed "/$1 $2/,+2d" | crontab
	# 筛掉 run_bot $1 $2 以及底下两行。
}


# echo 所做操作：
# 	每隔一天，在执行脚本的当天中每隔6分钟执行run_bot.
# 	每隔5天，在0点1分清除bot记录
# 	每周日凌晨2点32更新token。
# $1: songslist-refname
# $2: dummy-refname
function modify_crontab() {
	echo -e "\
*/6 * */2 * * cd $curr_dir && /usr/bin/bash $curr_dir/${0##*/} -f run_bot -s $1 -d $2\n\
1 0 */5 * * /usr/bin/cat /dev/null > $log_path\n\
32 2 * * 0 cd $curr_dir &&/usr/bin/bash $curr_dir/${0##*/} -f update_config -n $2" | crontab
	crontab -l
}

function self_validate() {
	sha256sum "$sh_name" | awk -F' ' '{ print $1 }'
	exit 0
}

############################### shell entry ###############################
"parse_options" "$@"
"validator"
"$func_name" "$@"
