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

    def host_information(self):
        """
        Returns information about the host.

        Returns:
            dict: A dictionary containing the hostname of the host.
        """
        host_information = {}
        host_information["Hypervisor information"] = self.conn.getInfo()
        self.conn.close()
        return host_information
    