/**
 * Utilitaire : Récupère le token CSRF pour les requêtes POST
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const cookiePair = cookie.trim();
            if (cookiePair.startsWith(`${name}=`)) {
                cookieValue = decodeURIComponent(cookiePair.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}

/**
 * Utilitaire : Récupère l'icône correspondant à l'état de la VM
 */
function getVmStateIcon(state) {
    const stateIcons = {
        running: '<i class="fa-solid fa-check" style="color: #74c93b;"></i>',
        starting: '<i class="fa-solid fa-hourglass-half" style="color: #fbff00;"></i>',
        paused: '<i class="fa-solid fa-pause" style="color: #ffbb00;"></i>',
        shutdown: '<i class="fa-solid fa-stop" style="color: #d30d0d;"></i>',
        shutoff: '<i class="fa-solid fa-stop" style="color: #d30d0d;"></i>',
        pmsuspended: '<i class="fa-solid fa-stop" style="color: #d30d0d;"></i>',
        crashed: '<i class="fa-solid fa-burst" style="color: #cd13b4;"></i>',
        blocked: '<i class="fa-solid fa-burst" style="color: #cd13b4;"></i>',
        unknown: '<i class="fa-solid fa-question" style="color: #185ed8;"></i>',
        default: '<i class="fa-solid fa-question" style="color: #185ed8;"></i>'
    };
    return stateIcons[state] || stateIcons['default'];
}

/**
 * Modifie le texte du loader en fonction de l'action et de la VM
 */
function updateLoaderText(action, vmName) {
    const actionTextMap = {
        start: 'Démarrage du',
        stop: 'Arrêt du',
        force_stop: 'Arrêt forcé du',
        kill: 'Arrêt forcé du',
        restart: 'Redémarrage du',
        delete: 'Suppression du',
        default: 'Action sur le'
    };
    const actionText = actionTextMap[action] || actionTextMap.default;
    $('#loader-text').text(`${actionText} domaine ${vmName}...`);
}

/**
 * Gestion de l'affichage du loader
 */
function toggleLoader(visible) {
    if (visible) {
        $('#loader, #overlay').show();
    } else {
        $('#loader, #overlay').hide();
    }
}

/**
 * Affiche une notification Toast en bas de l'écran
 */
function showToast(message, vmName = 'Notification') {
    const toastContainer = document.querySelector('.toast-container');
    const existingToasts = toastContainer.querySelectorAll('.toast');

    if ([...existingToasts].some(toast => toast.querySelector('.toast-body').textContent === message)) {
        return; // Ne pas afficher de notifications en double
    }

    const toastTemplate = document.querySelector('.toast');
    const newToast = toastTemplate.cloneNode(true);
    newToast.querySelector('.toast-header strong').textContent = vmName;
    newToast.querySelector('.toast-body').textContent = message;
    newToast.classList.add('hide');
    toastContainer.appendChild(newToast);

    const toastInstance = new bootstrap.Toast(newToast);
    toastInstance.show();

    newToast.addEventListener('hidden.bs.toast', () => newToast.remove());
}

/**
 * Met à jour les actions possibles d'une VM en fonction de son état
 */
function updateVmActions(vmRow, state) {
    const actions = vmRow.querySelectorAll('.dropdown-item');
    actions.forEach(action => {
        const actionText = action.textContent.trim().toLowerCase();

        if (state === 'running') {
            // Si la VM est en cours d'exécution, "Start" doit être désactivé
            if (actionText === 'start') {
                action.classList.add('dropdown-item-disabled');
            } else if (['stop', 'kill', 'restart'].includes(actionText)) {
                action.classList.remove('dropdown-item-disabled');
            }
        } else if (['shutoff', 'shutdown'].includes(state)) {
            // Si la VM est arrêtée, seules "Start" doit être activée, "Stop", "Restart", "Kill" doivent être désactivées
            if (actionText === 'start') {
                action.classList.remove('dropdown-item-disabled');
            } else if (['stop', 'restart', 'kill'].includes(actionText)) {
                action.classList.add('dropdown-item-disabled');
            }
            // Permettre toujours l'accès à "Info" et "Delete"
            if (['info', 'delete'].includes(actionText)) {
                action.classList.remove('dropdown-item-disabled');
            }
        } else {
            // Pour les autres états, toutes les actions sont activées par défaut sauf "Start"
            if (actionText === 'start') {
                action.classList.add('dropdown-item-disabled');
            } else {
                action.classList.remove('dropdown-item-disabled');
            }
        }
    });
}

/**
 * Met à jour l'icône et les actions de la VM
 */
function updateVmStateAndActions(vmRow, state) {
    const stateIcon = getVmStateIcon(state);
    vmRow.querySelector('.vm-state').innerHTML = stateIcon;
    updateVmActions(vmRow, state);
}

/**
 * Gère les actions sur une VM avec requêtes AJAX
 */
function handleVmAction(event) {
    const action = event.target.textContent.trim().toLowerCase();
    const vmName = $(this).closest('.vm').find('.vm-name').text().trim();
    const csrfToken = getCookie('csrftoken');

    if (action === 'info') return;

    updateLoaderText(action, vmName);
    toggleLoader(true);

    const finalAction = action === 'kill' ? 'force_stop' : action;

    fetch(`/domains/${finalAction}/${vmName}/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken
        }
    }).then(response => response.text())
    .then(text => {
        const lines = text.split('\n');
        lines.forEach(line => {
            if (line) {
                const response = JSON.parse(line.trim());
                showToast(response.message, response.status.charAt(0).toUpperCase() + response.status.slice(1));
            }
        });
        toggleLoader(false);
    })
    .catch(() => {
        toggleLoader(false);
        console.error('Erreur lors de la requête.');
    });
}

/**
 * Rafraîchit les informations d'une VM spécifique et met à jour son état
 */
function refreshVmDetails(vmName, vmTableBody) {
    fetch(`/domain_informations/${vmName}/`)
        .then(response => response.json())
        .then(vmInfo => {
            let vmRow = vmTableBody.querySelector(`tr[data-id="${vmInfo.name}"]`);

            if (vmRow) {
                updateVmStateAndActions(vmRow, vmInfo.state.toLowerCase());
                vmRow.querySelector('.vm-name').textContent = vmInfo.name;
                vmRow.querySelector('td:nth-child(4)').textContent = vmInfo.memory;
                vmRow.querySelector('td:nth-child(5)').textContent = vmInfo.vcpus;
            } else {
                // Créer une nouvelle ligne si la VM n'existe pas
                const vmRowHtml = `
                    <tr data-id="${vmInfo.name}">
                        <td>
                            <div class="os-info">
                                <div class="dropdown">
                                    <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                        <i class="fa-solid fa-gears"></i>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><h6 class="dropdown-header">${vmInfo.name}</h6></li>
                                        <li><a class="dropdown-item"><i class="icon-action fa-solid fa-circle-info"></i> Info</a></li>
                                        <li><hr class="dropdown-divider"></li>
                                        <li><a class="dropdown-item"><i class="icon-action fa-solid fa-play"></i> Start</a></li>
                                        <li><a class="dropdown-item"><i class="icon-action fa-solid fa-stop"></i> Stop</a></li>
                                        <li><a class="dropdown-item"><i class="icon-action fa-solid fa-skull"></i> Kill</a></li>
                                        <li><a class="dropdown-item"><i class="icon-action fa-solid fa-rotate"></i> Restart</a></li>
                                        <li><a class="dropdown-item"><i class="icon-action fa-solid fa-trash"></i> Delete</a></li>
                                    </ul>
                                </div>
                                <div class="vm-state">${getVmStateIcon(vmInfo.state)}</div>
                            </div>
                        </td>
                        <td>${vmInfo.os}</td>
                        <td class="vm-name">${vmInfo.name}</td>
                        <td>${vmInfo.memory}</td>
                        <td>${vmInfo.vcpus}</td>
                    </tr>
                `;
                vmTableBody.insertAdjacentHTML('beforeend', vmRowHtml);
            }
        })
        .catch(error => console.error(`Erreur lors du lookup pour ${vmName}:`, error));
}

/**
 * Rafraîchit la liste des VMs
 */
function refreshVmList() {
    const vmTableBody = document.querySelector('#vmTable tbody');
    
    fetch('/domains_list') 
        .then(response => response.json())
        .then(vmNames => {
            vmNames.forEach(vmName => {
                // Rafraîchir les détails pour chaque VM
                refreshVmDetails(vmName, vmTableBody); 
            });
        })
        .catch(error => console.error('Erreur lors du rafraîchissement des VMs:', error));
}

/**
 * Initialisation au chargement du DOM
 */
$(document).ready(function() {
    $('.modal-body pre').each(function() {
        let rawContent = $(this).text();
        let beautifiedContent = js_beautify(rawContent);
        let trimmedContent = beautifiedContent.replace(/^\s+/gm, '');
        $(this).text(trimmedContent);
    });

    // Rafraîchit la liste toutes les 2 secondes
    setInterval(refreshVmList, 2000);
    
    // Gestion des actions des VMs
    $('.dropdown-item').on('click', handleVmAction); 
});
