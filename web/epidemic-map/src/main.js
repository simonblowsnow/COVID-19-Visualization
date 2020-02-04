import Vue from 'vue'
import App from './App.vue'

import echarts from 'echarts'
Vue.prototype.$echarts = echarts

import 'element-ui/lib/theme-chalk/index.css';
import ElementUI from 'element-ui';
Vue.use(ElementUI);


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
