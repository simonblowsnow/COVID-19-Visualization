
// 注：在本项目中没什么用，只用高德。因为轮廓坐标为高德坐标系，懒得写自动转换程序。

// 请自行申请Key
let key = "pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXFhYTA2bTMyeW44ZG0ybXBkMHkifQ.gUGbDOPUN1v1fTs5SeOR4A";
let MAPS = {
    "Gaode": {
      name: '高德',
      urlTemplate: 'http://wprd0{s}.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=8',
      subdomains: ['1', '2', '3', '4'],
      attribution: '&copy; <a target="_blank" href="http://ditu.amap.com">高德地图</a>',
      weixing: 'http://wprd0{s}.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7'
    },
    "Baidu": {
      name: '百度',
      spatialReference: {projection : 'baidu'},
      urlTemplate: 'http://online{s}.map.bdimg.com/onlinelabel/?qt=tile&x={x}&y={y}&z={z}&styles=pl&scaler=1&p=1',
      subdomains: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
      attribution: '&copy; <a target="_blank" href="http://map.baidu.com">Baidu</a>'
    },
    "OpenStreetMap": {
      name: 'OpenStreet',
      urlTemplate: 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
      subdomains: ['a', 'b', 'c'],
      attribution: '&copy; <a href="http://osm.org">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/">CARTO</a>',
      weixing: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"
    },
    "Mapbox": {
      name: 'Mapbox',
      urlTemplate: 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}?access_token=' + key,
      subdomains: ['a', 'b', 'c', 'd'],
      attribution: '&copy; <a target="_blank" href="http://mapbox.cn">Mapbox</a>',
      weixing: 'https://{s}.tiles.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=' + key,
    }
  };

  let MapList = [];
  let keys = ['Gaode', 'OpenStreetMap', 'Mapbox']; // 'Baidu', 'Google', 'OSM'
  keys.forEach(k => {
    MapList.push({label: MAPS[k].name, value: k + "_0"});
    if (MAPS[k].weixing) MapList.push({label: MAPS[k].name + "卫星", value: k + "_1"});
  });


  export {MAPS, MapList};