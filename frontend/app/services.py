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
    
    if response.status_code != 200:
        print(f"Failed to get domains, status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    data = response.json()
    return JsonResponse(data, safe=False)


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
    
    if response.status_code != 200:
        print(f"Failed to get host information, status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    data = response.json()
    return JsonResponse(data, safe=False)


"""
Permet de récupérer les statistiques mémoire de l'hôte
"""
def get_host_memory(request):
    response = requests.get(f"{API_URL}/hypervisor/memory_stats")
    
    if response.status_code != 200:
        print(f"Failed to get host memory stats, status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    data = response.json()
    return JsonResponse(data, safe=False)


"""
Permet de récupérer les templates disponibles sur l'hôte
"""
def get_templates():
    response = requests.get(f"{API_URL}/volumes/list/templates/")
    
    if response.status_code != 200:
        print(f"Failed to get templates, status code: {response.status_code}")
        return []
    
    templates = response.json().get('message', [])
    result = []
    
    for template in templates:
        extension = template.split('.')[-1]
        value = template.split('.')[0]
        label = f"{value} ({extension})"
        result.append((template, label))
    
    return result


"""
Permet de créer une VM sur l'hôte avec les paramètres passés en argument
"""
def create_vm(name, template_name):
    response = requests.post(f"{API_URL}/domains/create/", 
                             json={"name": name, "template": template_name})
    
    if response.status_code != 200:
        print(f"Failed to create VM '{name}', status code: {response.status_code}")
        return {'error': f"Failed to create VM '{name}'"}
    
    return response.json()


"""
Permet de démarrer un domaine par son nom
"""
def start_domain(request, dom_name):
    response = requests.get(f"{API_URL}/domains/start/{dom_name}")
    
    if response.status_code != 200:
        print(f"Failed to start domain '{dom_name}', status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    return JsonResponse({'status': 'success', 'message': f'Domain {dom_name} successfully started'})


"""
Permet d'arrêter un domaine par son nom
"""
def stop_domain(request, dom_name):
    response = requests.get(f"{API_URL}/domains/stop/{dom_name}")
    
    if response.status_code != 200:
        print(f"Failed to stop domain '{dom_name}', status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    return JsonResponse({'status': 'success', 'message': f'Domain {dom_name} successfully stopped'})


"""
Permet de forcer l'arrêt d'un domaine par son nom
"""
def force_stop_domain(request, dom_name):
    response = requests.get(f"{API_URL}/domains/force_stop/{dom_name}")
    
    if response.status_code != 200:
        print(f"Failed to force stop domain '{dom_name}', status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    return JsonResponse({'status': 'success', 'message': f'Domain {dom_name} successfully killed'})


"""
Permet de forcer l'arrêt d'un domaine par son nom
"""
def restart_domain(request, dom_name):
    response = requests.get(f"{API_URL}/domains/restart/{dom_name}")
    
    if response.status_code != 200:
        print(f"Failed to restart domain '{dom_name}', status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    return JsonResponse({'status': 'success', 'message': f'Domain {dom_name} successfully restarted'})


"""
Permet de supprimer un domaine par son nom
"""
def delete_domain(request, dom_name):
    response = requests.post(f"{API_URL}/domains/delete/{dom_name}")
    response_data = response.json()

    if response.status_code != 200:
        print(f"Failed to delete domain '{dom_name}', status code: {response.status_code}")
        return JsonResponse({'error': f"Failed to delete domain '{dom_name}'"}, status=500)

    status = response_data.get('status')
    message = response_data.get('message', 'No message provided')

    if status == 'success':
        return JsonResponse({'status': 'success', 'message': message})
    else:
        print(f"Failed to delete domain '{dom_name}', message: {message}")
        return JsonResponse({'status': 'error', 'message': message})


"""
Permet d'optenir les informations d'un domaine par son nom
"""
def get_domain_informations(request, dom_name):
    response = requests.get(f"{API_URL}/domains/information/{dom_name}")
    
    if response.status_code != 200:
        print(f"Failed to get domain '{dom_name}' information, status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    data = response.json()
    return JsonResponse(data, safe=False)


"""
Permet d'optenir les informations de tous les pools
"""
def get_pools_informations(request):
    response = requests.get(f"{API_URL}/pools/all_informations")
    
    if response.status_code != 200:
        print(f"Failed to get pool information, status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    data = response.json()
    return JsonResponse(data, safe=False)


"""
Permet d'optenir les informations d'un pool par son nom
"""
def get_pool_informations(request, pool_name):
    response = requests.get(f"{API_URL}/pools/informations/{pool_name}")
    
    if response.status_code != 200:
        print(f"Failed to get pool information '{pool_name}', status code: {response.status_code}")
        return JsonResponse({'error': 'API backend inaccessible'}, status=500)
    
    data = response.json()
    return JsonResponse(data, safe=False)