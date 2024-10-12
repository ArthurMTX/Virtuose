from fastapi import FastAPI

from routes import domains
from routes import hypervisor
from routes import pools
from routes import volumes

app = FastAPI()

app.include_router(domains.router)
app.include_router(hypervisor.router)
app.include_router(pools.router)
app.include_router(volumes.router)

@app.get("/")
def welcome():
    return {"message": "Welcome to the QEMU API!"}