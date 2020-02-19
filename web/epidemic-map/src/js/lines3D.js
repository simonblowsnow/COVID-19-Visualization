import * as maptalks from 'maptalks';
import * as THREE from "three";
import { ThreeLayer, BaseObject } from 'maptalks.three';
import { InitBloom } from "./bloom";


let threeLayer;

function loadLines3D (map, data) {
    var labelMeshes = [];
    if (map.getLayer('lines')) threeLayer.remove();
    threeLayer = new ThreeLayer('lines', {
        forceRenderOnMoving: true, forceRenderOnRotating: true
    });

    threeLayer.prepareToDraw = function (gl, scene) {
        var light = new THREE.DirectionalLight(0xffffff);
        light.position.set(0, -10, 10).normalize();
        scene.add(light);
        
        this.initBloom();
        this.setRendererRenderScene();

        data.features.forEach(function (g) {
            // if (g.geometry.type == "MultiPolygon") return;
            let name = g.properties.name;
            if (name.length < 5) name += "   "
            let labelMaterial = getMaterial(50, name);
            let label = new Circle(g.properties.cp, {
                len: name.length
            }, labelMaterial, threeLayer);
            labelMeshes.push(label);
        });
        threeLayer.addMesh(labelMeshes);
        addLines(data);
    };
    threeLayer.addTo(map);
    InitBloom();
}

// Polygon to LineString
function translate (data) {
    let geojson = {"features": [], "type": "FeatureCollection"};
    data.features.forEach((g) => {
        // TODO: 处理MultiPolygon
        if (g.geometry.type == "MultiPolygon") return;
        // 框架有一个奇葩的BUG，坐标点序列中不能有连续相同的点，在此简单去重。
        let coordinates = [];
        let cache = new Set();
        g.geometry.coordinates[0].forEach((c, j) => {
            if (!cache.has(c.join("_"))) {
                if (j > 0) cache.add(c.join("_"))
                coordinates.push(c);
            }
        });
        let d = {
            "type": "Feature",
            "properties": {
                "name": g.properties.name, 
                "date": g.properties.date
            },
            "geometry": {"type": "LineString", "coordinates": coordinates}
        }
        geojson.features.push(d);
    })
    return geojson;
}

function addLines(data) {
    var baseLineMaterial = new THREE.LineBasicMaterial({
        linewidth: 1,
        color: 'rgb(255,90,0)',
        // opacity: 0.5,
        blending: THREE.AdditiveBlending,
        transparent: true
    });
    let geojson = translate(data);
    var lineStrings = maptalks.GeoJSON.toGeometry(geojson);
    let baseLines = lineStrings.map(function (d) {
        var line = threeLayer.toLine(d, {}, baseLineMaterial);
        line.getObject3d().layers.enable(1);
        return line;
    });
    threeLayer.addMesh(baseLines);

    addExtrudeLine(lineStrings);
}


function addExtrudeLine(lineStrings) {
    var material = new THREE.MeshBasicMaterial({
        color: 'rgb(255,45,0)', transparent: true, blending: THREE.AdditiveBlending
    });
    var highlightmaterial = new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true });
    var lines = [];
    lineStrings.forEach((d) => {
        let line = threeLayer.toExtrudeLine(d, { altitude: 0, width: 10, height: 50 }, material);
        line.getObject3d().layers.enable(1);
        lines.push(line);
    });
    let lineTrails = [];
    lineStrings.forEach((d) => {
        var line = threeLayer.toExtrudeLineTrail(d, { altitude: 0, width: 10, height: 30, chunkLength: 50, speed: 1, trail: 6 }, highlightmaterial);
        line.getObject3d().layers.enable(1);
        lineTrails.push(line);
    });
    threeLayer.addMesh(lines);
    threeLayer.addMesh(lineTrails);
    animation();
}

function getMaterial(fontSize, text) {
    var SIZE = 400;
    var canvas = document.createElement('canvas');
    canvas.width = SIZE;
    canvas.height = 16 * text.length;
    var ctx = canvas.getContext('2d');
    var gradient = ctx.createLinearGradient(0, 0, SIZE, 0);
    // gradient.addColorStop("0", "#ffffff");
    gradient.addColorStop("0.0", "#ff0000");
    gradient.addColorStop("1.0", "#ff0000");
    // gradient.addColorStop("0.66", "white");
    // gradient.addColorStop("1.0", "red");

    ctx.strokeStyle = gradient;
    // ctx.lineWidth = 20;
    ctx.font = `${fontSize}px Aria`;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillStyle = "#f00";
    ctx.fillText(text, 5, 10);
    // ctx.rect(0, 0, SIZE * 3, SIZE);
    var texture = new THREE.Texture(canvas);
    texture.needsUpdate = true; //使用贴图时进行更新

    var material = new THREE.MeshPhongMaterial({
        map: texture,
        side: THREE.FrontSide,
        transparent: false
    });
    return material;
}

var OPTIONS = {
    len: 4,
    altitude: 0
};

class Circle extends BaseObject {
    constructor(coordinate, options, material, layer) {
        options = maptalks.Util.extend({}, OPTIONS, options, { layer, coordinate });
        super();
        //Initialize internal configuration
        // https://github.com/maptalks/maptalks.three/blob/1e45f5238f500225ada1deb09b8bab18c1b52cf2/src/BaseObject.js#L135
        this._initOptions(options);
        // const { altitude } = options;
        // debugger
        //generate geometry
        // const r = layer.distanceToVector3(radius, radius).x
        const geometry = new THREE.PlaneGeometry(options.len * 1.5, 4.5);

        //Initialize internal object3d
        // https://github.com/maptalks/maptalks.three/blob/1e45f5238f500225ada1deb09b8bab18c1b52cf2/src/BaseObject.js#L140
        this._createMesh(geometry, material);

        //set object3d position
        // const z = layer.distanceToVector3(altitude, altitude).x;
        const position = layer.coordinateToVector3(coordinate, 0);
        this.getObject3d().position.copy(position);
        // this.getObject3d().rotation.x = -Math.PI;
    }
    /**
     * animateShow test
     * 
     * */
    animateShow(options = {}, cb) {
        if (this._showPlayer) {
            this._showPlayer.cancel();
        }
        if (maptalks.Util.isFunction(options)) {
            options = {};
            cb = options;
        }
        const duration = options['duration'] || 1000,
            easing = options['easing'] || 'out';
        const player = this._showPlayer = maptalks.animation.Animation.animate({
            'scale': 1
        }, {
            'duration': duration,
            'easing': easing
        }, frame => {
            const scale = frame.styles.scale;
            if (scale > 0) {
                this.getObject3d().scale.set(scale, scale, scale);
            }
            if (cb) {
                cb(frame, scale);
            }
        });
        player.play();
        return player;
    }
}

function animation() {
    // layer animation support Skipping frames
    threeLayer._needsUpdate = !threeLayer._needsUpdate;
    if (threeLayer._needsUpdate) {
        threeLayer.getRenderer().clearCanvas();
        threeLayer.renderScene();
    }
    requestAnimationFrame(animation);
}


export {loadLines3D};