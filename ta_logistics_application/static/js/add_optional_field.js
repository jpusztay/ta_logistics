$( document ).ready( function () {

    $('#id_data_type').change(function () {
        if ($('#id_data_type').val() == "TEXT") {
            $("#id_max_length").parent().show();
            $("#id_select_options").parent().show();
        } else if ($('#id_data_type').val() == "CMFT") {
            $("#id_select_options").parent().hide();
            $("#id_max_length").parent().hide();
        } else {
            $("#id_select_options").parent().show();
            $("#id_max_length").parent().show();
        }

        if($('#id_data_type').val() == "INT" || $('#id_data_type').val() == "REAL"){
            $("label[for='#id_max_length']").text('Max Size');
        } else {
            $("label[for='#id_max_length']").text('Max Length');
        }
    });
});