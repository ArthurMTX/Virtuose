from app.api.models.conLibvirt import LibvirtHandler
import libvirt


class domainInfos(LibvirtHandler):
    def __init__(self, name:str = None, uid:str = None):
        """
        Initializes a connection to the libvirt daemon.
        
        Args:
            uri (str): The URI of the libvirt daemon.
            name (str, optional): The name of the domain. Defaults to None.
            uid (str, optional): The UID of the domain. Defaults to None.
        Raises:
            ValueError: If neither name nor uid is provided.
        """
        super().__init__()
        self.domain = None
        if name:
            self.domain = self.get_domain(name)
        elif uid:
            self.domain = self.get_domain_by_uid(uid)
        else:
            raise ValueError("Either name or uid must be provided.")

    def get_domain(self, name: str) :
        """
        Returns a domain object by its name.

        Args:
            name (str): The name of the domain.

        Returns:
            libvirt.virDomain: The domain object.

        Raises:
            libvirt.libvirtError: If the domain cannot be found.
        """
        try:
            self.domain = self.conn.lookupByName(name)
        except libvirt.libvirtError:
            return None
    
    def get_domain_by_uid(self, uid: str):
        """
        Returns a domain object by its UUID.
        
        Args:
            uid (str): The UUID of the domain.
        
        Raises:
            libvirt.libvirtError: If the domain cannot be found.
        """
        try:
            self.domain = self.conn.lookupByUUIDString(uid)
        except libvirt.libvirtError:
            return None

    def is_domain_active(self):
        """
        Checks if the domain is active.

        Returns:
            bool: True if the domain is active, False otherwise.
        """
        return self.domain.isActive()

    def get_domain_info(self):
        """
        Returns information about a specific domain.

        Args:
            name (str): The name of the domain.

        Returns:
            dict: A dictionary containing information about the domain.
        """
        domain_info = {}
        domain_info["name"] = self.domain.name()
        domain_info["id"] = self.domain.ID()
        domain_info["state"] = self.domain.state()
        domain_info["vcpus"] = self.domain.maxVcpus()
        domain_info["memory"] = self.domain.maxMemory()
        domain_info["autostart"] = self.domain.autostart()
        domain_info["uuid"] = self.domain.UUIDString()
        domain_info["xml"] = self.domain.XMLDesc()

    def start_domain(self):
        self.domain.create()

    def stop_domain(self):
        self.domain.destroy()
        self.domain.undefine()
        self.domain.free()