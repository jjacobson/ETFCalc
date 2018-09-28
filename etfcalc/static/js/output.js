function back() {
    window.location.replace('/');
}

$(document).ready(function () {
    $('#output_table').DataTable({
        "order": [[ 2, "desc" ]],
        "pageLength": 25
    });
});