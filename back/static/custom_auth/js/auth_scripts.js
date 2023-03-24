
function redirect_to_page(msg){
    document.location.href = msg.next_page;
}

function event_list() {
    $(document).on('click', '#form-login button', function (event) {
        event.stopPropagation();
        event.preventDefault();
        let form_selector = $(this).parents('form:first');
        clear_form(form_selector);
        let [data, status] = json_from_form($(form_selector));
        if (status) {
            send_json_ajax(data, '', redirect_to_page, show_exception_on_form, form_selector);
        }
    });
    let myModal = document.getElementById('modalWindow');
    myModal.addEventListener('hide.bs.modal', function () {
        window.location.reload();
    });

}

$(document).ready(event_list);