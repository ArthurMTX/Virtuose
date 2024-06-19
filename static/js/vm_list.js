$('.dropdown-item').click(function() {
    let action = $(this).text().trim().toUpperCase();
    let vm_uuid = $(this).closest('.vm').data('id');
    let vm_name = $(this).closest('.vm').find('.vm-name').text().trim();

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/domains/actions/' + vm_uuid + '/' + action, true);

    let responseBuffer = '';

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 3 || xhr.readyState === 4) {
            responseBuffer += xhr.responseText;
            let lines = responseBuffer.split('\n');
            responseBuffer = lines.pop();

            for (let line of lines) {
                if (line) {
                    try {
                        let response = JSON.parse(line);
                        showToast(response.status, vm_name);
                    } catch (e) {
                        console.error('Error parsing JSON response: ', e);
                    }
                }
            }

            if (xhr.readyState === 4 && responseBuffer) {
                try {
                    let response = JSON.parse(responseBuffer);
                    showToast(response.status, vm_name);
                } catch (e) {
                    console.error('Error parsing final JSON response: ', e);
                }
            }
        }
    };

    xhr.onerror = function() {
        console.error('Request failed.');
    };
    xhr.send();
});

function createToast(message) {
    let toast = document.createElement("div");
    toast.classList.add("toast");
    toast.setAttribute("role", "alert");
    toast.setAttribute("aria-live", "assertive");
    toast.setAttribute("aria-atomic", "true");

    let toastHeader = document.createElement("div");
    toastHeader.classList.add("toast-header");

    let strong = document.createElement("strong");
    strong.classList.add("me-auto");
    strong.textContent = "Notification";

    let button = document.createElement("button");
    button.type = "button";
    button.classList.add("btn-close");
    button.setAttribute("data-bs-dismiss", "toast");
    button.setAttribute("aria-label", "Close");

    toastHeader.appendChild(strong);
    toastHeader.appendChild(button);

    let toastBody = document.createElement("div");
    toastBody.classList.add("toast-body");
    toastBody.textContent = message;

    toast.appendChild(toastHeader);
    toast.appendChild(toastBody);

    return toast;
}

function showToast(message) {
    let toastContainer = document.querySelector(".toast-container");
    let toast = createToast(message);
    toastContainer.appendChild(toast);
    let bootstrapToast = new bootstrap.Toast(toast);
    bootstrapToast.show();
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
