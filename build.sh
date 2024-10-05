#!/bin/bash

echo "Shutdown services with Docker Compose..."
docker compose down

# Vérification de la réussite du Docker Compose down
if [ $? -ne 0 ]; then
    echo "Error during docker compose down, Exiting."
    exit 1
fi

echo "Building and starting services with Docker Compose..."
docker compose up -d --build

# Vérification de la réussite du Docker Compose up
if [ $? -ne 0 ]; then
    echo "Error during Docker Compose up. Exiting."
    exit 1
fi

echo "Docker services built and started successfully."
