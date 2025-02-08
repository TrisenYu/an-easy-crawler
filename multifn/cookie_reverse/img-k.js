// only for reference.
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
window = dom.window;
document = window.document;
XMLHttpRequest = window.XMLHttpRequest;
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
var J = ["uniform2f"], Ja = ['MoolBoran'],
    B = ["Date", "MinibarPlugin", "decodeURIComponent", "NPPlayerShell",
        "MS Reference Sans Serif", "Hiragino Sans GB", "serif", "getContext"];
function k() {
    try {
        var h = document.createElement("canvas")
            , d = h[B[7]](b[354])
            , f = c[105];
        console.log(h, d, f);
        d[c[169]] = b[235];
        d[b[145]] = b[333];
        d[c[169]] = b[202];
        d[b[219]] = c[10];
        // key([d[c[169]], d[b[145]], d[c[169]], d[b[219]]].join('$$$')): 
        //      "top$$$10px sans-serif$$$top$$$#000000"
        // val([b[235],b[333],b[202],c[10]].join("###")): 
        //      "top###70px 'Arial'###alphabetic####f60"
        d[c[11]](a[281], a[541], a[152], a[66]); // "125$$$$1$$$$62$$$$20", $$$$ as spliter
        // d[c[11]] = fillRect
        d[b[219]] = c[170];
        d.fillText(f, a[16], a[56]);
        d[b[219]] = b[313];
        d.fillText(f, a[23], a[60]);
        return h[b[149]]()
    } catch (l) {
        return b[237]
    }
}

var aaa = document.createElement("canvas");
console.log(aaa);
