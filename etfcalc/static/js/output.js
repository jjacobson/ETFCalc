var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"];

document.addEventListener('DOMContentLoaded', function () {
    load_news_section();
});

$(document).ready(function () {
    let table = $('#output-table').DataTable({
        "order": [[3, "desc"]],
        "lengthMenu": [15, 25, 50, 100],
        "pageLength": 15
    });
    $('#output-table tbody').on('click', 'tr', function () {
        let data = table.row(this).data();
        holding_modal(data[0], data[1]);
    });

    let chart_data = $('#chart_data').data('charts');
    display_charts(chart_data)
});

function display_charts(chart_data) {
    let chart = new CanvasJS.Chart('chart-sector', {
        animationEnabled: true,
        backgroundColor: "transparent",
        title: {
            text: "Holding Sectors"
        },
        data: [{
            type: "pie",
            startAngle: 240,
            yValueFormatString: "##0.00\"%\"",
            indexLabel: "{label} {y}",
            dataPoints: get_data_points(chart_data)
        }]
    });
    chart.render();
}

function get_data_points(chart_data) {
    data_points = [];
    for (row in chart_data) {
        value = chart_data[row];
        data_points.push({ y: value, label: row });
    }
    return data_points;
}

function load_news_section() {
    let count = 5;
    let news = document.getElementById('news');
    for (i = 0; i < news.children.length, count != 0; i++) {
        let news_item = news.children[i];
        if (!news_item) {
            disable_news_btn();
            break;
        }
        if (!news_item.classList.contains('gone')) {
            continue;
        }
        news_item.classList.remove('gone');
        count -= 1;
        if (i == news.children.length - 1) {
            disable_news_btn();
        }
    }
}

function disable_news_btn() {
    let btn = document.getElementById('btn-news');
    btn.disabled = true;
}

function back() {
    window.location.replace('/');
}

function holding_modal(name, ticker) {
    name = $(name).text();
    let title = name + ' - ' + ticker;
    $('#modal-title').text(title);
    $('#holding-data').modal();
    $.ajax({
        data: {
            ticker: ticker
        },
        type: 'POST',
        url: '/holding_data'
    }).done(function (data) {
        $('#spinner').addClass('gone');
        $('#modal-data').removeClass('gone');
        if (data.error) {
            console.log('Error fetching stock data', data.error);
            return;
        }
        if (data == 'null') {
            console.log('null data')
            // todo handle null data
            return;
        }
        data = JSON.parse(data);
        data = data[ticker];
        price_display(data['quote']);
        candle_chart(name, data['chart']);
    });
}

function price_display(quote_data) {
    // price
    let price = parseFloat(quote_data['latestPrice'])
    $('#price').text(price);

    // change
    let change = quote_data['change'];
    let icon_id = change > 0 ? '.oi-caret-top' : '.oi-caret-bottom';
    let change_type = change > 0 ? 'positive' : 'negative';
    $(icon_id).removeClass('gone');
    $('#change-header').addClass(change_type);
    let change_text = change + ' (' + quote_data['changePercent'].toFixed(2) + ')';
    $('#change').text(change_text);

    // formatted date and time
    let date = new Date(quote_data['latestUpdate']);
    var am_pm = (date.getHours() < 12) ? "AM" : "PM";
    var hour = (date.getHours() < 12) ? date.getHours() : date.getHours() - 12;
    let timestring = months[date.getMonth()] + ' ' + date.getDate() + ', ' +
        hour + ':' + ('0' + date.getMinutes()).slice(-2) + ' ' + am_pm;
    $('#date').text(timestring);
}

function candle_chart(name, chart_data) {
    let data_points = []
    let chart = new CanvasJS.Chart('chart-stock', {
        animationEnabled: true,
        zoomEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title: {
            text: name + " 1 Year Chart"
        },
        subtitles: [{
            text: "Weekly Averages"
        }],
        axisX: {
        },
        axisY: {
            includeZero: false,
            prefix: "$",
        },
        toolTip: {
            content: "Date: {x}<br/><strong>Price:</strong><br/>Open: {y[0]}, Close: {y[3]}<br />High: {y[1]}, Low: {y[2]}"
        },
        data: [{
            type: "candlestick",
            yValueFormatString: "$##0.00",
            dataPoints: data_points
        }]
    });
    parse_data_points(chart_data, data_points)
    chart.render();
    $('#holding-data').on('hidden.bs.modal', function () {
        $('#spinner').removeClass('gone');
        $('#modal-data').addClass('gone');
        $('#change-header').removeClass('positive negative');
        $('.caret').addClass('gone');
        chart.destroy();
    })
}

function parse_data_points(chart_data, data_points) {
    for (day of chart_data) {
        let date = new Date(day['date'])
        let candle = [day['open'], day['high'], day['low'], day['close']];
        data_points.push({ x: date, y: candle })
    }
}