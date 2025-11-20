"""
"playlist_fav-add": {
    type: "GET",
    url: "/api/playlist/subscribe",
    filter: function(e4i) {
        var ds5x = e4i.ext || {};
        e4i.ext = NEJ.X(ds5x, e4i.data);
        e4i.data = {
            id: e4i.ext.id
        }
    },
    format: function(Q4U, e4i) {
        n4r.bb4f.I4M({
            tip: "收藏成功" + (Q4U.point > 0 ? ' 获得<em class="s-fc6">' + Q4U.point + "积分</em>" : "")
        });
        var q4u = e4i.ext;
        q4u.subscribedCount++;
        return q4u
    },
    finaly: function(d4h, e4i) {
        h4l.z4D(p4t.cAg6a, "listchange", d4h);
        h4l.z4D(p4t.cAg6a, "itemchange", {
            attr: "subscribedCount",
            data: d4h.data
        })
    },
    onmessage: function() {
        var lF6z = {
            404: "歌单不存在！",
            501: "歌单已经收藏！",
            506: "歌单收藏数量超过上限！"
        };
        return function(cb4f) {
            n4r.bb4f.I4M({
                type: 2,
                tip: lF6z[cb4f] || "收藏失败，请稍后再试！"
            })
        }
    }()
},
"playlist_fav-del": {
    url: "/api/playlist/unsubscribe",
    type: "GET",
    filter: function(e4i) {
        e4i.id = e4i.data.id = e4i.data.pid
    },
    finaly: function(d4h, e4i) {
        h4l.z4D(p4t.iC6w, "listchange", d4h)
    },
    onmessage: function() {
        var lF6z = {
            404: "歌单不存在！",
            405: "你操作太快了，请休息一会再试！",
            406: "你操作太快了，请休息一会再试！"
        };
        return function(cb4f) {
            n4r.bb4f.I4M({
                tip: lF6z[cb4f],
                type: 2
            })
        }
    }()
},
"""