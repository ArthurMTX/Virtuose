#!/bin/bash

./clean_docker_and_up.sh

# Nom des images
IMAGE_NAME_QEMU="virtuose-hypervisor"
IMAGE_NAME_FASTAPI="virtuose-backend"

# Chemins des Dockerfiles
DOCKERFILE_QEMU_PATH="./hypervisor/dockerfile"
DOCKERFILE_FASTAPI_PATH="./backend/dockerfile"

# Constructions des images
echo "Building Docker images..."

docker build -t $IMAGE_NAME_QEMU -f $DOCKERFILE_QEMU_PATH .
docker build -t $IMAGE_NAME_FASTAPI -f $DOCKERFILE_FASTAPI_PATH .

# Vérification de la réussite des builds
if [ $? -ne 0 ]; then
    echo "Error during Docker build. Exiting."
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
    exit 1
fi

# Ajouter la clé publique au fichier authorized_keys dans le conteneur hypervisor
docker exec virtuose-hypervisor bash -c "echo '$pub_key' >> /root/.ssh/authorized_keys"
if [ $? -ne 0 ]; then
    echo "Error adding public key to virtuose-hypervisor. Exiting."
    exit 1
fi

docker exec virtuose-hypervisor bash -c "chmod 600 /root/.ssh/authorized_keys"
if [ $? -ne 0 ]; then
    echo "Error setting permissions on authorized_keys in virtuose-hypervisor. Exiting."
    exit 1
fi

echo "Public key added to hypervisor successfully."
