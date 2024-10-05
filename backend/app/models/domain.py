from app.models.conLibvirt import LibvirtHandler
import xml.etree.ElementTree as ET
from time import sleep
import libvirt


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
        self.namespaces = {'libosinfo': 'http://libosinfo.org/xmlns/libvirt/domain/1.0'}
        self.domain_state = {
            0: 'No state',
            1: 'Running',
            2: 'Blocked',
            3: 'Paused',
            4: 'Shutdown',
            5: 'Shutoff',
            6: 'Crashed',
            7: 'Suspended',
        }
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
    
    def state(self, domain_name: str) -> dict:
        """
        Returns the state of a domain.

        Returns:
            dict: A dictionary containing the state of the domain.
        """
        super().initialize_domain_object(domain_name)
        if self.domain:
            state = self.domain.state()[0]
            return {'status': 'success', 'message': self.domain_state.get(state, 'Unknown')}
        else:
            return {'status': 'error', 'message': 'Domain not found.'}

    def IP(self, domain_name: str) -> dict:
        """
        Returns the IP of a domain.

        Returns:
            dict: A dictionary containing the IP of the domain.
        """
        super().initialize_domain_object(domain_name)
        if self.domain and self.state(domain_name)["message"] == 'Running':
            ipv4_addresses = dict()
            ifaces = self.domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
            for iface_name, iface_info in ifaces.items():
                for addr_info in iface_info['addrs']:
                    if addr_info['type'] == 0:  # IPv4
                        ipv4_addresses[iface_name] = addr_info['addr']
            return {'status': 'success', 'message': ipv4_addresses}
        else:
            if not self.domain:
                return {'status': 'error', 'message': 'Domain not found.'}            
            elif self.state(domain_name)["message"] == 'Paused':
                return {'status': 'warning', 'message': 'Domain is paused.'}
            elif self.domain.isActive() == 0:
                return {'status': 'warning', 'message': 'Domain not running.'}
            else:
                return {'status': 'error', 'message': 'Failed to retrieve IP information.'}

    
    def information(self, domain_name: str) -> dict:
        """
        Returns information about a domain.

        Returns:
            dict: A dictionary containing information about the domain.
        """
        super().initialize_domain_object(domain_name)
        if self.domain:
            return {
                'status': 'success',
                'name': self.domain.name(),
                'state': self.domain_state.get(self.domain.state()[0], 'Unknown'),
                'vcpus': self.domain.vcpusFlags(),
                'memory': int(self.domain.maxMemory() / 1024),
                'graphics': self.graphics(domain_name)["message"],
                'interfaces': self.IP(domain_name)["message"]
            }
        else:
            return {'status': 'error', 'message': 'Domain not found.'}

    def graphics(self, domain_name: str) -> dict:
        """
        Returns the graphics of a domain.

        Returns:
            dict: A dictionary containing the graphics of the domain.
        """
        super().initialize_domain_object(domain_name)
        if self.domain and self.domain.isActive() == 1:
            graphics_information = dict()
            root = ET.fromstring(self.domain.XMLDesc())
            for graphics in root.findall('devices/graphics'):
                graphics_info = dict()
                graphics_info["listen"] = graphics.attrib.get('listen', 'unknow')
                graphics_info["port"] = graphics.attrib.get('port', 'unknow')
                graphics_information[graphics.attrib.get('type')] = graphics_info
            return {'status': 'succes', 'message': graphics_information}
        else:
            if self.domain.isActive() == 0:
                return {'status': 'error', 'message': 'Domain not running.'}
            elif not self.domain:
                return {'status': 'error', 'message': 'Domain not found'}
            else:
                return {'status': 'error', 'message': 'Failed to retrieve graphics information.'}

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
    
    def restart(self, domain_name: str) -> dict:
        """
        Restarts a domain.

        Returns:
            dict: A dictionary containing the result of the operation.
        """
        super().initialize_domain_object(domain_name)
        if self.domain:
            if self.domain.isActive() == 1:
                self.domain.reboot(1)
                sleep(2)
                if self.domain.isActive() == 1:
                    return {'status': 'success', 'message': 'Domain restarted successfully.'}
            else:
                return {'status': 'error', 'message': 'Domain is not running.'}
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
                    <on_poweroff>destroy</on_poweroff>
                    <on_reboot>restart</on_reboot>
                    <on_crash>restart</on_crash>
                    <devices>
                        <disk type='file' device='disk'>
                        <driver name='qemu' type='qcow2'/>
                        <source file='/opt/virtuose/storage/{domain_name}.qcow2'/>
                        <target dev='vda' bus='virtio'/>
                        <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
                        </disk>
                        <interface type='network'>
                        <source network='virtuose-network'/>
                        <model type='virtio'/>
                        <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
                        </interface>
                        <graphics type='vnc' port='-1' autoport='yes'/>
                        <channel type='unix'>
                        <source mode='bind' path='/var/lib/libvirt/qemu/f16x86_64.agent'/>
                        <target type='virtio' name='org.qemu.guest_agent.0'/>
                        </channel>
                    </devices>
                    <features>
                        <pae/>
                        <acpi/>
                    </features> 
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