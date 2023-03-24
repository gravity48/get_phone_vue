var errorMessage = 'Что-то пошло не так...';

$(document).ready(function () {
    $('#dialog-btn').mousedown(function () {
        $(this).addClass('pressed');
    }).mouseup(function () {
        $(this).removeClass('pressed');
    }).click(function () {
        var popup = $('#' + $(this).data('popup-id'));
        if (!popup)
            return;

        popup.removeClass('hidden');
        loadFirstContent(popup.find('.folder-tree--panel'));
    });
    $('.popup-overlay').click(function () {
        $(this).addClass('hidden');
    });
    $('.popup-content').click(function (e) {
        e.stopPropagation();
    });
    $('.popup-content .close-button').click(function () {
        $(this).parents('.popup-overlay').click();
    });
});

function loadFirstContent(treePanelElement) {
    if (treePanelElement.data('loaded')) {
        if (!treePanelElement.hasClass('selected')) {
            treePanelElement.parent().find('.selected').removeClass('selected');
            treePanelElement.addClass('selected');
        }
        return;
    }

    var loader = treePanelElement.siblings('.loader');
    $.ajax({
        url: '/loadFileSystemData.php',
        type: 'post',
        dataType: 'json',
        data: {
            isFirst: true
        },
        complete: function () {
            loader.addClass('hidden');
        },
        success: function (arr) {
            if (arr.success == '0') {
                console.log(arr.error);
                alert(errorMessage);
            } else {
                treePanelElement.empty();
                treePanelElement.append(arr.drives);
                treePanelElement.data('loaded', true);
                if (!treePanelElement.hasClass('selected')) {
                    treePanelElement.parent().find('.selected').removeClass('selected');
                    treePanelElement.addClass('selected');
                }
                treePanelElement.find('li').click(function (e) {
                    e.stopPropagation();
                    loadSubFolders($(this));
                });
            }
        },
        error: function (xhr) {
            console.log(xhr);
            alert(errorMessage);
        }
    });
}

function loadSubFolders(parentElement) {
    if (parentElement.hasClass('loading'))
        return;

    if (parentElement.data('loaded')) {
        parentElement.toggleClass('expanded');
        if (!parentElement.hasClass('expanded'))
            parentElement.find('li.expanded').removeClass('expanded');
        if (!parentElement.hasClass('selected')){
            parentElement.parents('.folder-tree--panel').find('.selected').removeClass('selected');
            parentElement.addClass('selected');
        }
        return;
    }

    $.ajax({
        url: '/loadFileSystemData.php',
        type: 'post',
        dataType: 'json',
        data: {
            isFirst: false,
            parentPath: parentElement.data('path')
        },
        beforeSend: function () {
            parentElement.addClass('loading');
        },
        complete: function () {
            parentElement.removeClass('loading');
        },
        success: function (arr) {
            if (arr.success == '0') {
                console.log(arr.error);
                alert(errorMessage);
            } else {
                parentElement.toggleClass('expanded');
                parentElement.data('loaded', true);
                if (arr.folders.length > 0) {
                    parentElement.append(arr.folders);
                    parentElement.find('li').click(function (e) {
                        e.stopPropagation();
                        loadSubFolders($(this));
                    });
                } else parentElement.addClass('empty');
                if (!parentElement.hasClass('selected')){
                    parentElement.parents('.folder-tree--panel').find('.selected').removeClass('selected');
                    parentElement.addClass('selected');
                }
            }
        },
        error: function (xhr) {
            console.log(xhr);
            alert(errorMessage);
        }
    });
}