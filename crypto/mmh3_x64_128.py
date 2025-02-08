_f = lambda x: x & 0xFFFF_FFFF
_g = lambda x: x & 0xFFFF

def x64Add(m: list[int], n: list[int]) -> list[int]:
	m = [_g(m[0] >> 16), _g(m[0]), _g(m[1] >> 16), _g(m[1])]
	n = [_g(n[0] >> 16), _g(n[0]), _g(n[1] >> 16), _g(n[1])]
	o = [0, 0, 0, 0]
	o[3] += m[3] + n[3]
	o[2] += o[3] >> 16
	o[3] = _g(o[3])
	o[2] += m[2] + n[2]
	o[1] += o[2] >> 16
	o[2] = _g(o[2])
	o[1] += m[1] + n[1]
	o[0] += o[1] >> 16
	o[1] = _g(o[1])
	o[0] += m[0] + n[0]
	o[0] = _g(o[0])
	return [_f((o[0] << 16) | o[1]), _f((o[2] << 16) | o[3])]


def x64Mul(m: list[int], n: list[int]) -> list[int]:
	m = [_g(m[0] >> 16), _g(m[0]), _g(m[1] >> 16), _g(m[1])]
	n = [_g(n[0] >> 16), _g(n[0]), _g(n[1] >> 16), _g(n[1])]
	o = [0, 0, 0, 0]
	o[3] += m[3] * n[3]
	o[2] += o[3] >> 16
	o[3] = _g(o[3])
	o[2] += m[2] * n[3]
	o[1] += o[2] >> 16
	o[2] = _g(o[2])
	o[2] += m[3] * n[2]
	o[1] += o[2] >> 16
	o[2] = _g(o[2])
	o[1] += m[1] * n[3]
	o[0] += o[1] >> 16
	o[1] = _g(o[1])
	o[1] += m[2] * n[2]
	o[0] += o[1] >> 16
	o[1] = _g(o[1])
	o[1] += m[3] * n[1]
	o[0] += o[1] >> 16
	o[1] = _g(o[1])
	o[0] += (m[0] * n[3]) + (m[1] * n[2]) + (m[2] * n[1]) + (m[3] * n[0])
	o[0] = _g(o[0])
	return [_f((o[0] << 16) | o[1]), _f((o[2] << 16) | o[3])]


def x64LRot(a: list[int], b: int) -> list[int]:
	b &= 0x3F	
	if b == 32:
		return [a[1], a[0]]
	elif b < 32:
		return [_f((a[0] << b) | a[1] >> (32 - b)), _f((a[1] << b) | a[0] >> (32 - b))]
	else:
		b -= 32
		return [_f((a[1] << b) | a[0] >> (32 - b)), _f((a[0] << b) | a[1] >> (32 - b))]


def x64LS(a: list[int], b: int) -> list[int]:
	b &= 0x3F
	if b == 0:
		return a
	if b < 32:
		return [_f((a[0] << b) | a[1] >> (32 - b)), _f(a[1] << b)]
	return [_f(a[1] << (b - 32)), 0]


def x64Xor(a: list[int], b: list[int]) -> list[int]:
	return [a[0] ^ b[0], a[1] ^ b[1]]


def x64Fmix(a: list[int]) -> list[int]:
	# 无符号右移？
	a = x64Xor(a, [0, _f(a[0] >> 1)])
	a = x64Mul(a, [0xff51afd7, 0xed558ccd])
	a = x64Xor(a, [0, _f(a[0] >> 1)])
	a = x64Mul(a, [0xc4ceb9fe, 0x1a85ec53])
	return x64Xor(a, [0, _f(a[0] >> 1)])


def _to_hex(a: int) -> str:
	return hex(_f(a))[2:].zfill(8)

def mmh3_x64_128(key: str, seed: int = 0):
	ed = len(key)
	remainder = ed & 0x0F
	divided = ed - remainder
	h1, h2 = [0, seed], [0, seed]
	c1, c2 = [0x87c37b91, 0x114253d5], [0x4cf5ad43, 0x2745937f]
	f = lambda x: ord(x) & 0xFF
	g = lambda x, y: x << (8 * y)
	h = lambda x, _i: f(x[_i]) | g(f(key[_i + 1]), 1) | g(f(key[_i + 2]), 2) | g(f(key[_i + 3]), 3)
	for i in range(0, divided, 16):
		k1 = [h(key, i + 4), h(key, i)]
		k2 = [h(key, i + 12), h(key, i + 8)]

		k1 = x64Mul(k1, c1)
		k1 = x64LRot(k1, 31)
		k1 = x64Mul(k1, c2)
		h1 = x64Xor(h1, k1)

		h1 = x64LRot(h1, 27)
		h1 = x64Add(h1, h2)
		h1 = x64Add(x64Mul(h1, [0, 5]), [0, 0x52dce729])

		k2 = x64Mul(k2, c2)
		k2 = x64LRot(k2, 33)
		k2 = x64Mul(k2, c1)
		h2 = x64Xor(h2, k2)

		h2 = x64LRot(h2, 31)
		h2 = x64Add(h2, h1)
		h2 = x64Add(x64Mul(h2, [0, 5]), [0, 0x38495ab5])

	k1, k2 = [0, 0], [0, 0]
	while remainder != 0:
		cur = [0, f(key[remainder-1+divided])]
		if 9 < remainder < 16:
			k2 = x64Xor(k2, x64LS(cur, (remainder - 9) * 8))
			remainder -= 1
			continue
		elif 1 < remainder < 9:
			k1 = x64Xor(k1, x64LS(cur, (remainder - 1) * 8))
			remainder -= 1
			continue
		elif remainder == 9:
			k2 = x64Xor(k2, cur)
			k2 = x64Mul(k2, c2)
			k2 = x64LRot(k2, 33)
			k2 = x64Mul(k2, c1)
			h2 = x64Xor(h2, k2)
			remainder -= 1
			continue
		elif remainder == 1:
			k1 = x64Xor(k1, cur)
			k1 = x64Mul(k1, c1)
			k1 = x64LRot(k1, 31)
			k1 = x64Mul(k1, c2)
			h1 = x64Xor(h1, k1)
			break

	h1 = x64Xor(h1, [0, ed])
	h2 = x64Xor(h2, [0, ed])

	h1 = x64Add(h1, h2)
	h2 = x64Add(h2, h1)

	h1 = x64Fmix(h1)
	h2 = x64Fmix(h2)

	h1 = x64Add(h1, h2)
	h2 = x64Add(h2, h1)
	return f'{_to_hex(h1[0])}{_to_hex(h1[1])}{_to_hex(h2[0])}{_to_hex(h2[1])}'


if __name__ == "__main__":
	print(mmh3_x64_128("PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
					   "Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
					   "Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
					   "Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf~"
					   "WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf"))

	print(mmh3_x64_128("卧槽马绝杀"))
