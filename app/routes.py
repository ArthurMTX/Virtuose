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
    try:
        conn = libvirt.open(QEMU_URI)
        dom = conn.lookupByUUIDString(dom_uuid)
    except libvirt.libvirtError as e:
        return JsonResponse({"error": "Unable to find the virtual machine. Please check the VM UUID."}, status=400)

    if request.method == "POST":
        try:
            if action == "START":
                if dom.isActive() == 1:
                    return JsonResponse({"status": "The virtual machine is already running."}, status=200)
                dom.create()
                return JsonResponse({"status": "The virtual machine has been successfully started."}, status=200)
            elif action == "RESTART":
                if dom.isActive() == 1:
                    dom.reboot()
                    return JsonResponse({"status": "The virtual machine has been successfully restarted."}, status=200)
                else:
                    dom.create()
                    return JsonResponse({"status": "The virtual machine has been successfully started."}, status=200)
            elif action == "STOP":
                if dom.isActive() == 1:
                    dom.shutdown()
                    return JsonResponse({"status": "The virtual machine has been successfully stopped."}, status=200)
                else:
                    return JsonResponse({"status": "The virtual machine is already stopped."}, status=200)
            elif action == "KILL":
                if dom.isActive() == 1:
                    dom.destroy()
                    return JsonResponse({"status": "The virtual machine has been forcefully stopped."}, status=200)
                else:
                    return JsonResponse({"status": "The virtual machine is not running."}, status=200)
            elif action == "DELETE":
                if dom.isActive() == 1:
                    dom.destroy()
                    return JsonResponse({"status": "The virtual machine has been forcefully stopped."}, status=200)
                dom.undefine()
                return JsonResponse({"status": "The virtual machine has been successfully deleted."}, status=200)
            else:
                return JsonResponse({"error": "Invalid action. Please check the action and try again."}, status=400)
        except libvirt.libvirtError as e:
            return JsonResponse({"error": "An error occurred while performing the action. Please try again."}, status=400)
        finally:
            conn.close()
            return JsonResponse({"status": f"Action {action} completed successfully."}, status=200)
    return JsonResponse({"error": "Invalid method. Please use the POST method."}, status=405)
