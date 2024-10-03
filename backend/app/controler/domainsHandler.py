import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.models.domain import Domains
from app.models.pool import Pool

def domain_list(QEMU_URI: str) -> dict:
    """
    Returns a list of all domains.

    Args:
        QEMU_URI (str): The URI of the QEMU service.

    Returns:
        dict: A dictionary containing all domains.
    """
    domains = Domains(QEMU_URI)
    return domains.list_all()

def domain_start(QEMU_URI: str, domain_name: str) -> dict:
    """
    Starts a domain.

    Args:
        QEUM_URI (str): The URI of the QEMU service.
        domain_name (str): The name of the domain to start.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return Domains(QEMU_URI).start(domain_name)

def domain_stop(QEMU_URI: str, domain_name: str) -> dict:
    """
    Stops a domain.

    Args:
        QEMU_URI (str): The URI of the QEMU service.
        domain_name (str): The name of the domain to stop.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return Domains(QEMU_URI).stop(domain_name)

def domain_force_stop(QEMU_URI: str, domain_name: str) -> dict:
    """
    Stops a domain immediately.

    Args:
        QEUM_URI (str): The URI of the QEMU service.
        domain_name (str): The name of the domain to stop.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return Domains(QEMU_URI).force_stop(domain_name)

def domain_delete(QEMU_URI: str, domain_name: str) -> dict:
    """
    Deletes a domain.

    Args:
        QEMU_URI (str): The URI of the QEMU service.
        domain_name (str): The name of the domain to delete.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return Domains(QEMU_URI).delete(domain_name)

def domain_create(QEMU_URI: str, domain_name: str, template_name: str) -> dict:
    """
    Creates a new domain.

    Args:
        QEMU_URI (str): The URI of the QEMU service.
        domain_name (str): The name of the domain to create.
        template_name (str): The name of the template disk image.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    if Domains(QEMU_URI).isDomainExist(domain_name):
        return {"status": "error", "message": "Domain already exists."}
    if Pool(QEMU_URI).create_linked_clone(template_name, domain_name)["status"] == "success":
        return Domains(QEMU_URI).create(domain_name)
    else:
        return Pool(QEMU_URI).create_linked_clone(template_name, domain_name)
