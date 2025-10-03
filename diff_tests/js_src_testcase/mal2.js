/// Last modified at 2025年08月11日 星期一 21时43分28秒
var a = 114_514 >> 1_919**810;
for (var i = 0; i < 123; i ++)
	console.log(a)
// 两个参数:
var fn = (x, y) => x * x + y * y

// 无参数:
var _ = () => 3.14

// 可变参数:
var any_fn = (x, y, ...rest) => {
    let i, sum = x + y;
    for (i=0; i<rest.length; i++) {
        sum += rest[i];
    }
    return sum;
}

console.log(fn(1, 2), _(), any_fn(12, 23, 4_5, 0.3_1, .3e+1, -114_51, 0b1101, 0X1_3))
<!-- what can we say? -->
