from fastapi import FastAPI, Response
from pydantic import BaseModel

from controler.hypervisorHandler import hypervisor_information,hypervisor_hostname, hypervisor_memory_stats
from controler.domainsHandler import domain_list, domain_start, domain_stop, domain_force_stop, domain_delete, domain_create, domain_restart, domain_state, domain_information
from controler.poolsHandler import listing_volume_in_pool, valid_template

app = FastAPI()

# Example URI, adjust based on how you expose the socket
QEMU_URI = 'qemu:///system'

class DomainCreationForm(BaseModel):
    name: str
    template: str

##### HYPERVISOR ROUTES #####

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

@app.get("/api/hypervisor/memory_stats")
def api_hypervisor_memory_stats():
    """
    Returns the memory parameters of the hypervisor.
    
    Returns:
        dict: A dictionary containing the memory parameters of the hypervisor.
    """
    return hypervisor_memory_stats(QEMU_URI)

##### DOMAINS ROUTES #####

@app.get("/api/domains/list")
def api_domain_list():
    """
    Returns a list of all domains.
    
    Returns:
        dict: A dictionary containing all domains.
    """
    return domain_list(QEMU_URI)

@app.get("/api/domains/state/{domain_name}")
def api_domain_state(domain_name: str):
    """
    Returns the state of a domain.
    
    Args:
        domain_name (str): The name of the domain.
    
    Returns:
        dict: A dictionary containing the state of the domain.
    """
    return domain_state(QEMU_URI, domain_name)

@app.get("/api/domains/information/{domain_name}")
def api_domain_information(domain_name: str):
    """
    Returns information about a domain.
    
    Args:
        domain_name (str): The name of the domain.
    
    Returns:
        dict: A dictionary containing information about the domain.
    """
    return domain_information(QEMU_URI, domain_name)

@app.get("/api/domains/start/{domain_name}")
def api_domain_start(domain_name: str):
    """
    Starts a domain.
    
    Args:
        domain_name (str): The name of the domain to start.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_start(QEMU_URI, domain_name)

@app.get("/api/domains/stop/{domain_name}")
def api_domain_stop(domain_name: str):
    """
    Stops a domain.
    
    Args:
        domain_name (str): The name of the domain to stop.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_stop(QEMU_URI, domain_name)

@app.get("/api/domains/force_stop/{domain_name}")
def api_domains_force_stop(domain_name: str):
    """
    Stops a domain immediately.
    
    Args:
        domain_name (str): The name of the domain to stop.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_force_stop(QEMU_URI, domain_name)

@app.get("/api/domains/restart/{domain_name}")
def api_domain_restart(domain_name: str):
    """
    Restarts a domain.
    
    Args:
        domain_name (str): The name of the domain to restart.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_restart(QEMU_URI, domain_name)

@app.post("/api/domains/delete/{domain_name}")
def api_domain_delete(domain_name: str):
    """
    Deletes a domain.
    
    Args:
        domain_name (str): The name of the domain to delete.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_delete(QEMU_URI, domain_name)

@app.post("/api/domains/create")
def api_domain_create(vm_form: DomainCreationForm):
    """
    Creates a domain.
    
    Args:
        domain_name (str): The name of the domain to create.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return domain_create(QEMU_URI, vm_form.name, vm_form.template)

##### POOLS ROUTES #####

@app.get("/api/pools/list/{pool_name}")
def api_pools_list(pool_name: str):
    """
    Returns a list of all storage volumes.
    
    Args:
        pool_name (str): The name of the pool.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return listing_volume_in_pool(QEMU_URI, pool_name)

@app.get("/api/pools/valid_template/{template_name}")
def api_pools_valid_template(template_name: str):
    """
    Checks if a template exists in the template folder.
    
    Args:
        template_name (str): The name of the template disk image.
    
    Returns:
        dict: A dictionary containing the result of the operation.
    """
    return valid_template(QEMU_URI, template_name)