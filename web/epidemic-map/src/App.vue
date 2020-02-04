<template>
  <div id="app">
    <el-container style="height: 100%; border: 1px solid #eee">
      <el-header style="text-align: right; font-size: 12px">
        1
      </el-header>
      <el-main>
        <Home msg="Welcome to Your Vue.js App"/>

      </el-main>
      <el-footer>
        3
      </el-footer>
    </el-container>
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
