<template>
    <div id="map" style="">地图</div>
</template>

<script>
// import {Utils} from "../js/utils";
import {MapCtl, POLYGON, GRAPHS} from "../js/map";
import {Provinces} from "../js/region";
import * as maptalks from 'maptalks';
// import * as THREE from "three";
// import { ThreeLayer } from 'maptalks.three';
// import {loadBuilding} from "../js/building";
import {loadLines3D} from "../js/lines3D";

export default {
    name: 'Map',
    data () {
        return {
            map: null,
            planeLayer: null,
            buildingLayer: null,
            currentProvince: "",
            currentCity: ""
        };
    },
    mounted () {
        this.init();
    },
    methods: {
        init () {
            let mapConfig = MapCtl.getConfig();
            this.map = new maptalks.Map('map', mapConfig);
            this.map.on('moveend', MapCtl.handleMapMove);
            this.planeLayer = new maptalks.VectorLayer("polygon").addTo(this.map);
            this.loadProvince("510000");
        },
        loadProvince (code) {
            let $this = this;
            MapCtl.loadData(code, function (features) {
                if (code in Provinces) {
                    // $this.map.setCenter(Provinces[code]);
                    
                    $this.map.setCenter([103.923941, 30.79559]);
                    // $this.map.setZoom(16);
                }
                // $this.loadGeometry(features);
                // $this.loadBuildding(features);
                // loadBuilding($this.map, features);
                loadLines3D($this.map, features);
            });
        },
        resetMap: function () {
            let base = MapCtl.getBase();
            this.map.setBaseLayer(new maptalks.TileLayer('base', base));
        },
        loadGeometry: function (data) {
            let $this = this;
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
                        'lineColor' : '#56435e',
                        'lineWidth' : 1,
                        'polygonFill' : '#5e534c',
                        'polygonOpacity' : 0.5,
                        'lineColorHighlight' : '#f00',
                        'polygonFillHighlight' : '#f00',
                    }
                }
            };
            let option = options['polygon'];
            debugger
            data.features.forEach(function (f) {
                let tp = f.geometry.type;
                if (!POLYGON[tp]) return;
                let polygon = new GRAPHS[tp](f.geometry.coordinates, option);
                polygon.addTo($this.planeLayer);
                // polygon.on('click', $this.handleClickPolygon, this);
            });
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.pageHead {
  height: 100px !important; 
  padding-top: 5px !important;
  padding-bottom: 10px !important;
}
#map {
    height: calc(100% - 115px); 
}


</style>
