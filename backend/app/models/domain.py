from app.models.conLibvirt import LibvirtHandler
from time import sleep


class Domains(LibvirtHandler):
    def __init__(self, uri: str):
        """
        Initializes a connection to the libvirt daemon.

        Args:
            domain_name (str): The name of the domain.
            uid (str): The UUID of the domain.

        Raises:
            libvirt.libvirtError: If the connection to the libvirt daemon fails or if the domain is not found.    
        """
        super().__init__(uri)
        self.domain = None
    
    def list_all(self) -> list:
        """
        Returns a list of all domains.

        Returns:
            list: A list containing all domains name.
        """
        domains = self.conn.listAllDomains(0)
        domain_list = list()
        for domain in domains:
            domain_list.append(domain.name())
        return domain_list

    def isDomainExist(self, domain_name: str) -> bool:
        """
        Checks if a domain exists.

        Returns:
            bool: True if the domain exists, False otherwise.
        """
        return domain_name in self.list_all()

    def start(self, domain_name: str) -> dict:
        """
        Starts a domain.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        super().initialize_domain_object(domain_name)
        if self.domain: 
            if self.domain.isActive() == 1:
                return {'status': 'error', 'message': 'Domain already running'}
            else:
                self.domain.create()
                sleep(2)
                if self.domain.isActive() == 1:
                    return {'status': 'success', 'message': 'Domain started successfully.'}
        else:
            return {'status': 'error', 'message': 'Domain not found.'}
    
    def stop(self, domain_name: str) -> dict:
        """
        Stops a domain.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        super().initialize_domain_object(domain_name)
        if self.domain:
            if self.domain.isActive() == 0:
                return {'status': 'error', 'message': 'Domain already stopped'}
            else:
                self.domain.shutdown()
                timeout = 30
                elapsed_time = 0
                interval = 2  # Vérifie toutes les 2 secondes

                while elapsed_time < timeout:
                    sleep(interval)
                    elapsed_time += interval
                    if self.domain.isActive() == 0:
                        return {'status': 'success', 'message': 'Domain stopped successfully.'}
            self.domain.destroy()
            return {'status': 'warning', 'message': 'Domain forced to stop (shutdown failed).'}
        else:
            return {'status': 'error', 'message': 'Domain not found.'}

    def force_stop(self, domain_name: str) -> dict:
        """
        Stops a domain immediately.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        super().initialize_domain_object(domain_name)
        if self.domain:
            if self.domain.isActive() == 0:
                return {'status': 'error', 'message': 'Domain already stopped'}
            else:
                self.domain.destroy()
                sleep(2)
                if self.domain.isActive() == 0:
                    return {'status': 'success', 'message': 'Domain stopped successfully.'}
        else:
            return {'status': 'error', 'message': 'Domain not found.'}
    
    def delete(self, domain_name: str) -> dict:
        """
        Deletes a domain.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        super().initialize_domain_object(domain_name)
        if self.domain:
            if self.domain.isActive() == 1:
                return {'status': 'error', 'message': 'Domain is running. Stop the domain before deleting it.'}
            else:
                self.domain.undefine()
                sleep(2)
                return {'status': 'success', 'message': 'Domain deleted successfully.'}
        else:
            return {'status': 'error', 'message': 'Domain not found.'}

    def create(self, domain_name: str) -> dict:
        """
        Creates a new domain.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        self.xml_config = f"""
                    <domain type='kvm'>
                    <name>{domain_name}</name>
                    <memory unit='MiB'>2048</memory>
                    <vcpu placement='static'>2</vcpu>
                    <os>
                        <type arch='x86_64' machine='pc'>hvm</type>
                        <boot dev='hd'/>
                    </os>
                    <devices>
                        <disk type='file' device='disk'>
                        <driver name='qemu' type='qcow2'/>
                        <source file='/opt/virtuose/storage/{domain_name}.qcow2'/>
                        <target dev='vda' bus='virtio'/>
                        <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
                        </disk>
                        <interface type='network'>
                        <mac address='52:54:00:6d:90:02'/>
                        <source network='virtuose-network'/>
                        <model type='virtio'/>
                        <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
                        </interface>
                        <graphics type='vnc' port='-1' autoport='yes'/>
                    </devices>
                    </domain>
                    """
        if self.isDomainExist(domain_name):
            return {'status': 'error', 'message': 'Domain already exists.'}
        else:
            self.domain = self.conn.defineXML(self.xml_config)
            sleep(2)
            self.domain.create()
            sleep(2)
            if self.domain.isActive() == 1:
                return {'status': 'success', 'message': 'Domain created successfully.'}
            else:
                return {'status': 'error', 'message': 'Failed to create domain.'}