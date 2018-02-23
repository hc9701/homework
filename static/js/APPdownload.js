function create_echart(id, data) {
    try {
        if (id.search('day') > -1) {
            create_day(id, data)
        } else {
            create_month(id, data)
        }
    } catch (e) {
        if (id.search('1') > -1 || id.search('2') > -1) {
            id.innerHTML = '还没有对应的数据，赶紧挑一个app关注吧'
        } else {
            id.innerHTML = '还没有对应的数据，试试搜索一下app吧'
        }
    }
}

function create_day(id, data) {
    if (data['daily_data'].length === 0) {
        throw new Error('找不到对应的app');
    }
    var option = {
        title: {
            text: data['app_name'] + '日下载量',
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: [data['app_name']]
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
                data: data['daily_data'][0]
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
                data: data['daily_data'][1],
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
    var myChart = echarts.init(document.getElementById(id));
    myChart.setOption(option);
}

function create_month(id, data) {
    if (data['monthly_data'].length === 0) {
        throw new Error('找不到对应的app')
    }
    var option = {

        title: {
            text: data['app_name'] + '月下载量',
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: [data['app_name']]
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
                data: data['monthly_data'][0]
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
                data: data['monthly_data'][1],
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
    var myChart = echarts.init(document.getElementById(id));
    myChart.setOption(option);
}

function search_app() {
    var app_name = $('#app_name').val();
    if (app_name === "" || app_name.trim() === "") {
        alert('app名字不能为空');
        return;
    }
    $.ajax({
        url: '/user/download/search/' + app_name,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            create_echart('day_search', data);
            create_echart('month_search', data);
        }
    })
}
