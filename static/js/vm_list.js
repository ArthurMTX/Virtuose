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
    $('.dropdown-toggle').each(function() {
        let vmState = $(this).data('state');
        if (vmState === 'running') {
            $(this).siblings('.dropdown-menu').find('[data-action="start"]').addClass('dropdown-item-disabled');
        }
        if (vmState === 'stopped') {
            $(this).siblings('.dropdown-menu').find('[data-action="stop"]').addClass('dropdown-item-disabled');
        }
    });
});