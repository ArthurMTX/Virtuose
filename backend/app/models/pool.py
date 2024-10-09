from app.models.conLibvirt import LibvirtHandler
import subprocess
import xml.etree.ElementTree as ET


class Pool(LibvirtHandler):
    def __init__(self, uri: str):
        """
        Initializes a connection to the libvirt daemon.

        Args:
            URI (str): The URI of the libvirt daemon.
        """
        super().__init__(uri)
        self.template_path = "/opt/virtuose/templates/"
        self.storage_path = "/opt/virtuose/storage/"
        self.pool = None

    def listing_storage_volume(self, pool_name) -> dict:
        """
        Returns a list of all storage volumes.

        Returns:
            list: A list of storage volumes.
        """
        super().initialize_pool_object(pool_name)
        if self.pool:
            self.pool.refresh(0)
            volumes = self.pool.listVolumes()
            return {"status": "success", "message": volumes}
        else:
            return {"status": "error", "message": "Pool not found."}
    
    def _isValidTemplate(self, template_name):
        """
        Checks if a template exists in the template folder.

        Args:
            template_name (str): The name of the template disk image.

        Returns:
            bool: True if the template exists, False otherwise.
        """
        return f"{template_name}" in self.listing_storage_volume("templates")['message']

    def listing_all_pool(self) -> list:
        """
        Returns a list of all storage pools.

        Returns:
            list: A list of storage pools.
        """
        pools = self.conn.listStoragePools()
        return pools
    
    def pool_path(self, pool_name: str) -> dict:
        """
        Returns the path of a storage pool.

        Args:
            pool_name (str): The name of the storage pool.
        """
        super().initialize_pool_object(pool_name)
        if not self.pool:
            return {"status": "error", "message": "Pool not found."}
        self.pool.refresh(0)
        pool_xml = self.pool.XMLDesc()
        root = ET.fromstring(pool_xml)
        path_element = root.find('./target/path')
        return {"status": "success", "message": path_element.text}

    def pool_information(self, pool_name: str) -> dict:
        """
        Returns information about a storage pool.

        Args:
            pool_name (str): The name of the storage pool.
        """
        super().initialize_pool_object(pool_name)
        if not self.pool:
            return {"status": "error", "message": "Pool not found."}
        self.pool.refresh(0)
        pool_info = self.pool.info()
        return {"status": "success", "message": {"Path": self.pool_path(pool_name)["message"],"capacity_MB": round(((pool_info[1]) / 1024 ** 2), 2), "allocation_MB": round( ((pool_info[2]) / 1024 ** 2), 2)} }
    
    def volume_information(self, volume_name: str) -> dict:
        """
        Returns information about a storage volume.

        Args:
            volume_name (str): The name of the storage volume.
        """
        for pool in self.listing_all_pool():
            if volume_name in self.listing_storage_volume(pool)["message"]:
                volume = self.pool.storageVolLookupByName(volume_name)
                vol_info = volume.info()    
                return {"status": "success", "message": {"capacity_MB": round(((vol_info[1]) / 1024 ** 2), 2), "allocation_MB": round( ((vol_info[2]) / 1024 ** 2), 2)} }
        return {"status": "error", "message": "Volume not found."}

    def create_linked_clone(self, template_name, clone_name):
        """
        Creates a linked clone of a disk image.

        Args:
            template_name (str): The name of the template disk image.
            clone_name (str): The name of the clone disk image.
        """
        if self._isValidTemplate(template_name):
            command = ['qemu-img', 'create', '-f', 'qcow2', '-F', 'qcow2', '-b', f"/opt/virtuose/templates/{template_name}", f"/opt/virtuose/storage/{clone_name}.qcow2"]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return {'status': 'success', 'message': 'Linked clone created successfully.'}
            else:
                return {'status': 'error', 'message': 'Failed to create linked clone.'}
        else:
            return {'status': 'error', 'message': 'Template does not exist'}
        
    def delete_disk(self, name):
        """
        Deletes a disk image.

        Args:
            name (str): The name of the disk image.
        """
        # Implementation needed
        pass
