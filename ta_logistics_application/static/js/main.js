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

    $('#select-all').click(function () {
        var status = this.checked;
        $('.select-applicant').each(function () {
            this.checked = status;
        });
    });

    $('#professor_class_table').DataTable({
        "paging": false,
        "info": false,
        "searching": false
    });
});