#!/bin/bash

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Générer un mot de passe sécurisé de 12 caractères
PASSWORD=$(openssl rand -base64 12)
PASSWORD_FILE="postgres_password.txt"

# Stocker le mot de passe dans un fichier
echo "PostgreSQL password: $PASSWORD" > $PASSWORD_FILE

# Imprimer le mot de passe à l'utilisateur
echo -e "${GREEN}Le mot de passe PostgreSQL généré a été stocké dans $PASSWORD_FILE${NC}"

# Vérification des droits de superutilisateur
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Veuillez exécuter ce script en tant que superutilisateur (root).${NC}"
  exit 1
fi

# Ajouter le dépôt apt PostgreSQL à sources.list.d/pgdg.list
echo -e "${GREEN}Ajout du dépôt PostgreSQL à sources.list.d/pgdg.list${NC}"
if ! sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'; then
  echo -e "${RED}Erreur lors de l'ajout du dépôt PostgreSQL.${NC}"
  exit 1
fi

# Ajouter la clé apt PostgreSQL
echo -e "${GREEN}Ajout de la clé apt PostgreSQL${NC}"
if ! wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -; then
  echo -e "${RED}Erreur lors de l'ajout de la clé apt PostgreSQL.${NC}"
  exit 1
fi

# Mise à jour des paquets et installation de PostgreSQL
echo -e "${GREEN}Mise à jour des paquets et installation de PostgreSQL${NC}"
if ! apt update && apt install postgresql-client-16 postgresql-16 postgresql-doc-16 -y; then
  echo -e "${RED}Erreur lors de la mise à jour des paquets ou de l'installation de PostgreSQL.${NC}"
  exit 1
fi

# Vérification de la version du client PostgreSQL
echo -e "${GREEN}Version du client PostgreSQL :${NC}"
if ! psql -V; then
  echo -e "${RED}Erreur lors de la vérification de la version du client PostgreSQL.${NC}"
  exit 1
fi

# Configuration PostgreSQL
echo -e "${GREEN}Configuration de PostgreSQL${NC}"
if ! sudo -i -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$PASSWORD'"; then
  echo -e "${RED}Erreur lors de la configuration du mot de passe PostgreSQL.${NC}"
  exit 1
fi

if ! sudo -i -u postgres psql -c "CREATE DATABASE postgres"; then
  echo -e "${RED}Erreur lors de la création de la base de données PostgreSQL.${NC}"
  exit 1
fi

if ! sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres"; then
  echo -e "${RED}Erreur lors de l'attribution des privilèges sur la base de données PostgreSQL.${NC}"
  exit 1
fi

# Mise à jour de pg_hba.conf
PG_HBA_CONF="/etc/postgresql/16/main/pg_hba.conf"
if grep -q "host    all             all             127.0.0.1/32            md5" "$PG_HBA_CONF"; then
  echo -e "${GREEN}La configuration pg_hba.conf est déjà mise à jour.${NC}"
else
  if ! echo "host    all             all             127.0.0.1/32            md5" >> "$PG_HBA_CONF"; then
    echo -e "${RED}Erreur lors de la mise à jour de pg_hba.conf.${NC}"
    exit 1
  fi
  echo -e "${GREEN}Configuration de pg_hba.conf mise à jour.${NC}"
fi

# Mise à jour de postgresql.conf
PG_CONF="/etc/postgresql/16/main/postgresql.conf"
if grep -q "listen_addresses = 'localhost'" "$PG_CONF"; then
  echo -e "${GREEN}listen_addresses est déjà configuré.${NC}"
else
  if ! echo "listen_addresses = 'localhost'" >> "$PG_CONF"; then
    echo -e "${RED}Erreur lors de la configuration de listen_addresses.${NC}"
    exit 1
  fi
  echo -e "${GREEN}listen_addresses configuré.${NC}"
fi

if grep -q "port = 5432" "$PG_CONF"; then
  echo -e "${GREEN}port est déjà configuré.${NC}"
else
  if ! echo "port = 5432" >> "$PG_CONF"; then
    echo -e "${RED}Erreur lors de la configuration du port.${NC}"
    exit 1
  fi
  echo -e "${GREEN}port configuré.${NC}"
fi

# Redémarrage de PostgreSQL
echo -e "${GREEN}Redémarrage de PostgreSQL${NC}"
if ! systemctl restart postgresql; then
  echo -e "${RED}Erreur lors du redémarrage de PostgreSQL.${NC}"
  exit 1
fi

# Vérification du statut de PostgreSQL
echo -e "${GREEN}Statut de PostgreSQL :${NC}"
if ! systemctl status postgresql; then
  echo -e "${RED}Erreur lors de la vérification du statut de PostgreSQL.${NC}"
  exit 1
fi

# Connexion à PostgreSQL pour vérifier l'installation
echo -e "${GREEN}Connexion à PostgreSQL pour vérifier l'installation${NC}"
if ! sudo -i -u postgres PGPASSWORD="$PASSWORD" psql -h localhost -U postgres -d postgres -c "\conninfo"; then
  echo -e "${RED}Erreur lors de la connexion à PostgreSQL.${NC}"
  exit 1
fi

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

# Connexion automatique à PostgreSQL
echo -e "${GREEN}Connexion automatique à PostgreSQL :${NC}"
if ! sudo -i -u postgres PGPASSWORD="$PASSWORD" psql -h localhost -U postgres -d postgres -c "\q"; then
  echo -e "${RED}Erreur lors de la connexion automatique à PostgreSQL.${NC}"
  exit 1
fi
