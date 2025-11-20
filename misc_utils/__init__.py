# Last modified at 2025/10/25 星期六 22:08:47
__author__ = 'kisfg@hotmail.com'
__develop_time_range__ = '2024/09 - 2025'
__license__ = 'GPL2.0-ONLY'
__all__ = [
	# alg/diff_calc
	"DiffOp",
	"myers_diff_comparer",

	# time_aux
	"US_TIME_FORMAT",
	"UNDERSCORE_FORMAT",
	"LOG_TIME_FORMAT",
	"unix_time",
	"unix_ms",
	"unix_us",
	"unix_sec",
	"unix_ts_to_time",
	"funix_ms",
	"funix_us",
	"unix_ms_of_next_year",
	"curr_time_formatter",

	# str_aux
	"dic2ease_json_str",
	"streplacer",
	"strip_underscore",
	"strip_space",

	# logger
	"GLOB_LOG_FORMAT",
	"GLOB_MAIN_LOG_PATH",
	"GLOB_TEST_LOG_PATH",
	"GLOB_BOT_LOG_PATH",

	# json/conf_reader
	"PRIVATE_CONFIG",
	"load_json_from_str",
	"deserialize_json_or_die",

	# file_opeartor
	"write_in_given_mode",
	"is_path_ok",
	"unsafe_read_text",
	"load_txt_via_file_or_die",

	# wrappers/
	"die_if_err",
	"seize_err_if_any",
	"get_interval",
	"eq_check",
	"eq_check_after_time_gauge",
	# opts/db/sqlite
	"DBfd"
]
from .algs.diff_calc import DiffOp, myers_diff_comparer

from .logger import (
	GLOB_LOG_FORMAT,
	GLOB_MAIN_LOG_PATH,
	GLOB_TEST_LOG_PATH,
	GLOB_BOT_LOG_PATH
)

from .str_aux import (
	dic2ease_json_str, streplacer,
	strip_space, strip_underscore
)

from .time_aux import (
	US_TIME_FORMAT, UNDERSCORE_FORMAT,
	LOG_TIME_FORMAT, unix_time,
	unix_ms, unix_us,
	unix_sec, unix_ts_to_time,
	funix_ms, funix_us,
	unix_ms_of_next_year, curr_time_formatter
)

from .wrappers.err_wrap import seize_err_if_any, die_if_err
from .wrappers.logic_wrap import eq_check, eq_check_after_time_gauge
from .wrappers.perf_wrap import get_interval

from .file_operator import (
	write_in_given_mode, is_fpath, is_path_ok,
	unsafe_read_text, load_txt_via_file_or_die
)


from .opts.json.conf_reader import (
	PRIVATE_CONFIG,
	load_json_from_str,
	deserialize_json_or_die,
)
from .opts.db.sqlite import DBfd