#!/usr/bin/env/bash
# update_config 的核心还没有实现，目前shell-script不可用!

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

py3=$(which python3)
curr_dir=$(pwd)
# TODO: log_path 可以留给 shell 设置，不一定要写死。
# 不过还是建议不要和 songs_list_info.py 分开。
log_path="$curr_dir/static_assets/bot_hits.log"

function run_bot() {
	# shellcheck disable=SC2086
	$py3 -m multifn.update_song_list_cnt.py --author="$1" --dummy="$2" >> $log_path 2>&1
}

# cookie 一般设成一年，所以应该不用实现？
# 但是一个配置疑似最多能用一周，没找到接口更新信息前，仍需要实现。
# function update_config() {
# 	echo "python program waits to do"
# }


function clean_crontab() {
	# 注意用空格隔开`， [ 和 ]。 
	# shellcheck disable=SC2046
	if [ $(crontab -l | grep -c "bot_hits" || echo '0') -ne '0' ]; then
        # TODO: 这里不是按参数删
		crontab -l | grep -v "bot_hits" | crontab
	fi
}


function write_to_crontab() {
	# 释义：每隔一天，在执行脚本的当天中每隔6分钟执行 run_bot.
	# 		每隔5天，在0点1分清除bot记录
	# 		每周日凌晨2点32修改config配置。
	echo -e "\
*/6 * */2 * * $curr_dir/${0##*/} run_bot $1 $2\n\
1 0 */5 * * /usr/bin/env/cat /dev/null > $log_path\n\
32 2 * * 0 $curr_dir/${0##*/} update_config" | crontab
	crontab -l
}


function help() {
	echo "用法: $0 <函数名> <参数一> <参数二>"
	echo "可选参数: write_to_crontab, run_bot, clean_crontab, help"
	echo "无需带多余的引号"
	echo ""
	echo -e "\twrite_to_crontab <target-name> <dummy-name>: 将定时脚本写入crontab"
	echo -e "\trun_bot <author> <dummy>: 运行bot"
	echo -e "\thelp: 帮助"
	echo -e "\tclean_crontab: 清除crontab" # TODO: 按参数删除参数所在行以及紧接的两行
}


if [ -z "$1" ]; then
	help
	exit 1
fi

func_name=$1
shift

if declare -F "$func_name" > /dev/null; then
	"$func_name" "$@"
else
	"help"
	exit 1
fi
