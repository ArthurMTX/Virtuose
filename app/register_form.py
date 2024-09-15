from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import context_processors

"""
Formulaire pour l'inscription d'un utilisateur, ajout de l'email en plus du username et des mots de passe
"""


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    """
    Définition des champs du formulaire
    """
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": context_processors.USERNAME_LABEL,
            "email": context_processors.EMAIL_LABEL,
            "password1": context_processors.PASSWORD_LABEL,
            "password2": context_processors.CONFIRM_PASSWORD_LABEL,
        }

    """
    Fonction pour sauvegarder l'utilisateur dans la base de données
    """
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
