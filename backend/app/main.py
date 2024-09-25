from fastapi import FastAPI, Response

from controler.hypervisorHandler import hypervisor_information,hypervisor_hostname
from controler.domainsHandler import domain_list

app = FastAPI()

# Example URI, adjust based on how you expose the socket
QEMU_URI = 'qemu+ssh://virtuose-hypervisor/system'

@app.get("/api/hypervisor/resume")
def api_hypervisor_resume():
    """
    Returns information about the hypervisor.
    
    Returns:
        dict: A dictionary containing information about the hypervisor.
    """
    return hypervisor_information(QEMU_URI)

@app.get("/api/hypervisor/hostname")
def api_hypervisor_hostname():
    """
    Returns the hostname of the hypervisor.
    
    Returns:
        dict: A dictionary containing the hostname of the hypervisor.
    """
    return hypervisor_hostname(QEMU_URI)

@app.get("/api/domains/list")
def api_domain_list():
    """
    Returns a list of all domains.
    
    Returns:
        dict: A dictionary containing all domains.
    """
    return domain_list(QEMU_URI)