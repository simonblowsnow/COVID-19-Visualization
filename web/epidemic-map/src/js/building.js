import * as maptalks from 'maptalks';
import * as THREE from "three";
import { ThreeLayer } from 'maptalks.three';

/* 
    地图上3D发光柱状建筑物图
*/


// param:
// map - maptalks instance
// data - GeoJson
function loadBuilding (map, data) {
    let threeLayer = map.getLayer('building');
    let labelLayer = map.getLayer('label');
    if (threeLayer) {
        threeLayer.remove();
        labelLayer.remove();
    }
    threeLayer = new ThreeLayer('building', {
        forceRenderOnMoving: true, forceRenderOnRotating: true
    });
    labelLayer = new maptalks.VectorLayer("label").addTo(map);
    
    let meshs = [];
    let material = new THREE.MeshBasicMaterial({ color: '#F55253', transparent: true });
    let highlightmaterial = new THREE.MeshBasicMaterial({ color: 'red', transparent: true });

    threeLayer.prepareToDraw = function (gl, scene) {
        let light = new THREE.DirectionalLight(0xffffff);
        light.position.set(0, -10, 10).normalize();
        scene.add(light);
        data.features.forEach(function (g) {
            let heightPerLevel = 50;
            let levels = g.properties.levels || 6;
            let mesh = threeLayer.toExtrudePolygon(maptalks.GeoJSON.toGeometry(g), {
                height: levels * heightPerLevel, topColor: '#fff'
            }, material);
            mesh.setInfoWindow(getInfo(g));

            ['mouseout', 'mouseover'].forEach(function (eventType) {
                mesh.on(eventType, function (e) {
                    if (e.type === 'mouseout') this.setSymbol(material);
                    if (e.type === 'mouseover') this.setSymbol(highlightmaterial);
                });
            });
            meshs.push(mesh);
            
            // 增加文字标签
            createLabel(g).addTo(labelLayer); 
        });
        threeLayer.addMesh(meshs);
        threeLayer.config('animation', true);
    };
    threeLayer.addTo(map);
}

function createLabel (feature) {
    let pos = feature.properties.cp;
    let name = feature.properties.name;
    let coord = [pos[0], pos[1] - 0.0022];
    let label = new maptalks.Label(name,
        coord,
        {
            'draggable' : true,
            'textSymbol': {
                'textFaceName' : 'monospace',
                'textFill' : '#34495e',
                'textHaloFill' : '#fff',
                'textHaloRadius' : 4,
                'textSize' : 18,
                'textWeight' : 'bold',
                'textVerticalAlignment' : 'top'
            },
            'boxStyle' : {
                'padding' : [12, 8]
            }
        }
    );
    label.setInfoWindow(getInfo(feature));
    label.on('click', function () {
        this.openInfoWindow();
    });
    return label;
}

// 依赖于css，见Map.vue
function getInfo (feature) {
    return {
        'single' : true,
        'width'  : 283,
        'height' : 105,
        'custom' : true,
        'dx' : -3,
        'dy' : -12,
        'content'   : '<div class="content">' +
          '<div class="pop_title">' + feature.properties.name + '</div>' +
          '<div class="pop_dept">时间：' + feature.properties.date + '</div>' +
          '<div class="arrow"></div>' +
          '</div>'
    };
}
export {loadBuilding, getInfo};