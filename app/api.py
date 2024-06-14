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
        return JsonResponse({"error": str(e)}, status=400)

    if request.method == "POST":
        try:
            if action == "START":
                if dom.isActive() == 1:
                    return JsonResponse({"status": context_processors.VM_ALREADY_RUNNING}, status=200)
                dom.create()
            elif action == "RESTART":
                if dom.isActive() == 1:
                    dom.reboot()
                else:
                    dom.create()
            elif action == "STOP":
                if dom.isActive() == 1:
                    dom.shutdown()
                else:
                    return JsonResponse({"status": context_processors.VM_ALREADY_STOPPED}, status=200)
            elif action == "KILL":
                if dom.isActive() == 1:
                    dom.destroy()
                else:
                    return JsonResponse({"status": context_processors.VM_ALREADY_RUNNING}, status=200)
            elif action == "DELETE":
                if dom.isActive() == 1:
                    dom.destroy()
                dom.undefine()
            else:
                return JsonResponse({"error": context_processors.VM_INVALID_ACTION}, status=400)
        except libvirt.libvirtError as e:
            return JsonResponse({"error": str(e)}, status=400)
        finally:
            conn.close()
        return JsonResponse({"status": f"{action} OK"}, status=200)
    return JsonResponse({"error": context_processors.VM_INVALID_METHOD}, status=405)
