#!/bin/bash

# Arrêter tous les conteneurs en cours d'exécution
echo "Arrêt de tous les conteneurs..."
docker stop $(docker ps -aq)

# Supprimer tous les conteneurs
echo "Suppression de tous les conteneurs..."
docker rm $(docker ps -aq)

# Supprimer toutes les images Docker
echo "Suppression de toutes les images Docker..."
docker rmi -f $(docker images -q)

# (Optionnel) Supprimer tous les volumes (si vous voulez également nettoyer les volumes)
# echo "Suppression de tous les volumes Docker..."
# docker volume rm $(docker volume ls -q)

# Supprimer les réseaux Docker (optionnel)
# echo "Suppression de tous les réseaux Docker..."
# docker network prune -f


