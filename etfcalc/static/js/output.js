function back() {
    window.location.replace('/');
}

$(document).ready(function () {
    $('#output-table').DataTable({
        "order": [[ 3, "desc" ]],
        "pageLength": 25
    });
});