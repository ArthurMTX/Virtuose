from xml.etree import ElementTree


def get_os_logo(os_info):
    # https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/ICONS.md
    base_url = 'https://cdn.jsdelivr.net/gh/walkxcode/dashboard-icons/png/'

    os_logo_mapping = {
        'Ubuntu': 'ubuntu.png',
        'Debian': 'debian.png',
        'Arch Linux': 'arch.png',
        'Windows Server 2019': 'windows-10.png',
        'Fedora': 'fedora.png',
        'CentOS': 'centos.png',
    }

    for os_name, os_logo in os_logo_mapping.items():
        if os_name in os_info:
            return base_url + os_logo
    return base_url + 'vm.png'


class VMList:
    def __init__(self, xml_file_path):
        self.vms = []

        tree = ElementTree.parse(xml_file_path)
        root = tree.getroot()

        for domain in root.findall('domain'):
            vm_data = {
                'name': domain.find('name').text,
                'memory': domain.find('memory').text,
                'vcpu': domain.find('vcpu').text,
                'os_info': domain.find('metadata/os_info').text,
                'os_logo': get_os_logo(domain.find('metadata/os_info').text),
            }
            self.vms.append(vm_data)

    def get_vms(self):
        return self.vms
