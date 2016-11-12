$( document ).ready( function () {

    $("input.optional_field").on('change', function() {
        $('input.optional_field').not(this).prop('checked', false);
    });


    $('#edit_optional_button').click( function (e) {
        if ($("#input.optional_field input:checkbox:checked").length > 0) {
            e.preventDefault();
            $('#edit_warning').show();

        }
    });

});