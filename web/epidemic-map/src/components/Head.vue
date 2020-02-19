<template>
  <div>
    <div style="text-align: left; " class="pageHead">
      <!-- 开源标识 -->
      <div style="text-align: right; ">
        <span>
          <a href="https://github.com/simonblowsnow/2019-ncov-vis" style="color: #fff; text-decoration:none">
            <img style="margin-bottom: -2px;" src="../assets/github.png" width="18" /> 
            <label style="font-size: 16px"> Github</label>
          </a>
        </span>
      </div>
      <div>
        <div style="font-size: 24px">新冠肺炎疫情<label style="font-size: 22px"> · 数据分析系统</label></div>
        <div style="font-size: 20px; margin-top: 5px; color: #ddd; font-family: 'Times New Roman', Times, serif">
          WuHan COVID-19 Data Visualization Analysis System
        </div>
        <!-- <div style="font-size: 14px; color: #ddd">—— 开发中，敬请期待!</div> -->
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Head',
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0px;
}
a, a>label { cursor: pointer }
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
.pageHead {
  height: 160px; 
  padding: 20px;
  background: url(../assets/head.png) center top / 100% no-repeat;
  color: #fff
}

.el-main { 
  padding: 0px 15px 20px 15px!important;
  height: calc(100% - 200px);
  /* min-height: calc(100% - 200px); */
}
.el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px; 
}
.el-footer {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
}
.el-scrollbar__wrap{
    overflow-x: hidden!important;
}

</style>
