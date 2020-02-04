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
                    <div class="sum_numb" :style="{color: item.color, fontSize: '28px', marginBottom: '8px'}">{{item.sum}}</div>
                    <div class="sum_numb" style="color: #333333, font-size: 22px">{{item.text}}病例</div>
                    <div class="sum_numb" style="font-size: 18px; color: #999999; margin-top: 8px">
                        <label style="font-weight:200">昨日 </label>
                        <label :style="{color: item.color}">{{item.add}}</label>
                    </div>
                </div>
            </el-col>
        </el-row>
    </el-card>
    <div style="padding: 10px">
        <div class="clearfix" style="height: 40px; text-align: left">
            <span>卡片名称</span>
            <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button>
        </div>
        <el-row :gutter="10">
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <div id="ecChina" class="chart1"></div>
            </el-col>
            <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
                <div id="ecProvince" class="chart1"></div>
            </el-col>
        </el-row>
    </div>

  </div>
</template>

<script>
import {Utils} from "../js/utils";
import {API} from "../js/server";
import chart1 from "../js/chartChina";

export default {
  name: 'Home',
  props: {
    msg: String
  },
  data(){
      return{
        sums: [
            {name: 'confirmed', text: '确诊', color: '#F55253', sum: 0, add: 0},
            {name: 'suspected', text: '疑似', color: '#FF961E', sum: 0, add: 0},
            {name: 'die', text: '死亡', color: '#66666c', sum: 0, add: 0},
            {name: 'ok', text: '治愈', color: '#178B50', sum: 0, add: 0}
        ],
        charts: [chart1]
      }
  },
  mounted () {
      this.init();
      this.loadChart(this.charts[0]);
  },
  methods: {
      init () {
          // alert("init");

      },
      loadDataChina (chart) {
        Utils.ajaxData(API.GetDataChina, {type: 0}, function (rst) {
            console.log(rst);
            Utils.formatRegion(chart.name, rst.data);
            
            Utils.draw(chart, "ecChina");
            
        });
      },
      loadChart (chart) {
        let $this = this;
        Utils.ajaxData(API.GetMap, {id: chart.name}, function (rst) {
            let geojson = rst.data;
            $this.$echarts.registerMap(chart.name, geojson);
            console.log(geojson);
            $this.loadDataChina(chart);

        });
          
          console.log(chart);
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
  .chart1{
      min-height: 500px;
  }
</style>
