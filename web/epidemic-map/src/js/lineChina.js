import {Utils} from "../js/utils";
import echarts from 'echarts';


function getOption () {
    let option = {
        title: [{
            text: '',
            left: 10,
            top: 0,
            textStyle:{
                fontSize:18,
                fontWeight:'normal',
            },
        }],
        tooltip: {
            trigger: 'axis',
            backgroundColor:'rgba(13,177,205,0.8)',
            axisPointer: {
                type: 'shadow',
                label: {
                    show: true,
                    backgroundColor: '#7B7DDC'
                },
                shadowStyle: {
                    color: 'rgba(250, 250, 250, 0.25)'
                }
            }
        },
        legend: {
            data: ['累计确诊', '新增确诊'],
            top: 0,
            right: '90'
        },
        grid:[
            {
                width:'85%',
                top: 30,
                height: 70
            }
        ],
        xAxis: [{
            data: ["02-01", "02-02", "02-03"],
            axisLine: {
                lineStyle: {
                    color: '#666'
                }
            },
            axisTick:{
                show:true,
            },
            axisLabel:{
                textStyle:{
                    fontSize:16
                }
            }
        }],
        yAxis: [
            {
                name:'累计',
                axisLine: {
                    lineStyle: {
                        color: '#666',
                    }
                },
                axisLabel:{
                    formatter:'{value} ',
                    textStyle:{
                        color:"#666",
                    }
                },
                splitLine: {
                    show: true,
                    lineStyle: {
                    color: 'rgba(205,205,205,0.3)'
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
            }
        ],
        series: [{
            name: '累计确诊',
            type: 'line',
            smooth: true,
            showAllSymbol: true,
            symbol: 'circle', // emptyCircle
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
    return option;
}

let option = getOption();

let chart = {
    name: "lineChina",
    option: option,
    initData: null,
    instance: null,
    useMaxValue: true
};

function translate (srcData) {
    let rs = {};
    for (let t in srcData) {
        srcData[t].forEach(d => {
            let code = d[0];
            if (!(code in rs)) rs[code] = {name: d[2], data: []};
            [d[0], d[2]] = [t, ""];
            rs[code].data.push(d);
        });
    }
    return rs;
}

// 针对事件序列数据，数据上升一个维度
// param:   dts : {'2020-02-01': []}
function getOptions (srcData) {
    let dts = translate(srcData);
    let codes = Object.keys(dts);
    [option.title, option.grid, option.xAxis, option.yAxis, option.series] = [[], [], [], [], []];
    codes.forEach((k, i) => {
        let opt = getOption();
        let [title, grid, xAxis, yAxis, series] = [opt.title[0], opt.grid[0], opt.xAxis[0], opt.yAxis, opt.series];
        title.text = k;
        title.top = i * 120;
        grid.top = i * 120 + 30;
        xAxis.gridIndex = i;
        yAxis[0].gridIndex = yAxis[1].gridIndex = i;
        series[0].xAxisIndex = series[1].xAxisIndex = i;
        // xAxis.data = codes[k][];
        // TODO:
        
        [series[0].yAxisIndex, series[1].yAxisIndex] = [i * 2, i * 2 + 1];
        option.title.push(title);
        option.grid.push(grid);
        option.xAxis.push(xAxis);
        option.yAxis.push(yAxis[0], yAxis[1]);
        option.series.push(series[0], series[1]);
    });

    return option;
}

chart.initData = function (srcData, id, level) {
    
    let _option = option;
    _option = getOptions(srcData, _option);
    
    // let grid = {
    //     width:'90%',
    //     top: 10,
    //     height: 100
    // }
    // option.grid.push(grid);


    console.log([srcData, id, level, _option]);
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
    let myChart = Utils.drawGraph(_option, id);
    return myChart;
    // myChart.dispatchAction({ type: 'legendUnSelect', name: "疑似" })
};

let chartLine = chart;
export default chartLine;