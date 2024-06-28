import libvirt
import sys
import xml.etree.ElementTree as ET
import subprocess
from .. import context_processors
from Virtuose.settings import QEMU_URI
from ..services import check_guest_agent_active


def is_domain_active(dom_name: str):
    try:
        conn = libvirt.open(QEMU_URI)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)
    try:
        dom = conn.lookupByName(dom_name)
        if dom is None:
            print(f"{context_processors.DOMAIN_NOT_FOUND} : {dom_name}")
            return False
        return dom.isActive() == 1
    finally:
        conn.close()


def list_all_domain():
    try:
        conn = libvirt.open(QEMU_URI)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)
    try:
        domainNames = conn.listDefinedDomains()
        if domainNames is None:
            print(context_processors.FAILED_TO_GET_DOMAIN_NAMES, file=sys.stderr)
            return None, context_processors.FAILED_TO_GET_DOMAIN_NAMES

        domainIDs = conn.listDomainsID()
        if domainIDs is None:
            print(context_processors.FAILED_TO_GET_DOMAIN_IDS, file=sys.stderr)
            return None, context_processors.FAILED_TO_GET_DOMAIN_IDS

        for domainID in domainIDs:
            domain = conn.lookupByID(domainID)
            domainNames.append(domain.name())

        return domainNames, None
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        return None, e
    finally:
        conn.close()


def list_dom_info_name(dom_name: str):
    dom_info = {}
    try:
        conn = libvirt.open(QEMU_URI)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)
    try:
        dom = conn.lookupByName(dom_name)
        if dom is None:
            print(f"{context_processors.DOMAIN_NOT_FOUND} : {dom_name}")
            return None, context_processors.DOMAIN_NOT_FOUND

        dom_info["name"] = dom_name
        dom_info["ID"] = dom.ID()
        dom_info["UUID"] = dom.UUIDString()

        # Information sur la RAM / VCPU
        state, max_mem, mem, num_cpu, cpu_time = dom.info()
        state_str = {
            0: context_processors.VM_NO_STATE,
            1: context_processors.VM_STATE_RUNNING,
            2: context_processors.VM_STATE_BLOCKED,
            3: context_processors.VM_STATE_PAUSED,
            4: context_processors.VM_STATE_SHUTDOWN,
            5: context_processors.VM_STATE_SHUTOFF,
            6: context_processors.VM_STATE_CRASHED,
            7: context_processors.VM_STATE_PMSUSPENDED
        }.get(state, context_processors.UNKNOWN)
        dom_info["state"] = state_str
        dom_info["memory_gb"] = mem / (1024 ** 2)
        dom_info["VCPU"] = num_cpu

        if dom_info['state'] == 'running' and not check_guest_agent_active(dom_info['UUID']):
            dom_info['state'] = 'starting'

        # Informations sur l'OS
        xml_desc = dom.XMLDesc()
        root = ET.fromstring(xml_desc)

        # Information sur le l'architecture de l'OS
        os_arch = root.find('os/type').attrib.get('arch', context_processors.UNKNOWN)
        dom_info["os_arch"] = os_arch

        # Espace de noms pour libosinfo
        namespaces = {'libosinfo': 'http://libosinfo.org/xmlns/libvirt/domain/1.0'}

        # Récupérer l'élément libosinfo:os
        libosinfo_os = root.find('metadata/libosinfo:libosinfo/libosinfo:os', namespaces)
        if libosinfo_os is not None:
            dom_info["libosinfo_os_id"] = libosinfo_os.attrib.get('id', context_processors.UNKNOWN)
            dom_info["os"] = dom_info["libosinfo_os_id"].split('/')[-2].lower()

        for graphics in root.findall('devices/graphics'):
            graphics_info = {}
            graphics_info["listen"] = graphics.attrib.get('listen', 'unknow')
            graphics_info["port"] = graphics.attrib.get('port', 'unknow')
            dom_info[graphics.attrib.get('type')] = graphics_info


        if state == 1:
            try:
                ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
                ips = []
                for iface in ifaces.values():
                    if iface['addrs']:
                        for addr in iface['addrs']:
                            if addr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                                ips.append(addr['addr'])
                dom_info["IPs"] = ips
            except libvirt.libvirtError:
                print(f"Failed to get IPs for {dom_name}")
                dom_info["IPs"] = []

        # Récupérer les volumes associés
        volumes = []
        disks = root.findall('devices/disk')
        for disk in disks:
            source = disk.find('source')
            if source is not None and 'file' in source.attrib:
                volumes.append(source.attrib['file'])
            elif source is not None and 'dev' in source.attrib:
                volumes.append(source.attrib['dev'])
            elif source is not None and 'volume' in source.attrib:
                volumes.append(source.attrib['volume'])
        dom_info["volumes"] = volumes
        return dom_info, None
    finally:
        conn.close()


def list_dom_info_uuid(dom_uuid: str):
    dom_info = {}
    try:
        conn = libvirt.open(QEMU_URI)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)
    try:
        dom = conn.lookupByUUIDString(dom_uuid)
        if dom is None:
            print(f"{context_processors.DOMAIN_NOT_FOUND} : {dom_uuid}")
            return None, context_processors.DOMAIN_NOT_FOUND

        dom_info["name"] = dom.name()
        dom_info["ID"] = dom.ID()
        dom_info["UUID"] = dom.UUIDString()

        state, max_mem, mem, num_cpu, cpu_time = dom.info()
        state_str = {
            0: context_processors.VM_NO_STATE,
            1: context_processors.VM_STATE_RUNNING,
            2: context_processors.VM_STATE_BLOCKED,
            3: context_processors.VM_STATE_PAUSED,
            4: context_processors.VM_STATE_SHUTDOWN,
            5: context_processors.VM_STATE_SHUTOFF,
            6: context_processors.VM_STATE_CRASHED,
            7: context_processors.VM_STATE_PMSUSPENDED
        }.get(state, context_processors.UNKNOWN)
        dom_info["state"] = state_str
        dom_info["memory_gb"] = mem / (1024 ** 2)
        dom_info["VCPU"] = num_cpu

        if dom_info['state'] == 'running' and not check_guest_agent_active(dom_info['UUID']):
            dom_info['state'] = 'starting'

        xml_desc = dom.XMLDesc()
        root = ET.fromstring(xml_desc)

        os_arch = root.find('os/type').attrib.get('arch', context_processors.UNKNOWN)
        dom_info["os_arch"] = os_arch

        for graphics in root.findall('devices/graphics'):
            graphics_info = {}
            graphics_info["listen"] = graphics.attrib.get('listen', 'unknow')
            graphics_info["port"] = graphics.attrib.get('port', 'unknow')
            dom_info[graphics.attrib.get('type')] = graphics_info

        namespaces = {'libosinfo': 'http://libosinfo.org/xmlns/libvirt/domain/1.0'}

        libosinfo_os = root.find('metadata/libosinfo:libosinfo/libosinfo:os', namespaces)
        if libosinfo_os is not None:
            dom_info["libosinfo_os_id"] = libosinfo_os.attrib.get('id', context_processors.UNKNOWN)

        if state == 1:
            try:
                ifaces = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
                ips = []
                for iface in ifaces.values():
                    if iface['addrs']:
                        for addr in iface['addrs']:
                            if addr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
                                ips.append(addr['addr'])
                dom_info["IPs"] = ips
            except libvirt.libvirtError:
                print(f"Failed to get IPs for {dom_uuid}")
                dom_info["IPs"] = []

        volumes = []
        disks = root.findall('devices/disk')
        for disk in disks:
            source = disk.find('source')
            if source is not None and 'file' in source.attrib:
                volumes.append(source.attrib['file'])
            elif source is not None and 'dev' in source.attrib:
                volumes.append(source.attrib['dev'])
            elif source is not None and 'volume' in source.attrib:
                volumes.append(source.attrib['volume'])
        dom_info["volumes"] = volumes
        return dom_info, None
    finally:
        conn.close()

        
def clone_volume_from_template(template_name: str,volume_name: str):
    command = ["quemu-img", "create", "-f", "qcow2", "-F", "qcow2", "-b", f"{template_name}.qcow2", f"{volume_name}.qcow2"]
    try:
        result = subprocess.run(command,check=True)
        return 0, None
    except subprocess.CalledProcessError as e:
        # Affichage de la sortie d'erreur en cas d'échec
        return None, e.stderr

def create_domain(domain_name: str,template_name: str):
    if context_processors.DOMAIN_TEMPLATE.get(template_name,None) is not None:
        template_volume_name = context_processors.DOMAIN_TEMPLATE[template_name]    
    else:
        return None, f"no template existing with name : {template_name}"
    try:
        clone_volume_from_template(template_volume_name,domain_name)
    except:
        return None, f"error cloning template : {template_volume_name}"
    command = [
        "virt-install", \
        "--virt-type=kvm", \
        f"--name={domain_name}", \
        "--ram", "2048", \
        "--vcpus=2", \
        "--virt-type=kvm", \
        "--hvm", \
        "--network network=default", \
        "--graphics", "vnc", \
        "--disk", f"{context_processors.TEMPLATE_PATH_POOL}{domain_name}.qcow2", \
        "--boot=hd", \
        "--noautoconsole"
    ]
    try:
        result = subprocess.run(command,check=True)
        return result, None
    except subprocess.CalledProcessError as e:
        return None, e.stderr
    