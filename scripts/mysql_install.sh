#!/bin/bash

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Vérification des droits de superutilisateur
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Veuillez exécuter ce script en tant que superutilisateur (root).${NC}"
  exit 1
fi

# Vérification des commandes apt, python3, pip et python3.11-venv
for cmd in apt python3 pip; do
  if ! command -v $cmd &> /dev/null; then
    echo -e "${RED}La commande $cmd n'est pas installée. Veuillez l'installer avant de continuer.${NC}"
    exit 1
  fi
done

# Mise à jour des paquets et installation des dépendances
echo -e "${GREEN}Mise à jour des paquets et installation des dépendances...${NC}"
apt update
apt install -y python3-pip python3.11-venv libvirt-dev postgresql-client-16 postgresql-16 postgresql-doc-16

# Vérification de l'installation des dépendances
if [ $? -ne 0 ]; then
  echo -e "${RED}Échec de l'installation des dépendances.${NC}"
  exit 1
fi

# Vérification de la version du client PostgreSQL
echo -e "${GREEN}Version du client PostgreSQL :${NC}"
if ! psql -V; then
  echo -e "${RED}Erreur lors de la vérification de la version du client PostgreSQL.${NC}"
  exit 1
fi

# Autres configurations PostgreSQL et installations...
# (Le reste de votre script PostgreSQL)

echo -e "${GREEN}Installation et configuration de PostgreSQL terminées.${NC}"
