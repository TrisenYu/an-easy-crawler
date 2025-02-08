(function () {
    var appId = '9d0ef7e0905d422cba1ecf7e73d77e67';
    var timeout = 6000 || 6000;
    var apiServer = 'https://fp-upload.dun.163.com';
    var cookieName = 'sDeviceId' || 'sDeviceId';
    var deviceType = 'WebOnline' || 'WebOnline';
    if (NesDeviceId) {
        NesDeviceId({ appId, timeout, apiServer, cookieName, deviceType });
    }
})();
(function () {
    if (window["device_updateDeviceInfo"]) {
        var delayTime = 4000;
        window["device_updateDeviceInfo"](delayTime);
    }
})();
(function () {
    if (window.CMFrontEncryptedSDK) {
        var disable = false || false;
        var injectData = {
            "WEVNSM": "1.0.0"
        } || {};
        var crawlerVersion = "01" || "01";
        var cookieOption = {
            "sameSite": "strict"
        } || {};
        var debug = false || false;
        var injectSites = [] || [];
        var env = 'prod' || 'prod';
        var isBubbleEncryptResult = true || false;
        var whiteAPIS = [
            "ac.dun.163yun.com/v3/d",
            "ac.dun.163.com/v2/config/js",
            "ac.dun.163yun.com/v3/b",
            "ac.dun.163yun.com/v2/b",
            "ac.dun.163yun.com/v2/d"
        ] || []

        var options = {
            env: env, disable: disable, injectData: injectData, crawlerVersion: crawlerVersion, cookieOption: cookieOption, debug: debug, injectSites: injectSites, isBubbleEncryptResult: isBubbleEncryptResult
        }
            ;
        window.CMFrontEncryptedSDK.init(options);
    }
})();

/*
    this.injectCookieName = "WNMCID",
    this.injectCookieValue = "",
 */
// this.injectCookieValue = "".concat(Rt(), ".").concat(Date.now().toString(), ".").concat(this.sdkOptions.crawlerVersion || "01", ".0")
// 8.01.0
// Rt() = () {
//      var Mt = "abcdefghijklmnopqrstuvwxyz";
//      for (var e = "", t = 0; t < 6; t++)
//          e += Mt.charAt(Math.floor(Math.random() * Mt.length));
//      return e
// }