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
    echo -e "${RED}La commande $cmd n'est pas installée.${NC}"
    apt install -y $cmd
  fi
done

# Mise à jour des paquets et installation des dépendances
echo -e "${GREEN}Mise à jour des paquets et installation des dépendances...${NC}"
apt update
apt install python3-pip python3-venv libvirt-dev postgresql-client-16 postgresql-16 postgresql-doc-16 -y

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
# Générer un mot de passe sécurisé de 12 caractères
PASSWORD=$(openssl rand -base64 12)
PASSWORD_FILE="postgres_password.txt"

# Stocker le mot de passe dans un fichier
echo "PostgreSQL password: $PASSWORD" > $PASSWORD_FILE

# Imprimer le mot de passe à l'utilisateur
echo -e "${GREEN}Le mot de passe PostgreSQL généré a été stocké dans $PASSWORD_FILE${NC}"

# Vérification des droits de superutilisateur
if [ "$EUID" -ne 0 ]; then
  echo "Veuillez exécuter ce script en tant que superutilisateur (root)."
  exit 1
fi

# Ajouter le dépôt apt PostgreSQL à sources.list.d/pgdg.list
echo -e "${GREEN}Ajout du dépôt PostgreSQL à sources.list.d/pgdg.list${NC}"
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Ajouter la clé apt PostgreSQL
echo -e "${GREEN}Ajout de la clé apt PostgreSQL${NC}"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

# Mise à jour des paquets et installation de PostgreSQL
echo -e "${GREEN}Mise à jour des paquets et installation de PostgreSQL${NC}"
apt update
apt install postgresql-client-16 postgresql-16 postgresql-doc-16 -y

# Vérification de la version du client PostgreSQL
echo -e "${GREEN}Version du client PostgreSQL :${NC}"
psql -V

# Configuration PostgreSQL
echo -e "${GREEN}Configuration de PostgreSQL${NC}"
sudo -i -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$PASSWORD';"
sudo -i -u postgres psql -c "CREATE DATABASE postgres;"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;"

# Mise à jour de pg_hba.conf
PG_HBA_CONF="/etc/postgresql/16/main/pg_hba.conf"
if grep -q "host    all             all             127.0.0.1/32            md5" "$PG_HBA_CONF"; then
  echo -e "${GREEN}La configuration pg_hba.conf est déjà mise à jour.${NC}"
else
  echo "host    all             all             127.0.0.1/32            md5" >> "$PG_HBA_CONF"
  echo -e "${GREEN}Configuration de pg_hba.conf mise à jour.${NC}"
fi

# Mise à jour de postgresql.conf
PG_CONF="/etc/postgresql/16/main/postgresql.conf"
if grep -q "listen_addresses = 'localhost'" "$PG_CONF"; then
  echo -e "${GREEN}listen_addresses est déjà configuré.${NC}"
else
  echo "listen_addresses = 'localhost'" >> "$PG_CONF"
  echo -e "${GREEN}listen_addresses configuré.${NC}"
fi

if grep -q "port = 5432" "$PG_CONF"; then
  echo -e "${GREEN}port est déjà configuré.${NC}"
else
  echo "port = 5432" >> "$PG_CONF"
  echo -e "${GREEN}port configuré.${NC}"
fi

# Redémarrage de PostgreSQL
echo -e "${GREEN}Redémarrage de PostgreSQL${NC}"
systemctl restart postgresql

# Vérification du statut de PostgreSQL
echo -e "${GREEN}Statut de PostgreSQL :${NC}"
systemctl status postgresql

# Connexion à PostgreSQL pour vérifier l'installation
echo -e "${GREEN}Connexion à PostgreSQL pour vérifier l'installation${NC}"
sudo -i -u postgres PGPASSWORD="$PASSWORD" psql -h localhost -U postgres -d postgres -c "\conninfo"

echo -e "${GREEN}Installation et configuration de PostgreSQL terminées.${NC}"

# Création du fichier .env
ENV_FILE="../.env"
echo "SECRET_KEY=django-insecure-$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)" > $ENV_FILE
echo "DB_NAME=postgres" >> $ENV_FILE
echo "DB_USER=postgres" >> $ENV_FILE
echo "DB_PASSWORD=$PASSWORD" >> $ENV_FILE
echo "DB_HOST=localhost" >> $ENV_FILE
echo "DB_PORT=5432" >> $ENV_FILE

echo -e "${GREEN}Fichier .env créé avec succès :${NC}"
cat $ENV_FILE

echo -e "${GREEN}Installation et configuration de PostgreSQL terminées.${NC}"
