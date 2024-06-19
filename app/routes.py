import json
import time

from django.http import JsonResponse
from .api.pools import *
from .api.domains import *
from .api.volumes import *
from django.views.decorators.csrf import csrf_exempt
from . import context_processors
from django.http import StreamingHttpResponse
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
    def stream_logs():
        try:
            conn = libvirt.open(QEMU_URI)
            dom = conn.lookupByUUIDString(dom_uuid)
            vm_name = dom.name()
        except libvirt.libvirtError as e:
            yield json.dumps({"error": context_processors.FAILED_TO_GET_DOMAIN_UUID}) + "\n"
            return

        if request.method == "POST":
            try:
                if action == "START":
                    if dom.isActive() == 1:
                        yield json.dumps({"status": context_processors.VM_ALREADY_RUNNING}) + "\n"
                    else:
                        dom.create()
                        yield json.dumps({"status": context_processors.VM_STARTED}) + "\n"
                        time.sleep(1)
                elif action == "RESTART":
                    if dom.isActive() == 1:
                        dom.reboot()
                        yield json.dumps({"status": context_processors.VM_RESTARTED}) + "\n"
                    else:
                        dom.create()
                        yield json.dumps({"status": context_processors.VM_STARTED}) + "\n"
                        time.sleep(1)
                elif action == "STOP":
                    if dom.isActive() == 1:
                        dom.shutdown()
                        yield json.dumps({"status": context_processors.VM_STOPPED}) + "\n"
                        time.sleep(1)
                    else:
                        yield json.dumps({"status": context_processors.VM_NOT_RUNNING}) + "\n"
                elif action == "KILL":
                    if dom.isActive() == 1:
                        dom.destroy()
                        yield json.dumps({"status": context_processors.VM_KILLED}) + "\n"
                        time.sleep(1)
                    else:
                        yield json.dumps({"status": context_processors.VM_NOT_RUNNING}) + "\n"
                elif action == "DELETE":
                    if dom.isActive() == 1:
                        dom.destroy()
                        yield json.dumps({"status": context_processors.VM_KILLED}) + "\n"
                        time.sleep(1)
                    dom.undefine()
                    yield json.dumps({"status": context_processors.VM_DELETED}) + "\n"
                elif action == "INFO":
                    yield json.dumps({"status": context_processors.VM_INFO}) + "\n"
                else:
                    yield json.dumps({"error": context_processors.VM_INVALID_ACTION}) + "\n"
            except libvirt.libvirtError as e:
                yield json.dumps({"error": context_processors.VM_ERROR}) + "\n"
            finally:
                conn.close()
                yield json.dumps({"status": f"Action {action} on VM {vm_name} completed."}) + "\n"
        else:
            yield json.dumps({"error": context_processors.VM_INVALID_METHOD}) + "\n"

    response = StreamingHttpResponse(stream_logs(), content_type='application/json')
    response['X-Accel-Buffering'] = 'no'
    return response
