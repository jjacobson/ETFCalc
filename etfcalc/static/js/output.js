function back() {
    window.location.replace('/');
}

$(document).ready(function () {
    $('#output-table').DataTable({
        "order": [[3, "desc"]],
        "pageLength": 25
    });
    let chart_data = $('#chart_data').data("charts");
    display_charts(chart_data)
});

function display_charts(chart_data) {
    console.log(chart_data)
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