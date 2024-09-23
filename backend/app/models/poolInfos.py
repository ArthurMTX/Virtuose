from app.api.models.conLibvirt import LibvirtHandler



class PoolInfos(LibvirtHandler):
    def __init__(self):
        super().__init__()
        self.pool = self.conn.storagePoolLookupByName('default')
        self.pool_info = self.pool.info()

    def create_disk(self, name, size):
        """
        Creates a new disk image.

        Args:
            name (str): The name of the disk image.
            size (int): The size of the disk image in bytes.
        """
        # Implementation needed
        pass

    def delete_disk(self, name):
        """
        Deletes a disk image.

        Args:
            name (str): The name of the disk image.
        """
        # Implementation needed
        pass

    def list_disks(self):
        """
        Returns a list of all disk images.

        Returns:
            list: A list of disk images.
        """
        # Implementation needed
        pass