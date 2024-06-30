import libvirt
import sys
from .. import context_processors
from Virtuose.settings import QEMU_URI


def list_all_pools():
    pools_list = []
    try:
        conn = libvirt.open(QEMU_URI)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        return None, str(e)

    pools = conn.listAllStoragePools(0)
    if pools is None:
        print(context_processors.NO_POOLS_STORAGE, file=sys.stderr)
        return None, context_processors.NO_POOLS_STORAGE

    for pool in pools:
        pools_list.append(pool.name())

    conn.close()

    return pools_list, None
