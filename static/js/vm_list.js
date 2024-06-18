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

    function refreshVmState(vm_uuid) {
        $.ajax({
            url: '/api/vm_state/' + vm_uuid,
            type: 'GET',
            success: function(response) {
                let vmStateElement = document.querySelector('.vm-state-' + vm_uuid);
                vmStateElement.textContent = response.state;
                console.log('VM ' + vm_uuid + ' state refreshed');
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    setInterval(function() {
        print('Refreshing VM states...');
        let vmUuids = Array.from(document.querySelectorAll('.vm')).map(function(vm) {
            return vm.dataset.id;
        });
        vmUuids.forEach(function(vm_uuid) {
            refreshVmState(vm_uuid);
        });
    }, 5000);
});