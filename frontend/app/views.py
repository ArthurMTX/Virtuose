from django.http import JsonResponse
import os
import signal
import json
from django.views.decorators.csrf import csrf_exempt
from Virtuose.settings import VNC_URL
from .services import *
from .vm_form import VMForm, get_form_fields_info
from . import context_processors
from .register_form import CustomUserCreationForm
import subprocess
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .vm_list import get_os_logo


"""
Render l'index (page d'accueil)
"""


def index(request):
    return render(request, 'app/index.html')


"""
Render la page de création de VM
Récupère les informations du formulaire et les enregistre dans un fichier XML
"""


@login_required
def new_vm(request):
    # Récupère les templates disponibles
    templates = get_templates()
    form_disabled = not templates

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = VMForm(request.POST)

        if form.is_valid():
            # Récupération des données du formulaire
            vm_data = form.cleaned_data
            vm_name = vm_data['name']
            template_name = vm_data['template']

            # Crée la VM via l'API et récupère la réponse de l'API
            api_response = create_vm(name=vm_name, template_name=template_name)

            # Renvoyer la réponse de l'API directement, avec le même code et message
            return JsonResponse(api_response, safe=False)
        else:
            # Retourne les erreurs de validation du formulaire sous forme de JSON
            return JsonResponse({
                'success': False,
                'message': 'Form validation failed. Please correct the errors and try again.',
                'errors': form.errors.as_json()
            }, status=400)  # Code 400 pour indiquer une erreur dans la requête

    # Pour les requêtes GET ou non-AJAX POST
    form = VMForm()
    fields_info = get_form_fields_info()
    return render(request, 'app/new_vm.html', {
        'fields_info': fields_info,
        'form': form,
        'form_disabled': form_disabled
    })


"""
Render la page de création de compte
Récupère les informations du formulaire et les enregistre dans la base de données
"""


def register(request):
    # Action POST, on récupère les données du formulaire
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Form valide, on vérifie si l'email n'est pas déjà utilisé
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                form.add_error('email', context_processors.ERROR_EMAIL_EXISTS)
                return render(request, 'registration/register.html', {'form': form})
            else:
                # Email non utilisé, on enregistre l'utilisateur
                user = form.save()
                auth_login(request, user)
                return redirect('index')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        # Action GET, on affiche le formulaire vide
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})


"""
Render la page de connexion
Récupère les informations du formulaire et les vérifie
"""

    
def login_view(request):
    # Action POST, on récupère les données du formulaire
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
            if user.check_password(password):
                # Mot de passe et email valides, on connecte l'utilisateur et on le redirige
                auth_login(request, user)
                return redirect('index')
            else:
                # Mot de passe ou email invalide
                messages.error(request, 'Mot de passe ou email invalide.')
        except user_model.DoesNotExist:
            # Mot de passe ou email invalide
            messages.error(request, 'Mot de passe ou email invalide.')
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})
    else:
        # Action GET, on affiche le formulaire vide
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


"""
Render la page de profil
Non utilisée pour le moment
"""


@login_required
def profile(request):
    return render(request, 'app/profile.html', {'user': request.user})


"""
Render la page des informations de l'utilisateur
"""


@login_required
def informations(request):
    user = request.user
    username = user.username
    email = user.email
    return render(request, 'app/informations.html', {'username': username, 'email': email})


"""
Render la page de profil
Non utilisée pour le moment
"""


@login_required
def securite(request):
    return render(request, 'app/security.html')


"""
Render la page des VMs
Récupère les informations des VMs et les affiche
Permet d'interagir avec les VMs (démarrer, arrêter, redémarrer, supprimer, voir la console)
"""


@login_required
def vm_list(request):
    vms_list = json.loads(get_all_domains(request).content)
    vms = []

    if vms_list:
        # Récupère les informations des VMs et les affiche
        for vm_name in vms_list:
            vm_info = get_domain_by_name(request, vm_name)
            if vm_info:
               vm_info['os_logo'] = get_os_logo(vm_info.get('os'))
               vms.append(vm_info)
            
            # TODO: Delete this block
            vm_info['os'] = 'OS'
            vm_info['name'] = vm_name
            vm_info['state'] = 'unknown'
            vm_info['memory_gb'] = 'RAM'
            vm_info['vcpu'] = 'VCPU'
    else:
        print("No VMs found")

    # Action POST, on récupère l'action à effectuer sur une VM
    if request.method == 'POST':
        action = request.POST.get('action').upper()
        vm_name = request.POST.get('data_name')
        vm_info = get_domain_by_name(vm_name)

        # VM non trouvée (name invalide?)
        if vm_info is None:
            print(f"VM with name {vm_name} not found")

        # Si l'action est 'CONSOLE VIEW', on redirige vers la page de la console
        if action == 'CONSOLE VIEW':
            return redirect('vm_view', vm_name=vm_name)

        # Si l'action est 'START', 'STOP', 'RESTART' ou 'KILL', on vérifie l'état de la VM
        elif action in ['START', 'STOP', 'RESTART', 'KILL']:
            if vm_info.get('state') == 'running':
                if action == 'START':
                    # Si la VM est déjà en cours d'exécution, on ne fait rien
                    print(f"VM with name {vm_name} already running")
                else:
                    # Si l'action est 'STOP' et que l'agent n'est pas actif, on ne peut pas arrêter la VM
                    if action == 'STOP' and not check_guest_agent_active(vm_name):
                        print(f"VM with name {vm_name} not ready, cannot stop")
                    return interact_with_domain(vm_name, action)
            else:
                if action == 'START':
                    interact_with_domain(vm_name, action)
                    if wait_for_vm_to_be_ready(vm_name):
                        # Si la VM est prête, on affiche un message
                        print(f"VM with name {vm_name} started and ready")
                    else:
                        # Si la VM n'est pas prête, on affiche un message d'erreur
                        print(f"VM with name {vm_name} started but not ready, timeout reached")
                # Si la VM n'est pas en cours d'exécution, on ne peut pas l'arrêter, la redémarrer ou la supprimer
                print(f"VM with name {vm_name} not running, cannot {action}")

        # Si l'action est 'DELETE', on vérifie si la VM est en cours d'exécution
        elif action == 'DELETE':
            if vm_info.get('state') == 'running':
                # Si la VM est en cours d'exécution, on ne peut pas la supprimer
                print(f"VM with name {vm_name} running, cannot delete")
            else:
                # La VM n'est pas en cours d'exécution, on peut la supprimer
                return interact_with_domain(vm_name, action)

        print(f"Action {action} on VM with name {vm_name} completed") 

    return render(request, 'app/vm_list.html', {'vms': vms})


"""
Render la page de la console, permet de voir l'affichage de la VM
Récupère le port de la VM et le redirige vers le websocket
Lance le processus websockify pour rediriger le flux VNC vers le websocket
"""


@login_required
def vm_view(request, vm_name):
    vm = get_domain_by_name(str(vm_name))
    vm_port = vm.get('vnc', {}).get('port')
    view_port = get_free_port()
    host = request.get_host()

    # VM non trouvée (nom invalide?)
    if vm_port is None:
        print(f"VM with name {vm_name} not found")
        return render(request, 'app/view.html', {'error': 'VM not found'})

    # Lancement du processus websockify pour rediriger le flux VNC vers le websocket
    websockify_command = f'websockify --web {VNC_URL} {view_port} 0.0.0.0:{vm_port}'
    websockify_process = subprocess.Popen(websockify_command, shell=True, preexec_fn=os.setsid)
    request.session['websockify_pid'] = websockify_process.pid

    websocket_url = f'{host}:{view_port}'

    return render(request, 'app/view.html', {'websocket_url': websocket_url, 'port': view_port, 'host': host})


"""
Libère le port utilisé par le processus websockify quand la page de la console est fermée
"""


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
                        # On tue le processus et son groupe
                        os.killpg(os.getpgid(int(pid)), signal.SIGTERM)
                        print(f"Process group {pid} killed successfully")
                    except ProcessLookupError as e:
                        # Le processus a déjà été tué (normalement impossible)
                        print(f"Process {pid} already terminated: {e}")

                return JsonResponse({'status': 'success'})
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            # Pas de port fourni (normalement impossible)
            print("No port provided")
            return JsonResponse({'status': 'error', 'message': 'No port provided'})

    # Méthode non autorisée (normalement impossible)
    print("Invalid request method")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



"""
Render la page des informations de l'hôte
"""


@login_required
def host_infos(request):
    host_infos_response = get_host_informations(request)
    host_memory_response = get_host_memory(request)

    if host_infos_response.status_code == 200 and host_memory_response.status_code == 200:
        host_infos = json.loads(host_infos_response.content)
        host_memory = json.loads(host_memory_response.content)
    else:
        host_infos = None
        host_memory = None

    if host_infos is None or host_memory is None:
        print("Failed to get host informations")
        return render(request, 'app/host.html', {'error': 'Failed to get host informations'})

    return render(request, 'app/host.html', {'host_infos': host_infos, 'host_memory': host_memory})