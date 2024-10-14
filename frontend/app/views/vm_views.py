"""Views for the virtual machine management."""

import json
import os
import signal
import subprocess

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView

from Virtuose.settings import VNC_URL
from ..services import (
    create_vm,
    get_all_domains,
    get_domain_informations,
    get_free_port,
    get_templates,
)
from ..vm_form import VMForm, get_form_fields_info
from ..vm_list import get_os_logo


class NewVMView(LoginRequiredMixin, View):
    """Handles the creation of a new virtual machine."""

    def get(self, request):
        """Displays the VM creation form.

        Args:
            request (HttpRequest): The received HTTP request.

        Returns:
            HttpResponse: The page with the VM creation form.
        """
        templates = get_templates()
        form_disabled = not templates
        form = VMForm()
        fields_info = get_form_fields_info()
        return render(request, 'app/new_vm.html', {
            'fields_info': fields_info,
            'form': form,
            'form_disabled': form_disabled
        })

    def post(self, request):
        """Processes the VM creation form submission.

        Args:
            request (HttpRequest): The received HTTP request.

        Returns:
            JsonResponse: A JSON response with the creation result.
        """
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = VMForm(request.POST)
            if form.is_valid():
                vm_data = form.cleaned_data
                vm_name = vm_data['name']
                template_name = vm_data['template']
                api_response = create_vm(
                    name=vm_name,
                    template_name=template_name
                )
                return JsonResponse(api_response, safe=False)
            return JsonResponse({
                'success': False,
                'message': 'Form validation failed. Please correct the errors and try again.',
                'errors': form.errors.as_json()
            }, status=400)
        return JsonResponse({'error': 'Invalid request'}, status=400)


class VMListView(LoginRequiredMixin, ListView):
    """Displays the list of virtual machines."""
    template_name = 'app/vm_list.html'
    context_object_name = 'vms'

    def get_queryset(self):
        """Retrieves the list of VMs with their information.

        Returns:
            list: List of dictionaries containing VM information.
        """
        vms = []
        try:
            vms_list = json.loads(get_all_domains(self.request).content)
            for vm_name in vms_list:
                vm_info = json.loads(get_domain_informations(self.request, vm_name).content)
                if vm_info:
                    vms.append({
                        'os_logo': get_os_logo(vm_info.get('os')),
                        'os': vm_info.get('os', 'OS'),
                        'name': vm_name,
                        'state': vm_info.get('state', '').lower(),
                        'memory_gb': vm_info.get('memory'),
                        'vcpus': vm_info.get('vcpus'),
                    })
        except Exception as e:
            print(f"An error occurred: {e}")
        return vms


class VMView(LoginRequiredMixin, TemplateView):
    """Displays the virtual machine console."""
    template_name = 'app/view.html'

    def get(self, request, vm_name):
        """Displays the VNC console of the specified VM.

        Args:
            request (HttpRequest): The received HTTP request.
            vm_name (str): The name of the VM.

        Returns:
            HttpResponse: The page with the VNC console or an error.
        """
        vm = get_domain_informations(request, str(vm_name))
        vm_port = vm.get('vnc', {}).get('port')
        view_port = get_free_port()
        host = request.get_host()

        if vm_port is None:
            print(f"VM with name {vm_name} not found")
            return render(request, 'app/view.html', {'error': 'VM not found'})

        websockify_command = [
            'websockify', '--web', VNC_URL, str(view_port), f'0.0.0.0:{vm_port}'
        ]
        websockify_process = subprocess.Popen(websockify_command, preexec_fn=os.setsid)
        request.session['websockify_pid'] = websockify_process.pid

        websocket_url = f'{host}:{view_port}'

        return render(request, 'app/view.html', {
            'websocket_url': websocket_url,
            'port': view_port,
            'host': host
        })


@method_decorator(csrf_exempt, name='dispatch')
class ReleasePortView(LoginRequiredMixin, View):
    """Releases the port used by the websockify process."""

    def post(self, request):
        """Releases the specified port by terminating the associated process.

        Args:
            request (HttpRequest): The received HTTP request.

        Returns:
            JsonResponse: Response indicating success or failure.
        """
        data = json.loads(request.body)
        port = data.get('port')

        if port:
            try:
                print(f"Trying to kill process on port {port}")
                result = subprocess.run(
                    ['lsof', '-t', '-i', f':{port}'],
                    capture_output=True,
                    text=True,
                    check=False
                )
                pids = result.stdout.strip().split()
                print(f"Result from lsof: {pids}")

                for pid in pids:
                    try:
                        os.killpg(os.getpgid(int(pid)), signal.SIGTERM)
                        print(f"Process group {pid} killed successfully")
                    except ProcessLookupError as e:
                        print(f"Process {pid} already terminated: {e}")

                return JsonResponse({'status': 'success'})
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)})
        print("No port provided")
        return JsonResponse({'status': 'error', 'message': 'No port provided'})