function back() {
    window.location.replace('/');
}

$(document).ready(function () {
    $('#output-table').DataTable({
        "order": [[ 2, "desc" ]],
        "pageLength": 25
    });
});