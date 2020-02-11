<template>
  <div class="hello">
    <div style="text-align: left">
        <div style="height: 40px; line-height: 40px">
            <label style="font-weight: 800; font-size: 18px">国内疫情</label>
            <label style="float: right; color: #4197FD">数据更新时间： </label>
        </div>
    </div>
    <!-- 总体数据汇总情况 -->
    <el-card class="box-card" style="background: #f4f4f5; ">
        <el-row :gutter="20">
            <el-col :span="6" v-for="item in sums" :key="item.name">
                <div class="grid-content ">
                    <div class="sum_numb" :style="{color: item.color, fontSize: '20px', marginBottom: '8px'}">{{item.sum}}</div>
                    <div class="sum_numb" style="color: #333333; font-size: 14px">{{item.text}}病例</div>
                    <div class="sum_numb" style="font-size: 13px; color: #999999; margin-top: 8px">
                        <label style="font-weight:200">昨日 </label>
                        <label :style="{color: item.color}">{{item.add}}</label>
                    </div>
                </div>
            </el-col>
        </el-row>
    </el-card>
    <div style="padding-top: 10px">
        <el-tabs v-model="activeName" @tab-click="handleClickTab">
            <el-tab-pane :label="c.label" :name="c.name" v-for="(c, i) in tabs" :key="i">
                <el-row :gutter="5" v-if="activeName==c.name">
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
            </el-tab-pane>
        </el-tabs>
        
        <!-- <div class="clearfix" style="height: 40px; text-align: left">
            <span>数据来源 · 各地区卫健委官网</span>
            <el-button style="float: right; padding: 3px 0" type="text"></el-button>
            <div style="font-size: 12px; color: #f00">注：点击地图行政区域查看辖区地图</div>
        </div> -->

        <!-- 全国 -->
        
    </div>
  </div>
</template>

<script>
import {Utils} from "../js/utils";
import {API} from "../js/server";
import chartMap from "../js/mapChina";
import chart2 from "../js/barChina";

export default {
    name: 'Home',
    props: {
        msg: String
    },
    data(){
        return{
            sums: [
                {name: 'confirmed', text: '确诊', color: Utils.Colors[0], sum: 24447, add: "+84"},
                {name: 'suspected', text: '疑似', color: Utils.Colors[1], sum: 23260 , add: "待更新"},
                {name: 'die', text: '死亡', color: Utils.Colors[2], sum: 493 , add: "+3"},
                {name: 'ok', text: '治愈', color: Utils.Colors[3], sum: 979, add: "+87"}
            ],
            showIndex: 0,
            tabs: [
                {label: "全国实时疫情", name: 'china', ids: ['ecChina', 'ecBar1'], level: 1, allTime: 0, data: null}, 
                {label: "时间序列回放", name: 'provinceTime', ids: ['ecProvinceTime', 'ecBarTime2'], level: 1, allTime: 1, data: null}, 
                {label: "省实时疫情", name: 'province', ids: ['ecProvince', 'ecBar2'], level: 2, allTime: 0, data: null},
                {label: "省舆情回放", name: 'chinaTime', ids: ['ecChinaTime', 'ecBarTime1'], level: 2, allTime: 1, data: null}
            ],
            activeName: 'china',
            charts: [chartMap, chart2],
            currentProvince: "420000",
            mapHeight: (Utils.getDevice() === 'xs') ? "300px" : "500px",
        }
    },
    mounted () {
        this.init();
    },
    methods: {
        init () {
            this.loadMap("china");
        },
        getTab (allTime, level) {
            return this.tabs[allTime + level - (level > 1 ? 0 : 1)];
        },
        // 加载地图类数据，先请求地图轮廓文件
        // param: mapName - 地图名称（echarts注册时使用，以行政区域代码为准，中国使用'china'）
        loadMap (mapName, level, allTime) {
            let $this = this;
            if (mapName in Utils.Names) return $this.loadData(mapName, level, allTime);

            // 已注册的地图会有名称映射信息存于Utils.Names，未注册的地图先请求地图文件
            Utils.ajaxData(API.GetMap, {id: mapName}, function (rst) {
                Utils.registerMap(mapName, rst.data);
                $this.loadData(mapName, level, allTime);
            });
        },
        /* 请求汇总数据
        params: code - 行政区域编码（全国除外，为'china'）
            level: 数据和地图的行政级别，不同级别的视图容器也不同
            allTime: 是否为所有时间序列数据
        */
        loadData (mapName, level, allTime) {
            let $this = this;
            if (!level) level = 1;
            if (!allTime) allTime = 0;
            let tab = this.getTab(allTime, level);
            // 优先使用缓存数据
            if (tab.data) return $this.drawGraph(tab.data, mapName, level, allTime);
            
            let key = allTime ? API.GetTimeData : API.GetDataDetails;
            Utils.ajaxData(key, {'level': level, 'name': mapName}, function (rst) {
                tab.data = rst.data;
                $this.drawGraph(rst.data, mapName, level, allTime);
            });
        },
        drawGraph (data, mapName, level, allTime) {
            let $this = this;
            let divs = $this.getTab(allTime, level).ids;
            // 绘图容器ID，动态调整尺寸
            let latestData = data;
            if (allTime) {
                let tms = Object.keys(data);
                latestData = data[tms[tms.length - 1]];   
            }
            document.getElementById(divs[1]).style.height = (26 * latestData.length + 20) + "px";
            // 依次画两图
            chartMap.initData(data, divs[0], mapName, allTime);
            chartMap.instance.on('click', function (d) {
                if (d.seriesType !== 'map') return;
                if (level++ == 2) {
                    alert(level);
                    return;
                }
                $this.activeName = $this.getTab(allTime, level).name;
                $this.loadMap(d.data.code, level, allTime);
            })
            let names = Utils.Names[mapName];
            chart2.initData(data, divs[1], names, allTime);
        },

        handleClickTab: function (p) {
            let tab = this.tabs[parseInt(p.index)];
            let mapName = tab.level == 1 ? "china" : this.currentProvince;
            console.log(this.activeName);
            this.loadMap(mapName, tab.level, tab.allTime);
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
