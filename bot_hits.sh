#!/usr/bin/bash
# SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
# (c) Author: <kisfg@hotmail.com>
# windows 要用 schtasks
# update_config 的核心还没有实现，目前shell-script不可用!
py3=$(which python3)
curr_dir=$(pwd)
# TODO: log_path 可以留给 shell 设置，不一定要写死。
log_path="$curr_dir/static_assets/bot_hits.log"

function run_bot() {
	# shellcheck disable=SC2086
	$py3 -m multifn.update_song_list_cnt.py --author="$1" --dummy="$2" >> $log_path 2>&1
}


# function update_config() {
# 	echo "python program waits to do"
# }


function clean_crontab() {
	# 注意用空格隔开`， [ 和 ]。 
	# shellcheck disable=SC2046
	if [ $(crontab -l | grep -c "bot_hits"|| echo '0') -ne '0' ]; then
        # TODO: 这里竟然不是按参数删
		crontab -l | grep -v "bot_hits" | crontab
	fi
}


function write_to_crontab() {
	# 释义：每隔一天，在执行脚本的当天中每隔6分钟执行 run_bot.
	# 		每隔5天，在0点1分清除bot记录
	# 		每周日凌晨2点32修改config配置。
	echo -e "\
*/6 * */2 * * $curr_dir/${0##*/} run_bot $1 $2\n\
1 0 */5 * * /dev/null > $log_path\n\
32 2 * * 0 $curr_dir/${0##*/} update_config" | crontab # >> $exam_file
	crontab -l
}


function help() {
	echo "用法: $0 <函数名> <参数一> <参数二>"
	echo "可选参数: write_to_crontab, run_bot, clean_crontab, help"
	echo "无需带多余的引号"
	echo ""
	echo -e "\twrite_to_crontab <target-name> <dummy-name>: 将定时脚本写入crontab"
	echo -e "\trun_bot：运行bot"
	echo -e "\thelp: 帮助"
	echo -e "\tclean_crontab: 清除crontab"
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
