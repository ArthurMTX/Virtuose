#!/bin/bash

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # Pas de couleur

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
apt update && apt install -y python3-pip python3.11-venv libvirt-dev

# Vérification de l'installation des dépendances
if [ $? -ne 0 ]; then
  echo -e "${RED}Échec de l'installation des dépendances.${NC}"
  exit 1
fi

cd .. 

# Création de l'environnement virtuel Python
if [ ! -d "venv" ]; then
  echo -e "${GREEN}Création de l'environnement virtuel Python...${NC}"
  python3 -m venv venv

  if [ $? -ne 0 ]; then
    echo -e "${RED}Échec de la création de l'environnement virtuel.${NC}"
    exit 1
  fi
else
  echo -e "${GREEN}L'environnement virtuel Python existe déjà.${NC}"
fi

# Activation de l'environnement virtuel
echo -e "${GREEN}Activation de l'environnement virtuel...${NC}"
source venv/bin/activate

# Installation des paquets Python nécessaires
echo -e "${GREEN}Installation des paquets Python nécessaires...${NC}"
pip install django django-environ tailwind django_browser_reload psycopg django-werkzeug pyopenssl libvirt-python django-rest-swagger drf-spectacular

if [ $? -ne 0 ]; then
  echo -e "${RED}Échec de l'installation des paquets Python.${NC}"
  deactivate
  exit 1
fi

# Exécution des migrations Django
if [ -f "manage.py" ]; then
  echo -e "${GREEN}Exécution des migrations Django...${NC}"
  python3 manage.py makemigrations
  python3 manage.py migrate

  if [ $? -ne 0 ]; then
    echo -e "${RED}Échec des migrations Django.${NC}"
    deactivate
    exit 1
  fi
else
  echo -e "${RED}Le fichier manage.py n'a pas été trouvé. Assurez-vous que vous êtes dans le répertoire racine du projet Django.${NC}"
  deactivate
  exit 1
fi

echo -e "${GREEN}Configuration réussie !${NC}"
