// Capture la soumission du formulaire
document.querySelector('.form-create-vm form').addEventListener('submit', function(event) {
    event.preventDefault();

    let form = event.target;
    let formData = new FormData(form);
    
    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Affiche une notification de succès
            showToast(data.message, data.action, false);
        } else {
            // Affiche le message d'erreur spécifique renvoyé par le serveur
            showToast(data.message || 'An error occurred.', 'Error', true);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Affiche le message d'erreur généré par le fetch en cas de problème inattendu
        showToast(error.message || 'An unexpected error occurred.', 'Error', true);
    });
});


// Fonction pour ajouter des toasts avec horodatage et stacking
function showToast(message, action, isError) {
    let toastContainer = document.getElementById('toastContainer');

    // Création d'un nouvel élément toast
    let newToast = document.createElement('div');
    newToast.classList.add('toast');
    newToast.setAttribute('role', 'alert');
    newToast.setAttribute('aria-live', 'assertive');
    newToast.setAttribute('aria-atomic', 'true');

    // Si c'est une erreur, ajoute une classe pour styliser en rouge
    if (isError) {
        newToast.classList.add('toast-error');
    }

    // Génération de l'heure actuelle pour l'horodatage
    let now = new Date();
    let timestamp = now.toLocaleTimeString(); // Format de l'heure locale (HH:MM:SS)

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
    let toastInstance = new bootstrap.Toast(newToast);
    toastInstance.show();

    // Suppression du toast une fois caché
    newToast.addEventListener('hidden.bs.toast', function () {
        newToast.remove();
    });
}