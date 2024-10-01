from app.models.conLibvirt import LibvirtHandler
import subprocess


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

    def listing_storage_volume(self, pool_name):
        """
        Returns a list of all storage volumes.

        Returns:
            list: A list of storage volumes.
        """
        super().initialize_pool_object(pool_name)
        if self.pool:
            volumes = self.pool.listVolumes()
            return volumes
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
        return f"{template_name}.qcow2" in self.listing_storage_volume("templates")

    def create_linked_clone(self, template_name, clone_name):
        """
        Creates a linked clone of a disk image.

        Args:
            template_name (str): The name of the template disk image.
            clone_name (str): The name of the clone disk image.
        """
        if self._isValidTemplate(template_name):
            command = ['qemu-img', 'create', '-f', 'qcow2', '-F', 'qcow2', '-b', f"/opt/virtuose/templates/{template_name}.qcow2", f"/opt/virtuose/storage/{clone_name}.qcow2"]
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
