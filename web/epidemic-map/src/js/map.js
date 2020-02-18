import {Utils} from "./utils";
import {API} from "./server";
import {MAPS} from './maps';
import * as maptalks from 'maptalks';


let POLYGON = {"Polygon": 1, "MultiPolygon": 1};
let GRAPHS = {'Polygon': maptalks.Polygon, 'MultiPolygon': maptalks.MultiPolygon};

let MapCtl = {
    $this: null,
    mapType: {
        map: "Gaode", //  OpenStreetMap  Mapbox
        type: "0"
    },
    mapConfig: {
        center: [104.071927,30.665132],
        zoom: 14,
        pitch : 52,
        baseLayer: null
    },
    init (that) {
        this.$this = that;
    },
    getBase () {
        // 从缓存加载地图
        let mapStyle = Utils.getCookie("mapStyle");
        if (mapStyle) {
            let ps = mapStyle.split("_");
            this.mapType = {map: ps[0], type: ps[1]};
            this.mapTypes = mapStyle;
        }
        let tile = MAPS[this.mapType.map];
        return {
            urlTemplate: parseInt(this.mapType.type) ? tile.weixing : tile.urlTemplate,
            subdomains: tile.subdomains,
            attribution: tile.attribution,
            opacity : 1,
            cssFilter : 'sepia(80%) invert(90%)',
            spatialReference: tile['spatialReference'] || null
        };
    },
    getConfig (base) {
        base = base || this.getBase();
        this.mapConfig.baseLayer = new maptalks.TileLayer('base', base);
        // 从缓存加载地图信息
        let mapInfo = Utils.getCookie('mapInfo');
        if (mapInfo && mapInfo !== 'undefined') {
            let ps = mapInfo.split("_");
            this.mapConfig.center = [parseFloat(ps[0]), parseFloat(ps[1])];
            this.mapConfig.zoom = parseInt(ps[2]);
        }

        // 是否使用视角倾斜
        if (this.mapType.map in {"Mapbox": 1, "OpenStreetMap": 1} && this.mapType.type == "1") 
            this.mapConfig.pitch = 52;
        else
            this.mapConfig.pitch = 45;
        return this.mapConfig;
    },
    handleMapMove (p) {
        // 记录用户历史位置
        let map = p.target;
        let center = map.getCenter();
        let info = [center.x, center.y, map.getZoom()].join("_");
        Utils.setCookie('mapInfo', info);
    },
    loadData (code, callback) {
        Utils.ajaxData(API.GetDataPos, {'code': code}, function (rst) {
            let features = [];
            rst.data.forEach(d => {
                if (!(d[1] in POLYGON)) return;
                let g = {
                    "type": "Feature",
                    "properties": {
                        "name": d[0], 
                        "cp": d[3] === "Point" ? JSON.parse(d[4]) : [],
                        "levels": 10,
                        "date": d[d.length - 1].substr(0, 10)
                    },
                    "geometry": {"type": d[1], "coordinates": JSON.parse(d[2])}
                };
                features.push(g);
            });
            callback({"features": features, "type": "FeatureCollection"});
        });
    }
}
    
export {MapCtl, POLYGON, GRAPHS};