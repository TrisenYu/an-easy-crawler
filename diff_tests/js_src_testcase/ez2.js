/// Last modified at 2025年08月15日 星期五 18时19分30秒
function anything() {
	var a = 0x1234_5678 << 0b10100101;
	a >>>= 13;
	a ^= 0x971a_b35d;
	for (var i = 1; i < a; i ++) {
		a *= 123_456;
		a <<= 3;
	}
	var b = 31 | a >>> 3;
	b >>= 3 | a >> 5;
	return a, b
}
// 我啊啊啊啊啊啊
const x = [
	"\"", "1'123abcakljsdj",  "我说的话是假话", "我测这人怎么这么坏？", "how long have we attempted?",
	'\'', '好烦的DFA', '', ""
];
// bababababababababababbabababbaabba
let str = '这是一段多行文本。\
它可以跨越多行，\
并保持格式。',
	str1 = "111555 \
223456, \
77889; \
";

let str2 = `模板字面量是 ES6 引入的一种新方法，它可以帮助我们借助反引号
来编写多行字符串。例如这是一段多行文本。
它可以跨越多行，
并且保持格式。`;

console.log(anything());
console.log(x);

var a = {
  "a": /1/y,
  "b": 123,
}, b = /1234/m, c=[/1234/y, /12345/, /abcd/], d = (/12345/g);
console.log(a, b, c, d);

var x = /gugugaga\0\x12\u1234\u{61234}\t\f\v\n\r\\'"\[\][]\??!$\$*\*\d\w\W\D\s\S/mygdiu,
$$ = x[Symbol.split];
    // 输出结果
console.log(url, x, $$
);
console.log(r);

try {
  nonExistentFunction();
} catch (error) {
  console.error(error);
  // Expected output: ReferenceError: nonExistentFunction is not defined
  // (Note: the exact output may be browser-dependent)
}
