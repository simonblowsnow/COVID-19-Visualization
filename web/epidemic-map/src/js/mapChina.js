import {Utils} from "../js/utils";
import getTimeline from "./timeline";

let option = {
    title: {text: '', top: 15, textStyle: {color: '#4197FD', fontSize: 16}},
    visualMap: {
        min: 0,
        // max: 1000,
        left: 'left',
        top: 'bottom',
        text: ['高', '低'],
        calculable: true,
        inRange: {
            color: ['#FFAA85', '#FF7B69', '#BF2121', '#7F1818'],
            symbolSize: [40, 40]
        }
    },
    series: [{
        name: 'china',
        type: 'map',
        mapType: 'china',
        roam: false,
        label: {
            emphasis: {
                show: true,
                formatter: function (p) {
                    let v = p.data ? p.data.tags[2] : 0;
                    return '{fline|' + p.name + '}\n{tline|确诊: '+ p.value +'\n死亡：' + v + '}\n';
                },
                position: 'top',
                align: 'left', 
                fontSize: 14,
                width: 150,
                backgroundColor: 'rgba(50, 50, 50, 0.8)',
                padding: [0, 0],
                borderRadius: 3,
                color: '#f7fafb',
                rich:{
                    fline:{
                        padding: [0, 5, 5, 10],
                        height : 20,
                        fontSize: 16,
                        fontWeight: 400,
                        color:'#FFFFFF'
                    },
                    tline:{
                        padding: [0, 5, 5, 10],
                        color: '#F55253'
                    }
                }
            },
            normal: {
                show: false
            }
        },
        itemStyle: {
            normal: {
                label: {
                    show: false
                }
            },
            emphasis: {
                areaColor: null,
                borderColor: '#BF2121',
                borderWidth: 1.5,
                shadowColor: 'red', 
                shadowOffsetX: -1,
                shadowOffsetY: -1,
                label: {
                    show: true
                }
            }
        },
        data: [
            {
                name: '北京',
                value: Math.round(Math.random() * 1000)
            }
        ]
    }]
}
// 全局变量，重新加载时需重新初始化
let secondMaxValues = [];
let superOption = {
    baseOption: {
        timeline: getTimeline(),
        visualMap: option.visualMap,
        series: option.series
    },
    options: []
};

let chart = {
    name: "china",
    option: option,
    superOption: superOption,
    initData: null,
    instance: null,
    useMaxValue: true
}

function getOption (srcData, mapName, _option) {
    let data = Utils.formatRegion(mapName, srcData);
    // [sum, max, secondMax]
    let vs = data.reduce((a, b) => {
        if (b.value > a[1]) a[1] = b.value;
        return [a[0] + b.value, a[1], (b.value > a[2] && b.value < a[1]) ? b.value : a[2]];
    }, [0, 10, 10]);
    _option.title.text = "全国确诊：" + vs[0] + "，湖北：" + vs[1];
    secondMaxValues.push(vs[2]);
    _option.series[0]['data'] = data;
    
    if (!chart.useMaxValue) _option['visualMap'] = {
        'max': parseInt(1.25 * secondMaxValues[secondMaxValues.length - 1])
    };
    return _option;
}

// 针对事件序列数据，数据上升一个维度
// param:   dts : {'2020-02-01': []}
function getOptions (dts, mapName) {
    // 理论上讲tms是有序的，若不是则应在此处排序
    let tms = Object.keys(dts);
    superOption.baseOption.timeline.data = tms;
    superOption.options = tms.map(k => {
        let _option = { title: {text: '', top: 55, textStyle: {color: '#bbb', fontSize: 16}}, series: [{}]};
        return getOption(dts[k], mapName, _option);
    });
    superOption.baseOption.timeline.autoPlay = false;
    return superOption;
}

// 需在地图注册后调用，注册地图时应使用name为名称
chart.initData = function (srcData, id, mapName, allTime) {
    mapName = mapName || "china";
    option.series[0].mapType = mapName;
    option.series[0].label.normal.show = mapName != "china";
    secondMaxValues = [];

    let _option = option;
    if (!allTime) {
        _option = getOption(srcData, mapName, _option);
    } else {
        _option = getOptions(srcData, mapName);
    }

    // 颜色渲染最大值，second * 1.25
    let maxColorValue = parseInt(1.25 * secondMaxValues.reduce((a, b) => a > b ? a : b));
    option.visualMap.max = maxColorValue;
    
    chart.instance = Utils.drawGraph(_option, id);
};

let chartMap = chart;
export default chartMap;