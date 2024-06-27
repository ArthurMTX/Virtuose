import json
import time

from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .api.pools import *
from .api.domains import *
from .api.volumes import *
from .api.host import *
from . import context_processors


@extend_schema(
    operation_id="get_host_info",
    description="Récupère les informations de l'hôte.",
    responses={
        200: 'OK',
        400: 'Bad Request',
    }
)
@api_view(['GET'])
def get_host_info(request):
    host, error = list_host_info()
    if error:
        return JsonResponse({'error': error}, status=400)
    return JsonResponse(host, safe=False)


@extend_schema(
    operation_id="domain_info_by_name",
    description="Récupère les informations du domaine par son nom.",
    parameters=[
        OpenApiParameter('dom_name', OpenApiParameter.PATH, description="Nom du domaine")
    ],
    responses={
        200: 'OK',
        500: 'Internal Server Error'
    }
)
@api_view(['GET'])
def domain_info_by_name(request, dom_name):
    domain_info, error = list_dom_info_name(dom_name)
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(domain_info, safe=False)


@extend_schema(
    operation_id="get_all_domain",
    description="Récupère tout les domaines.",
    responses={
        200: 'OK',
        500: 'Internal Server Error'
    }
)
@api_view(['GET'])
def get_all_domain(request):
    domains, error = list_all_domain()
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(domains, safe=False)


@extend_schema(
    operation_id="get_pools",
    description="Récupère tout les pools.",
    responses={
        200: 'OK',
        500: 'Internal Server Error'
    }
)
@api_view(['GET'])
def get_pools(request):
    pools, error = listAllPool()
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(pools, safe=False)


@extend_schema(
    operation_id="volumes_info",
    description="Récupère les informations de volume pour un pool spécifique.",
    parameters=[
        OpenApiParameter('pool_name', OpenApiParameter.PATH, description="Nom du pool")
    ],
    responses={
        200: 'OK',
        500: 'Internal Server Error'
    }
)
@api_view(['GET'])
def volumes_info(request, pool_name):
    volumes, error = listVolumeInfo(pool_name)
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(volumes, safe=False)


@extend_schema(
    operation_id="dom_info_by_uuid",
    description="Récupère les informations du domaine par son UUID.",
    parameters=[
        OpenApiParameter('dom_uuid', OpenApiParameter.PATH, description="UUID du domaine")
    ],
    responses={
        200: 'OK',
        500: 'Internal Server Error'
    }
)
@api_view(['GET'])
def dom_info_by_uuid(request, dom_uuid):
    domain_info, error = list_dom_info_uuid(dom_uuid)
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(domain_info, safe=False)


@extend_schema(
    operation_id="volumes_info_all",
    description="Récupère toutes les informations de volume.",
    responses={
        200: 'OK',
        500: 'Internal Server Error'
    }
)
@api_view(['GET'])
def volumes_info_all(request):
    vol_info, error = list_all_vol_info()
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse(vol_info, safe=False)


@csrf_exempt
@extend_schema(
    operation_id="dom_actions",
    description="Effectue une action spécifique sur un domaine spécifique.",
    parameters=[
        OpenApiParameter('dom_uuid', OpenApiParameter.PATH, description="UUID du domaine"),
        OpenApiParameter('action', OpenApiParameter.PATH, description="Action à effectuer sur le domaine")
    ],
    responses={
        200: 'OK',
        500: 'Internal Server Error'
    }
)
@api_view(['POST'])
def dom_actions(request, dom_uuid, action):
    def stream_logs():
        try:
            conn = libvirt.open(QEMU_URI)
            dom = conn.lookupByUUIDString(dom_uuid)
            vm_name = dom.name()
        except libvirt.libvirtError as e:
            yield json.dumps({"error": context_processors.FAILED_TO_GET_DOMAIN_UUID}) + "\n"
            return

        action_lower = action.lower()
        print(f"Action method: {request.method}, action: {action_lower}, VM name: {vm_name}")

        if request.method == "POST":
            try:
                if action_lower == "start":
                    if dom.info()[0] == 1:  # Si le domaine est "running"
                        yield json.dumps({"status": context_processors.VM_ALREADY_RUNNING}) + "\n"
                    elif dom.info()[0] == 3:  # Si le domaine est "paused"
                        dom.resume()
                        yield json.dumps({"status": context_processors.VM_STARTED}) + "\n"
                        time.sleep(1)
                    elif dom.info()[0] != 1:  # Si le domaine est différent de "running"
                        dom.create()
                        yield json.dumps({"status": context_processors.VM_STARTED}) + "\n"
                        time.sleep(1)
                elif action_lower == "restart":
                    if dom.isActive() == 1:
                        dom.reboot()
                        yield json.dumps({"status": context_processors.VM_RESTARTED}) + "\n"
                    else:
                        dom.create()
                        yield json.dumps({"status": context_processors.VM_STARTED}) + "\n"
                        time.sleep(1)
                elif action_lower == "stop":
                    if dom.isActive() == 1:
                        dom.shutdown()
                        yield json.dumps({"status": context_processors.VM_STOPPED}) + "\n"
                        time.sleep(1)
                    else:
                        yield json.dumps({"status": context_processors.VM_NOT_RUNNING}) + "\n"
                elif action_lower == "kill":
                    if dom.isActive() == 1:
                        dom.destroy()
                        yield json.dumps({"status": context_processors.VM_KILLED}) + "\n"
                        time.sleep(1)
                    else:
                        yield json.dumps({"status": context_processors.VM_NOT_RUNNING}) + "\n"
                elif action_lower == "delete":
                    if dom.isActive() == 1:
                        dom.destroy()
                        yield json.dumps({"status": context_processors.VM_KILLED}) + "\n"
                        time.sleep(1)
                    dom.undefine()
                    yield json.dumps({"status": context_processors.VM_DELETED}) + "\n"
                elif action_lower == "info":
                    yield json.dumps({"status": context_processors.VM_INFO}) + "\n"
                else:
                    yield json.dumps({"error": context_processors.VM_INVALID_ACTION}) + "\n"
            except libvirt.libvirtError as e:
                yield json.dumps({"error": context_processors.VM_ERROR}) + "\n"
            finally:
                conn.close()
        else:
            yield json.dumps({"error": context_processors.VM_INVALID_METHOD}) + "\n"

    response = StreamingHttpResponse(stream_logs(), content_type='application/json')
    response['X-Accel-Buffering'] = 'no'
    return response
