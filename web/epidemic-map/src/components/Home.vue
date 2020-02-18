<template>
  <div class="hello">
    <Summary :title="title" :updateTime="updateTime" :sums="sums"></Summary>
    
    <div style="padding-top: 10px">
        <el-tabs v-model="activeName" @tab-click="handleClickTab">
            <!-- 标签页 -->
            <el-tab-pane :label="c.label" :name="c.name" v-for="(c, i) in tabs" :key="i">
                <el-row :gutter="5" v-if="i<4" v-show="activeName==c.name">
                    <!-- 地图 -->
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <div :id="c.ids[0]" class="chart" :style="{height: mapHeight}"></div>
                    </el-col>

                    <!-- 柱状图，可能太长，使用滚动条 -->
                    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                        <div class="chart" style="height: 500px">
                            <el-scrollbar style="height:100%">
                                <div :id="c.ids[1]" style="height:900px"></div>
                            </el-scrollbar>
                        </div>
                    </el-col>
                </el-row>
                <!-- 曲线分析 -->
                <el-row v-else v-show="activeName==c.name">
                    <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
                        <div :id="c.ids[0]" class="chart" style="height: 500px"></div>
                    </el-col>
                </el-row>
            </el-tab-pane>
        </el-tabs>
        
        <!-- <div class="clearfix" style="height: 40px; text-align: left">
            <span>数据来源 · 各地区卫健委官网</span>
            <el-button style="float: right; padding: 3px 0" type="text"></el-button>
            <div style="font-size: 12px; color: #f00">注：点击地图行政区域查看辖区地图</div>
        </div> -->

        <!-- 全国 -->
        
    </div>

    <div style="height: 20px"></div>
  </div>
</template>

<script>
import Summary from './Summary.vue'
import {Utils} from "../js/utils";
import {API} from "../js/server";
import chartMap from "../js/mapChina";
import chartBar from "../js/barChina";
import chartLine from "../js/lineChina";

export default {
    name: 'Home',
    components: {Summary},
    props: {
        msg: String
    },
    data(){
        return{
            title: "国内疫情",
            sums: [
                {name: 'confirmed', text: '确诊', color: Utils.Colors[0], sum: 63951, add: "+19"},
                {name: 'suspected', text: '疑似', color: Utils.Colors[1], sum: 10109 , add: "+2450"},
                {name: 'die', text: '死亡', color: Utils.Colors[2], sum: 1382 , add: "+1"},
                {name: 'ok', text: '治愈', color: Utils.Colors[3], sum: 7094, add: "+366"}
            ],
            updateTime: '2020.02.15 02:29',
            tabs: [
                { 
                    label: "全国实时疫情", name: 'china', ids: ['ecChina', 'ecBar1'], level: 1, 
                    allTime: 0, data: null, mapName: 'china'
                },
                {
                    label: "时间序列回放", name: 'chinaTime', ids: ['ecChinaTime', 'ecBarTime1'], level: 1, 
                    allTime: 1, data: null, mapName: "china"
                },
                {
                    label: "省实时疫情", name: 'province', ids: ['ecProvince', 'ecBar2'], level: 2, 
                    allTime: 0, data: null, mapName: "420000"
                },
                {
                    label: "省舆情回放", name: 'provinceTime', ids: ['ecProvinceTime', 'ecBarTime2'], 
                    level: 2, allTime: 1, data: null, mapName: '420000'
                }, 
                {
                    label: "曲线分析", name: "lineChina", ids: ['ecLineChina'], level: 1, isLine: 1, 
                    allTime: 1, data: null, mapName: "china"
                }
            ],
            activeName: 'china',
            mapHeight: (Utils.getDevice() === 'xs') ? "330px" : "500px",
        }
    },
    mounted () {
        this.init();
    },
    methods: {
        init () {
            // this.loadMap(this.tabs[0]);
            this.activeName = "lineChina";
            this.loadData(this.tabs[4]);
        },
        // 加载地图类数据，先请求地图轮廓文件
        // param: mapName - 地图名称（echarts注册时使用，以行政区域代码为准，中国使用'china'）
        loadMap (tab) {
            let $this = this;
            let mapName = tab.mapName;
            if (mapName in Utils.Names) return $this.loadData(tab);

            // 已注册的地图会有名称映射信息存于Utils.Names，未注册的地图先请求地图文件
            Utils.ajaxData(API.GetMap, {id: mapName}, function (rst) {
                Utils.registerMap(mapName, rst.data);
                $this.loadData(tab);
            });
        },
        /* 请求汇总数据
        params: code - 行政区域编码（全国除外，为'china'）
            level: 数据和地图的行政级别，不同级别的视图容器也不同
            allTime: 是否为所有时间序列数据
        */
        loadData (tab) {
            let $this = this;
            let [mapName, level, allTime] = [tab.mapName, tab.level, tab.allTime];
            if (tab.data) return $this.drawGraph(tab);
            
            let key = allTime ? API.GetTimeData : API.GetDataDetails;
            Utils.ajaxData(key, {'level': level, 'name': mapName}, function (rst) {
                tab.data = rst.data;
                $this.drawGraph(tab, rst.data);
            });
        },
        // 绘图入口
        drawGraph (tab, data) {
            let $this = this;
            let [mapName, level, allTime] = [tab.mapName, tab.level, tab.allTime];
            if (!data) data = tab.data;
            if (tab.isLine) {
                let ec = chartLine.initData(data, tab.ids[0], level);
                ec.on('click', function (p) {
                    console.log(p);
                });
                return;
            }
            // 依次画两图
            let ec = chartMap.initData(data, tab.ids[0], mapName, allTime);
            ec.off('click');
            ec.on('click', function (d) {
                if (d.seriesType !== 'map') return;
                // TODO: 判断三级区域
                let cTab = $this.tabs[2 + allTime]; 
                [cTab.mapName, cTab.data] = [d.data.code, null];
                $this.activeName = cTab.name;
                $this.loadMap(cTab);
            })
            let names = Utils.Names[mapName];
            chartBar.initData(data, tab.ids[1], names, allTime);
        },
        // 绘制曲线图
        drawLines: function (data, level) {
            console.log([data, level]);
        },
        handleClickTab: function (p) {
            let tab = this.tabs[parseInt(p.index)];
            if (tab.isLine) return this.loadData(tab);
            this.loadMap(tab);
        }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 0px 0 16px 0;
}

a {
  color: #42b983;
}

  .grid-content {
    border-radius: 4px;
    min-height: 46px;
  }
  .sum_numb {
      height: 20px;
      font-weight: 700;
  }
  .chart{
      min-height: 320px;
      margin-bottom: 20px;
  }


</style>
