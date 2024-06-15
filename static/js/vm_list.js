$('.dropdown-item').click(function() {
    let action = $(this).text().trim();
    let dataId = $(this).closest('.vm').data('id');

    $.ajax({
        url: '/action-vms/',
        type: 'POST',
        data: {
            'action': action,
            'data_id': dataId,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        }
    });
});

$(document).ready(function() {
    $('.modal-body pre').each(function() {
        let rawContent = $(this).text();
        let beautifiedContent = js_beautify(rawContent);
        let trimmedContent = beautifiedContent.replace(/^\s+/gm, '');
        $(this).text(trimmedContent);
    });
});