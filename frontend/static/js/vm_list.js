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
    $('.modal-body pre').each(function() {
        const beautifiedContent = js_beautify($(this).text()).replace(/^\s+/gm, '');
        $(this).text(beautifiedContent);
    });

    // Fonctionnalité pour rafraîchir les données des VMs toutes les 2 secondes
    /*
    setInterval(refreshData, 2000);

    function refreshData() {
        fetch('/domains_list')
            .then(response => response.json())
            .then(data => {
                data.forEach(vmName => {
                    fetch(`/domain_by_name/${vmName}`)
                        .then(response => response.json())
                        .then(vmData => updateVMInfo(vmData))
                        .catch(error => console.error('Erreur:', error));
                });
            })
            .catch(error => console.error('Erreur:', error));
    }
    */

    // Mise à jour des icônes des VMs selon leur état
    function getVmStateIcon(state) {
        const stateIcons = {
            running: '<i class="fa-solid fa-check" style="color: #74c93b;"></i>',
            shutoff: '<i class="fa-solid fa-stop" style="color: #d30d0d;"></i>',
            shutdown: '<i class="fa-solid fa-stop" style="color: #d30d0d;"></i>',
            pmsuspended: '<i class="fa-solid fa-stop" style="color: #d30d0d;"></i>',
            paused: '<i class="fa-solid fa-pause" style="color: #ffbb00;"></i>',
            crashed: '<i class="fa-solid fa-burst" style="color: #cd13b4;"></i>',
            blocked: '<i class="fa-solid fa-burst" style="color: #cd13b4;"></i>',
            starting: '<i class="fa-solid fa-hourglass-half" style="color: #fbff00;"></i>',
            default: '<i class="fa-solid fa-question" style="color: #185ed8;"></i>'
        };

        return stateIcons[state] || stateIcons.default;
    }
});