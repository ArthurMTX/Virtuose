import libvirt


class LibvirtHandler:
    def __init__(self, uri: str):
        """
        Initializes a connection to the libvirt daemon.

        Args:
            uri (str): The URI of the libvirt daemon.

        Raises:
            libvirt.libvirtError: If the connection to the libvirt daemon fails.
        """
        try:
            self.conn = libvirt.open(uri)
        except libvirt.libvirtError as e:
            self.conn = None
            print('Failed to open connection to ' + uri, e) 
    
    def initialize_pool_object(self, pool_name: str):
        """
        Initializes the pool object.

        Args:
            pool_name (str): The name of the pool.

        Returns:
            libvirt.virStoragePool: The pool object.
        """
        try:
            self.pool = self.conn.storagePoolLookupByName(pool_name)
        except libvirt.libvirtError:
            self.pool = None
    
    def initialize_domain_object(self, domain_name: str):
        """
        Initializes the domain object.

        Args:
            domain_name (str): The name of the domain.

        Returns:
            libvirt.virDomain: The domain object.
        """
        try:
            self.domain = self.conn.lookupByName(domain_name)
        except libvirt.libvirtError:
            self.domain = None

    def close(self):
        """
        Closes the connection to the libvirt daemon.
        """
        self.conn.close()