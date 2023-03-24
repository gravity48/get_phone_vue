const DEFAULT_SIZE_FILE = 100000000;
var FILES_COUNT = 0;
var CURRENT_FORM;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function closeOrNot(e) {
    if (!e) e = window.event;
    e.cancelBubble = true;
    e.returnValue = '';
    if (e.stopPropagation) {
        e.stopPropagation();
        e.preventDefault();
    }
}

function clear_form(form_selector) {
    $(form_selector).find('input').removeClass('is-valid');
    $(form_selector).find('input').removeClass('is-invalid');
}

function serialize_form(elem) {
    let form = $(elem).parents('form:first');
    return form.serialize();
}

function json_from_data_map_form(form) {
    let status = true;
    let data_array_item = 'data_array';
    let form_map = {};
    $(form).find('input, textarea, select').each(function () {
        if($(this).parents('.data-map').length){
            return;
        }
        if ($(this).prop('readonly')) {
            return
        }
        if ($(this).prop('disabled')) {
            return
        }
        if($(this).is(':checkbox') && !$(this).is(':checked')){
            return
        }
        if($(this).prop('required')){
            if($(this).val()===""){
                $(this).addClass('is-invalid');
                status = false;
            }
        }
        let value = $(this).val();
        let item = $(this).attr("name");
        form_map[item] = value;
    });
    $(form).find('.data-map').each(function () {
        let [data_map, status] = json_from_form($(this));
        form_map[data_array_item] = data_map;
    });
    return [form_map, status];
}

function json_from_form(form) {
    let status = true;
    let form_map = {};
    $(form).find('input, textarea, select').each(function () {
        if ($(this).prop('disabled')) {
            return
        }
        if($(this).is(':checkbox') && !$(this).is(':checked')){
            return
        }
        if($(this).prop('required')){
            if($(this).val()===""){
                $(this).addClass('is-invalid');
                status = false;
            }
        }
        let value = $(this).val();
        let item = $(this).attr("name");
        form_map[item] = value;
    });
    return [form_map, status];
}

function close_modal_form(msg) {
    $('#modal_form')
        .animate({opacity: 0, top: '45%'}, 200,  // плaвнo меняем прoзрaчнoсть нa 0 и oднoвременнo двигaем oкнo вверх
            function () { // пoсле aнимaции
                $(this).css('display', 'none'); // делaем ему display: none;
                $('#overlay').fadeOut(400); // скрывaем пoдлoжку
            }
        );
}

function show_exception_on_form(msg, form_selector) {
    let errors_map = new Map(Object.entries(msg.responseJSON));
    let input_list = $(form_selector).find('input');
    $.each(input_list, function (index, input) {
        let attribute = $(input).attr('name');
        if (errors_map.has(attribute)) {
            $(input).addClass('is-invalid');
            $(input).siblings('.invalid-feedback').html(errors_map.get(attribute)[0].message);
        } else {
            $(input).addClass('is-valid');
        }
    });

}

function send_json_ajax(data, url, success_event, error_event, context = null, type = 'POST') {
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: type,
        url: url,
        data: JSON.stringify(data),
        dataType: "json",
        context: context,
        contentType: 'application/json',
        beforeSend: function(){
            $('.preloader').removeClass('hidden');
        },
        complete: function (){
            $('.preloader').addClass('hidden');
        },
        success: function (msg) {
            msg['context'] = $(this);
            success_event(msg);
        },
        error: function (msg) {
            msg['context'] = $(this);
            error_event(msg, context);
        }
    });
}

function send_ajax(data, url, success_event, error_event, context=null, type = 'POST') {
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        type: type,
        url: url,
        context: context,
        data: data,
        beforeSend: function(){
            $('.preloader').removeClass('hidden');
        },
        complete: function (){
            $('.preloader').addClass('hidden');
        },
        success: function (msg) {
            success_event(msg);
        },
        error: function (msg) {
            msg['context'] = context;
            error_event(msg, context);
        }
    });

}

function default_send_form_ajax(button, url, success_event, error_event) {
    var current_form = $(button).parent();
    CURRENTLY_FORM = $(button).parent();
    $(current_form).find('.help-block').html('');
    $(current_form).find('.input-group').removeClass('has-success');
    $(current_form).find('.input-group').removeClass('has-error');
    let data = json_from_form(button);
    send_json_ajax(data, url, success_event, error_event);
}

function send_file_ajax(form_data, url = '', success_event, error_event, context = null) {
    $.ajax({
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        url: '',
        data: form_data,
        processData: false,
        contentType: false,
        context: context,
        type: 'POST',
        beforeSend: function(){
            $('.preloader').removeClass('hidden');
        },
        complete: function (){
            $('.preloader').addClass('hidden');
        },
        success: function (msg) {
            success_event(msg);
        },
        error: function (msg) {
            msg['context'] = context
            error_event(msg, context);
        }
    });
}

function console_log(msg) {
    console.log(msg);
}

function reload_window(event){
    window.location.reload();
}

function show_popup_form(selector, text, type = 'INFO', commit_func = null, param = null) {
    $(selector).find('.modal-header > .modal-title').html(type);
    $(selector).find('.modal-body > p').html(text);
    if (type === 'COMMIT') {
        let success_button = $(selector).find('.modal-footer > .btn-success');
        $(success_button).removeClass('hidden');
        if (commit_func != null) {
            $(success_button).off("click.success_event");
            $(success_button).bind("click.success_event", param, commit_func);
        }
    }
    $(selector).modal('show');
}

function commit_transaction(msg){
    $('#connect-row input').val('');
    show_popup_form('#modalWindow', msg.text_info);
}
