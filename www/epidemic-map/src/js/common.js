import {Utils} from "../js/utils";
import {API} from "../js/server";
import chartMap from "../js/mapChina";
import chartBar from "../js/barChina";
import chartLine from "../js/lineChina";
import Vue from 'vue'

let Loader = {
    title: "",
    updateTime: "",
    tabs: [],
    sums: [],
    activeName: 'china',
    code: 86,
    level: 1,
    init (title, updateTime, sums, tabs) {
        [this.title, this.updateTime, this.sums, this.tabs] = [title, updateTime, sums, tabs];
    },
    loadSummary () {
        let $this = this;
        Utils.ajaxData(API.GetDataSummary, {'level': this.level, 'name': this.code}, function (rst) {
            $this.updateTime = rst.data.updateTime;
            let _sums = rst.data.summary;
            for (let i = 0; i < 4; i++) {
                if (_sums[0][i]) Vue.set($this.sums[i], 'sum', _sums[0][i]);
                if (_sums[1][i])Vue.set($this.sums[i], 'add', "+" + _sums[1][i]);
            }
        });
    },
    // 加载地图类数据，先请求地图轮廓文件
    // param: mapName - 地图名称（echarts注册时使用，以行政区域代码为准，中国使用'china'）
    loadMap (tab) {
        let $this = this;
        let mapName = tab.mapName;
        if (mapName in Utils.Names) return $this.loadData(tab);

        // 已注册的地图会有名称映射信息存于Utils.Names，未注册的地图先请求地图文件
        Utils.ajaxData(API.GetMap, {id: mapName}, function (rst) {
            Utils.registerMap(mapName, rst.data);
            $this.loadData(tab);
        });
    },
    /* 请求汇总数据
    params: code - 行政区域编码（全国除外，为'china'）
        level: 数据和地图的行政级别，不同级别的视图容器也不同
        allTime: 是否为所有时间序列数据
    */
    loadData (tab) {
        let $this = this;
        let [mapName, level, allTime] = [tab.mapName, tab.level, tab.allTime];
        if (tab.data) return $this.drawGraph(tab);
        
        let key = allTime ? API.GetTimeData : API.GetDataDetails;
        Utils.ajaxData(key, {'level': level, 'name': mapName}, function (rst) {
            tab.data = rst.data;
            $this.drawGraph(tab, rst.data);
        });
    },
    // 绘图入口
    drawGraph (tab, data) {
        let $this = this;
        let [mapName, level, allTime] = [tab.mapName, tab.level, tab.allTime];
        if (!data) data = tab.data;
        if (tab.isLine) {
            let ec = chartLine.initData(data, tab.ids[0], level);
            ec.on('click', function (p) {
                console.log(p);
            });
            return;
        }
        // 依次画两图
        let ec = chartMap.initData(data, tab.ids[0], mapName, allTime);
        ec.off('click');
        ec.on('click', function (d) {
            if (d.seriesType !== 'map') return;
            // TODO: 判断三级区域
            let cTab = $this.tabs[2 + allTime]; 
            [cTab.mapName, cTab.data] = [d.data.code, null];
            $this.activeName = cTab.name;
            $this.loadMap(cTab);
        })
        let names = Utils.Names[mapName];
        chartBar.initData(data, tab.ids[1], names, allTime);
    },
    // 切换标签页
    handleClickTab: function (index) {
        let tab = this.tabs[index];
        if (tab.isLine) return this.loadData(tab);
        this.loadMap(tab);
    }
};

export default Loader;