import json
import os.path

from utils.throw_err import die_if_err, throw_err_if_exist


@die_if_err
def load_config(inp: str) -> dict:
	payload_str: str = ''
	with open(inp, 'r') as fd:
		while True:
			flows: str = fd.read()
			if flows is None or len(flows) == 0:
				break
			payload_str += flows
	payload = json.loads(payload_str)
	return payload


@die_if_err
def load_json_from_str_or_die(inp: str) -> dict:
	return json.loads(inp)


@throw_err_if_exist
def load_json_from_str(inp: str) -> dict:
	return json.loads(inp)


CURR_DIR = os.path.dirname(__file__)
PRIVATE_CONFIG = load_config(CURR_DIR + '/./config.json')

if __name__ == "__main__":
	print(PRIVATE_CONFIG)
