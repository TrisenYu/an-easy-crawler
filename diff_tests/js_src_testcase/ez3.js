/// Last modified at 2025年08月19日 星期二 17时53分15秒
var x = 5 + 3 > 7 === true, y = x ^ 1 + 1 < 2 === false;
let z = x && !y;
if (x) {
	console.log('yes', z)
} else if (y) {
	console.log(x)
} else console.log("hahaha")

for (var a = 0; a < 10; a ++) {
	for (var b = 0; b < 10; b ++)
		console.log(a*10+b)
		console.log(a);
}

const strings = [
  // 单独的前导代理
  "ab\uD800",
  "ab\uD800c",
  // 单独的后尾代理
  "\uDFFFab",
  "c\uDFFFab",
  // 格式正确
  "abc",
  "ab\uD83D\uDE04c",
];

for (const str of strings) {
  console.log(str.toWellFormed());
}
// Logs:
// "ab�"
// "ab�c"
// "�ab"
// "c�ab"
// "abc"
// "ab😄c"
@log
class Animal {
  constructor(name, age) {
    this.name = name
    this.age = age
  }
}

const cat = new Animal('Hello kitty', 2)
//  ["Hello kitty", 2]
console.log(cat.name)
// Hello kitty
