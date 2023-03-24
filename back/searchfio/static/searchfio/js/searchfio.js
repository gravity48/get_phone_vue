function show_prs_data(msg){
    $('#block-result-view .body-panel tbody').html(msg.prs_data_view);
    $('#pagination-block').html(msg.page_nav);
    $('#save-result-block').removeClass('hidden');
}

function event_list(){
    $(document).on('click', '#search-fio button', function (event) {
        event.stopPropagation();
        event.preventDefault();
        let [data, status] = json_from_form('#search-fio');
        if (status){
            send_json_ajax(data, '', show_prs_data, console_log);
        }
    });
    $(document).on('keyup', '#search-fio input', function (event) {
        if (event.key != "Enter"){
            return;
        }
        $('#search-fio button').click();
    });
}

$(document).ready(event_list);