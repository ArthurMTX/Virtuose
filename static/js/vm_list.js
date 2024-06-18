$('.dropdown-item').click(function() {
    let action = $(this).text().trim().toUpperCase();
    let vm_uuid = $(this).closest('.vm').data('id');

    $.ajax({
        url: '/api/domains/actions/' + vm_uuid + '/' + action,
        method: 'POST',
        success: function(response) {
            let message = JSON.parse(response.responseText).status;
            showToast(message);
            console.log(response);
        },
        error: function(response) {
            showToast(response.responseText);
            console.log(response);
        }
    });
});

function showToast(message) {
    let toastElement = document.querySelector('.toast');
    let toastInstance = new bootstrap.Toast(toastElement);
    toastElement.querySelector('.toast-body').textContent = message;
    toastInstance.show();
}

$(document).ready(function() {
    $('.modal-body pre').each(function() {
        let rawContent = $(this).text();
        let beautifiedContent = js_beautify(rawContent);
        let trimmedContent = beautifiedContent.replace(/^\s+/gm, '');
        $(this).text(trimmedContent);
    });

    function refreshData() {
        fetch('/api/domains/')
            .then(response => response.json())
            .then(data => {
                data.forEach(vm_name => {
                    fetch('/api/domains/' + vm_name)
                        .then(response => response.json())
                        .then(vm_data => {
                            let vmElement = document.querySelector(`tr[data-id='${vm_data.UUID}']`);
                            vmElement.querySelector('.vm-state').innerHTML = getVmStateIcon(vm_data.state);
                            vmElement.querySelector('.os-info p').textContent = vm_data.os;
                            vmElement.querySelector('td:nth-child(4)').textContent = vm_data.memory_gb;
                            vmElement.querySelector('td:nth-child(5)').textContent = vm_data.VCPU;

                            let dropdownItems = vmElement.querySelectorAll('.dropdown-item');
                            dropdownItems.forEach(item => {
                                let action = item.textContent.trim();
                                if ((action === 'Start' && vm_data.state === 'running') || (action === 'Stop' && vm_data.state !== 'running')) {
                                    item.classList.add('dropdown-item-disabled');
                                } else {
                                    item.classList.remove('dropdown-item-disabled');
                                }
                            });
                        })
                        .catch(error => console.error('Error:', error));
                });
            })
            .catch(error => console.error('Error:', error));
    }

    setInterval(refreshData, 2000);

    function getVmStateIcon(state) {
        switch (state) {
            case 'running':
                return '<i class="fa-solid fa-check" style="color: #74c93b;"></i>';
            case 'shutoff':
            case 'shutdown':
            case 'pmsuspended':
                return '<i class="fa-solid fa-stop" style="color: #d30d0d;"></i>';
            case 'paused':
                return '<i class="fa-solid fa-pause" style="color: #ffbb00;"></i>';
            case 'crashed':
            case 'blocked':
                return '<i class="fa-solid fa-burst" style="color: #cd13b4;"></i>';
            case 'starting':
                return '<i class="fa-solid fa-hourglass-half" style="color: #fbff00;"></i>';
            default:
                return '<i class="fa-solid fa-question" style="color: #185ed8;"></i>';
        }
    }
});