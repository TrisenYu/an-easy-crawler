/// SPDX-LICENSE-IDENTIFIER: GPL2.0-ONLY
/// (c) Author: <kisfg@hotmail.com in 2025>
///
/// This program is free software; you can redistribute it and/or
/// modify it under the terms of the GNU Library General Public
/// License as published by the Free Software Foundation.
/// This program is distributed in the hope that it will be useful,
/// but WITHOUT ANY WARRANTY; without even the implied warranty of
/// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
/// Library General Public License for more details.
/// You should have received a copy of the GNU Library General Public
/// License along with this library; if not, see
/// <https://www.gnu.org/licenses/>.

typedef unsigned long long _u64;
typedef unsigned int _u32;
typedef unsigned char _u08;

static inline _u64 _x64(_u64 x) { return x & 0xFFFFFFFFFFFFFFFFuLL; }
static inline _u32 _x32(_u64 x) { return x & 0xFFFFFFFFuLL; }

static inline _u32 _group_s(_u08 *str, int st, int s) {
    _u32 res = str[st + s];
    res |= (_u32)(str[st + s + 1]) << 0x08;
    res |= (_u32)(str[st + s + 2]) << 0x10;
    res |= (_u32)(str[st + s + 3]) << 0x18;
    return res;
}

static inline _u64 _rot_l(_u64 m, _u08 x) {
    x &= 0x3F;
    return (m << x) | (m >> (64 - x));
}

static inline _u64 _f_mix(_u64 x) {
    x ^= (x >> 33);
    x *= 0xff51afd7ed558ccduLL;
    x ^= (x >> 33);
    x *= 0xc4ceb9fe1a85ec53uLL;
    x ^= (x >> 33);
    return x;
}

// clang-format off
typedef struct _x128 { _u64 h1, h2; } _x128;
// clang-format on

_x128 mmh3_x64_128(_u08 *key, _u64 lenk, _u32 seed) {
    _u08 r = lenk & 0xF;
    _u64 div = lenk - r;
    _u64 h1 = _x64(seed), h2 = _x64(seed);
    _u64 c1 = 0x87c37b91114253d5uLL;
    _u64 c2 = 0x4cf5ad432745937fuLL;
    for (_u64 i = 0; i < div; i += 16) {
        _u64 k1 =
            (_x64(_group_s(key, i, 0x4)) << 32) | _x32(_group_s(key, i, 0x0));
        _u64 k2 =
            (_x64(_group_s(key, i, 0xC)) << 32) | _x32(_group_s(key, i, 0x8));

        k1 = _rot_l(k1 * c1, 31) * c2;
        h1 = (_rot_l(h1 ^ k1, 27) + h2) * 5 + 0x52dce729;

        k2 = _rot_l(k2 * c2, 33) * c1;
        h2 = (_rot_l(h2 ^ k2, 31) + h1) * 5 + 0x38495ab5;
    }
    _u64 k1 = 0, k2 = 0;
    switch (r) {
    case 0xf:
        k2 ^= (_u64)(key[div + 0xe]) << 48;
    case 0xe:
        k2 ^= (_u64)(key[div + 0xd]) << 40;
    case 0xd:
        k2 ^= (_u64)(key[div + 0xc]) << 32;
    case 0xc:
        k2 ^= (_u64)(key[div + 0xb]) << 24;
    case 0xb:
        k2 ^= (_u64)(key[div + 0xa]) << 16;
    case 0xa:
        k2 ^= (_u64)(key[div + 0x9]) << 8;
    case 0x9:
        k2 = _rot_l((k2 ^ key[div + 0x8]) * c2, 33) * c1;
        h2 ^= k2;
    case 0x8:
        k1 ^= (_u64)(key[div + 0x7]) << 56;
    case 0x7:
        k1 ^= (_u64)(key[div + 0x6]) << 48;
    case 0x6:
        k1 ^= (_u64)(key[div + 0x5]) << 40;
    case 0x5:
        k1 ^= (_u64)(key[div + 0x4]) << 32;
    case 0x4:
        k1 ^= (_u64)(key[div + 0x3]) << 24;
    case 0x3:
        k1 ^= (_u64)(key[div + 0x2]) << 16;
    case 0x2:
        k1 ^= (_u64)(key[div + 0x1]) << 8;
    case 0x1:
        k1 = _rot_l((k1 ^ key[div]) * c1, 31) * c2;
        h1 ^= k1;
    default:
        break;
    }
    h1 ^= lenk, h2 ^= lenk;
    h1 += h2, h2 += h1;
    h1 = _f_mix(h1);
    h2 = _f_mix(h2);
    h1 += h2, h2 += h1;
    _x128 res = {h1, h2};
    return res;
}