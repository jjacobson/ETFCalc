document.addEventListener('DOMContentLoaded', function () {
    for (let i = 0; i < 3; i++) {
        add_row();
    }

    load_data();
});

function save_data() {
    if (typeof(Storage) == 'undefined') {
        return;
    }

    let data = []
    let table = document.getElementById('holding-table');
    for (let i = 0; i < table.rows.length; i++) {
        let row = table.rows[i];
        let ticker = row.querySelector('[name=tickers]').value;
        let shares = row.querySelector('[name=shares]').value;
        let price = row.querySelector('[name=prices]').value;
        if (!(ticker && shares && price)) 
            continue;
        data.push([ticker.toUpperCase(), shares, price]);
    }
    sessionStorage.setItem('form-data', JSON.stringify(data));
}

function load_data() {
    console.log('loading');
    let table = document.getElementById('holding-table');
    let session_data = sessionStorage['form-data'];

    if (!session_data) {
        return;
    }
    let data = JSON.parse(session_data);
    for (let i = table.rows.length; i < data.length; i++) {
        add_row();
    }

    console.log('data is ', data, data.length)

    for (let i = 0; i < data.length; i++) {
        console.log('loading ticker ', i);

        if (!(data[i][0] && data[i][1] && data[i][2])) 
            continue;

        let row = table.rows[i];
        row.querySelector('[name=tickers]').value = data[i][0];
        row.querySelector('[name=shares]').value = data[i][1];
        row.querySelector('[name=prices]').value = data[i][2];
    }
}

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