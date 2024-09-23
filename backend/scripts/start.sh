#!/bin/bash

# Ajouter l'hôte hypervisor au fichier known_hosts
ssh-keyscan -H virtuose-hypervisor >> /root/.ssh/known_hosts

# Lancer l'application FastAPI
uvicorn main:app --host 0.0.0.0
