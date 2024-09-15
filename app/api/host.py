import libvirt
import sys
import xml.etree.ElementTree as ET
from .. import context_processors
from Virtuose.settings import QEMU_URI
from ..services import check_guest_agent_active


def list_host_info():
    try:
        conn = libvirt.open(QEMU_URI)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        exit(1)
    host_information = {}
    host_information["hostname"] = conn.getHostname()

    return host_information