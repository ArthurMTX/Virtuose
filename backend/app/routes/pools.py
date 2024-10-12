from fastapi import APIRouter

from controler.poolsHandler import (
    pools_list,
    get_pool_information,
    all_pools_information
)

from app.settings import QEMU_URI

router = APIRouter()

@router.get("/api/pools/list")
def api_pools_list():
    """
    Returns a list of all storage pools.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return pools_list(QEMU_URI)

@router.get("/api/pools/informations/{pool_name}")
def api_pools_information(pool_name: str):
    """
    Returns information about all storage pools.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return get_pool_information(QEMU_URI, pool_name)

@router.get("/api/pools/all_informations")
def api_pools_all_informations():
    """
    Returns information about all storage pools.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return all_pools_information(QEMU_URI)