# Last modified at 2025/10/25 星期六 22:09:18
# create __init__ for unix system.
# TODO: 如果后续专门做其它网站的密码学逆向工程，这里也要相应用结构化的方法来调用
__author__ = 'kisfg@hotmail.com'
__date__ = '2024/09 - 2025'
__license__ = 'GPL2.0-ONLY'
__description__ = "非侧信道防护级的密码学辅助库，目前只有加密与哈希。\n" \
                  "This package currently only implementes incomprehensive\n" \
                  "encryption functions and hash functions. Further more,\n"  \
                  "the package might be weak at side-channel attack."
__all__ = [
    "ran_str_gen",
    "encSecKey_gen",
    "base64_str_gen",
    "dilphabet_16_str_gen",
    "dilphabet_32_str_gen",
    "encText_gen",
    "netease_encryptor",
    "sm4_encryptor",
    "rsa_encrypt_without_token",
    "netease_md5",
    "netease_crc32",
    "netease_mmh32_checksum",
    "netease_mmh32",
    "netease_mmh128",
    "sha256",
	# js interpreter
    "native_encSecKey_gen",
    "native_encText_gen",
    "native_netease_encryptor",
    "native_sm4_encryptor",
    "native_rsa_encrypt_without_token",
    "native_md5",
    "raw_mmh3",
    "native_wm_nike_gen"
]
from .native_js import *
from .manual_deobfus import *