__author__ = 'kisfg@hotmail.com'
__date__ = '2024/09 - 2025'
__license__ = 'GPL2.0-ONLY'
__description__ = "multtp: "                                               \
                  "\t包内的多种实现主要用于和后端交互。\n"                        \
                  "\tMultiple implementations defined in this package\n"    \
                  "\tare mainly used for network interaction.\n"
__all__ = [
	"getter",
	"poster",
	"gen_fake_browser_and_http_header",
	"alter_header",
]
from multtp.meths.header import gen_fake_browser_and_http_header, alter_header
from multtp.meths.man import getter, poster