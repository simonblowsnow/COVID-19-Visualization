<template>
<div>
    <div class="hello">
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
    </div>
    <div style="height: 20px"></div>
</div>
</template>

<script>
import {Utils} from "../js/utils";

export default {
    name: 'Common',
    props: {
        title: String,
        updateTime: String,
        sums: Array,
        tabs: Array,
        activeName_: String
    },
    data () {
        return {
            activeName: '',
            mapHeight: (Utils.getDevice() === 'xs') ? "330px" : "500px"
        }
    },
    watch: {
        activeName_ (v) {
            this.activeName = v;
        }
    },
    methods: {
        handleClickTab: function (p) {
            this.$emit("handleClickTab", parseInt(p.index));
        }
    }
}
</script>

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
