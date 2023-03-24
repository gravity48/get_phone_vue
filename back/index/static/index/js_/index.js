function delete_disabled_button(msg){
    let proj_div = msg['context'][0];
    $.each($(proj_div).find('.play-block .play-btn'), function (index, item){
        $(item).removeAttr('disabled');
    });
    $.each($(proj_div).find('.settings-block button'), function (index, item){
        $(item).attr('disabled', true);
    });
    $(proj_div).find('form').find('input, textarea, select').each(function (){
        $(this).attr('disabled', true);
    });
}

function update_log(){
    function show_log(msg){
        $('#block3 .body-panel').html(decodeURI(msg.render_html));
    }
    if($('#block3').is(':visible')){
        let data = {
            'event': 'update_log'
        }
        send_json_ajax(data, '', show_log, console_log);
    }
}

function error_run_project(msg){
    $('#error-block h5').html(msg.responseJSON.error_txt);
    $('#error-block').removeClass('hidden');
}


function event_list() {
    $(document).on('click', '.verification-btn', function (event) {
        let proj_div = $(this).parents('.proj-div:first');
        CURRENT_FORM = $(proj_div).find('.settings-form:first')
        $(CURRENT_FORM).find('input').removeClass('is-valid');
        $(CURRENT_FORM).find('input').removeClass('is-invalid');
        let [data, status] = json_from_data_map_form($(CURRENT_FORM));
        if (status) {
            send_json_ajax(data, '', delete_disabled_button, show_exception_on_form, proj_div);
        }
    });

    $(document).on('click', 'form .play-btn ', function (event){
        let data = {
            'event': $(this).siblings('input').val(),
        }
        send_json_ajax(data, '', reload_window, error_run_project);
    });

    $(document).on('click', 'form .stop-btn', function (event) {
        let data = {
            'event': 'stop_proj',
            'proj_name': $(this).attr("data-proj"),
        }
        send_json_ajax(data, '', reload_window, error_run_project);

    });
    $(document).on('click', '.auto-date-check', function (event) {
        let datepicker = $(".datepicker-here", $(this).parents('.input-group'));
        if ($(datepicker).attr('disabled')) {
            $(datepicker).prop('disabled', false);
        }
        else{
            $(datepicker).prop('disabled', true);
        }
    });


    /*
    update_log();
    setInterval(update_log, 20000);
    */
}

$(document).ready(event_list);