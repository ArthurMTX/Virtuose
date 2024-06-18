from django.http import HttpResponse, JsonResponse
import os
import signal
import json
from django.views.decorators.csrf import csrf_exempt
from Virtuose.settings import VNC_URL
from .services import get_all_domains, get_domain_by_name, get_domain_by_uuid, get_free_port, interact_with_domain, \
    check_guest_agent_active, get_dom_object, wait_for_vm_to_be_ready
from .vm_form import VMForm, get_form_fields_info
from . import context_processors
from .register_form import CustomUserCreationForm
from uuid import uuid4
import subprocess
from xml.etree import ElementTree
from xml.dom import minidom
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .vm_list import get_os_logo


def index(request):
    return render(request, 'app/index.html')


@login_required
def new_vm(request):
    if request.method == "POST":
        form = VMForm(request.POST)
        if form.is_valid():
            vm_data = form.cleaned_data
            vm_name = vm_data['name']
            # selon le RFC4122
            uuid = str(uuid4())

            root = ElementTree.Element("VM")
            ElementTree.SubElement(root, "name").text = vm_name
            ElementTree.SubElement(root, "uuid").text = uuid

            system = ElementTree.SubElement(root, "system")
            for key, value in vm_data.items():
                if key != 'name':
                    ElementTree.SubElement(system, key).text = str(value)

            try:
                xml_str = ElementTree.tostring(root, encoding='unicode')
                xml_pretty = minidom.parseString(xml_str).toprettyxml(indent="    ")

                with open(f'tmp./{vm_name}_{uuid}.xml', 'w') as f:
                    f.write(xml_pretty)

                return HttpResponse(context_processors.CREATE_VM_SUCCESS)
            except Exception as e:
                print(e)
                return HttpResponse(f"{context_processors.CREATE_VM_ERROR} : {e}")
        else:
            fields_info = get_form_fields_info()
            errors = form.errors
            return render(request, 'app/new_vm.html', {'fields_info': fields_info, 'errors': errors, 'form': form})
    else:
        form = VMForm()
        fields_info = get_form_fields_info()
        return render(request, 'app/new_vm.html', {'fields_info': fields_info, 'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                form.add_error('email', context_processors.ERROR_EMAIL_EXISTS)
                return render(request, 'registration/register.html', {'form': form})
            else:
                user = form.save()
                auth_login(request, user)
                return redirect('index')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
            if user.check_password(password):
                auth_login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Mot de passe ou email invalide.')
        except user_model.DoesNotExist:
            messages.error(request, 'Mot de passe ou email invalide.')
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'app/profile.html', {'user': request.user})


@login_required
def informations(request):
    user = request.user
    username = user.username
    email = user.email
    return render(request, 'app/informations.html', {'username': username, 'email': email})


@login_required
def securite(request):
    return render(request, 'app/security.html')


@login_required
def vm_list(request):
    if request.method == 'POST':
        action = request.POST.get('action').upper()
        vm_uuid = request.POST.get('data_id')
        vm_info = get_domain_by_uuid(vm_uuid)
        print(vm_info)

        if vm_info is None:
            print(f"VM with UUID {vm_uuid} not found")

        if action == 'CONSOLE VIEW':
            return redirect('vm_view', vm_uuid=vm_uuid)

        elif action in ['START', 'STOP', 'RESTART', 'KILL']:
            if vm_info.get('state') == 'running':
                if action == 'START':
                    print(f"VM with UUID {vm_uuid} already running")
                else:
                    if action == 'STOP' and not check_guest_agent_active(vm_uuid):
                        print(f"VM with UUID {vm_uuid} not ready, cannot stop")
                    return interact_with_domain(vm_uuid, action)
            else:
                if action == 'START':
                    interact_with_domain(vm_uuid, action)
                    if wait_for_vm_to_be_ready(vm_uuid):
                        print(f"VM with UUID {vm_uuid} started and ready")
                    else:
                        print(f"VM with UUID {vm_uuid} started but not ready, timeout reached")
                print(f"VM with UUID {vm_uuid} not running, cannot {action}")

        elif action == 'DELETE':
            if vm_info.get('state') == 'running':
                print(f"VM with UUID {vm_uuid} running, cannot delete")
            else:
                return interact_with_domain(vm_uuid, action)

        print(f"Action {action} on VM with UUID {vm_uuid} completed")

    vms_list = get_all_domains()
    vms = []

    for vm_name in vms_list:
        vm_info = get_domain_by_name(vm_name)
        if vm_info:
            vm_info['os_logo'] = get_os_logo(vm_info.get('os'))
            vms.append(vm_info)

    return render(request, 'app/vm_list.html', {'vms': vms})



@login_required
def vm_view(request, vm_uuid):
    vm = get_domain_by_uuid(str(vm_uuid))
    vm_port = vm.get('graphics_port')
    view_port = get_free_port()
    host = request.get_host()

    websockify_command = f'websockify --web {VNC_URL} {view_port} 0.0.0.0:{vm_port}'
    websockify_process = subprocess.Popen(websockify_command, shell=True, preexec_fn=os.setsid)
    request.session['websockify_pid'] = websockify_process.pid

    websocket_url = f'{host}:{view_port}'

    return render(request, 'app/view.html', {'websocket_url': websocket_url, 'port': view_port, 'host': host})


@csrf_exempt
@login_required
def release_port(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        port = data.get('port')

        if port:
            try:
                print(f"Trying to kill process on port {port}")
                result = subprocess.run(['lsof', '-t', '-i', f':{port}'], capture_output=True, text=True)
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
        else:
            print("No port provided")
            return JsonResponse({'status': 'error', 'message': 'No port provided'})
    print("Invalid request method")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
