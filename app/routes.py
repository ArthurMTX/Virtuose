from django.http import JsonResponse
from .api.pools import *
from .api.domains import *
from .api.volumes import *
from django.views.decorators.csrf import csrf_exempt
from . import context_processors
from Virtuose.settings import QEMU_URI


def domain_info_by_name(request, dom_name):
    domain_info, error = list_dom_info_name(dom_name)
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(domain_info, safe=False)


def get_all_domain(request):
    domains, error = list_all_domain()
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(domains, safe=False)


def get_pools(request):
    pools, error = listAllPool()
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(pools, safe=False)


def volumes_info(request, pool_name):
    volumes, error = listVolumeInfo(pool_name)
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(volumes, safe=False)


def dom_info_by_uuid(request, dom_uuid):
    domain_info, error = list_dom_info_uuid(dom_uuid)
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(domain_info, safe=False)


def volumes_info_all(request):
    vol_info, error = list_all_vol_info()
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(vol_info, safe=False)


@csrf_exempt
def dom_actions(request, dom_uuid, action):
    logs = []
    try:
        conn = libvirt.open(QEMU_URI)
        dom = conn.lookupByUUIDString(dom_uuid)
    except libvirt.libvirtError as e:
        logs.append({"error": "Unable to find the virtual machine. Please check the VM UUID."})
        return JsonResponse(logs, safe=False, status=400)

    if request.method == "POST":
        try:
            if action == "START":
                if dom.isActive() == 1:
                    logs.append({"status": "The virtual machine is already running."})
                else:
                    dom.create()
                    logs.append({"status": "The virtual machine has been successfully started."})
            elif action == "RESTART":
                if dom.isActive() == 1:
                    dom.reboot()
                    logs.append({"status": "The virtual machine has been successfully restarted."})
                else:
                    dom.create()
                    logs.append({"status": "The virtual machine has been successfully started."})
            elif action == "STOP":
                if dom.isActive() == 1:
                    dom.shutdown()
                    logs.append({"status": "The virtual machine has been successfully stopped."})
                else:
                    logs.append({"status": "The virtual machine is already stopped."})
            elif action == "KILL":
                if dom.isActive() == 1:
                    dom.destroy()
                    logs.append({"status": "The virtual machine has been forcefully stopped."})
                else:
                    logs.append({"status": "The virtual machine is not running."})
            elif action == "DELETE":
                if dom.isActive() == 1:
                    dom.destroy()
                    logs.append({"status": "The virtual machine has been forcefully stopped."})
                dom.undefine()
                logs.append({"status": "The virtual machine has been successfully deleted."})
            else:
                logs.append({"error": "Invalid action. Please check the action and try again."})
        except libvirt.libvirtError as e:
            logs.append({"error": "An error occurred while performing the action. Please try again."})
        finally:
            conn.close()
            logs.append({"status": f"Action {action} completed successfully."})
            return JsonResponse(logs, safe=False, status=200)
    logs.append({"error": "Invalid method. Please use the POST method."})
    return JsonResponse(logs, safe=False, status=405)
