/**
 * Récupère le token CSRF pour les requêtes POST
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(`${name}=`)) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}

/**
 * Map des actions pour un affichage lisible du texte
 */
const actionTextMap = {
    start: 'Démarrage du',
    stop: 'Arrêt du',
    force_stop: 'Arrêt forcé du',
    kill: 'Arrêt forcé du',
    restart: 'Redémarrage du',
    delete: 'Suppression du',
    default: 'Action sur le'
};

/**
 * Modifie le texte du loader en fonction de l'action et de la VM
 */
function updateLoaderText(action, vmName) {
    const actionText = actionTextMap[action] || actionTextMap.default;
    $('#loader-text').text(`${actionText} domaine ${vmName}...`);
}

/**
 * Affiche et masque le loader et l'overlay
 */
function toggleLoader(visible) {
    if (visible) {
        $('#loader').show();
        $('#overlay').show();
    } else {
        $('#loader').hide();
        $('#overlay').hide();
    }
}

/**
 * Affiche une notification Toast en bas de l'écran
 */
function showToast(message, vmName = 'Notification') {
    const toastContainer = document.querySelector('.toast-container');
    const existingToasts = toastContainer.querySelectorAll('.toast');

    // Vérifie si une notification identique n'est pas déjà affichée
    if ([...existingToasts].some(toast => toast.querySelector('.toast-body').textContent === message)) {
        return;
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
 * Gère les actions des VMs avec requêtes AJAX
 */
$('.dropdown-item').click(function() {
    const action = $(this).text().trim().toLowerCase();
    const vmName = $(this).closest('.vm').find('.vm-name').text().trim();
    const csrfToken = getCookie('csrftoken');

    // Met à jour le texte du loader
    updateLoaderText(action, vmName);

    // Affiche le loader et l'overlay
    toggleLoader(true);

    const finalAction = action === 'kill' ? 'force_stop' : action;

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/domains/${finalAction}/${vmName}/`, true);
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    let responseBuffer = '';

    xhr.onreadystatechange = function() {
        if (xhr.readyState >= 3) {
            responseBuffer = xhr.responseText;

            const lines = responseBuffer.split('\n');
            responseBuffer = lines.pop();

            lines.forEach(line => {
                if (line) {
                    try {
                        const response = JSON.parse(line.trim());
                        showToast(response.message, response.status.charAt(0).toUpperCase() + response.status.slice(1));
                    } catch (e) {
                        console.error('Erreur lors du parsing de la réponse JSON :', e);
                    }
                }
            });

            if (xhr.readyState === 4) {
                try {
                    const finalResponse = JSON.parse(responseBuffer.trim());
                    showToast(finalResponse.message, finalResponse.status.charAt(0).toUpperCase() + finalResponse.status.slice(1));
                } catch (e) {
                    console.error('Erreur lors du parsing final de la réponse JSON :', e);
                }
                toggleLoader(false);  // Cacher le loader après la fin de la requête
            }
        }
    };

    xhr.onerror = function() {
        console.error('Échec de la requête.');
        toggleLoader(false);  // Cacher le loader en cas d'erreur
    };

    xhr.send();
});

/**
 * Reformatage du contenu des balises <pre> dans les modales pour les rendre plus lisibles
 */
$(document).ready(function() {
    // Rafraîchissement de la liste des VMs toutes les 2 secondes
    setInterval(refreshVmList, 2000);

    // Variable pour stocker la dernière liste de VMs
    let currentVmNames = [];

    function refreshVmList() {
        fetch('/domains_list')  // Appel à l'API pour récupérer la liste des VMs
            .then(response => response.json())
            .then(data => {
                const vmTableBody = $('tbody'); // Sélectionne le tbody de ton tableau des VMs
                const newVmNames = data;  // La nouvelle liste de noms de VMs

                // Mise à jour des lignes existantes
                newVmNames.forEach(vmName => {
                    const existingRow = vmTableBody.find(`tr[data-id="${vmName}"]`);
                    if (existingRow.length) {
                        // La ligne existe déjà, on peut mettre à jour son contenu texte si nécessaire
                        existingRow.find('.vm-name').text(vmName);
                        // Tu peux aussi mettre à jour d'autres colonnes ici si besoin
                    } else {
                        // Si la ligne n'existe pas, on la crée
                        const vmRow = `
                            <tr data-id="${vmName}">
                                <td>
                                    <div class="os-info">
                                        <div class="dropdown">
                                            <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                <i class="fa-solid fa-gears"></i>
                                            </button>
                                            <ul class="dropdown-menu">
                                                <li><h6 class="dropdown-header">${vmName}</h6></li>
                                                <li><a class="dropdown-item" data-bs-toggle="modal" data-bs-target="#vmInfoModal${vmName}">
                                                    <i class="icon-action fa-solid fa-circle-info"></i> Info
                                                </a></li>
                                                <li><hr class="dropdown-divider"></li>
                                                <li><a class="dropdown-item">
                                                    <i class="icon-action fa-solid fa-play"></i> Start
                                                </a></li>
                                                <li><a class="dropdown-item">
                                                    <i class="icon-action fa-solid fa-stop"></i> Stop
                                                </a></li>
                                                <li><a class="dropdown-item">
                                                    <i class="icon-action fa-solid fa-skull"></i> Kill
                                                </a></li>
                                                <li><a class="dropdown-item">
                                                    <i class="icon-action fa-solid fa-rotate"></i> Restart
                                                </a></li>
                                                <li><a class="dropdown-item">
                                                    <i class="icon-action fa-solid fa-trash"></i> Delete
                                                </a></li>
                                            </ul>
                                        </div>
                                        <div class="vm-state">
                                            <i class="fa-solid fa-question" style="color: #185ed8;"></i> <!-- Placeholder pour l'icône d'état -->
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <div class="os-info">
                                        <img src="/static/assets/os/default.png" alt="OS logo" width="50" height="50">
                                        <p>OS</p>
                                    </div>
                                </td>
                                <td class="vm-name">${vmName}</td>
                                <td>RAM</td>
                                <td>VCPU</td>
                            </tr>
                        `;
                        vmTableBody.append(vmRow);  // Ajout de la nouvelle ligne
                    }
                });

                // Suppression des lignes qui ne sont plus dans la nouvelle liste de VMs
                currentVmNames.forEach(vmName => {
                    if (!newVmNames.includes(vmName)) {
                        vmTableBody.find(`tr[data-id="${vmName}"]`).remove();  // Supprime la ligne si le VM a disparu
                    }
                });

                // Mise à jour de la liste courante
                currentVmNames = [...newVmNames];
            })
            .catch(error => console.error('Erreur lors du rafraîchissement des VMs:', error));
    }
});
