from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import context_processors


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": context_processors.USERNAME_LABEL,
            "email": context_processors.EMAIL_LABEL,
            "password1": context_processors.PASSWORD_LABEL,
            "password2": context_processors.CONFIRM_PASSWORD_LABEL,
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
