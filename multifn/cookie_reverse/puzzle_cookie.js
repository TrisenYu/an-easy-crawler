// TODO.
// puzzle.js
"use strict";
function _typeof(e) {
    return (_typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (e) {
        return typeof e
    }
        : function (e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        }
    )(e)
}
function _defineProperty(e, t, r) {
    return t in e ? Object.defineProperty(e, t, {
        value: r,
        enumerable: !0,
        configurable: !0,
        writable: !0
    }) : e[t] = r,
        e
}
function ownKeys(t, e) {
    var r = Object.keys(t);
    if (Object.getOwnPropertySymbols) {
        var n = Object.getOwnPropertySymbols(t);
        e && (n = n.filter(function (e) {
            return Object.getOwnPropertyDescriptor(t, e).enumerable
        })),
            r.push.apply(r, n)
    }
    return r
}
function _objectSpread2(t) {
    for (var e = 1; e < arguments.length; e++) {
        var r = null != arguments[e] ? arguments[e] : {};
        e % 2 ? ownKeys(Object(r), !0).forEach(function (e) {
            _defineProperty(t, e, r[e])
        }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(r)) : ownKeys(Object(r)).forEach(function (e) {
            Object.defineProperty(t, e, Object.getOwnPropertyDescriptor(r, e))
        })
    }
    return t
}
!function (r, f, e, t, l, i) {
    var n = void 0 !== e && e.resolve
        , c = r[t];
    function s(e) {
        this.module = e,
            this.vars = {},
            this.init()
    }
    c || ((c = r[t] = function () {
        this.modules = {}
    }
    ).callbacks = [],
        c.ready = n ? function () {
            return c.instance ? e.resolve(c.instance.vars()) : new e(function (e) {
                return c.callbacks.push(e)
            }
            )
        }
            : function (e) {
                return c.instance ? e(c.instance.vars()) : c.callbacks.push(e)
            }
    ),
        s.prototype.init = function () {
            var n = this;
            this.module.vars.filter(function (e) {
                return "var" === e.fn || "fn" === e.fn
            }).forEach(function (e, t) {
                var r = n["exec" + e.fn];
                r && r.call(n, e)
            })
        }
        ,
        s.prototype.exec = function () {
            var n = this;
            this.module.vars.filter(function (e) {
                return "var" !== e.fn
            }).forEach(function (e, t) {
                var r = n["exec" + e.fn];
                r && r.call(n, e)
            })
        }
        ,
        s.prototype.execvar = function (e) {
            var t = e.name
                , r = e.value;
            this.vars[t] = r
        }
        ,
        s.prototype.execfn = function (e) {
            var t = e.name
                , r = e.value;
            this.vars[t] = r
        }
        ,
        s.prototype.execscript = function (e) {
            var r, n = this, t = e.url, o = e.boot, a = e.attrs, i = this.module.buildInVars, c = void 0 === i ? {} : i;
            (r = f.createElement(l)).src = t;
            var s = a || {};
            Object.keys(s).forEach(function (e) {
                var t = s[e];
                "boolean" == typeof t ? r[e] = t : r.setAttribute(e, t)
            });
            var u = f.getElementsByTagName(l)[0];
            u && u.parentNode ? u.parentNode.insertBefore(r, u) : f.body.appendChild(r),
                o && o.length && (o = o.replace(/\$\{(\s*[A-z0-9_-]+\s*)\}/g, function (e, t) {
                    var r = void 0 !== n.vars[t] ? n.vars[t] : c[t];
                    if (Array.isArray(r) || "object" === _typeof(r))
                        try {
                            r = JSON.stringify(r)
                        } catch (e) {
                            r = Array.isArray(r) ? "[]" : "{}"
                        }
                    return r
                }),
                    r.onload = function () {
                        var e = f.createElement(l);
                        e.innerHTML = o,
                            u && u.parentNode ? u.parentNode.insertBefore(e, u) : f.body.appendChild(e)
                    }
                )
        }
        ;
    var o = c.prototype;
    o.boot = function () {
        var n = this
            , e = i.modules
            , t = i.buildInVars
            , o = void 0 === t ? {} : t
            , a = [];
        (void 0 === e ? [] : e).filter(function (e) {
            var t = n.modules[e.name] = new s(_objectSpread2(_objectSpread2({}, e), {}, {
                buildInVars: o
            }))
                , r = Number(t.vars.moduleLoadRate);
            isNaN(r) && (r = r || 1),
                Math.random() < r && a.push(t)
        }),
            a.forEach(function (e) {
                var t = r.__puzzleIgnoreModules__ || [];
                Array.isArray(t) && -1 !== t.indexOf(e.module.name) || e.exec()
            }),
            c.callbacks.forEach(function (e) {
                e(n.vars())
            }),
            c.callbacks = []
    }
        ,
        o.vars = function () {
            var r = this
                , n = {};
            return Object.keys(this.modules).forEach(function (e) {
                var t = r.modules[e];
                n[e] = t.vars
            }),
                n.CP_VARS = i.buildInVars || {},
                n
        }
        ,
        c.instance = new c,
        c.instance.boot()
}(window, document, window.Promise, "puzzle", "script", {
    "version": 48197,
    "env": "",
    "modules": [{
        "name": "music-kickout",
        "vars": [{
            "fn": "script",
            "url": "https://st.music.163.com/music-kick/kickout.min.js",
            "attrs": {
                "async": true
            },
            "boot": "(function() {\n    var runDomains = ${runDomains};\n    if (CMKickOutSDK) {\n        CMKickOutSDK.init({runDomains});\n    }\n})()"
        }, {
            "fn": "var",
            "name": "on",
            "value": true
        }, {
            "fn": "var",
            "name": "moduleLoadRate",
            "value": 1
        }, {
            "fn": "var",
            "name": "runDomains",
            "value": []
        }]
    }, {
        "name": "browser-get",
        "vars": [{
            "fn": "script",
            "url": "https://st.music.163.com/browser-get/getBrowser.js",
            "attrs": {
                "async": false
            },
            "boot": "(function() {\n    if (window[\"device_updateDeviceInfo\"]) {\n        var delayTime = ${delayTime};\n        window[\"device_updateDeviceInfo\"](delayTime);\n    }\n})()"
        }, {
            "fn": "var",
            "name": "on",
            "value": true
        }, {
            "fn": "var",
            "name": "moduleLoadRate",
            "value": 1
        }, {
            "fn": "var",
            "name": "delayTime",
            "value": 4000
        }]
    }, {
        "name": "MainsiteUplinkSms",
        "vars": [{
            "fn": "script",
            "url": "https://st.music.163.com/g/ct-web-smsup/smsUpLink.main.js"
        }, {
            "fn": "var",
            "name": "on",
            "value": true
        }, {
            "fn": "var",
            "name": "moduleLoadRate",
            "value": 1
        }]
    }, {
        "name": "WebDeviceId",
        "vars": [{
            "name": "timeout",
            "fn": "var",
            "value": 6000
        }, {
            "fn": "script",
            "url": "https://st.music.163.com/device/signature/create/deviceid.js",
            "boot": "(function() {\n\tvar appId = '${appId}';\n\tvar timeout = ${timeout} || 6000;\n\tvar apiServer = '${apiServer}';\n\tvar cookieName = '${cookieName}' || 'sDeviceId';\n        var deviceType = '${deviceType}' || 'WebOnline';\n  if (NesDeviceId) {\n\t\tNesDeviceId({appId, timeout, apiServer, cookieName, deviceType});\n\t}\n})();",
            "attrs": {
                "async": true
            }
        }, {
            "fn": "var",
            "name": "on",
            "value": true
        }, {
            "fn": "var",
            "name": "moduleLoadRate",
            "value": 1
        }, {
            "fn": "var",
            "name": "appId",
            "value": "9d0ef7e0905d422cba1ecf7e73d77e67"
        }, {
            "fn": "var",
            "name": "apiServer",
            "value": "https://fp-upload.dun.163.com"
        }, {
            "fn": "var",
            "name": "cookieName",
            "value": "sDeviceId"
        }, {
            "fn": "var",
            "name": "deviceType",
            "value": "WebOnline"
        }]
    }, {
        "name": "music-encrypt-2_vali",
        "vars": [{
            "fn": "script",
            "url": "https://st.music.163.com/cmf-validator-sdk/validatorsdk.min.js",
            "boot": "(function (){\n\tif(window.CMFrontEncryptedValidator){\n\t\tvar validatorOptions=${options}\n\t\t || {\n\t}\n\t\t;\n\t\tvar env='${CP_ENV}' || 'prod';\n\t\tvar sampleRate=${sampleRate}\n\t\t || 1;\n\t\tvar disable=${disable}\n\t\t || false;\n\t\tvar businessType='${businessType}' || 'music';\n\t\tvar grayReleaseRate=Number(${grayReleaseRate}) || 1;\n\t\tvar showToast=${showToast} || false;\n\t\tvalidatorOptions.grayReleaseRate=grayReleaseRate;\n\t\tvalidatorOptions.showToast=showToast;\n\t\tvalidatorOptions.env=env;\n\t\tvalidatorOptions.businessType=businessType;\n\t\tvalidatorOptions.sampleRate=sampleRate;\n\t\tvalidatorOptions.disable=disable;\n\t\twindow.CMFrontEncryptedValidator(validatorOptions);\n\t}\n})()",
            "attrs": {
                "async": true
            }
        }, {
            "name": "disable",
            "fn": "var",
            "value": false
        }, {
            "name": "options",
            "fn": "var",
            "value": "{\n\"captchaOptions\": {\n  \"qrSize\": 150\n}\n}"
        }, {
            "fn": "var",
            "name": "on",
            "value": true
        }, {
            "fn": "var",
            "name": "moduleLoadRate",
            "value": 1
        }, {
            "fn": "var",
            "name": "sampleRate",
            "value": "1"
        }, {
            "fn": "var",
            "name": "businessType",
            "value": "music"
        }, {
            "fn": "var",
            "name": "grayReleaseRate",
            "value": "1"
        }, {
            "fn": "var",
            "name": "showToast",
            "value": false
        }]
    }, {
        "name": "music-encrypt-sdk_2",
        "vars": [{
            "fn": "script",
            "url": "https://st.music.163.com/cmf-injector-sdk/injectorsdk.min.js",
            "boot": "(function (){\n\tif(window.CMFrontEncryptedSDK){\n\t\tvar disable=${disable} || false;\n\t\tvar injectData=${injectData} || {};\n\t\tvar crawlerVersion= \"${crawlerVersion}\" || \"01\";\n\t\tvar cookieOption=${cookieOption} || {};\n\t\tvar debug=${debug} || false;\n\t\tvar injectSites=${injectSites} || [];\n\t\tvar env='${CP_ENV}' || 'prod';\n\t\tvar isBubbleEncryptResult=${isBubbleEncryptResult} || false;\n                var whiteAPIS=${whiteAPIS} || []\n\t\t\n\t\tvar options={\n\t\t\tenv:env,disable:disable,injectData:injectData,crawlerVersion:crawlerVersion,cookieOption:cookieOption,debug:debug,injectSites:injectSites,isBubbleEncryptResult:isBubbleEncryptResult\n\t\t}\n\t\t;\n\t\twindow.CMFrontEncryptedSDK.init(options);\n\t}\n})()",
            "attrs": {
                "async": true
            }
        }, {
            "name": "disable",
            "fn": "var",
            "value": false
        }, {
            "name": "cookieOption",
            "fn": "var",
            "value": "{\n  \"sameSite\": \"strict\"\n}"
        }, {
            "name": "crawlerVersion",
            "fn": "var",
            "value": "01"
        }, {
            "name": "injectData",
            "fn": "var",
            "value": "{\n\"WEVNSM\": \"1.0.0\"\n} "
        }, {
            "name": "debug",
            "fn": "var",
            "value": false
        }, {
            "name": "injectSites",
            "fn": "var",
            "value": "[]"
        }, {
            "name": "whiteAPIS",
            "fn": "var",
            "value": "[\n    \"ac.dun.163yun.com/v3/d\",\n    \"ac.dun.163.com/v2/config/js\",\n    \"ac.dun.163yun.com/v3/b\",\n    \"ac.dun.163yun.com/v2/b\",\n    \"ac.dun.163yun.com/v2/d\"\n  ]"
        }, {
            "fn": "var",
            "name": "on",
            "value": true
        }, {
            "fn": "var",
            "name": "moduleLoadRate",
            "value": 1
        }, {
            "fn": "var",
            "name": "isBubbleEncryptResult",
            "value": true
        }, {
            "fn": "var",
            "name": "grayReleaseRate",
            "value": 1
        }, {
            "fn": "var",
            "name": "grayReleaseUserIds",
            "value": []
        }]
    }, {
        "name": "music-wapm",
        "vars": [{
            "fn": "script",
            "url": "https://s6.music.126.net/static_public/5c25ca49ac1f4d2d427da0fa/1.6.8/musicapm.min.js",
            "boot": "(function(){\n     if (window.MusicAPM) {\n        var puzzleEnv = '${CP_ENV}' || 'prod';\n        var prodKey = '${appkey}';\n        var testKey = '${test_appkey}';\n        var uploadToTest = puzzleEnv !== 'prod' && testKey;\n        var appKey = uploadToTest ? testKey : prodKey;\n        var uploadServer = uploadToTest ? 'https://qa-wapm.igame.163.com' : 'https://sentry.music.163.com/wapm';\n        var sampleRate = uploadToTest ? 1.0 : ${sampleRate}\n        var udfCDNHostRegString = '${udfCDNHostRegString}'\n\n        var options = {\n           enableSPA: ${enableSPA},\n           hashSPA: ${hashSPA},\n           warningImageSize: ${warningImageSize},\n           filterCropImg: ${filterCropImg},\n           traceLongtask: ${traceLongtask},\n           traceResource: ${traceResource},\n           ignoreUrlPath: ${ignoreUrlPath},\n           uploadServer: uploadServer,\n           syncConfig: false,\n           debug: uploadToTest,\n           sampleRate: sampleRate,\n           vitalsBadline: ${vitalsBadline},\n           pendingRequest: ${pendingRequest},\n           useOverseaDomain: ${useOverseaDomain},\n           udfCDNHostRegString: udfCDNHostRegString\n        };\n        MusicAPM.install(appKey, options);\n   }\n})();",
            "attrs": {
                "async": true
            }
        }, {
            "fn": "var",
            "name": "on",
            "value": true
        }, {
            "fn": "var",
            "name": "moduleLoadRate",
            "value": 1
        }, {
            "fn": "var",
            "name": "appkey",
            "value": "e47f02ee-3307-450b-94c4-a2c7b40255be"
        }, {
            "fn": "var",
            "name": "test_appkey",
            "value": "38cccb2c-9e9d-464e-97af-7f323bb5c973"
        }, {
            "fn": "var",
            "name": "enableSPA",
            "value": true
        }, {
            "fn": "var",
            "name": "hashSPA",
            "value": true
        }, {
            "fn": "var",
            "name": "traceLongtask",
            "value": false
        }, {
            "fn": "var",
            "name": "sampleRate",
            "value": "0.05"
        }, {
            "fn": "var",
            "name": "warningImageSize",
            "value": 200
        }, {
            "fn": "var",
            "name": "filterCropImg",
            "value": false
        }, {
            "fn": "var",
            "name": "udfCDNHostRegString",
            "value": ""
        }, {
            "fn": "var",
            "name": "ignoreUrlPath",
            "value": " [{ rule: /\\/\\d+\\//, target: '/**/' }, { rule: /\\/\\d+$/, target: '/**' }]"
        }, {
            "fn": "var",
            "name": "vitalsBadline",
            "value": {
                "LCP": 5000,
                "CLS": 0.5,
                "FID": 500
            }
        }, {
            "fn": "var",
            "name": "pendingRequest",
            "value": false
        }, {
            "fn": "var",
            "name": "useOverseaDomain",
            "value": true
        }, {
            "fn": "var",
            "name": "traceResource",
            "value": false
        }]
    }, {
        "name": "MainsiteLogin",
        "vars": [{
            "fn": "script",
            "url": "https://st.music.163.com/g/ct-web-login/ctWebLogin.main.js"
        }, {
            "fn": "var",
            "name": "on",
            "value": true
        }, {
            "fn": "var",
            "name": "moduleLoadRate",
            "value": 1
        }]
    }, {
        "name": "music-corona",
        "vars": [{
            "fn": "script",
            "url": "https://s6.music.126.net/static_public/5e7dd9894cb30d2fd378f94f/2.15.0/music-corona.min.js",
            "attrs": {
                "async": true,
                "crossorigin": "anonymous"
            },
            "boot": "(function (){\n\tif(window.MusicCorona){\n\t\tvar puzzleEnv='${CP_ENV}' || 'prod';\n\t\tvar projectId=${id};\n\t\twindow.corona=MusicCorona({\n\t\t    id:projectId,\n\t\t    env:puzzleEnv\n\t    });\n    }\n})();"
        }, {
            "fn": "var",
            "name": "on",
            "value": true
        }, {
            "fn": "var",
            "name": "moduleLoadRate",
            "value": 1
        }, {
            "fn": "var",
            "name": "id",
            "value": 3224
        }]
    }],
    "buildInVars": {
        "CP_ENV": "prod",
        "CP_APP_NAME": "music-web-mainsite",
        "CP_APP_ID": "0002A4"
    }
});
