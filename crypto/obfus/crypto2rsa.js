// core.js
// 密码(限制长度117个字节)前接 128-密码长度的随机 pad，然后送去 a^e mod p.
var dbits;
var canary = 0xdeadbeefcafe;
var j_lm = 15715070 == (16777215 & canary);
function BigInteger(e, t, n) {
    if (null != e)
        if ("number" == typeof e)
            this.fromNumber(e, t, n);
        else if (null == t && "string" != typeof e)
            this.fromString(e, 256);
        else
            this.fromString(e, t);
}
function nbi() {
    return new BigInteger(null)
}
function am1(e, t, n, i, r, a) {
    for (; --a >= 0;) {
        var s = t * this[e++] + n[i] + r;
        r = Math.floor(s / 67108864);
        n[i++] = 67108863 & s
    }
    return r
}
function am2(e, t, n, i, r, a) {
    var s = 32767 & t
        , o = t >> 15;
    for (; --a >= 0;) {
        var c = 32767 & this[e];
        var l = this[e++] >> 15;
        var u = o * c + l * s;
        c = s * c + ((32767 & u) << 15) + n[i] + (1073741823 & r);
        r = (c >>> 30) + (u >>> 15) + o * l + (r >>> 30);
        n[i++] = 1073741823 & c
    }
    return r
}
function am3(e, t, n, i, r, a) {
    var s = 16383 & t
        , o = t >> 14;
    for (; --a >= 0;) {
        var c = 16383 & this[e];
        var l = this[e++] >> 14;
        var u = o * c + l * s;
        c = s * c + ((16383 & u) << 14) + n[i] + r;
        r = (c >> 28) + (u >> 14) + o * l;
        n[i++] = 268435455 & c
    }
    return r
}
//
//if (j_lm && "Microsoft Internet Explorer" == navigator.appName) {
//    BigInteger.prototype.am = am2;
//    dbits = 30
//} else if (j_lm && "Netscape" != navigator.appName) {
//    BigInteger.prototype.am = am1;
//    dbits = 26
//} else {
BigInteger.prototype.am = am3;
dbits = 28
//}
BigInteger.prototype.DB = dbits;
BigInteger.prototype.DM = (1 << dbits) - 1;
BigInteger.prototype.DV = 1 << dbits;
var BI_FP = 52;
BigInteger.prototype.FV = Math.pow(2, BI_FP);
BigInteger.prototype.F1 = BI_FP - dbits;
BigInteger.prototype.F2 = 2 * dbits - BI_FP;
var BI_RM = "0123456789abcdefghijklmnopqrstuvwxyz";
var BI_RC = new Array;
var rr, vv;
rr = "0".charCodeAt(0);
for (vv = 0; vv <= 9; ++vv)
    BI_RC[rr++] = vv;
rr = "a".charCodeAt(0);
for (vv = 10; vv < 36; ++vv)
    BI_RC[rr++] = vv;
rr = "A".charCodeAt(0);
for (vv = 10; vv < 36; ++vv)
    BI_RC[rr++] = vv;
function int2char(e) {
    return BI_RM.charAt(e)
}
function intAt(e, t) {
    var n = BI_RC[e.charCodeAt(t)];
    return null == n ? -1 : n
}
function bnpCopyTo(e) {
    for (var t = this.t - 1; t >= 0; --t)
        e[t] = this[t];
    e.t = this.t;
    e.s = this.s
}
function bnpFromInt(e) {
    this.t = 1;
    this.s = e < 0 ? -1 : 0;
    if (e > 0)
        this[0] = e;
    else if (e < -1)
        this[0] = e + DV;
    else
        this.t = 0
}
function nbv(e) {
    var t = nbi();
    t.fromInt(e);
    return t
}
function bnpFromString(e, t) {
    var n;
    if (16 == t)
        n = 4;
    else if (8 == t)
        n = 3;
    else if (256 == t)
        n = 8;
    else if (2 == t)
        n = 1;
    else if (32 == t)
        n = 5;
    else if (4 == t)
        n = 2;
    else {
        this.fromRadix(e, t);
        return
    }
    this.t = 0;
    this.s = 0;
    var i = e.length
        , r = !1
        , a = 0;
    for (; --i >= 0;) {
        var s = 8 == n ? 255 & e[i] : intAt(e, i);
        if (!(s < 0)) {
            r = !1;
            if (0 == a)
                this[this.t++] = s;
            else if (a + n > this.DB) {
                this[this.t - 1] |= (s & (1 << this.DB - a) - 1) << a;
                this[this.t++] = s >> this.DB - a
            } else
                this[this.t - 1] |= s << a;
            a += n;
            if (a >= this.DB)
                a -= this.DB
        } else if ("-" == e.charAt(i))
            r = !0
    }
    if (8 == n && 0 != (128 & e[0])) {
        this.s = -1;
        if (a > 0)
            this[this.t - 1] |= (1 << this.DB - a) - 1 << a
    }
    this.clamp();
    if (r)
        BigInteger.ZERO.subTo(this, this)
}
function bnpClamp() {
    var e = this.s & this.DM;
    for (; this.t > 0 && this[this.t - 1] == e;)
        --this.t
}
function bnToString(e) {
    if (this.s < 0)
        return "-" + this.negate().toString(e);
    var t;
    if (16 == e)
        t = 4;
    else if (8 == e)
        t = 3;
    else if (2 == e)
        t = 1;
    else if (32 == e)
        t = 5;
    else if (4 == e)
        t = 2;
    else
        return this.toRadix(e);
    var n = (1 << t) - 1, i, r = !1, a = "", s = this.t;
    var o = this.DB - s * this.DB % t;
    if (s-- > 0) {
        if (o < this.DB && (i = this[s] >> o) > 0) {
            r = !0;
            a = int2char(i)
        }
        for (; s >= 0;) {
            if (o < t) {
                i = (this[s] & (1 << o) - 1) << t - o;
                i |= this[--s] >> (o += this.DB - t)
            } else {
                i = this[s] >> (o -= t) & n;
                if (o <= 0) {
                    o += this.DB;
                    --s
                }
            }
            if (i > 0)
                r = !0;
            if (r)
                a += int2char(i)
        }
    }
    return r ? a : "0"
}
function bnNegate() {
    var e = nbi();
    BigInteger.ZERO.subTo(this, e);
    return e
}
function bnAbs() {
    return this.s < 0 ? this.negate() : this
}
function bnCompareTo(e) {
    var t = this.s - e.s;
    if (0 != t)
        return t;
    var n = this.t;
    t = n - e.t;
    if (0 != t)
        return this.s < 0 ? -t : t;
    for (; --n >= 0;)
        if (0 != (t = this[n] - e[n]))
            return t;
    return 0
}
function nbits(e) {
    var t = 1, n;
    if (0 != (n = e >>> 16)) {
        e = n;
        t += 16
    }
    if (0 != (n = e >> 8)) {
        e = n;
        t += 8
    }
    if (0 != (n = e >> 4)) {
        e = n;
        t += 4
    }
    if (0 != (n = e >> 2)) {
        e = n;
        t += 2
    }
    if (0 != (n = e >> 1)) {
        e = n;
        t += 1
    }
    return t
}
function bnBitLength() {
    if (this.t <= 0)
        return 0;
    else
        return this.DB * (this.t - 1) + nbits(this[this.t - 1] ^ this.s & this.DM)
}
function bnpDLShiftTo(e, t) {
    var n;
    for (n = this.t - 1; n >= 0; --n)
        t[n + e] = this[n];
    for (n = e - 1; n >= 0; --n)
        t[n] = 0;
    t.t = this.t + e;
    t.s = this.s
}
function bnpDRShiftTo(e, t) {
    for (var n = e; n < this.t; ++n)
        t[n - e] = this[n];
    t.t = Math.max(this.t - e, 0);
    t.s = this.s
}
function bnpLShiftTo(e, t) {
    var n = e % this.DB;
    var i = this.DB - n;
    var r = (1 << i) - 1;
    var a = Math.floor(e / this.DB), s = this.s << n & this.DM, o;
    for (o = this.t - 1; o >= 0; --o) {
        t[o + a + 1] = this[o] >> i | s;
        s = (this[o] & r) << n
    }
    for (o = a - 1; o >= 0; --o)
        t[o] = 0;
    t[a] = s;
    t.t = this.t + a + 1;
    t.s = this.s;
    t.clamp()
}
function bnpRShiftTo(e, t) {
    t.s = this.s;
    var n = Math.floor(e / this.DB);
    if (!(n >= this.t)) {
        var i = e % this.DB;
        var r = this.DB - i;
        var a = (1 << i) - 1;
        t[0] = this[n] >> i;
        for (var s = n + 1; s < this.t; ++s) {
            t[s - n - 1] |= (this[s] & a) << r;
            t[s - n] = this[s] >> i
        }
        if (i > 0)
            t[this.t - n - 1] |= (this.s & a) << r;
        t.t = this.t - n;
        t.clamp()
    } else
        t.t = 0
}
function bnpSubTo(e, t) {
    var n = 0
        , i = 0
        , r = Math.min(e.t, this.t);
    for (; n < r;) {
        i += this[n] - e[n];
        t[n++] = i & this.DM;
        i >>= this.DB
    }
    if (e.t < this.t) {
        i -= e.s;
        for (; n < this.t;) {
            i += this[n];
            t[n++] = i & this.DM;
            i >>= this.DB
        }
        i += this.s
    } else {
        i += this.s;
        for (; n < e.t;) {
            i -= e[n];
            t[n++] = i & this.DM;
            i >>= this.DB
        }
        i -= e.s
    }
    t.s = i < 0 ? -1 : 0;
    if (i < -1)
        t[n++] = this.DV + i;
    else if (i > 0)
        t[n++] = i;
    t.t = n;
    t.clamp()
}
function bnpMultiplyTo(e, t) {
    var n = this.abs()
        , i = e.abs();
    var r = n.t;
    t.t = r + i.t;
    for (; --r >= 0;)
        t[r] = 0;
    for (r = 0; r < i.t; ++r)
        t[r + n.t] = n.am(0, i[r], t, r, 0, n.t);
    t.s = 0;
    t.clamp();
    if (this.s != e.s)
        BigInteger.ZERO.subTo(t, t)
}
function bnpSquareTo(e) {
    var t = this.abs();
    var n = e.t = 2 * t.t;
    for (; --n >= 0;)
        e[n] = 0;
    for (n = 0; n < t.t - 1; ++n) {
        var i = t.am(n, t[n], e, 2 * n, 0, 1);
        if ((e[n + t.t] += t.am(n + 1, 2 * t[n], e, 2 * n + 1, i, t.t - n - 1)) >= t.DV) {
            e[n + t.t] -= t.DV;
            e[n + t.t + 1] = 1
        }
    }
    if (e.t > 0)
        e[e.t - 1] += t.am(n, t[n], e, 2 * n, 0, 1);
    e.s = 0;
    e.clamp()
}
function bnpDivRemTo(e, t, n) {
    var i = e.abs();
    if (!(i.t <= 0)) {
        var r = this.abs();
        if (!(r.t < i.t)) {
            if (null == n)
                n = nbi();
            var a = nbi()
                , s = this.s
                , o = e.s;
            var c = this.DB - nbits(i[i.t - 1]);
            if (c > 0) {
                i.lShiftTo(c, a);
                r.lShiftTo(c, n)
            } else {
                i.copyTo(a);
                r.copyTo(n)
            }
            var l = a.t;
            var u = a[l - 1];
            if (0 != u) {
                var d = u * (1 << this.F1) + (l > 1 ? a[l - 2] >> this.F2 : 0);
                var _ = this.FV / d
                    , h = (1 << this.F1) / d
                    , f = 1 << this.F2;
                var p = n.t
                    , g = p - l
                    , m = null == t ? nbi() : t;
                a.dlShiftTo(g, m);
                if (n.compareTo(m) >= 0) {
                    n[n.t++] = 1;
                    n.subTo(m, n)
                }
                BigInteger.ONE.dlShiftTo(l, m);
                m.subTo(a, a);
                for (; a.t < l;)
                    a[a.t++] = 0;
                for (; --g >= 0;) {
                    var b = n[--p] == u ? this.DM : Math.floor(n[p] * _ + (n[p - 1] + f) * h);
                    if ((n[p] += a.am(0, b, n, g, 0, l)) < b) {
                        a.dlShiftTo(g, m);
                        n.subTo(m, n);
                        for (; n[p] < --b;)
                            n.subTo(m, n)
                    }
                }
                if (null != t) {
                    n.drShiftTo(l, t);
                    if (s != o)
                        BigInteger.ZERO.subTo(t, t)
                }
                n.t = l;
                n.clamp();
                if (c > 0)
                    n.rShiftTo(c, n);
                if (s < 0)
                    BigInteger.ZERO.subTo(n, n)
            }
        } else {
            if (null != t)
                t.fromInt(0);
            if (null != n)
                this.copyTo(n)
        }
    }
}
function bnMod(e) {
    var t = nbi();
    this.abs().divRemTo(e, null, t);
    if (this.s < 0 && t.compareTo(BigInteger.ZERO) > 0)
        e.subTo(t, t);
    return t
}
function Classic(e) {
    this.m = e
}
function cConvert(e) {
    if (e.s < 0 || e.compareTo(this.m) >= 0)
        return e.mod(this.m);
    else
        return e
}
function cRevert(e) {
    return e
}
function cReduce(e) {
    e.divRemTo(this.m, null, e)
}
function cMulTo(e, t, n) {
    e.multiplyTo(t, n);
    this.reduce(n)
}
function cSqrTo(e, t) {
    e.squareTo(t);
    this.reduce(t)
}
Classic.prototype.convert = cConvert;
Classic.prototype.revert = cRevert;
Classic.prototype.reduce = cReduce;
Classic.prototype.mulTo = cMulTo;
Classic.prototype.sqrTo = cSqrTo;
function bnpInvDigit() {
    if (this.t < 1)
        return 0;
    var e = this[0];
    if (0 == (1 & e))
        return 0;
    var t = 3 & e;
    t = t * (2 - (15 & e) * t) & 15;
    t = t * (2 - (255 & e) * t) & 255;
    t = t * (2 - ((65535 & e) * t & 65535)) & 65535;
    t = t * (2 - e * t % this.DV) % this.DV;
    return t > 0 ? this.DV - t : -t
}
function Montgomery(e) {
    this.m = e;
    this.mp = e.invDigit();
    this.mpl = 32767 & this.mp;
    this.mph = this.mp >> 15;
    this.um = (1 << e.DB - 15) - 1;
    this.mt2 = 2 * e.t
}
function montConvert(e) {
    var t = nbi();
    e.abs().dlShiftTo(this.m.t, t);
    t.divRemTo(this.m, null, t);
    if (e.s < 0 && t.compareTo(BigInteger.ZERO) > 0)
        this.m.subTo(t, t);
    return t
}
function montRevert(e) {
    var t = nbi();
    e.copyTo(t);
    this.reduce(t);
    return t
}
function montReduce(e) {
    for (; e.t <= this.mt2;)
        e[e.t++] = 0;
    for (var t = 0; t < this.m.t; ++t) {
        var n = 32767 & e[t];
        var i = n * this.mpl + ((n * this.mph + (e[t] >> 15) * this.mpl & this.um) << 15) & e.DM;
        n = t + this.m.t;
        e[n] += this.m.am(0, i, e, t, 0, this.m.t);
        for (; e[n] >= e.DV;) {
            e[n] -= e.DV;
            e[++n]++
        }
    }
    e.clamp();
    e.drShiftTo(this.m.t, e);
    if (e.compareTo(this.m) >= 0)
        e.subTo(this.m, e)
}
function montSqrTo(e, t) {
    e.squareTo(t);
    this.reduce(t)
}
function montMulTo(e, t, n) {
    e.multiplyTo(t, n);
    this.reduce(n)
}
Montgomery.prototype.convert = montConvert;
Montgomery.prototype.revert = montRevert;
Montgomery.prototype.reduce = montReduce;
Montgomery.prototype.mulTo = montMulTo;
Montgomery.prototype.sqrTo = montSqrTo;
function bnpIsEven() {
    return 0 == (this.t > 0 ? 1 & this[0] : this.s)
}
function bnpExp(e, t) {
    if (e > 4294967295 || e < 1)
        return BigInteger.ONE;
    var n = nbi()
        , i = nbi()
        , r = t.convert(this)
        , a = nbits(e) - 1;
    r.copyTo(n);
    for (; --a >= 0;) {
        t.sqrTo(n, i);
        if ((e & 1 << a) > 0)
            t.mulTo(i, r, n);
        else {
            var s = n;
            n = i;
            i = s
        }
    }
    return t.revert(n)
}
function bnModPowInt(e, t) {
    var n;
    if (e < 256 || t.isEven())
        n = new Classic(t);
    else
        n = new Montgomery(t);
    return this.exp(e, n)
}
BigInteger.prototype.copyTo = bnpCopyTo;
BigInteger.prototype.fromInt = bnpFromInt;
BigInteger.prototype.fromString = bnpFromString;
BigInteger.prototype.clamp = bnpClamp;
BigInteger.prototype.dlShiftTo = bnpDLShiftTo;
BigInteger.prototype.drShiftTo = bnpDRShiftTo;
BigInteger.prototype.lShiftTo = bnpLShiftTo;
BigInteger.prototype.rShiftTo = bnpRShiftTo;
BigInteger.prototype.subTo = bnpSubTo;
BigInteger.prototype.multiplyTo = bnpMultiplyTo;
BigInteger.prototype.squareTo = bnpSquareTo;
BigInteger.prototype.divRemTo = bnpDivRemTo;
BigInteger.prototype.invDigit = bnpInvDigit;
BigInteger.prototype.isEven = bnpIsEven;
BigInteger.prototype.exp = bnpExp;
BigInteger.prototype.toString = bnToString;
BigInteger.prototype.negate = bnNegate;
BigInteger.prototype.abs = bnAbs;
BigInteger.prototype.compareTo = bnCompareTo;
BigInteger.prototype.bitLength = bnBitLength;
BigInteger.prototype.mod = bnMod;
BigInteger.prototype.modPowInt = bnModPowInt;
BigInteger.ZERO = nbv(0);
BigInteger.ONE = nbv(1);
function bnClone() {
    var e = nbi();
    this.copyTo(e);
    return e
}
function bnIntValue() {
    if (this.s < 0) {
        if (1 == this.t)
            return this[0] - this.DV;
        else if (0 == this.t)
            return -1
    } else if (1 == this.t)
        return this[0];
    else if (0 == this.t)
        return 0;
    return (this[1] & (1 << 32 - this.DB) - 1) << this.DB | this[0]
}
function bnByteValue() {
    return 0 == this.t ? this.s : this[0] << 24 >> 24
}
function bnShortValue() {
    return 0 == this.t ? this.s : this[0] << 16 >> 16
}
function bnpChunkSize(e) {
    return Math.floor(Math.LN2 * this.DB / Math.log(e))
}
function bnSigNum() {
    if (this.s < 0)
        return -1;
    else if (this.t <= 0 || 1 == this.t && this[0] <= 0)
        return 0;
    else
        return 1
}
function bnpToRadix(e) {
    if (null == e)
        e = 10;
    if (0 == this.signum() || e < 2 || e > 36)
        return "0";
    var t = this.chunkSize(e);
    var n = Math.pow(e, t);
    var i = nbv(n)
        , r = nbi()
        , a = nbi()
        , s = "";
    this.divRemTo(i, r, a);
    for (; r.signum() > 0;) {
        s = (n + a.intValue()).toString(e).substr(1) + s;
        r.divRemTo(i, r, a)
    }
    return a.intValue().toString(e) + s
}
function bnpFromRadix(e, t) {
    this.fromInt(0);
    if (null == t)
        t = 10;
    var n = this.chunkSize(t);
    var i = Math.pow(t, n)
        , r = !1
        , a = 0
        , s = 0;
    for (var o = 0; o < e.length; ++o) {
        var c = intAt(e, o);
        if (!(c < 0)) {
            s = t * s + c;
            if (++a >= n) {
                this.dMultiply(i);
                this.dAddOffset(s, 0);
                a = 0;
                s = 0
            }
        } else if ("-" == e.charAt(o) && 0 == this.signum())
            r = !0
    }
    if (a > 0) {
        this.dMultiply(Math.pow(t, a));
        this.dAddOffset(s, 0)
    }
    if (r)
        BigInteger.ZERO.subTo(this, this)
}
function bnpFromNumber(e, t, n) {
    if ("number" == typeof t)
        if (e < 2)
            this.fromInt(1);
        else {
            this.fromNumber(e, n);
            if (!this.testBit(e - 1))
                this.bitwiseTo(BigInteger.ONE.shiftLeft(e - 1), op_or, this);
            if (this.isEven())
                this.dAddOffset(1, 0);
            for (; !this.isProbablePrime(t);) {
                this.dAddOffset(2, 0);
                if (this.bitLength() > e)
                    this.subTo(BigInteger.ONE.shiftLeft(e - 1), this)
            }
        }
    else {
        var i = new Array
            , r = 7 & e;
        i.length = (e >> 3) + 1;
        t.nextBytes(i);
        if (r > 0)
            i[0] &= (1 << r) - 1;
        else
            i[0] = 0;
        this.fromString(i, 256)
    }
}
function bnToByteArray() {
    var e = this.t
        , t = new Array;
    t[0] = this.s;
    var n = this.DB - e * this.DB % 8, i, r = 0;
    if (e-- > 0) {
        if (n < this.DB && (i = this[e] >> n) != (this.s & this.DM) >> n)
            t[r++] = i | this.s << this.DB - n;
        for (; e >= 0;) {
            if (n < 8) {
                i = (this[e] & (1 << n) - 1) << 8 - n;
                i |= this[--e] >> (n += this.DB - 8)
            } else {
                i = this[e] >> (n -= 8) & 255;
                if (n <= 0) {
                    n += this.DB;
                    --e
                }
            }
            if (0 != (128 & i))
                i |= -256;
            if (0 == r && (128 & this.s) != (128 & i))
                ++r;
            if (r > 0 || i != this.s)
                t[r++] = i
        }
    }
    return t
}
function bnEquals(e) {
    return 0 == this.compareTo(e)
}
function bnMin(e) {
    return this.compareTo(e) < 0 ? this : e
}
function bnMax(e) {
    return this.compareTo(e) > 0 ? this : e
}
function bnpBitwiseTo(e, t, n) {
    var i, r, a = Math.min(e.t, this.t);
    for (i = 0; i < a; ++i)
        n[i] = t(this[i], e[i]);
    if (e.t < this.t) {
        r = e.s & this.DM;
        for (i = a; i < this.t; ++i)
            n[i] = t(this[i], r);
        n.t = this.t
    } else {
        r = this.s & this.DM;
        for (i = a; i < e.t; ++i)
            n[i] = t(r, e[i]);
        n.t = e.t
    }
    n.s = t(this.s, e.s);
    n.clamp()
}
function op_and(e, t) {
    return e & t
}
function bnAnd(e) {
    var t = nbi();
    this.bitwiseTo(e, op_and, t);
    return t
}
function op_or(e, t) {
    return e | t
}
function bnOr(e) {
    var t = nbi();
    this.bitwiseTo(e, op_or, t);
    return t
}
function op_xor(e, t) {
    return e ^ t
}
function bnXor(e) {
    var t = nbi();
    this.bitwiseTo(e, op_xor, t);
    return t
}
function op_andnot(e, t) {
    return e & ~t
}
function bnAndNot(e) {
    var t = nbi();
    this.bitwiseTo(e, op_andnot, t);
    return t
}
function bnNot() {
    var e = nbi();
    for (var t = 0; t < this.t; ++t)
        e[t] = this.DM & ~this[t];
    e.t = this.t;
    e.s = ~this.s;
    return e
}
function bnShiftLeft(e) {
    var t = nbi();
    if (e < 0)
        this.rShiftTo(-e, t);
    else
        this.lShiftTo(e, t);
    return t
}
function bnShiftRight(e) {
    var t = nbi();
    if (e < 0)
        this.lShiftTo(-e, t);
    else
        this.rShiftTo(e, t);
    return t
}
function lbit(e) {
    if (0 == e)
        return -1;
    var t = 0;
    if (0 == (65535 & e)) {
        e >>= 16;
        t += 16
    }
    if (0 == (255 & e)) {
        e >>= 8;
        t += 8
    }
    if (0 == (15 & e)) {
        e >>= 4;
        t += 4
    }
    if (0 == (3 & e)) {
        e >>= 2;
        t += 2
    }
    if (0 == (1 & e))
        ++t;
    return t
}
function bnGetLowestSetBit() {
    for (var e = 0; e < this.t; ++e)
        if (0 != this[e])
            return e * this.DB + lbit(this[e]);
    if (this.s < 0)
        return this.t * this.DB;
    else
        return -1
}
function cbit(e) {
    var t = 0;
    for (; 0 != e;) {
        e &= e - 1;
        ++t
    }
    return t
}
function bnBitCount() {
    var e = 0
        , t = this.s & this.DM;
    for (var n = 0; n < this.t; ++n)
        e += cbit(this[n] ^ t);
    return e
}
function bnTestBit(e) {
    var t = Math.floor(e / this.DB);
    if (t >= this.t)
        return 0 != this.s;
    else
        return 0 != (this[t] & 1 << e % this.DB)
}
function bnpChangeBit(e, t) {
    var n = BigInteger.ONE.shiftLeft(e);
    this.bitwiseTo(n, t, n);
    return n
}
function bnSetBit(e) {
    return this.changeBit(e, op_or)
}
function bnClearBit(e) {
    return this.changeBit(e, op_andnot)
}
function bnFlipBit(e) {
    return this.changeBit(e, op_xor)
}
function bnpAddTo(e, t) {
    var n = 0
        , i = 0
        , r = Math.min(e.t, this.t);
    for (; n < r;) {
        i += this[n] + e[n];
        t[n++] = i & this.DM;
        i >>= this.DB
    }
    if (e.t < this.t) {
        i += e.s;
        for (; n < this.t;) {
            i += this[n];
            t[n++] = i & this.DM;
            i >>= this.DB
        }
        i += this.s
    } else {
        i += this.s;
        for (; n < e.t;) {
            i += e[n];
            t[n++] = i & this.DM;
            i >>= this.DB
        }
        i += e.s
    }
    t.s = i < 0 ? -1 : 0;
    if (i > 0)
        t[n++] = i;
    else if (i < -1)
        t[n++] = this.DV + i;
    t.t = n;
    t.clamp()
}
function bnAdd(e) {
    var t = nbi();
    this.addTo(e, t);
    return t
}
function bnSubtract(e) {
    var t = nbi();
    this.subTo(e, t);
    return t
}
function bnMultiply(e) {
    var t = nbi();
    this.multiplyTo(e, t);
    return t
}
function bnSquare() {
    var e = nbi();
    this.squareTo(e);
    return e
}
function bnDivide(e) {
    var t = nbi();
    this.divRemTo(e, t, null);
    return t
}
function bnRemainder(e) {
    var t = nbi();
    this.divRemTo(e, null, t);
    return t
}
function bnDivideAndRemainder(e) {
    var t = nbi()
        , n = nbi();
    this.divRemTo(e, t, n);
    return new Array(t, n)
}
function bnpDMultiply(e) {
    this[this.t] = this.am(0, e - 1, this, 0, 0, this.t);
    ++this.t;
    this.clamp()
}
function bnpDAddOffset(e, t) {
    if (0 != e) {
        for (; this.t <= t;)
            this[this.t++] = 0;
        this[t] += e;
        for (; this[t] >= this.DV;) {
            this[t] -= this.DV;
            if (++t >= this.t)
                this[this.t++] = 0;
            ++this[t]
        }
    }
}
function NullExp() { }
function nNop(e) {
    return e
}
function nMulTo(e, t, n) {
    e.multiplyTo(t, n)
}
function nSqrTo(e, t) {
    e.squareTo(t)
}
NullExp.prototype.convert = nNop;
NullExp.prototype.revert = nNop;
NullExp.prototype.mulTo = nMulTo;
NullExp.prototype.sqrTo = nSqrTo;
function bnPow(e) {
    return this.exp(e, new NullExp)
}
function bnpMultiplyLowerTo(e, t, n) {
    var i = Math.min(this.t + e.t, t);
    n.s = 0;
    n.t = i;
    for (; i > 0;)
        n[--i] = 0;
    var r;
    for (r = n.t - this.t; i < r; ++i)
        n[i + this.t] = this.am(0, e[i], n, i, 0, this.t);
    for (r = Math.min(e.t, t); i < r; ++i)
        this.am(0, e[i], n, i, 0, t - i);
    n.clamp()
}
function bnpMultiplyUpperTo(e, t, n) {
    --t;
    var i = n.t = this.t + e.t - t;
    n.s = 0;
    for (; --i >= 0;)
        n[i] = 0;
    for (i = Math.max(t - this.t, 0); i < e.t; ++i)
        n[this.t + i - t] = this.am(t - i, e[i], n, 0, 0, this.t + i - t);
    n.clamp();
    n.drShiftTo(1, n)
}
function Barrett(e) {
    this.r2 = nbi();
    this.q3 = nbi();
    BigInteger.ONE.dlShiftTo(2 * e.t, this.r2);
    this.mu = this.r2.divide(e);
    this.m = e
}
function barrettConvert(e) {
    if (e.s < 0 || e.t > 2 * this.m.t)
        return e.mod(this.m);
    else if (e.compareTo(this.m) < 0)
        return e;
    else {
        var t = nbi();
        e.copyTo(t);
        this.reduce(t);
        return t
    }
}
function barrettRevert(e) {
    return e
}
function barrettReduce(e) {
    e.drShiftTo(this.m.t - 1, this.r2);
    if (e.t > this.m.t + 1) {
        e.t = this.m.t + 1;
        e.clamp()
    }
    this.mu.multiplyUpperTo(this.r2, this.m.t + 1, this.q3);
    this.m.multiplyLowerTo(this.q3, this.m.t + 1, this.r2);
    for (; e.compareTo(this.r2) < 0;)
        e.dAddOffset(1, this.m.t + 1);
    e.subTo(this.r2, e);
    for (; e.compareTo(this.m) >= 0;)
        e.subTo(this.m, e)
}
function barrettSqrTo(e, t) {
    e.squareTo(t);
    this.reduce(t)
}
function barrettMulTo(e, t, n) {
    e.multiplyTo(t, n);
    this.reduce(n)
}
Barrett.prototype.convert = barrettConvert;
Barrett.prototype.revert = barrettRevert;
Barrett.prototype.reduce = barrettReduce;
Barrett.prototype.mulTo = barrettMulTo;
Barrett.prototype.sqrTo = barrettSqrTo;
function bnModPow(e, t) {
    var n = e.bitLength(), i, r = nbv(1), a;
    if (n <= 0)
        return r;
    else if (n < 18)
        i = 1;
    else if (n < 48)
        i = 3;
    else if (n < 144)
        i = 4;
    else if (n < 768)
        i = 5;
    else
        i = 6;
    if (n < 8)
        a = new Classic(t);
    else if (t.isEven())
        a = new Barrett(t);
    else
        a = new Montgomery(t);
    var s = new Array
        , o = 3
        , c = i - 1
        , l = (1 << i) - 1;
    s[1] = a.convert(this);
    if (i > 1) {
        var u = nbi();
        a.sqrTo(s[1], u);
        for (; o <= l;) {
            s[o] = nbi();
            a.mulTo(u, s[o - 2], s[o]);
            o += 2
        }
    }
    var d = e.t - 1, _, h = !0, f = nbi(), p;
    n = nbits(e[d]) - 1;
    for (; d >= 0;) {
        if (n >= c)
            _ = e[d] >> n - c & l;
        else {
            _ = (e[d] & (1 << n + 1) - 1) << c - n;
            if (d > 0)
                _ |= e[d - 1] >> this.DB + n - c
        }
        o = i;
        for (; 0 == (1 & _);) {
            _ >>= 1;
            --o
        }
        if ((n -= o) < 0) {
            n += this.DB;
            --d
        }
        if (h) {
            s[_].copyTo(r);
            h = !1
        } else {
            for (; o > 1;) {
                a.sqrTo(r, f);
                a.sqrTo(f, r);
                o -= 2
            }
            if (o > 0)
                a.sqrTo(r, f);
            else {
                p = r;
                r = f;
                f = p
            }
            a.mulTo(f, s[_], r)
        }
        for (; d >= 0 && 0 == (e[d] & 1 << n);) {
            a.sqrTo(r, f);
            p = r;
            r = f;
            f = p;
            if (--n < 0) {
                n = this.DB - 1;
                --d
            }
        }
    }
    return a.revert(r)
}
function bnGCD(e) {
    var t = this.s < 0 ? this.negate() : this.clone();
    var n = e.s < 0 ? e.negate() : e.clone();
    if (t.compareTo(n) < 0) {
        var i = t;
        t = n;
        n = i
    }
    var r = t.getLowestSetBit()
        , a = n.getLowestSetBit();
    if (a < 0)
        return t;
    if (r < a)
        a = r;
    if (a > 0) {
        t.rShiftTo(a, t);
        n.rShiftTo(a, n)
    }
    for (; t.signum() > 0;) {
        if ((r = t.getLowestSetBit()) > 0)
            t.rShiftTo(r, t);
        if ((r = n.getLowestSetBit()) > 0)
            n.rShiftTo(r, n);
        if (t.compareTo(n) >= 0) {
            t.subTo(n, t);
            t.rShiftTo(1, t)
        } else {
            n.subTo(t, n);
            n.rShiftTo(1, n)
        }
    }
    if (a > 0)
        n.lShiftTo(a, n);
    return n
}
function bnpModInt(e) {
    if (e <= 0)
        return 0;
    var t = this.DV % e
        , n = this.s < 0 ? e - 1 : 0;
    if (this.t > 0)
        if (0 == t)
            n = this[0] % e;
        else
            for (var i = this.t - 1; i >= 0; --i)
                n = (t * n + this[i]) % e;
    return n
}
function bnModInverse(e) {
    var t = e.isEven();
    if (this.isEven() && t || 0 == e.signum())
        return BigInteger.ZERO;
    var n = e.clone()
        , i = this.clone();
    var r = nbv(1)
        , a = nbv(0)
        , s = nbv(0)
        , o = nbv(1);
    for (; 0 != n.signum();) {
        for (; n.isEven();) {
            n.rShiftTo(1, n);
            if (t) {
                if (!r.isEven() || !a.isEven()) {
                    r.addTo(this, r);
                    a.subTo(e, a)
                }
                r.rShiftTo(1, r)
            } else if (!a.isEven())
                a.subTo(e, a);
            a.rShiftTo(1, a)
        }
        for (; i.isEven();) {
            i.rShiftTo(1, i);
            if (t) {
                if (!s.isEven() || !o.isEven()) {
                    s.addTo(this, s);
                    o.subTo(e, o)
                }
                s.rShiftTo(1, s)
            } else if (!o.isEven())
                o.subTo(e, o);
            o.rShiftTo(1, o)
        }
        if (n.compareTo(i) >= 0) {
            n.subTo(i, n);
            if (t)
                r.subTo(s, r);
            a.subTo(o, a)
        } else {
            i.subTo(n, i);
            if (t)
                s.subTo(r, s);
            o.subTo(a, o)
        }
    }
    if (0 != i.compareTo(BigInteger.ONE))
        return BigInteger.ZERO;
    if (o.compareTo(e) >= 0)
        return o.subtract(e);
    if (o.signum() < 0)
        o.addTo(e, o);
    else
        return o;
    if (o.signum() < 0)
        return o.add(e);
    else
        return o
}
var lowprimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997];
var lplim = (1 << 26) / lowprimes[lowprimes.length - 1];
function bnIsProbablePrime(e) {
    var t, n = this.abs();
    if (1 == n.t && n[0] <= lowprimes[lowprimes.length - 1]) {
        for (t = 0; t < lowprimes.length; ++t)
            if (n[0] == lowprimes[t])
                return !0;
        return !1
    }
    if (n.isEven())
        return !1;
    t = 1;
    for (; t < lowprimes.length;) {
        var i = lowprimes[t]
            , r = t + 1;
        for (; r < lowprimes.length && i < lplim;)
            i *= lowprimes[r++];
        i = n.modInt(i);
        for (; t < r;)
            if (i % lowprimes[t++] == 0)
                return !1
    }
    return n.millerRabin(e)
}
function bnpMillerRabin(e) {
    var t = this.subtract(BigInteger.ONE);
    var n = t.getLowestSetBit();
    if (n <= 0)
        return !1;
    var i = t.shiftRight(n);
    e = e + 1 >> 1;
    if (e > lowprimes.length)
        e = lowprimes.length;
    var r = nbi();
    for (var a = 0; a < e; ++a) {
        r.fromInt(lowprimes[Math.floor(Math.random() * lowprimes.length)]);
        var s = r.modPow(i, this);
        if (0 != s.compareTo(BigInteger.ONE) && 0 != s.compareTo(t)) {
            var o = 1;
            for (; o++ < n && 0 != s.compareTo(t);) {
                s = s.modPowInt(2, this);
                if (0 == s.compareTo(BigInteger.ONE))
                    return !1
            }
            if (0 != s.compareTo(t))
                return !1
        }
    }
    return !0
}
BigInteger.prototype.chunkSize = bnpChunkSize;
BigInteger.prototype.toRadix = bnpToRadix;
BigInteger.prototype.fromRadix = bnpFromRadix;
BigInteger.prototype.fromNumber = bnpFromNumber;
BigInteger.prototype.bitwiseTo = bnpBitwiseTo;
BigInteger.prototype.changeBit = bnpChangeBit;
BigInteger.prototype.addTo = bnpAddTo;
BigInteger.prototype.dMultiply = bnpDMultiply;
BigInteger.prototype.dAddOffset = bnpDAddOffset;
BigInteger.prototype.multiplyLowerTo = bnpMultiplyLowerTo;
BigInteger.prototype.multiplyUpperTo = bnpMultiplyUpperTo;
BigInteger.prototype.modInt = bnpModInt;
BigInteger.prototype.millerRabin = bnpMillerRabin;
BigInteger.prototype.clone = bnClone;
BigInteger.prototype.intValue = bnIntValue;
BigInteger.prototype.byteValue = bnByteValue;
BigInteger.prototype.shortValue = bnShortValue;
BigInteger.prototype.signum = bnSigNum;
BigInteger.prototype.toByteArray = bnToByteArray;
BigInteger.prototype.equals = bnEquals;
BigInteger.prototype.min = bnMin;
BigInteger.prototype.max = bnMax;
BigInteger.prototype.and = bnAnd;
BigInteger.prototype.or = bnOr;
BigInteger.prototype.xor = bnXor;
BigInteger.prototype.andNot = bnAndNot;
BigInteger.prototype.not = bnNot;
BigInteger.prototype.shiftLeft = bnShiftLeft;
BigInteger.prototype.shiftRight = bnShiftRight;
BigInteger.prototype.getLowestSetBit = bnGetLowestSetBit;
BigInteger.prototype.bitCount = bnBitCount;
BigInteger.prototype.testBit = bnTestBit;
BigInteger.prototype.setBit = bnSetBit;
BigInteger.prototype.clearBit = bnClearBit;
BigInteger.prototype.flipBit = bnFlipBit;
BigInteger.prototype.add = bnAdd;
BigInteger.prototype.subtract = bnSubtract;
BigInteger.prototype.multiply = bnMultiply;
BigInteger.prototype.divide = bnDivide;
BigInteger.prototype.remainder = bnRemainder;
BigInteger.prototype.divideAndRemainder = bnDivideAndRemainder;
BigInteger.prototype.modPow = bnModPow;
BigInteger.prototype.modInverse = bnModInverse;
BigInteger.prototype.pow = bnPow;
BigInteger.prototype.gcd = bnGCD;
BigInteger.prototype.isProbablePrime = bnIsProbablePrime;
BigInteger.prototype.square = bnSquare;
var RSAPublicKey = function (e, t) {
    this.modulus = new BigInteger(Hex.encode(e), 16);
    this.encryptionExponent = new BigInteger(Hex.encode(t), 16)
};
var UTF8 = {
    encode: function (e) {
        e = e.replace(/\r\n/g, "\n");
        var t = "";
        for (var n = 0; n < e.length; n++) {
            var i = e.charCodeAt(n);
            if (i < 128)
                t += String.fromCharCode(i);
            else if (i > 127 && i < 2048) {
                t += String.fromCharCode(i >> 6 | 192);
                t += String.fromCharCode(63 & i | 128)
            } else {
                t += String.fromCharCode(i >> 12 | 224);
                t += String.fromCharCode(i >> 6 & 63 | 128);
                t += String.fromCharCode(63 & i | 128)
            }
        }
        return t
    },
    decode: function (e) {
        var t = "";
        var n = 0;
        var i = $c1 = $c2 = 0;
        for (; n < e.length;) {
            i = e.charCodeAt(n);
            if (i < 128) {
                t += String.fromCharCode(i);
                n++
            } else if (i > 191 && i < 224) {
                $c2 = e.charCodeAt(n + 1);
                t += String.fromCharCode((31 & i) << 6 | 63 & $c2);
                n += 2
            } else {
                $c2 = e.charCodeAt(n + 1);
                $c3 = e.charCodeAt(n + 2);
                t += String.fromCharCode((15 & i) << 12 | (63 & $c2) << 6 | 63 & $c3);
                n += 3
            }
        }
        return t
    }
};
var Base64 = {
    base64: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    encode: function (e) {
        if (!e)
            return !1;
        var t = "";
        var n, i, r;
        var a, s, o, c;
        var l = 0;
        do {
            n = e.charCodeAt(l++);
            i = e.charCodeAt(l++);
            r = e.charCodeAt(l++);
            a = n >> 2;
            s = (3 & n) << 4 | i >> 4;
            o = (15 & i) << 2 | r >> 6;
            c = 63 & r;
            if (isNaN(i))
                o = c = 64;
            else if (isNaN(r))
                c = 64;
            t += this.base64.charAt(a) + this.base64.charAt(s) + this.base64.charAt(o) + this.base64.charAt(c)
        } while (l < e.length);
        return t
    },
    decode: function (e) {
        if (!e)
            return !1;
        e = e.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        var t = "";
        var n, i, r, a;
        var s = 0;
        do {
            n = this.base64.indexOf(e.charAt(s++));
            i = this.base64.indexOf(e.charAt(s++));
            r = this.base64.indexOf(e.charAt(s++));
            a = this.base64.indexOf(e.charAt(s++));
            t += String.fromCharCode(n << 2 | i >> 4);
            if (64 != r)
                t += String.fromCharCode((15 & i) << 4 | r >> 2);
            if (64 != a)
                t += String.fromCharCode((3 & r) << 6 | a)
        } while (s < e.length);
        return t
    }
};
var Hex = {
    hex: "0123456789abcdef",
    encode: function (e) {
        if (!e)
            return !1;
        var t = "";
        var n;
        var i = 0;
        do {
            n = e.charCodeAt(i++);
            t += this.hex.charAt(n >> 4 & 15) + this.hex.charAt(15 & n)
        } while (i < e.length);
        return t
    },
    decode: function (e) {
        if (!e)
            return !1;
        e = e.replace(/[^0-9abcdef]/g, "");
        var t = "";
        var n = 0;
        do
            t += String.fromCharCode(this.hex.indexOf(e.charAt(n++)) << 4 & 240 | 15 & this.hex.indexOf(e.charAt(n++)));
        while (n < e.length);
        return t
    }
};
var ASN1Data = function (e) {
    this.error = !1;
    this.parse = function (e) {
        if (!e) {
            this.error = !0;
            return null
        }
        var t = [];
        for (; e.length > 0;) {
            var n = e.charCodeAt(0);
            e = e.substr(1);
            var i = 0;
            if (5 == (31 & n))
                e = e.substr(1);
            else if (128 & e.charCodeAt(0)) {
                var r = 127 & e.charCodeAt(0);
                e = e.substr(1);
                if (r > 0)
                    i = e.charCodeAt(0);
                if (r > 1)
                    i = i << 8 | e.charCodeAt(1);
                if (r > 2) {
                    this.error = !0;
                    return null
                }
                e = e.substr(r)
            } else {
                i = e.charCodeAt(0);
                e = e.substr(1)
            }
            var a = "";
            if (i) {
                if (i > e.length) {
                    this.error = !0;
                    return null
                }
                a = e.substr(0, i);
                e = e.substr(i)
            }
            if (32 & n)
                t.push(this.parse(a));
            else
                t.push(this.value(128 & n ? 4 : 31 & n, a))
        }
        return t
    }
        ;
    this.value = function (e, t) {
        if (1 == e)
            return t ? !0 : !1;
        else if (2 == e)
            return t;
        else if (3 == e)
            return this.parse(t.substr(1));
        else if (5 == e)
            return null;
        else if (6 == e) {
            var n = [];
            var i = t.charCodeAt(0);
            n.push(Math.floor(i / 40));
            n.push(i - 40 * n[0]);
            var r = [];
            var a = 0;
            var s;
            for (s = 1; s < t.length; s++) {
                var o = t.charCodeAt(s);
                r.push(127 & o);
                if (128 & o)
                    a++;
                else {
                    var c;
                    var l = 0;
                    for (c = 0; c < r.length; c++)
                        l += r[c] * Math.pow(128, a--);
                    n.push(l);
                    a = 0;
                    r = []
                }
            }
            return n.join(".")
        }
        return null
    }
        ;
    this.data = this.parse(e)
};
var RSA = {
    getPublicKey: function (e) {
        if (e.length < 50)
            return !1;
        if ("-----BEGIN PUBLIC KEY-----" != e.substr(0, 26))
            return !1;
        e = e.substr(26);
        if ("-----END PUBLIC KEY-----" != e.substr(e.length - 24))
            return !1;
        e = e.substr(0, e.length - 24);
        e = new ASN1Data(Base64.decode(e));
        if (e.error)
            return !1;
        e = e.data;
        if ("1.2.840.113549.1.1.1" == e[0][0][0])
            return new RSAPublicKey(e[0][1][0][0], e[0][1][0][1]);
        else
            return !1
    },
    encrypt: function (e, t) {
        if (!t)
            return !1;
        var n = t.modulus.bitLength() + 7 >> 3;
        e = this.pkcs1pad2(e, n);
        if (!e)
            return !1;
        e = e.modPowInt(t.encryptionExponent, t.modulus);
        if (!e)
            return !1;
        e = e.toString(16);
        for (; e.length < 2 * n;)
            e = "0" + e;
        return Base64.encode(Hex.decode(e))
    },
    decrypt: function (e) {
        var t = new BigInteger(e, 16)
    },
    pkcs1pad2: function (e, t) {
        if (t < e.length + 11)
            return null;
        var n = [];
        var i = e.length - 1;
        for (; i >= 0 && t > 0;)
            n[--t] = e.charCodeAt(i--);
        n[--t] = 0;
        for (; t > 2;)
            n[--t] = Math.floor(254 * Math.random()) + 1;
        n[--t] = 2;
        n[--t] = 0;
        return new BigInteger(n)
    }
};

// 加密中途有用随机数，导致结果基本不可验证。
// 但至少能用就是了。
// console.log(pwd_encrypt_wrapper('123456abcdhahaha'))
function pwd_encrypt_wrapper(password) {
    var pub = "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfrRxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0Sa4R4qhPO3I2MQIDAQAB-----END PUBLIC KEY-----";
    var t = RSA.getPublicKey(pub);
    return RSA.encrypt(password, t)
}
console.log(pwd_encrypt_wrapper('123'))
/*
c._$init = function() {
    window.MP = {
        setTicket: function(e) {
            window.MP.TICKET = e || ""
        },
        encrypt: function(e, t) {
            t = t.toLowerCase();
            var n = RSA.getPublicKey(f);
            return RSA.encrypt(e + "`" + t, n)
        },
        encrypt2: function(e) {
            var t = RSA.getPublicKey(f);
            return RSA.encrypt(e, t)
        },
        getCookieId: function(e, t) {
            var n = a._$cookie(e);
            t(n)
        },
        getId: function(e, t) {
            var n = a._$cookie(h + e);
            t(n)
        },
        getCaptcha: function() {
            return this.getCaptcha()
        }
        ._$bind(this),
        getCaptchaLogin: function(e, t) {
            return this.getCaptchaLogin(e, t)
        }
        ._$bind(this),
        "mb-ncp": function(e) {
            return this["mb-ncp"](e)
        }
        ._$bind(this),
        "mb-reg-cp": function() {
            return this["mb-reg-cp"]()
        }
        ._$bind(this),
        "mb-cp": function(e, t, n, i) {
            return this["mb-cp"](e, t, n, i)
        }
        ._$bind(this)
    }
}
*/