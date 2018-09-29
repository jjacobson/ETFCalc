document.addEventListener('DOMContentLoaded', function () {
    for (var i = 0; i < 3; i++) {
        add_row();
    }
});

function add_row() {
    let row = document.getElementsByTagName('template')[0];
    let table = document.getElementById('holding-table');
    let clone = row.content.cloneNode(true);
    table.appendChild(clone);
}

function remove_row(el) {
    let tr = el.parentElement.parentElement;
    tr.parentElement.removeChild(tr);
}

function ticker_value(el, ticker) {
    if (!ticker) {
        return;
    }
    $.ajax({
        data: {
            ticker: ticker
        },
        type: 'POST',
        url: '/ticker_value'
    }).done(function (data) {
        if (data.error) {
            console.log('Error fetching price data', data.error);
            return;
        }
        if (data == 'null') {
            return;
        }
        let tr = el.parentElement.parentElement;
        price_input = tr.querySelectorAll('input')[2];
        price_input.value = data;
    });
}