from fastapi import APIRouter

from app.controler.poolsHandler import (
    all_volumes_information,
    volume_information,
    listing_all_volumes,
    listing_volume_in_pool,
    delete_volume
)

from app.settings import QEMU_URI

router = APIRouter()

@router.get("/api/volumes/informations")
def api_pools_volumes_list():
    """
    Returns information about all storage volumes.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return all_volumes_information(QEMU_URI)

@router.get("/api/volumes/informations/{volume_name}")
def api_pools_volume_information(volume_name: str):
    """
    Returns information about a storage volume.
    
    Args:
        pool_name (str): The name of the pool.
        volume_name (str): The name of the storage volume.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return volume_information(QEMU_URI, volume_name)

@router.get("/api/volumes/list")
def api_pools_list():
    """
    Returns a list of all storage volumes name in all pool.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return listing_all_volumes(QEMU_URI)

@router.get("/api/volumes/list/{pool_name}")
def api_pools_list(pool_name: str):
    """
    Returns a list of all storage volumes in a pool.
    
    Args:
        pool_name (str): The name of the pool.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return listing_volume_in_pool(QEMU_URI, pool_name)

@router.post("/api/volumes/delete/{volume_name}")
def api_pools_delete_volume(volume_name: str):
    """
    Deletes a storage volume.
    
    Args:
        volume_name (str): The name of the storage volume.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return delete_volume(QEMU_URI, volume_name)