<template>
  <div id="app">
    <!-- <el-container style="height: 100%; border: 1px solid #eee"> -->
      
    <div style="text-align: left; height: 160px; padding: 20px" class="pageHead">
      <!-- 开源标识 -->
      <div style="text-align: right; ">
        <span>
          <a href="https://github.com/simonblowsnow/2019-ncov-vis" style="color: #fff; text-decoration:none">
            <img style="margin-bottom: -2px;" src="./assets/github.png" width="18" /> 
            <label style="font-size: 16px"> Github</label>
          </a>
        </span>
      </div>
      <div>
        <div style="font-size: 26px">新冠肺炎疫情<label style="font-size: 24px"> · 数据分析系统</label></div>
        <div style="font-size: 22px; margin-top: 5px; color: #ddd; font-family: 'Times New Roman', Times, serif">
          WuHan 2019-nCoV Data Visualization Analysis System
        </div>
      </div>
    </div>
      <!-- <el-header style="text-align: right; font-size: 12px">
        1
      </el-header> -->
      <el-main>
        <Home msg="Welcome to Your Vue.js App"/>

      </el-main>
      <!-- <el-footer>
        3
      </el-footer> -->
    <!-- </el-container> -->
  </div>
</template>

<script>
import Home from './components/Home.vue'

export default {
  name: 'app',
  components: {
    Home
  }
}
</script>

<style>
html, body {
  height: 100%;
  margin: 0px;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
  .pageHead {
    background: url(./assets/head.png) center top / 100% no-repeat;
    color: #fff
  }

  .el-main { padding: 0px 15px 20px 15px!important}
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
