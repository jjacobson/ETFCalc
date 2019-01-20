document.addEventListener('DOMContentLoaded', function () {
    for (let i = 0; i < 3; i++) {
        add_row();
    }

    load_data();
});

document.addEventListener('focusout', function () {
    validate_inputs();    
})

document.addEventListener('input', function () {
    validate_inputs();    
})

function save_data() {
    if (typeof (Storage) == 'undefined') {
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
    let table = document.getElementById('holding-table');
    let session_data = sessionStorage['form-data'];

    if (!session_data) {
        return;
    }
    let data = JSON.parse(session_data);
    for (let i = table.rows.length; i < data.length; i++) {
        add_row();
    }

    for (let i = 0; i < data.length; i++) {
        if (!(data[i][0] && data[i][1] && data[i][2]))
            continue;

        let row = table.rows[i];
        row.querySelector('[name=tickers]').value = data[i][0];
        row.querySelector('[name=shares]').value = data[i][1];
        row.querySelector('[name=prices]').value = data[i][2];
    }
    validate_inputs();
}

function add_row() {
    let row = document.getElementsByTagName('template')[0];
    let table = document.getElementById('holding-table');
    let clone = row.content.cloneNode(true);
    if (table.rows.length == 1) {
        let button = table.rows[0].querySelector('button');
        button.removeAttribute('disabled');
    }
    table.appendChild(clone);
}

function remove_row(el) {
    let tr = el.parentElement.parentElement;
    let table = document.getElementById('holding-table');

    $(tr.querySelectorAll('input')[0]).tooltip({ trigger: 'manual' }).tooltip('hide');
    tr.parentElement.removeChild(tr);

    if (table.rows.length == 1) {
        let button = table.rows[0].querySelector('button');
        button.setAttribute('disabled', true);
    }
    validate_inputs();
}

function ticker_value(el, ticker) {
    if (!ticker) {
        return;
    }
    let tr = el.parentElement.parentElement;
    let spinner = tr.querySelector('.spinner');
    spinner.classList.remove('hidden');
    $.ajax({
        data: {
            ticker: ticker
        },
        type: 'POST',
        url: '/ticker_value'
    }).done(function (data) {
        spinner.classList.add('hidden');
        if (data.error) {
            console.log('Error fetching price data', data.error);
            return;
        }
        if (data == 'null') {
            invalid_ticker(el, ticker);
            return;
        }
        let price_input = tr.querySelectorAll('input')[2];
        $(el).tooltip({ trigger: 'manual' }).tooltip('hide');
        price_input.value = data;
        validate_inputs();
    });
}

function invalid_ticker(el) {
    $(el).tooltip({ trigger: 'manual' }).tooltip('show');
}

function validate_inputs() {
    let valid_input = false;
    let table = document.getElementById('holding-table');
    let button = document.getElementById('submit');
    for (let i = 0; i < table.rows.length; i++) {
        let row = table.rows[i];
        if (valid_row(row)) {
            valid_input = true;
        }
    }
    button.disabled = !valid_input;
}

function valid_row(row) {
    let ticker = row.querySelector('[name=tickers]').value;
    let shares = row.querySelector('[name=shares]').value;
    let price = row.querySelector('[name=prices]').value;
    return (ticker && (shares > 0) && price);
}