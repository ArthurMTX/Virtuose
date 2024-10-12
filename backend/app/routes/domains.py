from fastapi import APIRouter

from controler.domainsHandler import (
    domain_list,
    domain_start,
    domain_stop,
    domain_restart,
    domain_pause,
    domain_state,
    domain_information,
    domain_create,
    domain_delete,
    domain_force_stop
)

from settings import QEMU_URI
from schemas import DomainCreationForm

router = APIRouter()

@router.get("/api/domains/list")
def api_domain_list():
    """
    Returns a list of all domains.
    
    Returns:
        dict: A dictionary containing all domains.
    """
    return domain_list(QEMU_URI)

@router.get("/api/domains/state/{domain_name}")
def api_domain_state(domain_name: str):
    """
    Returns the state of a domain.
    
    Args:
        domain_name (str): The name of the domain.
    
    Returns:
        dict: A dictionary containing the state of the domain.
    """
    return domain_state(QEMU_URI, domain_name)

@router.get("/api/domains/information/{domain_name}")
def api_domain_information(domain_name: str):
    """
    Returns information about a domain.
    
    Args:
        domain_name (str): The name of the domain.
    
    Returns:
        dict: A dictionary containing information about the domain.
    """
    return domain_information(QEMU_URI, domain_name)

@router.get("/api/domains/start/{domain_name}")
def api_domain_start(domain_name: str):
    """
    Starts a domain.
    
    Args:
        domain_name (str): The name of the domain to start.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_start(QEMU_URI, domain_name)

@router.get("/api/domains/stop/{domain_name}")
def api_domain_stop(domain_name: str):
    """
    Stops a domain.
    
    Args:
        domain_name (str): The name of the domain to stop.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_stop(QEMU_URI, domain_name)

@router.get("/api/domains/force_stop/{domain_name}")
def api_domains_force_stop(domain_name: str):
    """
    Stops a domain immediately.
    
    Args:
        domain_name (str): The name of the domain to stop.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_force_stop(QEMU_URI, domain_name)

@router.get("/api/domains/restart/{domain_name}")
def api_domain_restart(domain_name: str):
    """
    Restarts a domain.
    
    Args:
        domain_name (str): The name of the domain to restart.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_restart(QEMU_URI, domain_name)

@router.get("/api/domains/pause/{domain_name}")
def api_domain_pause(domain_name: str):
    """
    Pauses a domain.
    
    Args:
        domain_name (str): The name of the domain to pause.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_pause(QEMU_URI, domain_name)


@router.post("/api/domains/delete/{domain_name}")
def api_domain_delete(domain_name: str):
    """
    Deletes a domain.
    
    Args:
        domain_name (str): The name of the domain to delete.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_delete(QEMU_URI, domain_name)

@router.post("/api/domains/create")
def api_domain_create(vm_form: DomainCreationForm):
    """
    Creates a domain.
    
    Args:
        domain_name (str): The name of the domain to create.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_create(QEMU_URI, vm_form.name, vm_form.template)