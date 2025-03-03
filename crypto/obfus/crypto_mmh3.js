// core.js
// 只作为样本以供参考。
var a = [82, 73, 50, 30, 45, 29, 28, 16, 82, 41, 77, 5, 27, 92, 27, 0, 2,
    1423857449, -2, 3, -3, 3432918353, 1555261956, 4, 2847714899, -4, 5,
    -5, 2714866558, 1281953886, 6, -6, 198958881, 1141124467, 2970347812,
    -7, 7, 3110523913, 8, -8, 2428444049, -9, 9, 10, -10, 11, -11, 2563907772,
    12, -12, 13, 2282248934, -13, 2154129355, -14, 14, 15, -15, 16, -16, 17, -17, 18,
    -18, 19, -19, 20, -20, 21, -21, -22, 22, 23, -23, 24, -24, -25, 25, -26, 26, 27,
    -27, 28, -28, 29, -29, -30, 30, 31, -31, -32, 32, -33, 33, -34, 34, -35, 35, -37,
    -36, 36, 37, -38, 39, -39, 38, -41, 41, 40, -40, 42, -43, 43, -42, -45, 45, -44, 44,
    -46, 47, 46, -47, 48, -48, 49, -49, 50, -51, 51, -50, 570562233, 53, -52, -53, 52, 55,
    54, -54, -55, 503444072, -57, -56, 57, 56, 58, -59, -58, 59, 60, 61, -61, -60, 62, 63,
    -63, -62, -66, 711928724, 64, -67, 66, 65, -64, -65, 67, -69, 68, 69, 70, -70, -68,
    -71, 71, -72, 3686517206, -75, -74, 75, 73, 72, 74, -73, 79, 76, -76, 77, -79, -78, 78,
    -77, 3554079995, 82, -80, 80, -83, -82, 81, -81, 83, -85, -84, -86, 86, 84, 85, 87, -87,
    -91, 90, 88, 89, -88, -90, 91, -89, 95, 94, -92, -95, 93, -94, -93, 92, -99, 99, -96, 98,
    -97, -98, 96, 97, -101, 3272380065, 100, -103, 101, 102, -102, -100, 103, 107, -105, 104,
    106, 105, -106, -104, -107, 111, 108, 110, 109, -108, -110, -109, -111, 251722036, -114, 115,
    113, 112, 114, -115, -112, -113, -118, 118, -116, -119, 116, 117, -117, 119, 123, 120, 122, 121,
    -120, -122, -121, -123, 125, 127, 3412177804, 126, 124, -125, -126, -124, -127, -128, 128, -129,
    1843258603, 3803740692, 984961486, 3939845945, 4195302755, 4066508878, 255, 1706088902, 256,
    1969922972, 365, 2097651377, 376229701, 853044451, 752459403, 1000, 426522225, 3772115230, 615818150,
    3904427059, 4167216745, 4027552580, 3654703836, 1886057615, 879679996, 3518719985, 3244367275, 2013776290,
    3373015174, 1759359992, 285281116, 1622183637, 1006888145, 10000, 1231636301, 83908371, 1090812512,
    2463272603, 1373503546, 2596254646, 2321926636, 1504918807, 2181625025, 2882616665, 2747007092,
    3009837614, 3138078467, 397917763, 81470997, 829329135, 2657392035, 956543938, 2517215374,
    2262029012, 40735498, 2394877945, 3266489909, 702138776, 2808555105, 2936675148, 1258607687,
    1131014506, 3218104598, 3082640443, 1404277552, 565507253, 534414190, 1541320221, 1913087877,
    2053790376, 1789927666, 3965973030, 3826175755, 4107580753, 4240017532, 1658658271, 3579855332,
    3708648649, 3453421203, 3317316542, 1873836001, 1742555852, 461845907, 3608007406, 1996959894,
    3747672003, 3485111705, 2137656763, 3352799412, 213261112, 3993919788, 1.01, 3865271297, 4139329115,
    4275313526, 282753626, 1068828381, 2768942443, 2909243462, 936918000, 3183342108, 27492, 141376813,
    1740000, 3050360625, 654459306, 2617837225, 1454621731, 2489596804, 2227061214, 1591671054, 2362670323,
    4294967295, 1308918612, 2246822507, 795835527, 1181335161, 414664567, 4279200368, 1661365465, 1037604311,
    4150417245, 3887607047, 1802195444, 4023717930, 2075208622, 1943803523, 901097722, 628085408, 755167117,
    3322730930, 3462522015, 3736837829, 3604390888, 2366115317, 0.4, 2238001368, 2512341634, 2647816111,
    -0.2, 314042704, 1510334235, 58964, 1382605366, 31158534, 450548861, 3020668471, 1119000684, 3160834842,
    2898065728, 1256170817, 1800000, 2765210733, 3060149565, 3188396048, 2932959818, 124634137, 2797360999,
    366619977, 62317068, -0.26, 1202900863, 498536548, 1340076626, 2405801727, 2265490386, 1594198024,
    1466479909, 2547177864, 249268274, 2680153253, 2125561021, 3294710456, 855842277, 3423369109,
    0.732134444, 3705015759, 3569037538, 1994146192, 1711684554, 1852507879, 997073096, 733239954,
    4251122042, 601450431, 4111451223, 167816743, 3855990285, 3988292384, 3369554304, 3233442989,
    3495958263, 3624741850, 65535, 453092731, -0.9, 2094854071, 1957810842, 325883990, 4057260610,
    1684777152, 4189708143, 3915621685, 162941995, 1812370925, 3775830040, 783551873, 3134207493,
    1172266101, 2998733608, 2724688242, 1303535960, 2852801631, 112637215, 1567103746, 651767980,
    1426400815, 906185462, 2211677639, 1047427035, 2344532202, 2607071920, 2466906013, 225274430,
    544179635, 2176718541, 2312317920, 1483230225, 1342533948, 2567524794, 2439277719, 1088359270,
    671266974, 1219638859, 953729732, 3099436303, 2966460450, 817233897, 2685067896, 2825379669,
    4089016648, 4224994405, 3943577151, 3814918930, 476864866, 1634467795, 335633487, 1762050814,
    1, 2044508324, -1, 3401237130, 3268935591, 3524101629, 3663771856, 1907459465
];
var b = ["", "GrayText", "parent", "幼圆", "plugins", "AdobeExManDetect", "0010", "Google Earth Plugin",
    "Veetle TV Core", "0007", "0004", "0002", "0003", "0000", "0001", "Unity Player", "Skype Web Plugin",
    "WebKit-integrierte PDF", "Bell MT", "0008", "getSupportedExtensions", "setTime", "0009", "SafeSearch",
    "\"", "$", "Univers", "%", "&", "'", "1110", "get plugin string exception", "ThreeDShadow", "+", ",", "-", "Arab",
    "苹果丽细宋", ".", "FUZEShare", "/", "0", "1", "2", "3", "4", "仿宋_GB2312", "5", "6", "InactiveCaptionText", "7",
    "WEBZEN Browser Extension", "8", "9", ":", "DivX Browser Plug-In", ";", "=", "Uplay PC", "canvas exception",
    "A", "B", "C", "D", "E", "微软雅黑", "F", "Harrington", "G", "H", "I", "J", "Gnome Shell Integration", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "Niagara Solid", "T", "SefClient Plugin", "U", "V", "1111", "W", "X", "Y", "Z",
    "Goudy Old Style", "\\", "Roblox Launcher Plugin", "Microsoft Office 2013", "QQMusic", "a", "Eurostile",
    "b", "rmocx.RealPlayer G2 Control.1", "c", "Scripting.Dictionary", "d", "仿宋", "e", "f", "g", "h",
    "Ma-Config.com plugin", "i", "1010", "Casual", "j", "k", "l", "m", "n", "o", "p", "1008", "ct", "doNotTrack",
    "q", "setTimeout", "丽宋 Pro", "r", "Gisha", "getTimezoneOffset", "s", "1005", "1004", "t", "u", "1003", "v",
    "1001", "w", "x", "drawArrays", "y", "z", "{", "}", "~", "font", "1009", "=null; path=/; expires=", "Shell.UIHelper",
    "toDataURL", "WindowText", "language", "do", "丽黑 Pro", "HighlightText", "div", "MenuText",
    "AOL Media Playback Plugin", "Citrix online plug-in", "ec", "Desdemona", "InactiveBorder",
    "RealPlayer", "HELLO", ", 'code':", "em", "npTongbuAddin", "createElement", "phantom", "MS PMincho", "楷体",
    "eval", "ex", "DivX VOD Helper Plug-in", "新细明体", "QuickTimeCheckObject.QuickTimeCheck.1",
    "FlyOrDie Games Plugin", "attachShader", "PlayOn Plug-in", "getTime", "1.01", "Broadway", "fp",
    "Alawar NPAPI utils", "Forte", "hashCode", "方正姚体", "ESN Sonar API", "HPDetect",
    "Bitdefender QuickScan", "IE Tab plugin", "',", "ButtonFace", "cpuClass", "Century Gothic",
    "Online Storage plug-in", "Safer Update", "Msxml2.DOMDocument", "Engravers MT", "Silverlight Plug-In",
    "Google Gears 0.5.33.0", "Citrix ICA Client", "alphabetic", "VDownloader", "华文楷体", "attrVertex",
    "宋体", "cookie", "%22", "%26", "Centaur", "4game", "Rockwell", "LogMeIn Plugin 1.0.0.961",
    "Octoshape Streaming Services", "toGMTString", "th=/", "SumatraPDF Browser Plugin", "PDF.PdfCtrl",
    "fillStyle", "je", "Adobe Ming Std", "TorchHelper", "Franklin Gothic Heavy", "华文仿宋", "Harmony Plug-In",
    "Gigi", "v1.1", "Kino MT", "SimHei", "AliSSOLogin plugin",
    "RealPlayer.RealPlayer(tm) ActiveX Control (32-bit)", "Yandex PDF Viewer", "Citrix Receiver Plug-in",
    "mai", "top", "AcroPDF.PDF", "canvas api exception", "InactiveCaption", "Menu",
    "precision mediump float; varying vec2 varyinTexCoordinate; void main() {   gl_FragColor = vec4(varyinTexCoordinate, 0, 1); }",
    "QQ2013 Firefox Plugin", "Google Update", "华文彩云", "eMusicPlugin DLM6", "Web Components",
    "Babylon ToolBar", "Coowon Update", "InfoText", "rmocx.RealPlayer G2 Control", "iMesh plugin",
    "RealDownloader Plugin", "Symantec PKI Client", "_phantom", "GDL Object Web Plug-in 16.00", "webgl", "华文宋体",
    "screen", "body", "TRIANGLE_STRIP", "n=", "TlwgMono", "':'", "LogMeIn Plugin 1.0.0.935", "function",
    "context.hashCode", "ArchiCAD", "VERTEX_SHADER", "Ubuntu", "Facebook Plugin", "ActiveCaption", "细明体",
    "Malgun Gothic", "News Gothic MT", "CaptionText", "aZbY0cXdW1eVf2Ug3Th4SiR5jQk6PlO7mNn8MoL9pKqJrIsHtGuFvEwDxCyBzA",
    "DejaVu LGC Sans Mono", "Copperplate Gothic Light", "Segoe Print", "Sawasdee", "Bauhaus 93", "Chalkduster",
    "Abadi MT Condensed Light", "Lucida Bright", "Wide Latin", "font detect error",
    "Kozuka Gothic Pr6N", "Html5 location provider", "DivX Plus Web Player", "Vladimir Script",
    "File Downloader Plug-in", "ob", "Adodb.Stream", "Menlo", "callPhantom", "Wolfram Mathematica",
    "CatalinaGroup Update", "Eras Bold ITC", "DevalVRXCtrl.DevalVRXCtrl.1", "JSESSIONID-WYYY", "华文细黑",
    "addBehavior", "pa", "Bitstream Vera Serif", "(function(){return 123;})();", "pi", "Tencent FTN plug-in",
    "removeChild", "Folx 3 Browser Plugin", "useProgram", "hostname", "phantom.injectJs", "ShockwaveFlash.ShockwaveFlash",
    "rgba(102, 204, 0, 0.7)", "AdblockPlugin", "Background", "AgControl.AgControl", "PhotoCenterPlugin1.1.2.2", "GungSeo",
    "s=", "decodeURI", "方正舒体", "华文新魏", "123", "webgl exception", "re", "WMPlayer.OCX", "72px", "AppWorkspace",
    "Highlight", "document", "Yandex Media Plugin", "ESN Launch Mozilla Plugin", "70px 'Arial'", "injectJs", "Loma",
    "BitCometAgent", "Calibri", "Bookman Old Style", "sessionStorage", "Utopia", "compileShader", "escape", "Scrollbar",
    "Window", "14744d95383cd3075DA42C93cDaAe7465CFA5fC0B93B1", "隶书", "Kaspersky Password Manager", "MingLiU-ExtB",
    "get system colors exception", "Skype.Detection", "FileLab plugin", "npAPI Plugin", "not_exist_host", "2d", "ActiveXObject",
    "Dotum", "PDF-XChange Viewer", "PMingLiU", "colorDepth"
];

var c = [
    "Nokia Suite Enabler Plugin", "RealVideo.RealVideo(tm) ActiveX Control (32-bit)", "Magneto",
    "AdobeExManCCDetect", "Gabriola", "Playbill", "navigator", "Rachana", "Tw Cen MT Condensed Extra Bold",
    "QQMiniDL Plugin", "#f60", "fillRect", "=null; path=/; domain=", "Default Browser Helper",
    "French Script MT", "标楷体", "encodeURI", "Umpush", "icp", "华文琥珀", "createProgram", "monospace",
    "ButtonShadow", "Bodoni MT", "STATIC_DRAW", "黑体", "downloadUpdater", "Aliedit Plug-In",
    "PDF integrado do WebKit", "uniformOffset", "encodeURIComponent", "Picasa", "Adobe Fangsong Std",
    "bindBuffer", "AVG SiteSafety plugin", "Orbit Downloader", "color", "hidden", "localStorage",
    "Google Talk Effects Plugin", "indexedDB", "Lucida Fax", "AmazonMP3DownloaderPlugin", "createBuffer",
    "Castellar", "linkProgram", "Californian FB", "ThreeDHighlight", "createShader", "Gulim", "NyxLauncher",
    "YouTube Plug-in", "楷体_GB2312", "SWCtl.SWCtl", "Google Earth Plug-in", "QQDownload Plugin",
    ".music.163.com;.igame.163.com;.music.hz.netease.com", "Norton Identity Safe", "parseInt", "Simple Pass",
    "Colonna MT", "zako", "getUniformLocation", "shaderSource", "Downloaders plugin", "location",
    "Heroes & Generals live", "window", "Showcard Gothic", "微软正黑体", "华文行楷", "Ginger", "RockMelt Update",
    "WindowFrame", "enableVertexAttribArray", "KacstOne",
    "attribute vec2 attrVertex; varying vec2 varyinTexCoordinate; uniform vec2 uniformOffset; void main() {   varyinTexCoordinate = attrVertex + uniformOffset;   gl_Position = vec4(attrVertex, 0, 1); }",
    "Perpetua", "openDatabase", "canvas", "iGetterScriptablePlugin", "Informal Roman", "Nitro PDF Plug-In",
    "Msxml2.XMLHTTP", "华文黑体", "NPLastPass", "ThreeDFace", "LastPass", "::", "parseFloat", "华文隶书", "; ",
    "getAttribLocation", "{'name':", "Nyala", "not_exist_hostname", "\\'", "GFACE Plugin", "undefined",
    "新宋体", "_iuqxldmzr_", "\\.", "Matura MT Script Capitals", "Arial Black", "FangSong",
    "mwC nkbafjord phsgly exvt zqiu, ὠ tphst/:/uhbgtic.mo/levva", "Braggadocio", "Harmony Firefox Plugin",
    "Palace Script MT", "Native Client", "userAgent", "QuickTime.QuickTime", "experimental-webgl",
    "ARRAY_BUFFER", "苹果丽中黑", "Alipay Security Control 3", "Script MT Bold", ", 'browserProp':",
    "TDCCtl.TDCCtl", "self", "InfoBackground", "Pando Web Plugin", "Haettenschweiler", "span", "ActiveBorder",
    "ThreeDLightShadow", "0202", "0203", "0200", "0201", "WPI Detector 1.4", "; expires=", "ThreeDDarkShadow",
    "Exif Everywhere", "Battlelog Game Launcher", "Impact", "VLC Multimedia Plugin", "Adobe Hebrew",
    "BlueStacks Install Detector", "wwwmmmmmmmmmmlli", "history", "sans-serif", "Papyrus", "ButtonText", "0211",
    "AppUp", "Parom.TV player plugin", "DealPlyLive Update", "Lohit Gujarati", "FRAGMENT_SHADER", "Agency FB",
    "MacromediaFlashPaper.MacromediaFlashPaper", "###", "WordCaptureX", "getComputedStyle", "platform", "0105",
    "Arabic Typesetting", "0106", "0103", "华文中宋", "0104", "0101", "0102", "0100", "0107", "ButtonHighlight",
    "vertexAttribPointer", "0108", "textBaseline", "#069", "doubleTwist Web Plugin", "unescape",
    "Thunder DapCtrl NPAPI Plugin", "Batang", "DFKai-SB", "Snap ITC"
];

var J = ["uniform2f"], Ja = ['MoolBoran'],
    B = ["Date", "MinibarPlugin", "decodeURIComponent", "NPPlayerShell",
        "MS Reference Sans Serif", "Hiragino Sans GB", "serif", "getContext"];

function M(h) {
    var c = a[88], d, f, e, g, k, m;
    d = h.length & a[19];
    f = h.length - d;
    e = c;
    c = a[21];
    g = a[375];
    // console.log(c, g, e, h[0], h[1], h[2], h[3])
    // e = 31.
    for (m = 0; m < f;)
        k = h.charCodeAt(m) & a[299] | (h.charCodeAt(++m) & a[299]) << a[38] | (h.charCodeAt(++m) & a[299]) << a[58] | (h.charCodeAt(++m) & a[299]) << a[74],
            ++m,
            k = (k & a[486]) * c + (((k >>> a[58]) * c & a[486]) << a[58]) & a[405],
            k = k << a[56] | k >>> a[60],
            k = (k & a[486]) * g + (((k >>> a[58]) * g & a[486]) << a[58]) & a[405],
            e ^= k, // seed: e.
            e = e << a[50] | e >>> a[64],
            e = (e & a[486]) * a[26] + (((e >>> a[58]) * a[26] & a[486]) << a[58]) & a[405],
            e = (e & a[486]) + a[394] + (((e >>> a[58]) + a[435] & a[486]) << a[58]);
    k = 0;
    switch (d) {
        case a[19]:
            k ^= (h.charCodeAt(m + a[16]) & a[299]) << a[58];
        case a[16]:
            k ^= (h.charCodeAt(m + a[541]) & a[299]) << a[38];
        case a[541]:
            k ^= h.charCodeAt(m) & a[299],
                k = (k & a[486]) * c + (((k >>> a[58]) * c & a[486]) << a[58]) & a[405],
                k = k << a[56] | k >>> a[60],
                k = (k & a[486]) * g + (((k >>> a[58]) * g & a[486]) << a[58]) & a[405],
                e ^= k
    }
    e ^= h.length;
    e ^= e >>> a[58];
    e = (e & a[486]) * a[407] + (((e >>> a[58]) * a[407] & a[486]) << a[58]) & a[405];
    e ^= e >>> a[50];
    e = (e & a[486]) * a[349] + (((e >>> a[58]) * a[349] & a[486]) << a[58]) & a[405];
    e ^= e >>> a[58];
    h = e >>> 0;
    d = [];
    d.push(h);
    // 上面是 murmurhash。
    // 下面才比较奇怪。
    try {
        for (var r, B = h + b[0], p = a[15], E = a[15], z = a[15]; z < B.length; z++)
            try {
                var q = parseInt(B.charAt(z) + b[0])
                    , p = q || q === a[15] ? p + q : p + a[541];
                E++
            } catch (n) {
                p += a[541],
                    E++
            }
        E = E == a[15] ? a[541] : E;
        r = ba(p * a[541] / E, N);
        for (var x, C = Math.floor(r / Math.pow(a[43], N - a[541])), G = h + b[0], w = a[15], D = a[15], H = a[15], u = a[15], F = a[15]; F < G.length; F++)
            try {
                var v = parseInt(G.charAt(F) + b[0]);
                v || v === a[15] ? v < C ? (D++,
                    w += v) : (u++,
                        H += v) : (u++,
                            H += C)
            } catch (A) {
                u++,
                    H += C
            }
        u = u == a[15] ? a[541] : u;
        D = D == a[15] ? a[541] : D;
        x = ba(H * a[541] / u - w * a[541] / D, T);
        d.push(ca(r, N, b[41]));
        d.push(ca(x, T, b[41]))
    } catch (y) {
        d = [],
            d.push(h),
            d.push(U(N, b[35]).join(b[0])),
            d.push(U(T, b[35]).join(b[0]))
    }
    return d.join(b[0])
}
function ba(h, c) {
    if (h < 0 || h >= 10)
        throw Error('1110');
    // console.log(0, '0', b[0] + h, b[38], b[0], typeof b[0], b[41]);
    for (var d = U(c, '0'), e = "" + h, f = 0, g = 0; f < d.length && g < e.length; g++) {
        var pmt = e.charAt(g);
        if (pmt === '.') continue;
        d[f++] = pmt;
    }
    return parseInt(d.join(''))
}
function ca(a, c, d) {
    a = b[0] + a;
    if (a.length > c)
        throw Error(b[87]);
    if (a.length == c)
        return a;
    for (var e = [], f = a.length; f < c; f++)
        e.push(d);
    e.push(a);
    return e.join(b[0])
}
function U(b, c) {
    if (b <= 0)
        return [0];
    for (var d = [], e = 0; e < b; e++)
        d.push(c);
    return d
}

// 改掉所有 a[15] 为 0.
// var payload = 'true###true###true###undefined###undefined######Win32###data:image/png;base64,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###ActiveBorder:rgb(0, 0, 0):ActiveCaption:rgb(0, 0, 0):AppWorkspace:rgb(255, 255, 255):Background:rgb(255, 255, 255):ButtonFace:rgb(240, 240, 240):ButtonHighlight:rgb(240, 240, 240):ButtonShadow:rgb(240, 240, 240):ButtonText:rgb(0, 0, 0):CaptionText:rgb(0, 0, 0):GrayText:rgb(109, 109, 109):Highlight:rgb(0, 120, 215):HighlightText:rgb(255, 255, 255):InactiveBorder:rgb(0, 0, 0):InactiveCaption:rgb(255, 255, 255):InactiveCaptionText:rgb(128, 128, 128):InfoBackground:rgb(255, 255, 255):InfoText:rgb(0, 0, 0):Menu:rgb(255, 255, 255):MenuText:rgb(0, 0, 0):Scrollbar:rgb(255, 255, 255):ThreeDDarkShadow:rgb(0, 0, 0):ThreeDFace:rgb(240, 240, 240):ThreeDHighlight:rgb(0, 0, 0):ThreeDLightShadow:rgb(0, 0, 0):ThreeDShadow:rgb(0, 0, 0):Window:rgb(255, 255, 255):WindowFrame:rgb(0, 0, 0):WindowText:rgb(0, 0, 0)';
// var payload2 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36###zh-CN###24###864x1536###-480######PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf$Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf$Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf$Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf$WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;';
// console.log(0xCC9E2D51 == 3432918353);
// # true
// console.log(M(payload));
