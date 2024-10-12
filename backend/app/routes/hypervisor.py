from fastapi import APIRouter

from controler.hypervisorHandler import (
    hypervisor_information,
    hypervisor_hostname,
    hypervisor_memory_stats
)

from app.settings import QEMU_URI

router = APIRouter()

@router.get("/api/hypervisor/resume")
def api_hypervisor_resume():
    """
    Returns information about the hypervisor.
    
    Returns:
        dict: A dictionary containing information about the hypervisor.
    """
    return hypervisor_information(QEMU_URI)

@router.get("/api/hypervisor/hostname")
def api_hypervisor_hostname():
    """
    Returns the hostname of the hypervisor.
    
    Returns:
        dict: A dictionary containing the hostname of the hypervisor.
    """
    return hypervisor_hostname(QEMU_URI)

@router.get("/api/hypervisor/memory_stats")
def api_hypervisor_memory_stats():
    """
    Returns the memory parameters of the hypervisor.
    
    Returns:
        dict: A dictionary containing the memory parameters of the hypervisor.
    """
    return hypervisor_memory_stats(QEMU_URI)