"""Views for the base app."""

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Displays the homepage."""
    template_name = 'app/index.html'
