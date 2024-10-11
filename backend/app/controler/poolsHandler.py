from app.models.pool import Pool

def linked_clone(QEMU_URI: str, template_name: str, clone_name: str) -> dict:
    """
    Creates a linked clone of a disk image.

    Args:
        QEMU_URI (str): The URI of the QEMU service.
        template_name (str): The name of the template disk image.
        clone_name (str): The name of the clone disk image.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return Pool(QEMU_URI).create_linked_clone(template_name, clone_name)

def valid_template(QEMU_URI: str, template_name: str) -> bool:
    """
    Checks if a template exists in the template folder.

    Args:
        QEMU_URI (str): The URI of the QEMU service.
        template_name (str): The name of the template disk image.

    Returns:
        bool: True if the template exists, False otherwise.
    """
    return {"response:" f"{Pool(QEMU_URI)._isValidTemplate(template_name)}"}

######## POOLS FUNCTIONS ########

def pools_list(QEMU_URI: str) -> dict:
    """
    Returns a list of all storage pools.

    Args:
        QEMU_URI (str): The URI of the QEMU service.

    Returns:
        list: A list of storage pools.
    """
    pool_object = Pool(QEMU_URI)
    list_of_pools = pool_object.listing_all_pool()
    pool_object.close()
    return {"status": "success", "message": list_of_pools}

def get_pool_information(QEMU_URI: str, pool_name: str) -> dict:
    """
    Returns information about a storage pool.

    Args:
        QEMU_URI (str): The URI of the QEMU service.
        pool_name (str): The name of the storage pool.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return Pool(QEMU_URI).pool_information(pool_name)

def all_pools_information(QEMU_URI: str) -> dict:
    """
    Returns information about all storage pools.

    Args:
        QEMU_URI (str): The URI of the QEMU service.

    Returns:
        dict: A dictionary containing the information about all storage pools.
    """
    informations_returned = dict()
    pool_object = Pool(QEMU_URI)
    pools = pool_object.listing_all_pool()
    for pool in pools:
        informations_returned[pool] = pool_object.pool_information(pool)["message"]
    return {"status": "success", "message": informations_returned}

######## VOLUMES FUNCTIONS ########

def delete_volume(QEMU_URI: str, volume_name: str) -> dict:
    """
    Deletes a storage volume.

    Args:
        QEMU_URI (str): The URI of the QEMU service.
        volume_name (str): The name of the storage volume.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return Pool(QEMU_URI).delete_storage_volume(volume_name)

def listing_volume_in_pool(QEMU_URI: str, pool_name: str ) -> dict:
    """
    Returns a list of all storage volumes.

    Args:
        QEMU_URI (str): The URI of the QEMU service.

    Returns:
        list: A list of storage volumes.
    """
    return Pool(QEMU_URI).listing_storage_volume(pool_name)

def listing_all_volumes(QEMU_URI: str) -> dict:
    """
    Returns a list of all storage volumes.

    Args:
        QEMU_URI (str): The URI of the QEMU service.

    Returns:
        list: A list of storage volumes.
    """
    informations_returned = dict()
    pool_object = Pool(QEMU_URI)
    pools = pool_object.listing_all_pool()
    for pool in pools:
        informations_returned[pool] = pool_object.listing_storage_volume(pool)["message"]
    return {"status": "success", "message": informations_returned}

def all_volumes_information(QEMU_URI: str) -> dict:
    """
    Returns information about all storage volumes.

    Args:
        QEMU_URI (str): The URI of the QEMU service.

    Returns:
        dict: A dictionary containing the information about all storage volumes.
    """
    informations_returned = dict()
    pool_object = Pool(QEMU_URI)
    pools = pool_object.listing_all_pool()
    for pool in pools:
        informations_returned[pool] = dict()
        volumes = pool_object.listing_storage_volume(pool)["message"]
        for volume in volumes:
            informations_returned[pool][volume] = pool_object.volume_information(volume)["message"]
    pool_object.close()
    return {"status": "success", "message": informations_returned}

def volume_information(QEMU_URI: str, volume_name: str) -> dict:
    """
    Returns information about a storage volume.

    Args:
        QEMU_URI (str): The URI of the QEMU service.
        volume_name (str): The name of the storage volume.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return Pool(QEMU_URI).volume_information(volume_name)

