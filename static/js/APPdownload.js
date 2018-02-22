function create_echart(id, data) {

}

function create_day(id, data) {
    
    var myChart = echarts.init(document.getElementById(id));
    var option = {
        title: {
            text: '日下载量',
            subtext: '纯属虚构'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['爱奇艺', '优酷']
        },
        //右上角工具条
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
            }
        ],
        yAxis: [
            {
                type: 'value',
                axisLabel: {
                    formatter: '{value} K'
                }
            }
        ],
        series: [
            {
                name: '爱奇艺',
                type: 'line',
                data: [30, 43, 70, 60, 80, 28, 51],
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            }
        ]
    };
    // 为echarts对象加载数据
    myChart.setOption(option);
}

function create_month(id, data) {
    var myChart = echarts.init(document.getElementById("mouthload"));
    var option = {

        title: {
            text: 'APP月下载量',
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['爱奇艺', '优酷']
        },
        //右上角工具条
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,

        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
            }
        ],
        yAxis: [
            {
                type: 'value',
                axisLabel: {
                    formatter: '{value} K'
                }
            }
        ],
        series: [
            {
                name: '爱奇艺',
                type: 'line',
                data: [300, 400, 452, 430, 700, 500, 600, 700, 600.800, 888, 901],
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            }
        ]
    };
    // 为echarts对象加载数据
    myChart.setOption(option);
}

