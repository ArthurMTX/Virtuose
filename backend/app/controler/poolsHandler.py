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

def listing_volume_in_pool(QEMU_URI: str, pool_name: str ) -> list:
    """
    Returns a list of all storage volumes.

    Args:
        QEMU_URI (str): The URI of the QEMU service.

    Returns:
        list: A list of storage volumes.
    """
    return Pool(QEMU_URI).listing_storage_volume(pool_name)

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