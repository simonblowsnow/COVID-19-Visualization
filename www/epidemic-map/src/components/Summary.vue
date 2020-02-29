<template>
  <div>
    <div style="text-align: left">
        <div style="height: 40px; line-height: 40px">
            <label style="font-weight: 800; font-size: 18px">{{title}}</label>
            <label style="float: right; color: #4197FD">数据更新时间： {{updateTime}}</label>
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
  </div>
</template>

<script>
// import {Utils} from "../js/utils";

export default {
    name: 'Summary',
    props: ['title', 'updateTime', 'sums']
    // data () {
    //     return{
    //         title: "国内疫情",
    //         updateTime: '2020.02.15 02:29',
    //         sums: [
    //             {name: 'confirmed', text: '确诊', color: Utils.Colors[0], sum: 63951, add: "+19"},
    //             {name: 'suspected', text: '疑似', color: Utils.Colors[1], sum: 10109 , add: "+2450"},
    //             {name: 'die', text: '死亡', color: Utils.Colors[2], sum: 1382 , add: "+1"},
    //             {name: 'ok', text: '治愈', color: Utils.Colors[3], sum: 7094, add: "+366"}
    //         ]
    //     }
    // }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.grid-content {
    border-radius: 4px;
    min-height: 46px;
  }
  .sum_numb {
      height: 20px;
      font-weight: 700;
  }


</style>
