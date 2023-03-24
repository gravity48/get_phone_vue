function commit_transaction(msg){
    $('#connect-row input').val('');
    show_popup_form('#modalWindow', msg.text_info);
}

function modal_hide(msg){
    $('#modalWindow').modal('hide');
}

function delete_user (event){
    let params = event.data;
    send_json_ajax(params, params['url'], modal_hide, console_log);
}
function event_list() {
    $(document).on('click', '#connect-bd', function (event) {
        event.stopPropagation();
        event.preventDefault();
        CURRENT_FORM = $(this).parents('form:first');
        $(CURRENT_FORM).find('input').removeClass('is-valid');
        $(CURRENT_FORM).find('input').removeClass('is-invalid');
        let [data, status] = json_from_form($(CURRENT_FORM));
        send_json_ajax(data, '', commit_transaction, show_exception_on_form, CURRENT_FORM);
    });
    $(document).on('click', '#user-add-button', function (event) {
        event.stopPropagation();
        event.preventDefault();
        CURRENT_FORM = $(this).parents('form:first');
        $(CURRENT_FORM).find('input').removeClass('is-valid');
        $(CURRENT_FORM).find('input').removeClass('is-invalid');
        let [data, status] = json_from_form($(CURRENT_FORM));
        send_json_ajax(data, '', commit_transaction, show_exception_on_form, CURRENT_FORM);
    });
    $(document).on('click', '#del-button', function (event){
       event.stopPropagation();
       event.preventDefault();
       console_log(this);
        let params = {
            'url': $(this).attr("data-url"),
            'event': $(this).attr("data-event"),
            'id': $(this).attr("data-id"),
        };
        show_popup_form('#modalWindow', `Удалить пользователя ${$(this).attr("data-alias")}?`, 'COMMIT', delete_user, params);
    });
    let myModal = document.getElementById('modalWindow');
    myModal.addEventListener('hide.bs.modal', function () {
        window.location.reload();
    });



}

$(document).ready(event_list);