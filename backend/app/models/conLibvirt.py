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
    
    def close(self):
        """
        Closes the connection to the libvirt daemon.
        """
        self.conn.close()