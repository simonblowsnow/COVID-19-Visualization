import {Utils} from "../js/utils";
import getTimeline from "./timeline";

let option = {
    title: {
        text: '',
        x: 'center',
        top: "3%",
        textStyle:{
            color:'#fff',
            fontSize:18,
            fontWeight:'normal',
        },
        
    },
    backgroundColor: '#051034',
    tooltip: {
        trigger: 'axis',
        backgroundColor:'rgba(255,255,255,0.1)',
        axisPointer: {
            type: 'shadow',
            label: {
                show: true,
                backgroundColor: '#7B7DDC'
            }
        }
    },
    legend: {
        data: ['累计确诊', '新增确诊',],
        textStyle: {
            color: '#ccc'
        },
        top:'7%',
        right:'10%'
    },
    grid:{
        left:'center',
        width:'90%',
        top:'10%',
    },
    xAxis: {
        data: ["02-01", "02-02", "02-03"],
        axisLine: {
            lineStyle: {
                color: '#B4B4B4'
            }
        },
        axisTick:{
            show:true,
        },
        axisLabel:{
            textStyle:{
                color:"#ccc",
                fontSize:16
            }
        }
    },
    yAxis: [{
        name:'累计',
        splitLine: {show: false},
        axisLine: {
            lineStyle: {
                color: '#B4B4B4',
            }
        },
        axisLabel:{
            formatter:'{value} ',
            textStyle:{
                 color:"#ccc",
                fontSize:16
            }
        }
    },
        {
        name:'新增',
        splitLine: {show: false},
        axisLine: {
            lineStyle: {
                color: '#B4B4B4',
            }
        }
    }],
    series: [{
        name: '累计确诊',
        type: 'line',
        smooth: true,
        showAllSymbol: true,
        symbol: 'emptyCircle',
        symbolSize: 8,
        yAxisIndex: 1,
        itemStyle: {
                normal: {
                color:'#F02FC2'},
        },
        data: [10, 20, 50]
    }, 
    {
        name: '新增确诊',
        type: 'bar',
        barWidth: 15,
        itemStyle: {
            normal: {
                barBorderRadius: 5,
                color: new echarts.graphic.LinearGradient(
                    0, 0, 0, 1,
                    [
                        {offset: 0, color: '#956FD4'},
                        {offset: 1, color: '#3EACE5'}
                    ]
                )
            }
        },
        data: [10, 8, 5]
    }
   ]
};

let legend = ["确诊", "疑似", "死亡", "治愈"];
// 全局变量，重新加载时需重新初始化
let maxValues = [0, 0, 0, 0];
let superOption = {
    baseOption: {
        timeline: getTimeline(),
        legend: option.legend,
        tooltip: option.tooltip,
        grid: option.grid,
        xAxis: option.xAxis,
        yAxis: option.yAxis,
        series: option.series,
        animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut"
    },
    options: []
};

let chart = {
    name: "barChina",
    option: option,
    superOption: superOption,
    initData: null,
    instance: null,
    useMaxValue: true
};


/*
Params:
 srcData: [[code, value1, name, value2, value3, value4, time]]
 id: 图形容器Div的ID
*/
function getOption (srcData, names, _option) {
    let dt = [[], [], [], []];
    console.log([srcData, names, _option]);
    return _option;
}

// 针对事件序列数据，数据上升一个维度
// param:   dts : {'2020-02-01': []}
function getOptions (dts, names) {
    // 理论上讲tms是有序的，若不是则应在此处排序
    let tms = Object.keys(dts);
    superOption.baseOption.timeline.data = tms;
    superOption.options = tms.map(k => {
        let _option = { title: {text: '', top: 65, textStyle: {color: '#bbb', fontSize: 14}}, 
            yAxis: [{data: []}, {data: []}, {data: []}] 
        }
        return getOption(dts[k], names, _option);
    });
    return superOption;
}

chart.initData = function (srcData, id, names, allTime) {
    let _option = option;
    
    console.log([srcData, id, names, allTime, _option]);
    // _option['legend']['data'] = legend;
    // maxValues = [0, 0, 0, 0];
    // if (!allTime) {
    //     _option = getOption(srcData, names, _option);
    // } else {
    //     _option = getOptions(srcData, names);
    // }
    // // 优化小尺寸设备显示
    // if (Utils.getDevice() === 'xs') option.grid[1].width = "51%";
    // // 数据尺度同一使用全局最大值为上限
    // if (chart.useMaxValue) {
    //     option.xAxis[1]['max'] = maxValues[0];
    //     option.xAxis[2]['max'] = maxValues[2] + maxValues[3]; // maxValues[1]
    // }
    // let myChart = Utils.drawGraph(_option, id);

    // myChart.dispatchAction({ type: 'legendUnSelect', name: "疑似" })
};

let chart3 = chart;
export default chart3;