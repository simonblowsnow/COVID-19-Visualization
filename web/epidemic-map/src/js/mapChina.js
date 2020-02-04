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
            color: ['#e0ffff', '#006edd'],
            symbolSize: [50, 50]
        }
    },
    series: [{
        name: 'china',
        type: 'map',
        mapType: 'china',
        roam: true,
        itemStyle: {
            normal: {
                label: {
                    show: false
                }
            },
            emphasis: {
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
    option.series[0].data = data;
    Utils.draw(chart1, id);
};


export default chart1;