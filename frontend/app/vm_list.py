
"""
Récupère le logo de l'OS en fonction de l'information de l'OS
"""


def get_os_logo(os_info):
    BASE_URL = '/static/assets/os/'
    DEFAULT_LOGO = 'default.png'

    # Si l'information de l'OS est vide, on retourne le logo par défaut (default.png)
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

    # Retourne le logo correspondant à l'OS
    for os_name, os_logo in os_logo_mapping.items():
        if os_name in os_info_normalized:
            return BASE_URL + os_logo

    return BASE_URL + DEFAULT_LOGO
