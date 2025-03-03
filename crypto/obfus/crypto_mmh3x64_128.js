// watchman.js
// 只作为样本以供参考。
var a = [0, 2, 1423857449, -2, 1873313359, 3, -3, 1555261956, 4, 2847714899, -1444681467, -4, -1732584194, 5, 1163531501,
    -5, 2714866558, 1281953886, 6, -6, 198958881, 1141124467, 2970347812, 7, -198630844, -7, 3110523913, 8, -8, 2428444049,
    1272893353, 9, -722521979, -9, 10, -10, 11, -11, 2563907772, -12, 12, 2282248934, 13, -13, 2154129355, 14, -14, 15, -15, 16, -16, 17,
    -17, 18, -18, -701558691, -19, 19, 20, -20, 21, -21, 22, -22, 23, -23, 24, -24, -25, 25, -26, 26, -27, 27, 28, -28, 29, -29, 30, -30, 31, -31,
    32, -33, 33, -32, -35, 34, -34, 35, 37, -37, 36, -36, 39, 38, -39, -38, 40, -40, 41, -41, -176418897, -43, 43, 42, -42, 45, 44, -45, -44, -46,
    47, -47, 46, 48, 49, -49, -48, 50, -50, -51, 51, 570562233, -52, -53, 52, 53, 54, 55, -55, -54, 503444072, -56, -57, 57, 56, -58, -59, 59, 58,
    60, -60, -61, 61, 63, 62, -62, -63, -65, 64, 711928724, 67, -64, -67, -66, 66, 65, -68, 71, 68, 70, 69, -70, -69, -71, 75, 3686517206, -72,
    72, -74, -73, 73, -75, 74, -79, -78, -76, 76, 78, 77, -77, 79, -80, 3554079995, -82, -83, 81, 83, -81, 80, 82, 84, 85, -87, -84, 87, -85, -86,
    86, -89, -91, 88, -88, -90, 91, 90, 89, -92, 95, -95, -94, 92, 94, 93, -93, 99, 97, -97, 98, -96, 96, -99, -98, 1735328473, 3272380065, 100,
    101, -103, -100, -101, 102, -102, 103, 105, 107, 104, -106, 106, -105, -107, -104, -110, 109, -108, -109, 111, 110, 108, -111,
    251722036, 112, -115, 115, 114, -114, -112, 113, -113, -116, 118, -117, 119, 117, 116, -119, -118, 123, -120, -122, 120, 121, -121,
    122, -123, 125, 127, 3412177804, -127, 124, -126, 126, -125, -124, -128, 128, -129, 130, 1843258603, 150, 3803740692, 984961486,
    3939845945, 44100, 4195302755, 200, 201, 202, 203, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216,
    217, 218, 221, 222, 223, 225, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 4066508878, 240, 241,
    242, 243, 255, 1706088902, 256, 300, 327, 1969922972, 2097651377, 1291169091, 376229701, 400, 401, 402, 403, 404, 405,
    606105819, 420, 450, 451, 470, 853044451, 500, 512, 701, 702, 703, 707, 704, 705, 706, 708, 709, 710, 711, 712, 713, 752459403, 800, 801,
    802, 803, 804, 658871167, 1000, 426522225, 1236535329, 3772115230, 615818150, 3904427059, 4167216745, 4027552580, 2000, 3654703836,
    1886057615, -145523070, 879679996, 3518719985, 3000, 3244367275, 2013776290, 3373015174, 1390208809, 4500, -1019803690, 5000, 1759359992,
    6000, 285281116, 1622183637, 1006888145, 1231636301, 10000, 83908371, -155497632, 1090812512, 1732584193, 2463272603, 1373503546, 2596254646, 2321926636, 1504918807,
    2181625025, 2882616665, 2747007092, -271733879, 3009837614, 60000, 3138078467, -30611744, -2054922799, -1502002290, -42063, 397917763, 81470997, 829329135,
    2657392035, 956543938, 2517215374, 2262029012, 40735498, 2394877945, 702138776, 2808555105, 38016083, 2936675148, 1258607687, 1131014506, 3218104598, 3082640443,
    1404277552, -1926607734, 565507253, 4283543511, 534414190, 1541320221, 1913087877, 2053790376, -660478335, 1789927666, 3965973030, 3826175755, 4107580753, 4240017532,
    1804603682, 1658658271, 3579855332, -1416354905, 3708648649, 3453421203, -358537222, 3317316542, -1560198380, -1473231341, 1873836001, 1742555852,
    3608007406, 1996959894, 3747672003, -1990404162, -995338651, 3485111705, 2137656763, -2022574463, 3352799412, 213261112, 3993919788, 1.01,
    3865271297, 4139329115, 4275313526, -405537848, -1094730640, 1549556828, 282753626, 1068828381, 909522486, 2768942443, 2909243462, 936918000, -1044525330,
    3183342108, 141376813, 3050360625, 654459306, 2617837225, 1454621731, 271733878, 2489596804, 76029189, 2227061214, 1591671054, 2362670323,
    4294967296, 4294967295, -40341101, 1308918612, 795835527, 1181335161, 414664567, 4279200368, 1661365465, 1839030562, 1037604311, 4150417245,
    3887607047, 1802195444, 4023717930, 2075208622, -165796510, 1943803523, 901097722, 568446438, 628085408, 755167117, 3322730930, 3462522015, 3736837829,
    3604390888, 2366115317, -187363961, 0.4, 2238001368, 2512341634, 2647816111, -1120210379, -0.2, 314042704, 1510334235, -1069501632, 1382605366,
    31158534, 450548861, 643717713, 3020668471, 1119000684, 3160834842, 2898065728, 1256170817, 2765210733, 3060149565, 3188396048, 2932959818,
    124634137, 2797360999, -373897302, -1894986606, -1530992060, 366619977, 62317068, -0.26, 1200080426, 1202900863, 498536548,
    1340076626, 1126891415, 2405801727, -1051523, 2265490386, 1594198024, 1466479909, 2547177864, 249268274, 2680153253, 2125561021, 3294710456, 855842277, 3423369109,
    0.732134444, 3705015759, 3569037538, 1994146192, -45705983, 1711684554, 1852507879, 997073096, -421815835, 289559509, 733239954, 4251122042, 601450431,
    4111451223, 167816743, 3855990285, 3981806797, 3988292384, 3369554304, 3233442989, 3495958263, 3624741850, 65535, 453092731, -0.9, 2094854071, 1957810842,
    325883990, 4057260610, 1684777152, 4189708143, 3915621685, 162941995, 1812370925, 3775830040, 783551873, 3134207493, 1172266101, 2998733608, 2724688242, 1303535960,
    2852801631, 112637215, 1567103746, 444984403, 651767980, 1426400815, -1958414417, -51403784, -680876936, 906185462, 2211677639, 1047427035, -57434055, 2344532202, 2607071920,
    681279174, 2466906013, 225274430, 544179635, 2176718541, 2312317920, 1483230225, 1342533948, 2567524794, 2439277719, 1088359270, 1309151649, 671266974, -343485551,
    1219638859, 718787259, 953729732, 2277735313, 3099436303, 2966460450, 817233897, 2685067896, 2825379669, -35309556, 4089016648, 530742520, 4224994405, 3943577151,
    3814918930, 1700485571, 0.25, -640364487, 476864866, 944331445, 1634467795, 335633487, 1762050814, -378558, -1, 1, 2044508324, 3401237130, 3268935591, 3524101629, 3663771856,
    1770035416, 1907459465, -389564586, 3301882366
];
var b = ["closePath", "release", "WebGLRenderingContext", "focus", "ipod", "_orientation", "UPDATE_FUNC_TIMING",
    "number", "navigation", "alphabetic", "mspointerup", "_motion", "getOwnPropertyDescriptor",
    "webgl fragment shader high float precision rangeMin:", "__webdriver_unwrapped", "e2891084", "attrVertex",
    "webgl fragment shader low int precision rangeMin:", "cookie", "%22", ").", "webgl max render buffer size:",
    "pike", "ip", "dns", "%26", "script", "Mac", "rgb(0,255,255)", "driver", "DEPTH_BITS", "fontSize", "fillStyle",
    "PDF.PdfCtrl", "interval", "ALPHA_BITS", "status", "Interval", "charset", "webgl max vertex attribs:",
    "webgl red bits:", "Max", "WEBKIT_EXT_texture_filter_anisotropic", "MAX_FRAGMENT_UNIFORM_VECTORS",
    "devicemotion", "send device data failed", "UPDATE_OPTIONS", "mac",
    "RealPlayer.RealPlayer(tm) ActiveX Control (32-bit)", "xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx", "top",
    "webgl vertex shader medium int precision rangeMax:", "MAX_TEXTURE_SIZE", "AcroPDF.PDF", "MAX_VIEWPORT_DIMS",
    " this is null or not defined", "MAX_VERTEX_UNIFORM_VECTORS", "_Selenium_IDE_Recorder", "java.lang.System.exit",
    "max", "touchstart", "hardwareConcurrency", "knee", "availWidth", "documentMode", ", ",
    "MAX_TEXTURE_MAX_ANISOTROPY_EXT", "rmocx.RealPlayer G2 Control", "getToken", "complete", "availHeight",
    "_phantom", "auto", "opera", "ARRAY", "webgl", "RED_BITS", "pointerdown", "precision", "screen", "超时了", "body",
    "TRIANGLE_STRIP", "MAX_RENDERBUFFER_SIZE", "clientWidth", "ontouchstart", "function", "context.hashCode",
    "readyState", "mmmmmmmmmmlli", "oncomplete", "VERTEX_SHADER", "\"this\" is null or not defined",
    "browserLanguage", "level", "UTF-8", "webgl fragment shader high int precision:", "__supportCaptcha__",
    "Android", "innerWidth", "200", " - ", "Failed to load ", "UPDATE_TIME_OFFSET", "position",
    "send devicedata failed: ", "cannot got value", "no", "[object Array]", "webgl max viewport dims:", "Windows",
    "BLUE_BITS", "webgl vertex shader medium int precision:", "head", "rect", "hasOwnProperty",
    "reduce called on null or undefined", "ALIASED_POINT_SIZE_RANGE", "Adodb.Stream", "webgl green bits:",
    "BatteryManager", "callPhantom", "floor", "__driver_unwrapped", "beta", "on", "RENDERER", "src",
    "DevalVRXCtrl.DevalVRXCtrl.1", "globalCompositeOperation", "addBehavior", "&nbsp;", "spawn", "HIGH_INT",
    "rangeMax", "batteryInterval", "CAT_WEBGL", "(function(){return 123;})();", "20030107", "stringify",
    "compatMode", "Windows Phone", "isPrototypeOf", "extensions:", "🧥🐶🍏⚽️✂🈲🚗⌚️❤️🏁▶", " is not a function",
    "NEWatchmanError", "00000000", "removeChild", "webgl aliased line width range:", "webgl max texture size:",
    "webgl vertex shader low int precision rangeMax:", "send behaviordata failed: ", "useProgram", "domAutomation",
    "hostname", "XDomainRequest", "Watchman", "requestStart", "phantom.injectJs", "clearTimeout", "ERROR",
    "touchend", "state", "webgl max anisotropy:", "ShockwaveFlash.ShockwaveFlash", "height",
    "webgl vertex shader medium int precision rangeMin:", "EXT_texture_filter_anisotropic", "/v2/collect",
    "AgControl.AgControl", "touchmove", "decodeURI", "clientHeight", "Firefox", "input", "123",
    "__webdriver_script_func", "WMPlayer.OCX", "72px", "webgl vertex shader low float precision:",
    "propertyIsEnumerable", "onreadystatechange", "safari", "behavior api response wrong", "document", "dns_city",
    "webgl fragment shader high float precision rangeMax:", "deviceorientation", "battery", "-9999px",
    "userLanguage", "businessKey is illegal", "pointermove", "arc", "SHADING_LANGUAGE_VERSION", "min", "attack",
    "LOW_FLOAT", "sessionStorage", "Object prototype may only be an Object: ", "compileShader", "iframe", "escape",
    "mspointermove", "systemLanguage", "languages", "Skype.Detection", "2d", "ActiveXObject", "absolute",
    "offsetHeight", "STRING", "XMLHttpRequest", "The server has encountered an error", "colorDepth", "open",
    "gamma", "domain=", "webgl vertex shader medium float precision rangeMin:", "ratio", "Other",
    "RealVideo.RealVideo(tm) ActiveX Control (32-bit)", "OfflineAudioContext", "webgl blue bits:", "navigator",
    "mspointerdown", "#f60", "webgl fragment shader medium int precision:", "isNaN", "fillRect", "frequency",
    "loaded", "encodeURI", "attachEvent", "webgl max vertex texture image units:", "MAX_VERTEX_TEXTURE_IMAGE_UNITS",
    "up", "webgl fragment shader high int precision rangeMax:", "device api response wrong", "createProgram",
    "GREEN_BITS", "isTrusted", "pageXOffset", "NUMBER", "innerHeight", "monospace", "clientY", "clientX",
    "constructor", "STATIC_DRAW", "productSub", "BOOLEAN", "opr", "MAX_TEXTURE_IMAGE_UNITS", "abort",
    "dAWsBhCqtOaNLLJ25hBzWbqWXwiK99Wd", "dns_province", "webgl aliased point size range:", "uniformOffset",
    "encodeURIComponent", "toLocaleString", "documentElement", "bindBuffer", "onerror", "string", "MEDIUM_FLOAT",
    "responseEnd", "MAX_COMBINED_TEXTURE_IMAGE_UNITS", "localStorage", "android", "canvas fp:", "destination",
    "description", "indexedDB", "createBuffer", "__driver_evaluate", "linkProgram", "button", "linux",
    "createShader", "Chrome", "normal", "webgl stencil bits:", "trident",
    "Reduce of empty array with no initial value", "yes", "SWCtl.SWCtl", "valueOf",
    "webgl vertex shader medium float precision:", "start", "WoeTpXnDDPhiAvsJUUIY3RdAo2PKaVwi", "createOscillator",
    "Does not support CORS", "detachEvent", "target", "parseInt", "gbk", "getUniformLocation", "WM_CONFIG",
    "\\((.+)\\)$", "shaderSource", "location", "HEX", "window", "initNEWatchman", "disconnect", "appVersion",
    "mousemove", "type", "webgl fragment shader medium float precision rangeMin:",
    "webgl vertex shader high int precision rangeMin:", "enableVertexAttribArray", "javaEnabled", "oscpu",
    "webgl fragment shader medium int precision rangeMax:", "options",
    "webgl vertex shader low float precision rangeMax:", "MAX_VARYING_VECTORS", "WM_NIKE", "openDatabase",
    "getParameter", "Buffer", "STENCIL_BITS", "canvas", "HIGH_FLOAT",
    "webgl vertex shader low int precision rangeMin:", ": ", "scroll", "batteryMax", "WM_NI", "DEPTH_BUFFER_BIT",
    "createDynamicsCompressor", "iphone", "webgl fragment shader low float precision:", "ip_province",
    "__selenium_evaluate", "Msxml2.XMLHTTP", "/v3/b", "pageYOffset", "GET", "style", "depthFunc", "Opera",
    "Can not find configuration", "::", "parseFloat", "webgl fragment shader low float precision rangeMin:",
    "getAttribLocation", "utf8", "webgl unmasked renderer:", "triangle", "unknown", "undefined", "\\.", "WM_DIV",
    "WM_TID", "event", "getExtension", "cache_", "offsetWidth", "userAgent", "QuickTime.QuickTime", "JSCookie",
    "experimental-webgl", "dischargingTime", "__nightmare", "ARRAY_BUFFER", "MEDIUM_INT", "request resource error",
    "withCredentials", "ip_city", "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/", "Missing business key",
    "width", "webgl max fragment uniform vectors:", "VERSION", "TDCCtl.TDCCtl", "self", "lineHeight",
    "ef8c9f09464240e5974d364643e19e27", "Sequentum", "span", "msg", "innerHTML", "cookieEnabled", "rhino",
    "firefox", "threshold", "appCodeName", "Netscape", "bb99db1_7", "bb99db1_6", "bb99db1_5", "protocol",
    "fontFamily", "bb99db1_4", "webgl max texture image units:", "bb99db1_9", "://", "scrollLeft", "bb99db1_3",
    "bb99db1_2", "bb99db1_1", "__fxdriver_evaluate", "[object Function]", "timing", "toSource", "CAT_FONTS",
    "Cwm fjordbank glyphs vext quiz, 😅😥👶😃🧥🐶🍏⚽️✂🈲🚗⌚️❤️🏁▶", "WM_DID", "application/x-www-form-urlencoded",
    "Response is empty", "0123456789abcdef", "sans-serif", "webgl max combined texture image units:",
    "webgl vertex shader high float precision rangeMin:", "history",
    "webgl vertex shader medium float precision rangeMax:", "webgl fragment shader high int precision rangeMin:",
    "scrollTop", "webgl vertex shader high int precision:", "FRAGMENT_SHADER", "ipad", "rgba(102, 204, 0, 0.2)",
    "MacromediaFlashPaper.MacromediaFlashPaper", "send", "domAutomationController", "screenX", "?&",
    "ALIASED_LINE_WIDTH_RANGE", "renderedBuffer", "Failed to load script(", "platform", "CSS1Compat", "clearColor",
    "getAttribute", "array", "setInterval",
    "This browser's implementation of Object.create is a shim and doesn't support a second argument.",
    "createEvent", "getBattery", "webgl vertex shader high int precision rangeMax:", "value", "win",
    "vertexAttribPointer", "__webdriver_script_function", "srcElement"
];
function da(b, f) {
    b = [b[0] >>> a[49], b[0] & a[602], b[1] >>> a[49], b[1] & a[602]];
    f = [f[0] >>> a[49], f[0] & a[602], f[1] >>> a[49], f[1] & a[602]];
    var e = [a[0], a[0], a[0], a[0]];
    e[3] += b[3] + f[3];
    e[2] += e[3] >>> a[49];
    e[3] &= a[602];
    e[2] += b[2] + f[2];
    e[1] += e[2] >>> a[49];
    e[2] &= a[602];
    e[1] += b[1] + f[1];
    e[0] += e[1] >>> a[49];
    e[1] &= a[602];
    e[0] += b[0] + f[0];
    e[0] &= a[602];
    return [e[0] << a[49] | e[1], e[2] << a[49] | e[3]]
}
function Q(b, f) {
    b = [b[0] >>> a[49], b[0] & a[602], b[1] >>> a[49], b[1] & a[602]];
    f = [f[0] >>> a[49], f[0] & a[602], f[1] >>> a[49], f[1] & a[602]];
    var e = [a[0], a[0], a[0], a[0]];
    e[3] += b[3] * f[3];
    e[2] += e[3] >>> a[49];
    e[3] &= a[602];
    e[2] += b[2] * f[3];
    e[1] += e[2] >>> a[49];
    e[2] &= a[602];
    e[2] += b[3] * f[2];
    e[1] += e[2] >>> a[49];
    e[2] &= a[602];
    e[1] += b[1] * f[3];
    e[0] += e[1] >>> a[49];
    e[1] &= a[602];
    e[1] += b[2] * f[2];
    e[0] += e[1] >>> a[49];
    e[1] &= a[602];
    e[1] += b[3] * f[1];
    e[0] += e[1] >>> a[49];
    e[1] &= a[602];
    e[0] += b[0] * f[3] + b[1] * f[2] + b[2] * f[1] + b[3] * f[0];
    e[0] &= a[602];
    return [e[0] << a[49] | e[1], e[2] << a[49] | e[3]]
}
function sa(b, f) {
    f %= a[150];
    if (f === a[82])
        return [b[1], b[0]];
    if (f < a[82])
        return [b[0] << f | b[1] >>> a[82] - f, b[1] << f | b[0] >>> a[82] - f];
    f -= a[82];
    return [b[1] << f | b[0] >>> a[82] - f, b[0] << f | b[1] >>> a[82] - f]
}
function O(b, f) {
    f %= a[150];
    return f === a[0] ? b : f < a[82] ? [b[0] << f | b[1] >>> a[82] - f, b[1] << f] : [b[1] << f - a[82], a[0]]
}
function F(a, b) {
    return [a[0] ^ b[0], a[1] ^ b[1]]
}
function Ib(b) {
    b = F(b, [a[0], b[0] >>> a[675]]);
    b = Q(b, [a[445], a[596]]);
    b = F(b, [a[0], b[0] >>> a[675]]);
    b = Q(b, [a[684], a[624]]);
    return b = F(b, [a[0], b[0] >>> a[675]])
}

function za(d, f) {
    d = d || c[150];
    f = f || a[0];
    for (var e = d.length % a[49], q = d.length - e, l = [a[0], f], u = [a[0], f], m = [a[0], a[0]], r = [a[0], a[0]], ra = [a[653], a[589]], g = [a[340], a[375]], k = a[0]; k < q; k += a[49])
        m = [d.charCodeAt(k + a[8]) & a[333] | (d.charCodeAt(k + a[13]) & a[333]) << a[27] | (d.charCodeAt(k + a[18]) & a[333]) << a[49] | (d.charCodeAt(k + a[23]) & a[333]) << a[66], d.charCodeAt(k) & a[333] | (d.charCodeAt(k + a[675]) & a[333]) << a[27] | (d.charCodeAt(k + a[1]) & a[333]) << a[49] | (d.charCodeAt(k + a[5]) & a[333]) << a[66]],
            r = [d.charCodeAt(k + a[40]) & a[333] | (d.charCodeAt(k + a[42]) & a[333]) << a[27] | (d.charCodeAt(k + a[45]) & a[333]) << a[49] | (d.charCodeAt(k + a[47]) & a[333]) << a[66], d.charCodeAt(k + a[27]) & a[333] | (d.charCodeAt(k + a[31]) & a[333]) << a[27] | (d.charCodeAt(k + a[34]) & a[333]) << a[49] | (d.charCodeAt(k + a[36]) & a[333]) << a[66]],
            m = Q(m, ra),
            m = sa(m, a[80]),
            m = Q(m, g),
            l = F(l, m),
            l = sa(l, a[73]),
            l = da(l, u),
            l = da(Q(l, [a[0], a[13]]), [a[0], a[394]]),
            r = Q(r, g),
            r = sa(r, a[84]),
            r = Q(r, ra),
            u = F(u, r),
            u = sa(u, a[80]),
            u = da(u, l),
            u = da(Q(u, [a[0], a[13]]), [a[0], a[669]]);
    m = [a[0], a[0]];
    r = [a[0], a[0]];
    switch (e) {
        case a[47]:
            r = F(r, O([a[0], d.charCodeAt(k + a[45])], a[115]));
        case a[45]:
            r = F(r, O([a[0], d.charCodeAt(k + a[42])], a[98]));
        case a[42]:
            r = F(r, O([a[0], d.charCodeAt(k + a[40])], a[82]));
        case a[40]:
            r = F(r, O([a[0], d.charCodeAt(k + a[36])], a[66]));
        case a[36]:
            r = F(r, O([a[0], d.charCodeAt(k + a[34])], a[49]));
        case a[34]:
            r = F(r, O([a[0], d.charCodeAt(k + a[31])], a[27]));
        case a[31]:
            r = F(r, [a[0], d.charCodeAt(k + a[27])]),
                r = Q(r, g),
                r = sa(r, a[84]),
                r = Q(r, ra),
                u = F(u, r);
        case a[27]:
            m = F(m, O([a[0], d.charCodeAt(k + a[23])], a[136]));
        case a[23]:
            m = F(m, O([a[0], d.charCodeAt(k + a[18])], a[115]));
        case a[18]:
            m = F(m, O([a[0], d.charCodeAt(k + a[13])], a[98]));
        case a[13]:
            m = F(m, O([a[0], d.charCodeAt(k + a[8])], a[82]));
        case a[8]:
            m = F(m, O([a[0], d.charCodeAt(k + a[5])], a[66]));
        case a[5]:
            m = F(m, O([a[0], d.charCodeAt(k + a[1])], a[49]));
        case a[1]:
            m = F(m, O([a[0], d.charCodeAt(k + a[675])], a[27]));
        case a[675]:
            m = F(m, [a[0], d.charCodeAt(k)]),
                m = Q(m, ra),
                m = sa(m, a[80]),
                m = Q(m, g),
                l = F(l, m)
    }
    l = F(l, [a[0], d.length]);
    u = F(u, [a[0], d.length]);
    l = da(l, u);
    u = da(u, l);
    l = Ib(l);
    u = Ib(u);
    l = da(l, u);
    u = da(u, l);
    return (b[147] + (l[0] >>> a[0]).toString(a[49])).slice(a[28]) + (b[147] + (l[1] >>> a[0]).toString(a[49])).slice(a[28]) + (b[147] + (u[0] >>> a[0]).toString(a[49])).slice(a[28]) + (b[147] + (u[1] >>> a[0]).toString(a[49])).slice(a[28])
}