# Virtuose

Virtualisation made simple :)

## Installation

### Hypervisor

execute as **root** the ./install.sh at the root of Virtuose project directory to install and configure the hypervisor on the host machine. (only tested on ubuntu 24 atm)

```bash
chmod +x install.sh
sudo ./install.sh
```

### Backend / database / frontend


You need to have [docker](https://docs.docker.com/get-started/get-docker/) and [docker compose](https://docs.docker.com/compose/install/) installed in order to run the project. 

To start the docker compose, run the build.sh at the root of Virtuose project directory.

```bash
chmod +x build.sh
sudo ./build.sh
```

### Start the project

Be sure libvirtd is running on the host (hypervisor) :
```bash
systemctl status libvirtd
```
Run the build.sh to start backend/frontend/database :
```bash
sudo ./build.sh
```

**Frontend is accessible from http://localhost:8000**  
**Api is accessible from http://localhost:8080**