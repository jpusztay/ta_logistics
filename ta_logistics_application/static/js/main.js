$( document ).ready( function () {
    $(window).resize(function() {
        if( $(window).width() >= 992 ) {
            $('#resume_view').show();
            $('#resume_link').hide();
        }
        if( $(window).width() < 992 ) {
            $('#resume_view').hide();
            $('#resume_link').show();
        }
    });

    $('#professor_class_table').DataTable({
        "paging": false,
        "info": false,
        "searching": false
    });
});