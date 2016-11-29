$( document ).ready( function () {

   $('#professor_class_table').DataTable({
        "paging": false,
        "info": false,
        "searching": false
    });

    $('#show_inactive').change(function () {
        if($('#inactive_classes').is(":visible")){
            $('#inactive_classes').hide();
        } else {
            $('#inactive_classes').show();
        }
    });

});
