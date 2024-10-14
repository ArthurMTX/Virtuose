from django import forms
from django.contrib.auth.forms import AuthenticationForm


class EmailAuthenticationForm(AuthenticationForm):
    """Formulaire d'authentification utilisant l'email au lieu du nom d'utilisateur."""
    username = forms.EmailField(label='Email', max_length=254)
