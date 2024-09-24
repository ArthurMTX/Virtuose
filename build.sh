#!/bin/bash

echo "Shutdown services with Docker Compose..."

docker compose down

# Vérification de la réussite des builds
if [ $? -ne 0 ]; then
    echo "Error during docker compose down, Exiting."
    exit 1
fi

# Lancer les services avec Docker Compose
echo "Starting services with Docker Compose..."

docker compose up -d

# Vérification de la réussite de Docker Compose
if [ $? -ne 0 ]; then
    echo "Error during Docker Compose up. Exiting."
    exit 1
fi

echo "Docker images built and services started successfully."

echo "Adding public key to hypervisor..."

# Récupérer la clé publique depuis le conteneur fastapi
pub_key=$(docker exec virtuose-backend cat /root/.ssh/id_rsa.pub)
if [ $? -ne 0 ]; then
    echo "Error retrieving public key from virtuose-backend. Exiting."
    docker compose down
    echo "Services stopped."
    exit 1
fi

# Ajouter la clé publique au fichier authorized_keys dans le conteneur hypervisor
docker exec virtuose-hypervisor bash -c "echo '$pub_key' >> /root/.ssh/authorized_keys"
if [ $? -ne 0 ]; then
    echo "Error adding public key to virtuose-hypervisor. Exiting."
    docker compose down
    echo "Services stopped."
    exit 1
fi

docker exec virtuose-hypervisor bash -c "chmod 600 /root/.ssh/authorized_keys"
if [ $? -ne 0 ]; then
    echo "Error setting permissions on authorized_keys in virtuose-hypervisor. Exiting."
    docker compose down
    echo "Services stopped."
    exit 1
fi

echo "Public key added to hypervisor successfully."
