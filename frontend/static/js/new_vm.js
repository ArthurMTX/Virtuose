document.querySelector('.form-create-vm form').addEventListener('submit', async function(event) {
    event.preventDefault();

    let form = event.target;
    let formData = new FormData(form);
    let vmName = formData.get('name');  // On récupère le nom de la VM à partir du formulaire

    // Affiche le loader avec le nom de la VM dans le texte
    toggleLoader(true, `Création de la machine virtuelle ${vmName}...`);

    try {
        let response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData,
        });

        let data = await response.json();
        toggleLoader(false);  // Cache le loader après la réponse

        if (data.status === 'success') {
            // Affiche une notification de succès avec le nom de la VM
            showToast(`La machine virtuelle ${vmName} a été créée avec succès.`, 'Succès', false);
        } else {
            if (data.errors) {
                let errorMessages = extractErrorMessages(data.errors);  // Utilise la fonction pour extraire les erreurs
                showToast(errorMessages, 'Erreur', true);  // Affiche les messages d'erreur
            } else {
                // Affiche un message d'erreur général
                showToast(data.message || `Une erreur est survenue lors de la création de la machine virtuelle ${vmName}.`, 'Erreur', true);
            }
        }
    } catch (error) {
        console.error('Erreur lors de la requête:', error);
        toggleLoader(false);  // Cache le loader en cas d'erreur
        // Affiche un message d'erreur générique en cas de problème inattendu
        showToast(`Une erreur inattendue est survenue lors de la création de la machine virtuelle ${vmName}.`, 'Erreur', true);
    }
});

/**
 * Extrait les messages d'erreurs d'un objet JSON retourné par le serveur
 * @param {Object} errors - L'objet contenant les erreurs (ex: {name: [{message: "erreur"}, ...]})
 * @returns {string} - Une chaîne avec tous les messages d'erreurs concaténés
 */
function extractErrorMessages(errors) {
    errors = JSON.parse(errors);
    let messages = [];

    // On boucle sur chaque clé de l'objet
    for (let key in errors) {
        // On boucle sur chaque objet de la liste de messages d'erreur
        for (let error of errors[key]) {
            messages.push(error.message);  // On ajoute le message à la liste
        }
    }

    return messages.join('<br>');
}

/**
 * Affiche ou cache le loader avec un texte personnalisé.
 * @param {boolean} visible - Si vrai, affiche le loader. Sinon, le masque.
 * @param {string} [text] - Texte à afficher dans le loader.
 */
function toggleLoader(visible, text = '') {
    const loaderText = document.getElementById('loader-text');
    if (visible) {
        if (text) {
            loaderText.textContent = text;  // Met à jour le texte du loader
        }
        $('#loader').show();
        $('#overlay').show();
    } else {
        $('#loader').hide();
        $('#overlay').hide();
    }
}

/**
 * Affiche une notification toast en bas de l'écran avec horodatage.
 * @param {string} message - Le message à afficher dans le toast.
 * @param {string} action - L'action ou le type de notification (ex: 'Succès', 'Erreur').
 * @param {boolean} isError - Si vrai, stylise le toast comme une erreur.
 */
function showToast(message, action, isError) {
    const toastContainer = document.getElementById('toastContainer');

    // Création d'un nouvel élément toast
    const newToast = document.createElement('div');
    newToast.classList.add('toast');
    newToast.setAttribute('role', 'alert');
    newToast.setAttribute('aria-live', 'assertive');
    newToast.setAttribute('aria-atomic', 'true');

    // Si c'est une erreur, ajoute une classe pour styliser en rouge
    if (isError) {
        newToast.classList.add('toast-error');
    }

    // Génération de l'heure actuelle pour l'horodatage
    const now = new Date();
    const timestamp = now.toLocaleTimeString(); // Format de l'heure locale (HH:MM:SS)

    // Structure HTML du toast avec le message, l'action et le timestamp
    newToast.innerHTML = `
        <div class="toast-header ${isError ? 'toast-error' : ''}">
            <strong class="me-auto">${action || 'Notification'}</strong>
            <small>${timestamp}</small>
            <button type="button" class="btn-close ${isError ? 'btn-close-white' : ''}" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;

    // Ajout du toast au conteneur
    toastContainer.appendChild(newToast);

    // Affichage du toast
    const toastInstance = new bootstrap.Toast(newToast);
    toastInstance.show();

    // Suppression du toast une fois qu'il est caché
    newToast.addEventListener('hidden.bs.toast', function () {
        newToast.remove();
    });
}