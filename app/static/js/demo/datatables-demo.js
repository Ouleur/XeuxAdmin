// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    dom: 'Bfrtip',
    buttons: [
        'excel',
    ]
});
  $('#dataMatiereTable').DataTable({
    dom: 'Bfrtip',
    buttons: [
        'excel',
    ]
});
});
