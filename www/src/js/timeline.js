
function getTimeline () {
    return {
        data: ["2016", "2017"],
        axisType: "category",
        autoPlay: true,
        loop: true,
        currentIndex: 0,
        playInterval: 1200,
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
    };
}

export default getTimeline;