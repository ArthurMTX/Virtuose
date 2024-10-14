"""Views for user authentication and profile management."""

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from ..login_form import EmailAuthenticationForm
from ..register_form import CustomUserCreationForm


class RegisterView(CreateView):
    """Handles new user registration."""
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """Validates the form, saves the user, and logs them in."""
        user = form.save()

        # Get email and password from the form data
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        print(f'Email: {email}, Password: {password}')

        # Authenticate the user
        user = authenticate(username=email, password=password)

        if user is not None:
            login(self.request, user, backend='app.backends.EmailBackend')
            print('User logged in')
            return super().form_valid(form)

        messages.error(self.request, 'There was a problem logging you in.')
        print('Failed to log in user')
        return self.form_invalid(form)


class LoginView(FormView):
    """Handles user login."""
    template_name = 'registration/login.html'
    form_class = EmailAuthenticationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """Validates the form and logs in the user if the credentials are correct.

        Args:
            form (EmailAuthenticationForm): The validated authentication form.

        Returns:
            HttpResponse: Redirects to the home page or re-displays the form with an error.
        """
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        print(f'Email: {email}, Password: {password}')
        
        user = authenticate(username=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        messages.error(self.request, 'Invalid email or password.')
        return self.form_invalid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """Displays the user's profile."""
    template_name = 'app/profile.html'


class InformationsView(LoginRequiredMixin, TemplateView):
    """Displays the user's information."""
    template_name = 'app/informations.html'

    def get_context_data(self, **kwargs):
        """Adds the user's information to the context.

        Returns:
            dict: The context updated with the username and email.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        return context


class SecurityView(LoginRequiredMixin, TemplateView):
    """Displays the user's security page."""
    template_name = 'app/security.html'
