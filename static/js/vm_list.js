/**
 * Sert à afficher les informations des VMs dans la page web
 * et à permettre de les démarrer, arrêter, suspendre, etc.
 */


// Gestion des actions sur les VMs
$('.dropdown-item').click(function() {
    let action = $(this).text().trim().toLowerCase();
    let vm_uuid = $(this).closest('.vm').data('id');
    let vm_name = $(this).closest('.vm').find('.vm-name').text().trim();
    let csrftoken = document.querySelector('#csrf-token-form [name=csrfmiddlewaretoken]').value;

    // Envoi de la requête POST pour effectuer l'action
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/domains/actions/' + vm_uuid + '/' + action, true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);

    let responseBuffer = '';

    // Gestion des réponses de la requête, pour afficher des notifications
    xhr.onreadystatechange = function() {
        // Si la requête est terminée
        if (xhr.readyState === 3 || xhr.readyState === 4) {
            responseBuffer += xhr.responseText;
            let lines = responseBuffer.split('\n');
            responseBuffer = lines.pop();

            // Pour chaque ligne de la réponse, on affiche une notification
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

            // Si la requête est terminée et qu'il reste des données à traiter
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

    // Gestion des erreurs de la requête
    xhr.onerror = function() {
        console.error('Request failed.');
    };
    xhr.send();
});

// Affiche une notification en bas de l'écran
function showToast(message, vmName) {
    let toastContainer = document.querySelector('.toast-container');
    let existingToasts = toastContainer.querySelectorAll('.toast');

    // On vérifie si une notification identique n'est pas déjà affichée
    for (let toast of existingToasts) {
        if (toast.querySelector('.toast-body').textContent === message) {
            return;
        }
    }

    let toastTemplate = document.querySelector('.toast');
    let newToast = toastTemplate.cloneNode(true);

    // On remplit la notification avec le message et le nom de la VM
    newToast.querySelector('.toast-header strong').textContent = vmName || 'Notification';
    newToast.querySelector('.toast-body').textContent = message;
    newToast.classList.add('hide');
    toastContainer.appendChild(newToast);

    // On affiche la notification
    let toastInstance = new bootstrap.Toast(newToast);
    toastInstance.show();

    // On supprime la notification une fois qu'elle est cachée
    newToast.addEventListener('hidden.bs.toast', function () {
        newToast.remove();
    });
}

$(document).ready(function() {
    // Reformatage du contenu des balises <pre> dans les modales pour les rendre plus lisibles
    $('.modal-body pre').each(function() {
        let rawContent = $(this).text();
        let beautifiedContent = js_beautify(rawContent);
        let trimmedContent = beautifiedContent.replace(/^\s+/gm, '');
        $(this).text(trimmedContent);
    });

    // Rafraîchissement des données des VMs toutes les 2 secondes pour afficher les changements en temps réel
    function refreshData() {
        // Récupère tous les noms de VMs
        fetch('/api/domains/')
            .then(response => response.json())
            .then(data => {
                data.forEach(vm_name => {
                    // Pour chaque VM, on récupère ses informations et on les affiche
                    fetch('/api/domains/' + vm_name)
                        .then(response => response.json())
                        .then(vm_data => {
                            let vmElement = document.querySelector(`tr[data-id='${vm_data.UUID}']`);
                            vmElement.querySelector('.vm-state').innerHTML = getVmStateIcon(vm_data.state);
                            vmElement.querySelector('.os-info p').textContent = vm_data.os;
                            vmElement.querySelector('td:nth-child(4)').textContent = vm_data.memory_gb;
                            vmElement.querySelector('td:nth-child(5)').textContent = vm_data.VCPU;

                            // Activation ou désactivation des actions en fonction de l'état de la VM
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

    // Rafraîchissement des données toutes les 2 secondes
    setInterval(refreshData, 2000);

    // Fonction pour obtenir l'icône correspondant à l'état de la VM
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
