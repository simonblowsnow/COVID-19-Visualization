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
    var threeLayer = new ThreeLayer('t', {
        forceRenderOnMoving: true,
        forceRenderOnRotating: true
        // animation: true
    });
    let meshs = [];
    let material = new THREE.MeshBasicMaterial({ color: '#F55253', transparent: true });
    let highlightmaterial = new THREE.MeshBasicMaterial({ color: 'red', transparent: true });

    threeLayer.prepareToDraw = function (gl, scene) {
        var light = new THREE.DirectionalLight(0xffffff);
        light.position.set(0, -10, 10).normalize();
        scene.add(light);
        data.features.forEach(function (g) {
            var heightPerLevel = 50;
            var levels = g.properties.levels || 6;
            var mesh = threeLayer.toExtrudePolygon(maptalks.GeoJSON.toGeometry(g), {
                height: levels * heightPerLevel, topColor: '#fff'
            }, material);
            mesh.setInfoWindow({
                title: g.properties.name,
                content: '确诊时间：' + g.properties.date,
                animationDuration: 1,
                autoOpenOn: false
            });

            ['mouseout', 'mouseover'].forEach(function (eventType) {
                mesh.on(eventType, function (e) {
                    if (e.type === 'mouseout') this.setSymbol(material);
                    if (e.type === 'mouseover') this.setSymbol(highlightmaterial);
                });
            });
            meshs.push(mesh);
        });
        threeLayer.addMesh(meshs);
        threeLayer.config('animation', true);
    };
    threeLayer.addTo(map);
}

export {loadBuilding};