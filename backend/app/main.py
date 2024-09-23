from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import libvirt
import json

from models.conLibvirt import LibvirtHandler

app = FastAPI()

# Example URI, adjust based on how you expose the socket
QEMU_URI = 'qemu+ssh://virtuose-hypervisor/system'

@app.get("/info")
def get_info():
    """
    Returns information about the hypervisor.
    
    Returns:
        dict: A dictionary containing information about the hypervisor.
    """
    conn = LibvirtHandler(QEMU_URI)
    return conn.host_information()

