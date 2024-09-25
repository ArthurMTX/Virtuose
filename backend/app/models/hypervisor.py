from app.models.conLibvirt import LibvirtHandler

class Hypervisor(LibvirtHandler):
    def __init__(self, uri: str):
        """
        Initializes a connection to the libvirt daemon.

        Args:
            uri (str): The URI of the libvirt daemon.

        Raises:
            libvirt.libvirtError: If the connection to the libvirt daemon fails.
        """
        super().__init__(uri)

    def general_information(self) -> list:
        """
        Returns information about the hypervisor.

        Returns:
            dict: A dictionary containing the hostname of the host.
        """
        return self.conn.getInfo()
    
    def libvirt_version(self) -> str:
        """
        Returns the version of the libvirt daemon.

        Returns:
            str: The version of the libvirt daemon.
        """
        return self.conn.getLibVersion()
    
    def hostname(self) -> str:
        """
        Returns the hostname of the host.

        Returns:
            str: The hostname of the host.
        """
        return self.conn.getHostname()

    def max_vcpus(self):
        """
        Returns the maximum number of virtual CPUs that can be assigned to a guest.

        Returns:
            int: The maximum number of virtual CPUs that can be assigned to a guest.
        """
        return self.conn.getMaxVcpus(None)
    
    def uri(self) -> str:
        """
        Returns the URI of the libvirt daemon.

        Returns:
            str: The URI of the libvirt daemon.
        """
        return self.conn.getURI()