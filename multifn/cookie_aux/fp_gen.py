from crypto.unk_hash import unk_hash2
import random

def just_crack_fp_for_wmdev() -> str:
	payload = ''
	# 收到 200 之后还有个 672 的。
	for _ in range(469+138+29):
		payload += chr(random.randint(0, 255))
	return unk_hash2(payload)


if __name__ == "__main__":
	print(len(just_crack_fp_for_wmdev()))