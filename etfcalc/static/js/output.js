var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"];

document.addEventListener('DOMContentLoaded', function () {
    load_news_section();
});

$(document).ready(function () {
    let holding_table = $('#output-table').DataTable({
        "order": [[3, "desc"]],
        "lengthMenu": [15, 25, 50, 100],
        "pageLength": 15
    });
    $('#output-table tbody').on('click', 'tr', function () {
        let data = holding_table.row(this).data();
        holding_modal(data[0], data[1]);
    });

    $('#div-table').DataTable({
        "order": [[0, "desc"]],
        "pageLength": 8,
        "lengthChange": false,
        "searching": false
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
        attribute_display(data['quote'], data['stats']);
        dividend_history(data['dividends']);
    });
}

function price_display(quote_data) {
    // title
    $('#title').text(quote_data['symbol']);

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
    var hour = (date.getHours() <= 12) ? date.getHours() : date.getHours() - 12;
    let timestring = months[date.getMonth()] + ' ' + date.getDate() + ', ' +
        hour + ':' + ('0' + date.getMinutes()).slice(-2) + ' ' + am_pm;
    $('#date').text(timestring);
}

function attribute_display(quote_data, stat_data) {
    $('#attr-close').text(quote_data['previousClose']);
    $('#attr-open').text(quote_data['open']);
    $('#attr-bid').text(bid_ask_display(quote_data['iexBidPrice'], quote_data['iexBidSize']));
    $('#attr-ask').text(bid_ask_display(quote_data['iexAskPrice'], quote_data['iexAskSize']));
    $('#attr-daily').text(quote_data['high'].toFixed(2) + ' - ' + quote_data['low'].toFixed(2));
    $('#attr-year').text(quote_data['week52Low'].toFixed(2) + ' - ' + quote_data['week52High'].toFixed(2));
    $('#attr-vol').text(quote_data['latestVolume'].toLocaleString());
    $('#attr-avg-vol').text(quote_data['avgTotalVolume'].toLocaleString());

    let change = (stat_data['ytdChangePercent'] * 100).toFixed(2);
    $('#attr-change').text(change > 0 ? '+' + change : change);
    $('#attr-mkt-cap').text(quote_data['marketCap']);
    $('#attr-pe').text(quote_data['peRatio']);
    $('#attr-eps').text(stat_data['latestEPS']);
    $('#attr-beta').text(stat_data['beta']);
    $('#attr-div-date').text(date_string(stat_data['exDividendDate']));
    $('#attr-div-yield').text(stat_data['dividendYield']);
    $('#attr-div-rate').text(stat_data['dividendRate'].toFixed(2));
}

function bid_ask_display(bid, ask) {
    return bid && ask ? bid + ' x ' + ask : 'Markets Closed'
}

function dividend_history(dividend_data) {
    let table = $('#div-body');
    for (let i = 0; i < dividend_data.length; i++) {
        let change = '-';
        if (dividend_data.length > i + 1) {
            let newer = dividend_data[i]['amount'];
            let older = dividend_data[i + 1]['amount'];
            if (newer != older) {
                change = (((newer - older) / older) * 100).toFixed(2) + '%';
            }
        }
        $('#div-table').DataTable().row.add([
            dividend_data[i]['exDate'], dividend_data[i]['paymentDate'], dividend_data[i]['amount'], change
        ]).draw();
    }
}

function candle_chart(name, chart_data) {
    let data_points = []
    let chart = new CanvasJS.Chart('chart-stock', {
        animationEnabled: true,
        zoomEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        title: {
            text: name + " - 5Y Chart"
        },
        axisY: {
            includeZero: false,
            prefix: "$",
        },
        toolTip: {
            content: get_tooltip()
        },
        data: [{
            type: "candlestick",
            color: "grey",
            risingColor: "green",
            fallingColor: "red",
            yValueFormatString: "$##0.00",
            xValueFormatString: "DD MMM YYYY",
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
        $('#div-body').empty();
        chart.destroy();
    })
}

function parse_data_points(chart_data, data_points) {
    for (day of chart_data) {
        let date = new Date(day['date']);
        let change = day['change'].toFixed(2);
        change = change > 0 ? '+' + change : change;
        let candle = [day['open'], day['high'], day['low'], day['close']];
        let data = [day['volume'].toLocaleString(), change];
        data_points.push({ x: date, y: candle, label: data });
    }
}

function get_tooltip() {
    return document.getElementById('tooltip').innerHTML;
}

function date_string(date_string) {
    date = new Date(date_string);
    return months[date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear();
}