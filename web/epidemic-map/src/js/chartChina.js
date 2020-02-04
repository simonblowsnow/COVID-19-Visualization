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
            },
            {
                name: '四川',
                value: Math.round(Math.random() * 1000)
            }
        ]
    }]
}

function init () {

}

let chart1 = {
    name: 'china',
    option: option,
    initData: init,
    instance: null
}

export default chart1;