from xml.etree import ElementTree


def get_os_logo(os_info):
    BASE_URL = '/static/assets/os/'
    DEFAULT_LOGO = 'default.png'

    if not os_info:
        return BASE_URL + DEFAULT_LOGO

    os_info_normalized = os_info.strip().lower()

    os_logo_mapping = {
        'ubuntu': 'ubuntu.png',
        'debian': 'debian.png',
        'arch linux': 'arch.png',
        'red hat': 'rhel.png',
        'rhel': 'rhel.png',
        'windows server': 'windows-server.png',
        'windows 10': 'windows-10.png',
        'fedora': 'fedora.png',
        'centos': 'centos.png',
        'macos': 'macos.png',
        'linux mint': 'mint.png',
        'kali linux': 'kali.png',
    }

    for os_name, os_logo in os_logo_mapping.items():
        if os_name in os_info_normalized:
            return BASE_URL + os_logo

    return BASE_URL + DEFAULT_LOGO


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
