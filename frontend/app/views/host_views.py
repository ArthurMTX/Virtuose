"""Views for host and storage pool information."""

import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..services import (
    get_host_informations,
    get_host_memory,
    get_pool_informations
)


class HostInfosView(LoginRequiredMixin, TemplateView):
    """Displays host information."""
    template_name = 'app/host.html'

    def get_context_data(self, **kwargs):
        """Adds host information to the context.

        Returns:
            dict: Context with host information or an error message.
        """
        context = super().get_context_data(**kwargs)
        host_infos_response = get_host_informations(self.request)
        host_memory_response = get_host_memory(self.request)

        if host_infos_response.status_code == 200 and host_memory_response.status_code == 200:
            context['host_infos'] = get_host_informations(self.request)
            context['host_memory'] = get_host_memory(self.request)
        else:
            print("Failed to get host information")
            context['error'] = 'Failed to get host information'
        return context


class PoolsInfosView(LoginRequiredMixin, TemplateView):
    """Displays storage pool information."""
    template_name = 'app/pools.html'

    def get_context_data(self, **kwargs):
        """Adds storage pool information to the context.

        Returns:
            dict: Context with pool information or an error message.
        """
        context = super().get_context_data(**kwargs)
        templates_response = get_pool_informations(self.request, "templates")
        default_response = get_pool_informations(self.request, "default")

        if templates_response.status_code == 200:
            context['pool_templates'] = json.loads(templates_response.content)['message']
        else:
            context['pool_templates'] = None

        if default_response.status_code == 200:
            context['pool_default'] = json.loads(default_response.content)['message']
        else:
            context['pool_default'] = None

        if context['pool_templates'] is None or context['pool_default'] is None:
            pool_who_failed = "templates" if context['pool_templates'] is None else "default"
            print(f"Failed to get pool information for {pool_who_failed}")
            context['error'] = f'Failed to get pool information for {pool_who_failed}'
        return context
