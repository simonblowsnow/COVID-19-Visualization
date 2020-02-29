<template>
    <div id="root">
        <div id="map" style="height: 100%">地图</div>
        <div style="position: fixed; right: 10px; top: 160px; width: 100px; ">
              <el-select v-model="currentProvince" size="small" placeholder="请选择" @change="loadProvince">
                <el-option
                v-for="item in provinces"
                :key="item.code"
                :label="item.name"
                :value="item.code">
                </el-option>
            </el-select>
        </div>

        <div style="position: fixed; right: 10px; top: 120px; width: 100px">
              <el-select v-model="mapIndex" size="small" placeholder="请选择" @change="resetMap">
                <el-option
                v-for="item in maps"
                :key="item.index"
                :label="item.label"
                :value="item.index">
                </el-option>
            </el-select>
        </div>

        <div style="position: fixed; right: 10px; top: 90px; font-weight: 400; font-family: 宋体;  " class="blink">
            <router-link to="/china">返回</router-link>
        </div>
    </div>
    
    
</template>

<script>
import {MapCtl, loadPolygon} from "../js/map";
import {Provinces} from "../js/region";
import * as maptalks from 'maptalks';
import {loadBuilding} from "../js/building";
import {loadLines3D} from "../js/lines3D";
import { Utils } from '../js/utils';

export default {
    name: 'Map',
    data () {
        return {
            map: null,
            planeLayer: null,
            buildingLayer: null,
            currentProvince: "510000",
            currentCity: "",
            data: null,
            maps: [
                {label: '常规地图', map: 'Gaode', type: '0', index: 0}, 
                {label: '暗黑2.5D', map: 'Gaode', type: '1', index: 1}, 
                {label: '3D场景', map: 'Gaode', type: '1', index: 2}],
            mapIndex: 1,
            provinces: Object.keys(Provinces).map(k => ({code: k, name: Provinces[k].name}))
        };
    },
    mounted () {
        this.mapIndex = parseInt(Utils.getCookie("mapIndex", 1));
        this.init();
        this.loadProvince(this.currentProvince);
    },
    methods: {
        init () {
            let mapConfig = MapCtl.getConfig();
            this.map = new maptalks.Map('map', mapConfig);
            this.map.on('moveend', MapCtl.handleMapMove);
        },
        loadProvince (code) {
            let $this = this;
            MapCtl.loadData(code, function (features) {
                let center = (code in Provinces) ? Provinces[code].cp : null;
                if (features.features[0]) center = features.features[0].properties.cp;
                $this.map.setCenter(center);
                $this.map.setZoom(11);
                $this.data = features;
                $this.loadMap($this.mapIndex, features);
            });
        },
        loadMap (idx, features) {
            let funs = [loadPolygon, loadBuilding, loadLines3D];
            funs[idx](this.map, features);
        },
        resetMap: function (idx) {
            let item = this.maps[idx];
            Utils.setCookie("mapStyle", [item.map, item.type].join("_"));
            Utils.setCookie("mapIndex", idx);
            this.map.remove();
            this.map = null;
            this.init();
            this.loadMap(idx, this.data);
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
#root {
    height: calc(100% - 115px); 
}
a{color: #dd4814}
.el-input__inner { color: #fff; background-color: #0c2c45}
.content{color:#fff;width:190px;height:80px;background-color:#051127;border:1px solid #0c2c45}
.pop_title{float:left;padding-left:10px;width:180px;height:36px;line-height:36px;background:url(../assets/title.png);font-weight:bold;font-size:16px}
.pop_dept{float:left;padding:12px 5px;line-height:15px;text-align:center;margin:0 10px}
.pop_arrow{float:left;width:15px;height:24px;line-height:24px;background:url(../assets/arrow.png) no-repeat center center}
.arrow{display:block;width:17px;height:10px;background:url(../assets/em.png) no-repeat;position:absolute;left:50%;margin-left:-5px;bottom:-10px}
</style>
