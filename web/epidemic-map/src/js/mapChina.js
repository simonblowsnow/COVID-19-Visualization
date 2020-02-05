import {Utils} from "../js/utils";

let option = {
    visualMap: {
        min: 0,
        max: 1000,
        left: 'left',
        top: 'bottom',
        text: ['高', '低'],
        calculable: true,
        inRange: {
            color: ['#FFAA85', '#FF7B69', '#BF2121', '#7F1818'],
            symbolSize: [50, 50]
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
                    let v = p.data ? p.data.tags[1] : 0;
                    return '{fline|' + p.name + '}\n{tline|确诊: '+ p.value +'\n疑似：' + v + '}';
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

let chart1 = {
    name: "china",
    option: option,
    initData: null,
    instance: null
}

// 需在地图注册后调用，注册地图时应使用name为名称
chart1.initData = function (srcData, id) {
    let data = Utils.formatRegion(chart1.name, srcData);
    if (data.length === 0) return;
    data.sort((a, b) => b.value - a.value);
    // 颜色渲染最大值，second * 1.25
    let maxColorValue = parseInt(1.25 * (data.length == 1 ? data[0].value : data[1].value));
    console.log(maxColorValue);
    option.visualMap.max = maxColorValue;
    option.series[0].data = data;
    Utils.draw(chart1, id);
};


export default chart1;