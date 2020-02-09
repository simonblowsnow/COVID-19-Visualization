import {Utils} from "../js/utils";

// 因图例1数值相对较大，同一比例尺下其它图例容易被湮没，故图形分左右两部分分别呈现
// 网格分三部分，1 - Y轴文字， 2 - 图形1， 3 - 图形2
let option = {
    tooltip : {
        trigger: 'axis',
        axisPointer : { type : 'shadow' }
    },
    legend: {
        show: true,
        data: ['L1', 'L2']
    },
    grid: [
        {
            left: 90,
            top: '38',
            bottom: '3%',
            // containLabel: true
        },
        {
            left: 40,
            width: '65%',
            top: '19',
            bottom: '3%',
            containLabel: true
        },
        {
            right: '2%',
            width: '25%',
            top: '19',
            bottom: '3%',
            containLabel: true
        },
    ],
    xAxis:  [
        {
            left: '10px',
            show: false, 
        },
        {
            type: 'value',
            show: false,
            position: 'top',
            gridIndex: 1
        },
        {
            type: 'value',
            show: false,
            position: 'top',
            gridIndex: 2
        },
    ],
    yAxis: [
        {
            type: 'category',
            inverse: true,
            data: ['福建','广州','厦门','南宁','北京','长沙','重庆'],
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
        {
            gridIndex: 1,
            type: 'category',
            inverse: true,
            show: false,
            data: ['福建','广州','厦门','南宁','北京','长沙','重庆'],
            axisLine: {show: false},
            axisTick: {show: false},
        }, 
        {
            gridIndex: 2,
            type: 'category',
            inverse: true,
            show: false,
            data: ['福建','广州','厦门','南宁','北京','长沙','重庆'],
            axisLine: {show: false},
            axisTick: {show: false},
        }
    ],
    series: [
        {
            name: 'L1',
            type: 'bar',
            barWidth: 20,
            xAxisIndex: 1,
            yAxisIndex: 1,
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
        },
        {
            name: 'L2',
            type: 'bar',
            stack: true,
            barWidth: 20,
            xAxisIndex: 2,
            yAxisIndex: 2,
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
            data: [200, 302, 301, 334, 390, 330, 320]
        }
    ]
};

let legend = ["确诊", "疑似", "死亡", "治愈"];
let superOption = {
    baseOption: {
        timeline: {
            data: ["2016", "2017"],
            axisType: "category",
            autoPlay: true,
            playInterval: 5000,
            left: "10%",
            right: "10%",
            bottom: "0%",
            width: "80%",
            symbolSize: 10,
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
            },
            
        },
        legend: {show: true, data: legend},
        tooltip: option.tooltip,
        grid: option.grid,
        xAxis: option.xAxis,
        yAxis: option.yAxis,
        series: option.series,
        animationDurationUpdate: 2000,
        animationEasingUpdate: "quinticInOut"
    },
    options: []
};

let chart = {
    name: "barChina",
    option: option,
    superOption: superOption,
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
function getOption (srcData, names) {
    debugger
    let dt = [[], [], [], []];
    srcData.sort((a, b) => { return b[1] - a[1]}).forEach(d => {
        dt[0].push(d[1]);
        dt[1].push(d[3]);
        dt[2].push(d[4]);
        dt[3].push(d[5]);
    });
    let nums = [0, 1, 2];
    let _option = {
        title: {text: "月日"},
        yAxis: nums.map(() => {
            return {"data": srcData.map(d => names[d[0]] || d[2])};
        }),
        series: legend.map((d, i) => {
            return {
                name: legend[i],
                type: 'bar',
                barWidth: 20,
                stack: i < 1 ? false : true,
                xAxisIndex: i < 1 ? 1 : 2,
                yAxisIndex: i < 1 ? 1 : 2,
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
                        show: i < 1 || i == 3,
                        distance: 5,
                        position: 'right' // insideRight
                    }
                },
                data: dt[i]
            };
        })
    }
    return _option;
}

chart.initData = function (srcData, id, names) {
    debugger
    superOption.options = [getOption(srcData, names), getOption(srcData, names)];

    console.log(superOption);
    let myChart = Utils.draw(chart, id);

    myChart.dispatchAction({ type: 'legendUnSelect', name: "疑似" })
};

let chart2 = chart;
export default chart2;