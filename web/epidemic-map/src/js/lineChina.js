import {Utils} from "../js/utils";


function getOption () {
    let option = {
        title: [{
            text: '',
            subtext: '',
            left: 10,
            top: 0,
            subtextStyle: {
                color: "#F55253"
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
            data: ['累计确诊', '新增确诊', '累计治愈'],
            top: 0,
            right: '90'
        },
        grid:[
            {
                width:'85%',
                top: 30,
                height: 85
            }
        ],
        xAxis: [{
            data: ["02-01", "02-02", "02-03"],
            axisLine: {
                lineStyle: {
                    color: '#999',
                    width: 0.6
                }
            },
            axisTick:{
                show:true,
            },
            axisLabel:{
                // rotate: 30,
                formatter: function (p) { return p.substr(5)}
            }
        }],
        yAxis: [
            {
                name: '',
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
                name:'',
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
            symbol: 'emptyCircle', // 
            symbolSize: 5,
            yAxisIndex: 0,
            itemStyle: {
                    normal: {color:'#F55253'},
            },
            data: [10, 20, 50]
        }, 
        {
            name: '新增确诊',
            type: 'bar',
            barWidth: 15,
            yAxisIndex: 1,
            itemStyle: {
                normal: {
                    barBorderRadius: 5,
                    color: '#F55253'
                }
            },
            data: [10, 8, 5]
        },
        {
            name: '累计治愈',
            type: 'line',
            smooth: true,
            showAllSymbol: true,
            symbol: 'roundRect', // emptyCircle
            symbolSize: 5,
            yAxisIndex: 1,
            itemStyle: {
                    normal: {color:'#178B50'},
            },
            data: [10, 20, 50]
        }
       ]
    };    
    return option;
}

let option = getOption();
let maxValues = [10, 10];
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

function last (ary) {
    return ary[ary.length - 1];
}

// 针对事件序列数据，数据上升一个维度
// param:   dts : {'2020-02-01': [code, confirmed, name, suspected, die, ok, addConfirmed]}
function getOptions (srcData) {
    let dts = translate(srcData);
    let codes = Object.keys(dts);
    codes.sort((a, b) => last(dts[b].data)[1] - last(dts[a].data)[1] );
    if (codes.length > 0) maxValues[0] = last(dts[codes[0]].data)[1]; 
    if (codes.length > 1) maxValues[1] = last(dts[codes[1]].data)[1];
    debugger
    let ic = new Utils.interpolateColor(['#FFAA85', '#FF7B69', '#BF2121', '#7F1818'], maxValues[1] * 1.5);
    
    [option.title, option.grid, option.xAxis, option.yAxis, option.series] = [[], [], [], [], []];
    codes.forEach((k, i) => {
        if (i > 5) return;
        let opt = getOption();
        let [title, grid, xAxis, yAxis, series] = [opt.title[0], opt.grid[0], opt.xAxis[0], opt.yAxis, opt.series];
        title.text = dts[k].name;
        title.top = i * 120;
        grid.top = i * 120 + 30;
        xAxis.gridIndex = i;
        yAxis[0].gridIndex = yAxis[1].gridIndex = i;
        series[0].xAxisIndex = series[1].xAxisIndex = series[2].xAxisIndex = i;
        [series[0].yAxisIndex, series[1].yAxisIndex, series[2].yAxisIndex] = [i * 2, i * 2 + 1, i * 2 + 1];
        
        let ds = dts[k].data.reduce((a, b, i) => {
            [a[0][i], a[1][i], a[2][i], a[3][i]] = [b[0], b[1], b[6], b[5]];
            return a;
        }, [[], [], [], []]);
        [xAxis.data, series[0].data, series[1].data, series[2].data] = ds;
        let numb = ds[1][ds[1].length - 1]; 
        title.subtext = "确诊：" + numb;
        series[0].itemStyle.normal.color = series[1].itemStyle.normal.color = ic.compute(numb);
        option.title.push(title);
        option.grid.push(grid);
        option.xAxis.push(xAxis);
        option.yAxis.push(yAxis[0], yAxis[1]);
        option.series.push(series[0], series[1], series[2]);
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