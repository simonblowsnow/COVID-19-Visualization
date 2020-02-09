import {Utils} from "../js/utils";

let option = {
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
        roam: true,
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
        timeline: {
            axisType: "category",
            autoPlay: true,
            playInterval: 1500,
            left: "0",
            right: "1%",
            top: "0%",
            width: "99%",
            symbolSize: 10,
            label: {
                formatter: function (d) { return d.substr(5); }
            },
            checkpointStyle: {
                borderColor: "#777",
                borderWidth: 2
            },
            controlStyle: {
                showNextBtn: true,
                showPrevBtn: true,
                normal: {
                    color: "#ff8800",
                    borderColor: "#ff8800"
                },
                emphasis: {
                    color: "#aaa",
                    borderColor: "#aaa"
                }
            }
        },
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
    data.sort((a, b) => b.value - a.value);
    secondMaxValues.push(data.length > 1 ? data[1].value : 10);
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
        console.log(k);
        let _option = { title: {text: ''}, series: [{}]};
        return getOption(dts[k], mapName, _option);
    });
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