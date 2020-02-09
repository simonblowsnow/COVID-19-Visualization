import axios from 'axios';
// import Qs from 'qs';
import {API} from "./server"
import echarts from 'echarts'

let Utils = {};


Utils.setCookie = function (name, value, hour) {
  hour = hour || 200;
  let exp = new Date();
  exp.setTime(exp.getTime() + hour * 3600 * 1000);
  document.cookie = name + '=' + escape(value) + ';expires=' + exp.toUTCString();
};

Utils.getCookie = function (name) {
  let reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)');
  let arr = document.cookie.match(reg);
  return (arr) ? unescape(arr[2]) : null;
};

Utils.postData = function (key, data, _callbackS, _callbackE, config) {
  data['tk'] = Utils.getCookie('tk');
  data['lc'] = Utils.getCookie('lc');
  axios.post('/api/' + key, data, config || {})
    .then(function (rst) {
      if (rst.data.error) {
        alert(rst.data.message);
        return;
      }
      if (_callbackS)_callbackS(rst.data);
    })
    .catch(function (rst) {
      if (_callbackE) _callbackE(rst);
    });
};

Utils.ajaxData = function (key, data, _callbackS, _callbackE) {
  data['tk'] = Utils.getCookie('tk');
  data['lc'] = Utils.getCookie('lc');
  axios.get('/api/' + key, {params: data})
    .then(function (rst) {
      if (rst.data.error) {
        alert(rst.data.message);
        return;
      }
      if (_callbackS)_callbackS(rst.data);
    })
    .catch(function (rst) {
      if (_callbackE) _callbackE(rst);
    });
};

Utils.login = function (username, password, callback) {
  Utils.postData(API.Login, {'username': username || 'david', 'password': password || '123456'}, function (res) {
    if (res.error) return;
    Utils.setCookie("tk", res.data.tk);
    Utils.setCookie("lc", res.data.lc);
    if (callback) callback();
  });
};

// 地图区域名称映射表
// {'china': {'510000': ''}, '510000': {}}
Utils.Names = {};
Utils.formatRegion = function (mapName, data) {
  let mapData = echarts.getMap(mapName);
  if (!mapData) return;
  let names = Utils.Names[mapName];

  // console.log(names);
  return data.map(d => ({
    name: names[d[0]], value: d[1], code: d[0], tags: d.slice(2)
  }));
};

Utils.registerMap = function (mapName, geoJson) {
  geoJson = JSON.parse(geoJson);
  echarts.registerMap(mapName, geoJson);
  
  // 缓存地图区域名称映射表
  Utils.Names[mapName] = geoJson.features.reduce((a, b) => {
      a[b.id.toString()] = b.properties.name;
      return a;
  }, {});
};

Utils.drawGraph = function (option, id) {
  let myChart = echarts.init(document.getElementById(id));
  myChart.setOption(option);
  return myChart;
};

Utils.draw = function (chart, id) {
  return Utils.drawGraph(chart.option, id);
};



Utils.getDevice = function () {
  let w = document.documentElement.offsetWidth || document.body.offsetWidth;
  if (w < 768) return 'xs'; 
  return (w < 1064) ? 'sm' : (w < 1200 ? 'md' : 'lg'); // 992
}



Utils.Colors = ['#F55253', '#FF961E', '#66666c', '#178B50'];


export {Utils};
