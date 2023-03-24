$(document).ready(function (){
    $('#doc-extensions').click(function (event){
        event.stopPropagation();
        $(this).siblings('.popup-div').stop().animate({'height': 'toggle'}, 200);
    });
    $('#doc-status').click(function (event){
        event.stopPropagation();
        $(this).siblings('.popup-div').stop().animate({'height': 'toggle'}, 200);
    });

    $('body').click(function (event){
        $.each($(this).find('.popup-div'), function (index, item) {
            if ($(item).css('display') != 'none'){
                $(item).stop().animate({'height': 'toggle'}, 200);
            }
        });

    });
    $('.popup-div').click(function (e){
        e.stopPropagation();
    });
});