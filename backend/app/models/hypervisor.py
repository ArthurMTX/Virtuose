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
    
    def __revert_version(self,version_number):
        """
        Reverts the version number to a human-readable format.

        Args:
            version_number (int): The version number.

        Returns:
            str: The version number in a human-readable format.
        """
        major = version_number // 1000000
        minor = (version_number % 1000000) // 1000
        release = version_number % 1000
        return f"{major}.{minor}.{release}"

    def libvirt_version(self) -> str:
        """
        Returns the version of the libvirt daemon.

        Returns:
            str: The version of the libvirt daemon.
        """
        return self.__revert_version(self.conn.getLibVersion())
    
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

    def memory_stats(self):
        """
        Returns the memory parameters of the host.

        Returns:
            dict: A dictionary containing the memory parameters of the host.
        """
        return self.conn.getMemoryStats(-1, 0)