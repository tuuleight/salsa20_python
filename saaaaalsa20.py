import os

def rot_left(x, y):
	return ((x << y) % (2**32-1))


# 3 the quarterround function
def quarterround(y):
	assert len(y) == 4
	z = [0] * 4		
	z[1] = y[1] ^ rot_left(((y[0] +y[3]) % 2**32), 7)
	z[2] = y[2] ^ rot_left(((z[1] +y[0]) % 2**32), 9)
	z[3] = y[3] ^ rot_left(((z[2] +z[1]) % 2**32), 13)
	z[0] = y[0] ^ rot_left(((z[3] +z[2]) % 2**32), 18)
	return z

robo_quarter = [0x00000001, 0x00000000, 0x00000000, 0x00000000]
assert quarterround(robo_quarter) == [0x08008145, 0x00000080, 0x00010200, 0x20500000]


# 4 The rowround function

def rowround(y):
	assert len(y) == 16
	z = [0] * 16
	z[0], z[1], z[2], z[3] = quarterround([y[0], y[1], y[2], y[3]])
	z[5], z[6], z[7], z[4] = quarterround([y[5], y[6], y[7], y[4]])
	z[10], z[11], z[8], z[9] = quarterround([y[10], y[11], y[8], y[9]])
	z[15], z[12], z[13], z[14] = quarterround([y[15], y[12], y[13], y[14]])
	return z

robo_rowround = [0x08521bd6, 0x1fe88837, 0xbb2aa576, 0x3aa26365,
                0xc54c6a5b, 0x2fc74c2f, 0x6dd39cc3, 0xda0a64f6,
                0x90a2f23d, 0x067f95a6, 0x06b35f61, 0x41e4732e,
                0xe859c100, 0xea4d84b7, 0x0f619bff, 0xbc6e965a]

assert rowround(robo_rowround) == [0xa890d39d, 0x65d71596, 0xe9487daa, 0xc8ca6a86,
                                   0x949d2192, 0x764b7754, 0xe408d9b9, 0x7a41b4d1,
                                   0x3402e183, 0x3c3af432, 0x50669f96, 0xd89ef0a8,
                                   0x0040ede5, 0xb545fbce, 0xd257ed4f, 0x1818882d]


# 5 The columnround function

def columnround(x):
	assert len(x) == 16
	y = [0] * 16
	y[0], y[4], y[8], y[12] = quarterround([x[0], x[4], x[8], x[12]])
	y[5], y[9], y[13], y[1] = quarterround([x[5], x[9], x[13], x[1]])
	y[10], y[14], y[2], y[6] = quarterround([x[10], x[14], x[2], x[6]])
	y[15], y[3], y[7], y[11] = quarterround([x[15], x[3], x[7], x[11]])
	return y

robo_columnround = [0x08521bd6, 0x1fe88837, 0xbb2aa576, 0x3aa26365,
                    0xc54c6a5b, 0x2fc74c2f, 0x6dd39cc3, 0xda0a64f6,
                    0x90a2f23d, 0x067f95a6, 0x06b35f61, 0x41e4732e,
                    0xe859c100, 0xea4d84b7, 0x0f619bff, 0xbc6e965a]

assert columnround(robo_columnround) == [0x8c9d190a, 0xce8e4c90, 0x1ef8e9d3, 0x1326a71a,
                                         0x90a20123, 0xead3c4f3, 0x63a091a0, 0xf0708d69,
                                         0x789b010c, 0xd195a681, 0xeb7d5504, 0xa774135c,
                                         0x481c2027, 0x53a8e4b5, 0x4c1f89c5, 0x3f78c9c8]


# 6 The doubleround function

def doubleround(x):
	return rowround(columnround(x))


# 7 the littleendian function

def littleendian(b):
	assert len(b) == 4
	return b[0] ^ (b[1] << 8) ^ (b[2] << 16) ^ (b[3] << 24)

assert littleendian([86, 75, 30, 9]) == 0x091e4b56
assert littleendian([255, 255, 255, 250]) == 0xfaffffff


def littleendian_invert(w):
	return [w & 0xff, (w >> 8) & 0xff, (w >> 16) & 0xff, (w >> 24) & 0xff]

assert littleendian_invert(0x091e4b56) == [86, 75, 30, 9]
assert littleendian_invert(0xfaffffff) == [255, 255, 255, 250]


# 8 The Salsa20 hash function

def salsa_20(x):
	_x = [0] * 16
	i = 0
	k = 0
	while i < 16:
		_x[i] = littleendian([x[k], x[k+1], x[k+2], x[k+3]])
		k += 4
		i+=1

	z = _x
	for j in range(10):
		z = doubleround(z)

	y = []
	for i in range(16):
		w = z[i] + _x[i]
		y.append(w & 0xff)
		y.append((w >> 8) & 0xff)
		y.append((w >> 16) & 0xff)
		y.append((w >> 24) & 0xff)

	return y


robo_salsa20 = [211,159, 13,115, 76, 55, 82,183, 3,117,222, 37,191,187,234,136,
                49,237,179, 48, 1,106,178,219,175,199,166, 48, 86, 16,179,207,
                31,240, 32, 63, 15, 83, 93,161,116,147, 48,113,238, 55,204, 36,
                79,201,235, 79, 3, 81,156, 47,203, 26,244,243, 88,118,104, 54]


assert salsa_20(robo_salsa20) == [109, 42,178,168,156,240,248,238,168,196,190,203, 26,110,170,154,
29, 29,150, 26,150, 30,235,249,190,163,251, 48, 69,144, 51, 57,
118, 40,152,157,180, 57, 27, 94,107, 42,236, 35, 27,111,114,114,
219,236,232,135,111,155,110, 18, 24,232, 95,158,179, 19, 48,202]


# 9 The Salsa20 expansion function
# encryption constants, byteorder = 'little'

sig_0 = [101, 120, 112, 97]
sig_1 = [110, 100, 32, 51]
sig_2 = [50, 45, 98, 121]
sig_3 = [116, 101, 32, 107]


def salsa20_stream(block_counter, nonce, key):
	assert len(block_counter) == 8
	assert len(nonce) == 8
	assert len(key) == 32
	
	k0 = key[:16]
	k1 = key[16:]
	return salsa_20(sig_0 + k0 + sig_1 + nonce + block_counter + sig_2 + k1 + sig_3)


# 10 The Salsa20 encryption function

def salsa20_xor(message, nonce, key):
	"""Input in bytes. Returns encrypted message in the form of bytearray"""
	assert len(nonce) == 8
	assert len(key) == 32
	_nonce = list(nonce)
	_key = list(key)
	block_counter = [0] * 8
	k0 = _key[:16]
	k1 = _key[16:]
	enc_list = [a ^ b for a, b in zip(salsa_20(sig_0 + k0 + sig_1 + _nonce + block_counter + sig_2 + k1 + sig_3), list(message))]
	return bytearray(enc_list)


# tested using https://pypi.python.org/pypi/salsa20/0.3.0
# eq = Salsa20_xor(message=m, nonce=n, key=k)

k = bytearray(range(1, 33))
n = bytearray([3, 1, 4, 1, 5, 9, 2, 6])
m = b'This is message to be encrypted'

eq = b":\xd4\xd4\xccV\x95\xbfD\xc6`'X\x8f\xed\x02\xeb\xb6\xe0\x82\x83$\xdb\x8a\xd5Y]\xe2Rml\xac"
assert salsa20_xor(m, n, k) == eq

gen_key = lambda num_bytes: os.urandom(num_bytes)
# key, nonce = random 32 & 8 bytes
k = b'\xde\x06`\x1a\xbd\xa8\xf9\xaegl\xc2\x06"\xe4\xec\xebM{1\x88p\x8e\xff\xe8\t\x08\xee)\xce\x0f\x1a\xc4'
n = b'\xfb\xbe\xaf\x99KP\xbbC'
eq = b'\xa3q\xaek\xd7\xa3\xf9n\x13e\xd5\xcf\xff%\xc9D\x93i\x87\xc9.\xe4\xc8\x80\xc8\xd83\xd0\x8b\xb9\xfd'
assert salsa20_xor(m, n, k) == eq
