from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import context_processors

"""
Formulaire pour l'inscription d'un utilisateur, ajout de l'email en plus du username et des mots de passe
"""


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": context_processors.USERNAME_LABEL,
            "email": context_processors.EMAIL_LABEL,
            "password1": context_processors.PASSWORD_LABEL,
            "password2": context_processors.CONFIRM_PASSWORD_LABEL,
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        UserModel = get_user_model()
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('Un utilisateur avec cet email existe déjà.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        UserModel = get_user_model()
        if UserModel.objects.filter(username=username).exists():
            raise forms.ValidationError('Un utilisateur avec ce nom d\'utilisateur existe déjà.')
        return username
