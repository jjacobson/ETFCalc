document.addEventListener('DOMContentLoaded', function(){
    //Wait to add event listeners until the DOM is fully loaded. This is needed
    // when wanting to access elements that are later in the HTML than the <script>.
    for (var i = 0; i < 5; i++) {
        add_row();
    }
});

function add_row() {
    var row = document.getElementsByTagName("template")[0];
    let table = document.getElementById('holding-table');
    let clone = row.content.cloneNode(true);
    table.appendChild(clone);
}