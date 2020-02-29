import Vue from 'vue'
import App from './App.vue'

import echarts from 'echarts'
Vue.prototype.$echarts = echarts

import 'element-ui/lib/theme-chalk/index.css';
import 'maptalks/dist/maptalks.css';
import ElementUI from 'element-ui';
Vue.use(ElementUI);

import router from './router.js';
Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  render(h){
    return h(App);
  }
})
