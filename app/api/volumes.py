import libvirt
import sys
from .. import context_processors
from Virtuose.settings import QEMU_URI


def list_volume_info(pool_name: str):
    try:
        conn = libvirt.open(QEMU_URI)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        return None, e
    pool = conn.storagePoolLookupByName(pool_name)
    if pool is None:
        print(context_processors.FAILED_TO_GET_STORAGE_POOL, file=sys.stderr)
        return None, context_processors.FAILED_TO_GET_STORAGE_POOL

    stg_info = {}

    stgvols = pool.listVolumes()
    for stgvolName in stgvols:
        stg_vol_info = {"pool_name": pool_name}
        try:
            stgvol = pool.storageVolLookupByName(stgvolName)
            v_type, v_capa, v_alloc = stgvol.info()
            type_str = {
                0: context_processors.VOLUME_FILE,
                1: context_processors.VOLUME_BLOCK,
                2: context_processors.VOLUME_DIR,
                3: context_processors.VOLUME_NETWORK,
                4: context_processors.VOLUME_NETDIR,
            }.get(v_type, context_processors.UNKNOWN)
            stg_vol_info["vol_type"] = type_str
            stg_vol_info["vol_capacity"] = v_capa / (1024 ** 3)
            stg_vol_info["vol_allocation"] = v_alloc / (1024 ** 2)
        except libvirt.libvirtError as e:
            stg_vol_info["error"] = e
        stg_info[stgvolName] = stg_vol_info

    conn.close()
    return stg_info, None


def list_all_vol_info():
    try:
        conn = libvirt.open(QEMU_URI)
    except libvirt.libvirtError as e:
        print(repr(e), file=sys.stderr)
        return None, e
    pools = conn.listAllStoragePools(0)
    if pools is None:
        print(context_processors.NO_POOLS_STORAGE, file=sys.stderr)
        return None, context_processors.NO_POOLS_STORAGE
    volume_pool_info = {}
    for pool in pools:
        volume_pool_info[pool.name()] = list_volume_info(pool.name())
    return volume_pool_info, None
