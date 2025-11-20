from typing import Optional

from curl_cffi import Response

from misc_utils import *
from crypto_aux import netease_encryptor
from multtp.meths.man import poster

def play_records(
	conf: dict[str, int|str],
	num: int=1000, # ？神秘接口，一下拉1000？怎么实际后端又只传100？看来这里的值无法被控制
	ofs: int=0
) -> Optional[Response]:
	msp = 'https://music.163.com'
	api = f'{msp}/weapi/v1/play/record?csrf_token={conf["csrf_token"]}'
	payload = dic2ease_json_str({
		"uid"       : f"{conf['user-id']}",
		"type"      : "-1",
		"limit"     : f"{num}",
		"offset"    : f"{ofs}",
		"total"     : "true",
		"csrf_token": f"{conf['csrf_token']}"
	})
	alter_attrs = {
		"Content-Type"  : "application/x-www-form-urlencoded",
		"Origin"        : msp,
		"Referer"       : f"{msp}/user/home?{conf['user-id']}",
		"Cookie"        : f"{conf['cookie']}",
		"Sec-Fetch-Dest": "empty",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Site": "same-origin",
	}
	encryted_payload, _ = netease_encryptor(payload)
	return poster(
		url=api, payload=encryted_payload,
		alter_dict=alter_attrs
	)


def related_playlists(
	conf: dict[str, int|str],
	num: int=1001,
	ofs: int=0
) -> Optional[Response]:
	msp = "https://music.163.com"
	api = "/weapi/user/playlist?csrf_token=" + conf['csrf_token']
	alter_attrs = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Origin"      : msp,
		"Referer"     : f"{msp}/user/home?{conf['user-id']}",
		'Cookie'      : f"{conf['cookie']}",
	}
	payload = {
		"offset"    : f"{ofs}",
		"limit"     : f"{num}",
		"uid"       : f"{conf['user-id']}",
		"csrf_token": f"{conf['csrf_token']}"
	}
	encryted_payload, _ = netease_encryptor(dic2ease_json_str(payload))
	return poster(
		url=msp+api,
		payload=encryted_payload,
		alter_dict=alter_attrs
	)


if __name__ == '__main__':
	from pathlib import Path
	from configs.args_loader import PARSER

	_args = PARSER.parse_args()
	del PARSER
	dummy_conf = PRIVATE_CONFIG['netease'][_args.login_dummy]
	ret = play_records(dummy_conf, 10, 0)
	if ret is not None:
		Path(__file__).parent.joinpath('tmp.json').write_text(ret.text, encoding='utf-8')
		print('ret is not None')
	else:
		print('ret is None!')
	ret = related_playlists(dummy_conf, 10, 0)
	if ret is not None:
		Path(__file__).parent.joinpath('tmp.related.json').write_text(ret.text, encoding='utf-8')
		print('ret is not None')
	else:
		print('ret is None!')
