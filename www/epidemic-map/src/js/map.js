import {Utils} from "./utils";
import {API} from "./server";
import {MAPS} from './maps';
import {getInfo} from "./building";

import * as maptalks from 'maptalks';


let POLYGON = {"Polygon": 1, "MultiPolygon": 1};
let GRAPHS = {'Polygon': maptalks.Polygon, 'MultiPolygon': maptalks.MultiPolygon};


let MapCtl = {
    $this: null,
    mapType: {
        map: "Gaode", //  Baidu OpenStreetMap  Mapbox  Gaode
        type: "1"
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
        let base = {
            urlTemplate: parseInt(this.mapType.type) ? tile.weixing : tile.urlTemplate,
            subdomains: tile.subdomains,
            attribution: tile.attribution,
            opacity : 1,
            spatialReference: tile['spatialReference'] || null
        };
        // 高德2图使用暗色系
        if (this.mapType.map === "Gaode" && this.mapType.type == "1") {
            base['cssFilter'] = 'sepia(80%) invert(90%)';
        }
        return base;
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
        if (this.mapType.map === "Gaode" && this.mapType.type == "0") 
            this.mapConfig.pitch = 0;
        else
            this.mapConfig.pitch = 52;
        return this.mapConfig;
    },
    handleMapMove (p) {
        console.log(1);
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

// 常规地图可视化
function loadPolygon (map, data) {
    let planeLayer = map.getLayer('polygon');
    if (!planeLayer) planeLayer = new maptalks.VectorLayer("polygon").addTo(map);
    let options = {
        'polygon': {
            visible : true,
            cursor : 'pointer',
            shadowBlur : 0,
            shadowColor : 'black',
            draggable : false,
            dragShadow : false,
            drawOnAxis : null,
            symbol: {
                'lineColor' : '#f00',
                'lineWidth' : 1,
                'polygonFill' : '#F55253',
                'polygonOpacity' : 0.5,
                'lineColorHighlight' : '#f00',
                'polygonFillHighlight' : '#f00',
            }
        }
    };
    let option = options['polygon'];
    data.features.forEach(function (f) {
        let tp = f.geometry.type;
        if (!POLYGON[tp]) return;
        let polygon = new GRAPHS[tp](f.geometry.coordinates, option);
        polygon.addTo(planeLayer);
        createLabel(f).addTo(planeLayer);
        // polygon.on('click', , this);
    });
}

function createLabel (feature) {
    let pos = feature.properties.cp;
    let name = feature.properties.name;
    let coord = [pos[0], pos[1] - 0.0012];
    let label = new maptalks.Label(name,
        coord,
        {
            'draggable' : true,
            'textSymbol': {
                'textFaceName' : 'monospace',
                'textFill' : '#f00',
                'textHaloFill' : '#fff',
                'textHaloRadius' : 4,
                'textSize' : 18,
                'textWeight' : 'bold',
                'textVerticalAlignment' : 'top'
            },
            'boxStyle' : {
                'padding' : [12, 8],
                'symbol' : {
                    'markerFill' : '#FF7F50'
                }
            }
        }
    );
    label.setInfoWindow(getInfo(feature));
    label.on('click', function () {
        this.openInfoWindow();
    });
    return label;
}

export {MapCtl, POLYGON, GRAPHS, loadPolygon};