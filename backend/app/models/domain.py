from app.models.conLibvirt import LibvirtHandler


class Domains(LibvirtHandler):
    def __init__(self, uri: str, domain_name = None, uid = None):
        """
        Initializes a connection to the libvirt daemon.

        Args:
            uri (str): The URI of the libvirt daemon.

        Raises:
            libvirt.libvirtError: If the connection to the libvirt daemon fails.
        """
        super().__init__(uri)
        self.domain = self.conn.lookupByName(domain_name) if domain_name else None
        self.uid = uid if uid else None
    
    def list_all(self) -> dict:
        """
        Returns a list of all domains.

        Returns:
            dict: A dictionary containing all domains.
        """
        domains = self.conn.listAllDomains(0)
        domain_list = dict()
        for domain in domains:
            domain_list[domain.name()] = domain.info()
        
        return domain_list


