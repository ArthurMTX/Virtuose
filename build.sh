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

docker compose up -d --build

# Vérification de la réussite de Docker Compose
if [ $? -ne 0 ]; then
    echo "Error during Docker Compose up. Exiting."
    exit 1
fi

echo "Docker images built and services started successfully."