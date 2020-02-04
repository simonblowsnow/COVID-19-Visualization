import {Utils} from "../js/utils";

let option = {
    tooltip : {
        trigger: 'axis',
        axisPointer : { type : 'shadow' }
    },
    legend: {
        show: true,
        data: ['L1']
    },
    grid: {
        left: '3%',
        right: '4%',
        top: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis:  {
        left: '260px',
        type: 'value',
        // max: 20000,
        show: false
    },
    yAxis: {
        type: 'category',
        inverse: true,
        data: ['福建','广州','厦门','南宁','背景','长沙','重庆'],
        axisLine: {show: false},
        axisTick: {show: false},
        axisLabel: {
            interval: 0,
            margin: 85,
            textStyle: {
                color: '#455A74',
                align: 'left',
                fontSize: 14
            },
            rich: {
                a: {
                    color: '#fff',
                    backgroundColor: '#FAAA39',
                    width: 20,
                    height: 20,
                    align: 'center',
                    borderRadius: 2
                },
                b: {
                    color: '#fff',
                    backgroundColor: '#4197FD',
                    width: 20,
                    height: 20,
                    align: 'center',
                    borderRadius: 2
                }
            },
            formatter: function (params, i) {
                return '{' + (i < 3 ? 'a' : 'b') + '|' + (i + 1) + '}' + '  ' + params
            }
        }
    },
    series: [
        {
            name: 'L1',
            type: 'bar',
            stack: true,
            barWidth: 20,
            itemStyle:{
                normal: {
                    color: '#F55253',
                    barBorderRadius: [20, 20, 20, 20],
                    shadowBlur: 20,
                    shadowColor: 'rgba(40, 40, 40, 0.5)'
                }
            },
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [320, 302, 301, 334, 390, 330, 320]
        }
    ]
};

let chart = {
    name: "barChina",
    option: option,
    initData: null,
    instance: null
};

/*
Params:
 srcData: [[code, value1, name, value2, value3, value4, time]]
 id: 图形容器Div的ID
 names: {code: name} (简称区域名映射表，来自地图文件)
 注：柱状图属于地图的补充描述，使用同一份数据
    柱状图分项使用地图区域名称简称，该名称来自于地图文件，使用行政区域代码对应关联，
    代码-名称映射表在地图数据转换时生成，并缓存，故柱状图绘制顺序应晚于对应地图绘制。
*/
chart.initData = function (srcData, id, names) {
    let legend = ["确诊", "疑似", "死亡", "治愈"];
    let dts = [[], [], [], []];
    srcData.sort((a, b) => { return b[1] - a[1]}).forEach(d => {
        dts[0].push(d[1]);
        dts[1].push(d[3]);
        dts[2].push(d[4]);
        dts[3].push(d[5]);
    });
    option['legend']['data'] = legend;
    option['yAxis']['data'] = srcData.map(d => names[d[0]]);
    option['series'] = legend.map((d, i) => {
        return {
            name: legend[i],
            type: 'bar',
            stack: '总量',
            itemStyle:{
                normal: {
                    barBorderRadius: [2, 2, 2, 2],
                    color: Utils.Colors[i],
                    shadowBlur: [0, 0, 0, 10],
                    shadowColor: Utils.Colors[i],
                }
            },
            label: {
                normal: {
                    show: i < 1,
                    distance: 5,
                    position: 'right' // insideRight
                }
            },
            data: dts[i]
        };
    });
    console.log(JSON.stringify(option));
    // option.series = series;
    // let data = Utils.formatRegion(chart1.name, srcData);
    // option.series[0].data = data;
    Utils.draw(chart, id);
};

let chart2 = chart;
export default chart2;