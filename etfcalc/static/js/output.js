document.addEventListener('DOMContentLoaded', function () {
    load_news_section();
});

$(document).ready(function () {
    $('#output-table').DataTable({
        "order": [[3, "desc"]],
        "lengthMenu": [15, 25, 50, 100],
        "pageLength": 15
    });
    let chart_data = $('#chart_data').data("charts");
    display_charts(chart_data)
});

function display_charts(chart_data) {
    let chart = new CanvasJS.Chart("chartContainer", {
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
            break;
        }
        if (!news_item.classList.contains('gone')) {
            continue;
        }
        news_item.classList.remove('gone');
        count -= 1;
    }
}

function back() {
    window.location.replace('/');
}