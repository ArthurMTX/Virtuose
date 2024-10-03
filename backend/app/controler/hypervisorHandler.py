import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.models.hypervisor import Hypervisor

def hypervisor_information(QEMU_URI: str) -> dict:
    """
    Returns information about the hypervisor.

    Returns:
        dict: A dictionary containing information about the hypervisor.
    """
    returned_dict = dict()
    hypervisor = Hypervisor(QEMU_URI)
    general_informations = hypervisor.general_information()
    returned_dict['hostname'] = hypervisor.hostname()
    returned_dict['libvirt_version'] = hypervisor.libvirt_version()
    returned_dict['uri'] = hypervisor.uri()
    returned_dict['cpu_model'] = general_informations[0]
    returned_dict['total_memory_size'] = general_informations[1]
    returned_dict['number_of_cpus'] = general_informations[2]
    returned_dict['cpu_mhz'] = general_informations[3]
    returned_dict['number_of_nodes'] = general_informations[4]
    returned_dict['number_of_sockets'] = general_informations[5]
    returned_dict['number_of_cores_per_socket'] = general_informations[6]
    returned_dict['number_of_threads_per_core'] = general_informations[7]
    returned_dict['max_vcpus'] = hypervisor.max_vcpus()
    hypervisor.close()
    
    return returned_dict

def hypervisor_libvirt_version(QEMU_URI: str) -> dict:
    """
    Returns the version of the libvirt daemon.

    Returns:
        dict: A dictionary containing the version of the libvirt daemon.
    """
    version = dict()
    hypervisor = Hypervisor(QEMU_URI)
    version["libvirt_version"] = hypervisor.libvirt_version()
    hypervisor.close()
    return version

def hypervisor_hostname(QEMU_URI: str) -> dict:
    """
    Returns the hostname of the hypervisor.

    Returns:
        dict: A dictionary containing the hostname of the hypervisor.
    """
    hostname = dict()
    hypervisor = Hypervisor(QEMU_URI)
    hostname["hostname"] = hypervisor.hostname()
    hypervisor.close()
    return hostname

def hypervisor_memory_stats(QEMU_URI: str) -> dict:
    """
    Returns the memory parameters of the hypervisor.
    
    Returns:
        dict: A dictionary containing the memory parameters of the hypervisor.
    """
    hypervisor = Hypervisor(QEMU_URI)
    mem_stats = hypervisor.memory_stats()
    for k, v in mem_stats.items():
        mem_stats[k] = int(v/1024)
    mem_stats["available"] = mem_stats["free"] + mem_stats["cached"]
    hypervisor.close()
    return mem_stats