import {Utils} from "../js/utils";


function getOption () {
    let option = {
        title: [
            {
                text: '',
                left: 0,
                textStyle: {
                    fontSize: 16
                }
            },
            {
                text: '',
                left: 100,
                textStyle: {
                    color: "#F55253",
                    fontWeight: 'normal',
                    fontSize: 12
                }
            }
        ],
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
        axisPointer: {
			link: {
				// xAxisIndex: 'all'
			}
		},
        legend: {
            data: ['累计确诊', '新增确诊', '累计治愈'],
            top: 0,
            right: '30'
        },
        grid:[
            {
                containLabel: true,
                left: 0,
                right: 0,
                top: 30,
                height: 120
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
                axisLabel: {
                    formatter: function (p) { return p < 5000 ? p : p / 1000 + "k"},
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
                min: 0,
                axisLine: {
                    lineStyle: {
                        color: '#B4B4B4',
                    }
                }, 
                axisLabel:{
                    formatter: function (p) { return p < 1000 ? p : p / 1000 + "k"},
                }
            }
        ],
        series: [{
            name: '累计确诊',
            type: 'line',
            smooth: true,
            showAllSymbol: true,
            symbol: 'emptyCircle', // 
            symbolSize: 4,
            yAxisIndex: 0,
            itemStyle: {
                normal: {color:'#F55253'}
            },
            lineStyle: {width: 1},
            data: [10, 20, 50]
        }, 
        {
            name: '新增确诊',
            type: 'bar',
            barMaxWidth: 20,
            yAxisIndex: 1,
            itemStyle: {
                normal: {
                    barBorderRadius: 3,
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
            symbolSize: 4,
            yAxisIndex: 1,
            itemStyle: {
                normal: {color:'#178B50'},
            },
            lineStyle: {width: 1},
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
    let tms = Object.keys(srcData).sort();
    tms.forEach(t => {
        srcData[t].forEach(d => {
            let code = d[0];
            if (!(code in rs)) rs[code] = {name: d[2], data: []};
            let line = [t, d[1], "", d[3], d[4], d[5], d[6], d[7]];
            rs[code].data.push(line);
        });
    });
    console.log(rs);
    return rs;
}

function autoSize (id, dataCount) {
    let height = dataCount * 150 + 40;
    document.getElementById(id).style.height = (height < 350 ? 350 : height) + "px";
}

function last (ary) {
    return ary[ary.length - 1];
}

function getStatus(ary) {
    let labels = ["↑", "↓"];
    if (ary.length < 2) return "";
    let status = last(ary) > ary[ary.length - 2] ? 0 : 1;
    let txt = labels[status];
    if (ary.length === 2) return txt;
    for (let i = ary.length - 3; i >= 0 ; i--) {
        let flag = ary[i + 1] > ary[i] ? 0 : 1;
        if (flag != status) break;
        txt += labels[flag];
    }
    if (txt.length > 5) return txt.substr(0, 5) + "➪" + txt.length;
    return txt;
}

// 针对事件序列数据，数据上升一个维度
// param:   dts : {'2020-02-01': [code, confirmed, name, suspected, die, ok, addConfirmed]}
function getOptions (srcData, id) {
    let dts = translate(srcData);
    let codes = Object.keys(dts);
    autoSize(id, codes.length);
    codes.sort((a, b) => last(dts[b].data)[1] - last(dts[a].data)[1] );
    if (codes.length > 0) maxValues[0] = last(dts[codes[0]].data)[1]; 
    if (codes.length > 1) maxValues[1] = last(dts[codes[1]].data)[1];
    let ic = new Utils.interpolateColor(['#FFAA85', '#FF7B69', '#BF2121', '#7F1818'], maxValues[1] * 1.5);
    
    [option.title, option.grid, option.xAxis, option.yAxis, option.series] = [[], [], [], [], []];
    codes.forEach((k, i) => {
        let opt = getOption();
        let [title, grid, xAxis, yAxis, series] = [opt.title, opt.grid[0], opt.xAxis[0], opt.yAxis, opt.series];
        title[0].text = dts[k].name;
        title[0].top = i * 150 + 40;
        title[1].top = i * 150 + 45;
        grid.top = i * 150 + 70;
        xAxis.gridIndex = i;
        yAxis[0].gridIndex = yAxis[1].gridIndex = i;
        series[0].xAxisIndex = series[1].xAxisIndex = series[2].xAxisIndex = i;
        [series[0].yAxisIndex, series[1].yAxisIndex, series[2].yAxisIndex] = [i * 2, i * 2 + 1, i * 2];
        
        let ds = dts[k].data.reduce((a, b, i) => {
            [a[0][i], a[1][i], a[2][i], a[3][i]] = [b[0], b[1], b[6], b[5]];
            return a;
        }, [[], [], [], []]);
        [xAxis.data, series[0].data, series[1].data, series[2].data] = ds;
        let numb = last(ds[1]); 
        title[1].text = "确诊 " + numb + ", 新增 " + last(ds[2]) + " · " + getStatus(ds[2]);
        title[1].left = dts[k].name.length * 15 + 15;
        series[0].itemStyle.normal.color = series[1].itemStyle.normal.color = ic.compute(numb);
        option.title.push(title[0], title[1]);
        option.grid.push(grid);
        option.xAxis.push(xAxis);
        option.yAxis.push(yAxis[0], yAxis[1]);
        option.series.push(series[0], series[1], series[2]);
    });
    
    return option;
}

chart.initData = function (srcData, id, level) {
    let _option = getOptions(srcData, id);

    console.log([srcData, id, level, _option]);
    let myChart = Utils.draw(chart, id);
    return myChart;
    // myChart.dispatchAction({ type: 'legendUnSelect', name: "疑似" })
};

let chartLine = chart;
export default chartLine;