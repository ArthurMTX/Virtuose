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
            url: '/api/domains/UUID/' + vm_uuid,
            type: 'GET',
            success: function(response) {
                let vmStateElement = document.querySelector(`tr[data-id='${vm_uuid}'] .vm-state`);
                switch (response.state) {
                    case 'running':
                        vmStateElement.innerHTML = '<i class="fa-solid fa-check" style="color: #74c93b;"></i>';
                        break;
                    case 'shutoff':
                        vmStateElement.innerHTML = '<i class="fa-solid fa-stop" style="color: #d30d0d;"></i>'
                        break;
                    case 'paused':
                        vmStateElement.innerHTML = '<i class="fa-solid fa-pause" style="color: #ffbb00;"></i>';
                        break;
                    case 'crashed':
                        vmStateElement.innerHTML = '<i class="fa-solid fa-burst" style="color: #cd13b4;"></i>';
                        break;
                    case 'suspended':
                        vmStateElement.innerHTML = '<i class="fa-solid fa-stop" style="color: #d30d0d;"></i>';
                        break;
                    case 'starting':
                        vmStateElement.innerHTML = '<i class="fa-solid fa-hourglass-half" style="color: #fbff00;"></i>';
                        break;
                    default:
                        vmStateElement.innerHTML = '<i class="fa-solid fa-question" style="color: #185ed8;"></i>';
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    setInterval(function() {
        console.log('Refreshing VM states...');
        let vmUuids = Array.from(document.querySelectorAll('.vm')).map(function(vm) {
            return vm.dataset.id;
        });
        vmUuids.forEach(function(vm_uuid) {
            refreshVmState(vm_uuid);
        });
    }, 2000);
});