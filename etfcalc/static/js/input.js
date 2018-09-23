document.addEventListener('DOMContentLoaded', function () {
    for (var i = 0; i < 3; i++) {
        add_row();
    }
});

function add_row() {
    let row = document.getElementsByTagName("template")[0];
    let table = document.getElementById('holding-table');
    let clone = row.content.cloneNode(true);
    table.appendChild(clone);
}

function remove_row(el) {
    let tr = el.parentElement.parentElement;
    tr.parentElement.removeChild(tr);
}
