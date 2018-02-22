function create_echart(id, data) {
    try {
        if (id.search('star') > -1) {
            create_star(id, data)
        } else {
            create_ping(id, data)
        }
    } catch (e) {
        if (id.search('1') > -1 || id.search('2') > -1) {
            id.innerText = '还没有对应的数据，赶紧挑一个app关注吧'
        } else {
            id.innerText = '还没有对应的数据，试试搜索一下app吧'
        }
    }

}

function create_star(id, data) {
    var ratings = data['xing'];
    if (ratings.length===0) return;
    var myChart = echarts.init(document.getElementById(id));
    option = {
        toolbox: {
            show: true,
            feature: {
                dataView: {show: true, readOnly: false},
                saveAsImage: {show: true}
            }
        },
        title: {
            text: data['app_name'] + '星级评分统计',
            x: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['1颗星', '2颗星', '3颗星', '4颗星', '5颗星']
        },
        series: [
            {
                name: '星级',
                type: 'pie',
                radius: '60%',
                center: ['50%', '50%'],
                data: [
                    {value: ratings[0], name: '1颗星'},
                    {value: ratings[1], name: '2颗星'},
                    {value: ratings[2], name: '3颗星'},
                    {value: ratings[3], name: '4颗星'},
                    {value: ratings[4], name: '5颗星'}
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    myChart.setOption(option);
}

function create_ping(id, data) {
    var ratings = data['ping'];
    if (ratings.length===0) return;
    var myChart = echarts.init(document.getElementById(id));
    option = {
        title: {
            text: data['app_name'] + '评分统计',
            x: 'center'
        },
        toolbox: {
            show: true,
            feature: {
                dataView: {show: true, readOnly: false},
                saveAsImage: {show: true}
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data: ['好评', '中评', '差评']
        },
        series: [
            {
                name: '评价',
                type: 'pie',
                radius: ['50%', '60%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data: [
                    {value: ratings[2], name: '好评'},
                    {value: ratings[1], name: '中评'},
                    {value: ratings[0], name: '差评'}
                ]
            }
        ]
    };
    myChart.setOption(option);
}

function search_app() {
    var app_name = $('#app_name').val();
    if (app_name === "" || app_name.trim() === "") {
        alert('app名字不能为空');
        return;
    }
    $.ajax({
        url: '/user/score/search/' + app_name,
        type: 'GET',
        dataType:'json',
        success: function (data) {
            create_star('star_search', data);
            create_ping('ping_search', data);
        }
    })
}
