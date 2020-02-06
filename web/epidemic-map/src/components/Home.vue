<template>
  <div class="hello">
    <div style="text-align: left">
        <h3>国内疫情</h3>
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
    <div style="padding: 10px">
        <div class="clearfix" style="height: 40px; text-align: left">
            <span>数据来源 · 各地区卫健委官网</span>
            <el-button style="float: right; padding: 3px 0" type="text">时间序列回放</el-button>
            <div style="font-size: 12px; color: #f00">注：点击地图行政区域查看辖区地图</div>
        </div>

        <!-- 全国 -->
        <el-row :gutter="5" v-for="(c, i) in ids" v-show="showIndex==0" :key="i">
            <!-- 地图 -->
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <div :id="c[0]" class="chart" :style="{height: mapHeight}"></div>
            </el-col>
            <!-- 柱状图，可能太长，使用滚动条 -->
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <div class="chart" style="height: 500px">
                    <el-scrollbar style="height:100%">
                        <div :id="c[1]" style="height:900px"></div>
                    </el-scrollbar>
                </div>
            </el-col>
        </el-row>
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
        ids: [['ecChina', 'ecBar1'], ['ecProvince', 'ecBar2']],
        charts: [chartMap, chart2],
        mapHeight: (Utils.getDevice() === 'xs') ? "300px" : "500px"
      }
  },
  mounted () {
      this.init();
      this.loadMap("china");
  },
  methods: {
      init () {
          // alert("init");

      },
      // 加载地图类数据，先请求地图轮廓文件
      // param: mapName - 地图名称（echarts注册时使用，以行政区域代码为准，中国使用'china'）
      loadMap (mapName, level) {
        let $this = this;
        if (mapName in Utils.Names) return $this.loadData(mapName, level);

        // 已注册的地图会有名称映射信息存于Utils.Names，未注册的地图先请求地图文件
        Utils.ajaxData(API.GetMap, {id: mapName}, function (rst) {
            Utils.registerMap(mapName, rst.data);
            $this.loadData(mapName, level);
        });
      },
      // 请求汇总数据
      // params: code - 行政区域编码（全国除外，为'china'）
      loadData (mapName, level) {
        let $this = this;
        if (!level) level = 1;
        Utils.ajaxData(API.GetDataDetails, {'level': level, 'name': mapName}, function (rst) {
            console.log(rst);
            // 绘图容器ID
            let divs = $this.ids[level - 1];
            document.getElementById(divs[1]).style.height = (26 * rst.data.length + 20) + "px";
            chartMap.initData(rst.data, divs[0], mapName);
            // debugger
            chartMap.instance.on('click', function (d) {
                let code = d.data.code;
                console.log(code);
                $this.loadMap(code, level + 1);
            })
            let names = Utils.Names[mapName];
            chart2.initData(rst.data, divs[1], names);
        });
      },


      // 暂时无用
      // func (chart, data) {
      //
      // }
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
