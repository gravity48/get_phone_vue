function show_numbers(msg){
    let new_msg = JSON.parse(msg);
    $('#block-result-view .body-panel tbody').html(new_msg.phone_render);
    $('#pagination-block').html(new_msg.page_nav);
    $('#save-result-block').removeClass('hidden');
}

function event_list(){
    $(document).on('click', '#download-button', function (event) {
        $('#download-hidden').click();
    });
    $(document).on('click', '#search-button', function (event){
        CURRENT_FORM = $('#search-form');
        let [data, status] = json_from_form('#search-form');
        send_ajax(data, '', show_numbers, show_exception_on_form, CURRENT_FORM);
    });
    $(document).on('change', '#download-hidden', function (event) {
        CURRENT_FORM = $('#search-form');
        event.preventDefault();
        event.stopPropagation();
        FILES_COUNT = this.files.length;
        FILES_SENT = 0;
        $.each(this.files, function (index, file) {
            if (file.size > DEFAULT_SIZE_FILE) {
                const text = file.name + ' большой размер файла';
                show_popup_form('.modal.fade', text);
                return false;
            } else {
                let data = new FormData();
                data.set('file', file, file.name);
                data.set('event', 'download_file');
                send_file_ajax(data, '', show_numbers, show_exception_on_form, CURRENT_FORM);
            }
        });
    });
    $(document).on('click', '#save-result-block button', function (e) {
        e.stopPropagation();
        e.preventDefault();
        window.open($(this).data('download'), '_blank');
    });
}

$(document).ready(event_list);

