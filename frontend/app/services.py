import socket
import libvirt
import time
import requests
from django.http import JsonResponse
from Virtuose.settings import API_URL, QEMU_URI

"""
Permet de récupérer un port libre pour le WebSocket Websockify
"""


def get_free_port():
    MIN_PORT = 6080
    MAX_PORT = 6981

    for port in range(MIN_PORT, MAX_PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                pass
    return None


"""
Permet de récupérer la liste des domaines
"""


def get_all_domains(request):
    response = requests.get(f"{API_URL}/domains/list")
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, safe=False)
    else:
        print(f"Failed to get domains, status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)


"""
Permet de récupérer un domaine par son UUID
"""


def get_domain_by_uuid(uuid):
    response = requests.get(f"{API_URL}/domains/UUID/{uuid}")
    if response.status_code == 200:
        return response.json()
    else:
        return None


"""
Permet de récupérer un domaine par son nom
"""


def get_domain_by_name(request, name):
    response = requests.get(f"{API_URL}/domains/{name}")
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, safe=False)
    else:
        print(f"Failed to get domain '{name}', status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)


"""
Permet d'interagir avec un domaine (start, stop, reboot, force stop)
"""


def interact_with_domain(dom_uuid, action):
    url = f"{API_URL}/domains/actions/{dom_uuid}/{action}"
    response = requests.post(url)

    if response.status_code == 200:
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': response.text})


"""
Permet de récupérer un objet domaine par son UUID
"""


def get_dom_object(dom_uuid):
    conn = libvirt.open(QEMU_URI)
    dom = conn.lookupByUUIDString(dom_uuid)
    return dom


"""
Permet d'attendre que la VM soit prête
"""


def wait_for_vm_to_be_ready(vm_uuid):
    DELAY = 3
    TIMEOUT = 60

    vm = get_dom_object(vm_uuid)
    if vm is None:
        return False

    start_time = time.time()
    while time.time() - start_time < TIMEOUT:
        if vm.isActive() and check_guest_agent_active(vm_uuid):
            return True
        time.sleep(DELAY)
    return False


"""
Permet de vérifier si l'agent QEMU est actif sur la VM par son UUID
"""


def check_guest_agent_active(vm_uuid):
    MAX_RETRIES = 5
    DELAY = 3

    try:
        vm = get_dom_object(vm_uuid)
        if vm.isActive() == 0:
            return False

        for attempt in range(MAX_RETRIES):
            try:
                if vm.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0):
                    return True
            except libvirt.libvirtError:
                pass
            time.sleep(DELAY)
    except libvirt.libvirtError:
        return False
    return False


"""
Permet de récupérer les statistiques de l'hôte
"""


def get_host_informations(request):
    response = requests.get(f"{API_URL}/hypervisor/resume")
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, safe=False)

    else:
        print(f"Failed to get host information, status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    

"""
Permet de récupérer les templates disponibles sur l'hôte
"""

def get_templates():
    response = requests.get(f"{API_URL}/pools/list/templates/")
    if response.status_code == 200:
        templates = response.json()

        result = []
        for template in templates:
            extension = template.split('.')[-1]
            value = template.split('.')[0]

            label = f"{value} ({extension})"

            result.append((value, label))
        return result
    else:
        print(f"Failed to get templates, status code: {response.status_code}")
        return []


"""
Permet de créer une VM sur l'hôte avec les paramètres passés en argument
"""

def create_vm(name, template_name):
    response = requests.post(f"{API_URL}/domains/create/", 
                             json={
                                "name": name,
                                "template": template_name
                             })
    
    return response.json()


