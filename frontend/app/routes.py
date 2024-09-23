import json
import time
from django.http import JsonResponse, StreamingHttpResponse
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
    pools, error = list_all_pools()
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
    volumes, error = list_volume_info(pool_name)
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

        # Si la méthode est POST (pour effectuer une action)
        if request.method == "POST":
            try:
                if action == "start":  # Si l'action est "start"
                    if dom.info()[0] == 1:  # Si le domaine est "running", alors notifier qu'il est déjà démarré
                        yield json.dumps({"status": context_processors.VM_ALREADY_RUNNING}) + "\n"
                    elif dom.info()[0] == 3:  # Si le domaine est "paused", alors le réveiller
                        dom.resume()
                        yield json.dumps({"status": context_processors.VM_STARTED}) + "\n"
                        time.sleep(1)
                    elif dom.info()[0] != 1:  # Si le domaine est différent de "running", alors le démarrer
                        dom.create()
                        yield json.dumps({"status": context_processors.VM_STARTED}) + "\n"
                        time.sleep(1)
                elif action == "restart":  # Si l'action est restart
                    if dom.isActive() == 1:  # Si le domaine est démarré, alors le redémarrer
                        dom.reboot()
                        yield json.dumps({"status": context_processors.VM_RESTARTED}) + "\n"
                    else:  # Si le domaine est pas démarré, alors le démarrer
                        dom.create()
                        yield json.dumps({"status": context_processors.VM_STARTED}) + "\n"
                        time.sleep(1)
                elif action == "stop":  # Si l'action est stop
                    if dom.isActive() == 1:  # Si le domaine est démarré, alors l'arrêter
                        dom.shutdown()
                        yield json.dumps({"status": context_processors.VM_STOPPED}) + "\n"
                        time.sleep(1)
                    else:  # Si le domaine est pas actif, alors notifier qu'il n'est pas actif
                        yield json.dumps({"status": context_processors.VM_NOT_RUNNING}) + "\n"
                elif action == "kill":  # Si l'action est kill
                    if dom.isActive() == 1:  # Si le domaine est démarré, alors le tuer
                        dom.destroy()
                        yield json.dumps({"status": context_processors.VM_KILLED}) + "\n"
                        time.sleep(1)
                    else:  # Si le domaine est pas actif, alors notifier qu'il n'est pas actif
                        yield json.dumps({"status": context_processors.VM_NOT_RUNNING}) + "\n"
                elif action == "delete":  # Si l'action est delete
                    if dom.isActive() == 1:  # Si le domaine est actif, alors le tuer
                        dom.destroy()
                        yield json.dumps({"status": context_processors.VM_KILLED}) + "\n"
                        time.sleep(1)
                    dom.undefine()
                    yield json.dumps({"status": context_processors.VM_DELETED}) + "\n"
                elif action == "info":  # Si l'action est info
                    yield json.dumps({"status": context_processors.VM_INFO}) + "\n"
                else:  # Si l'action est invalide
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


@extend_schema(
    operation_id="dom_create",
    description="Créer un domaine",
    parameters=[
        OpenApiParameter('domain_name', OpenApiParameter.PATH, description="Nom du domaine"),
        OpenApiParameter('template_name', OpenApiParameter.PATH, description="Nom du template"),
    ],
    responses={
        200: 'OK',
        500: 'Internal Server Error'
    }
)
@api_view(['POST'])
def dom_create(request, domain_name, template_name):
    if request.method == "POST":
        result, error = create_domain(domain_name, template_name)
        if error:
            return JsonResponse({'error': error}, status=500)
        return JsonResponse(result, safe=False)
    else:
        return JsonResponse({"error": context_processors.VM_INVALID_METHOD}, status=405)
