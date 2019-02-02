document.addEventListener('DOMContentLoaded', function () {
    console.log('Options built');
    load_options();
});

function reset_options() {
    if (typeof (Storage) == 'undefined') {
        return;
    }
    localStorage.setItem('option-data', JSON.stringify(default_options));

    load_options();
}

function save_options() {
    if (typeof (Storage) == 'undefined') {
        return;
    }

    let data = [];
    let table = document.querySelector('#options-table');
    for (let i = 0; i < table.rows.length; i++) {
        let row = table.rows[i];
        let option = undefined;
        let input;

        try {
            input = row.querySelector('[name=option_val_toggle]');
            option = input.checked;
        } catch (err) {
            try {
                input = row.querySelector('[name=option_val_text]');
                option = input.value;
            } catch (err) {

            }
        }

        if (option === undefined)
            continue;
        data.push(option);
    }
    localStorage.setItem('option-data', JSON.stringify(data));
}

function load_options() {
    let table = document.getElementById('options-table');
    let session_data = localStorage['option-data'];

     if (!session_data) {
         reset_options();
        return;
    }
    session_data = JSON.parse(session_data);
    let data = get_option_array();
    while (table.firstChild) {
        table.removeChild(table.firstChild);
    }

    for (let i = 0; i < session_data.length; i++) {
        data[i].value = session_data[i];
        add_option(data[i].type);
    }

    for (let i = 0; i < data.length; i++) {
        let row = table.rows[i];
        let cells = row.querySelectorAll('td');
        cells[0].innerText = data[i].title;
        if (data[i].type === 'toggle') {
            cells[1].querySelector('input').checked = data[i].value;
        } else {
            cells[1].querySelector('input').value = data[i].value;
        }
        cells[2].innerText = data[i].description;
    }
}

function add_option(type) {
    let row = document.getElementById(type + '-template');
    let table = document.getElementById('options-table');
    let clone = row.content.cloneNode(true);
    table.appendChild(clone);
}

function get_option_array() {
    return [
        {
            title: 'Use Yahoo as backup data source',
            type: 'toggle',
            description: 'When enabled a webscraper will search through Yahoo page code for quotes on ticker symbols' +
                'hat are unknown to our other sources. This will however slow down the data fetching.'
        },
        {
            title: 'Default currency',
            type: 'text',
            description: 'This sets your preferred default currency, used for all calculations in this tool.'
        }
    ]
}