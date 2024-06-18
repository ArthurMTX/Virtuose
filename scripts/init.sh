#!/bin/bash

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Fonction pour exécuter un script et vérifier son succès
execute_script() {
  local script=$1

  if [ -f "$script" ]; then
    echo -e "${GREEN}Exécution de $script...${NC}"
    if bash "$script"; then
      echo -e "${GREEN}$script terminé avec succès.${NC}"
    else
      echo -e "${RED}Erreur lors de l'exécution de $script.${NC}"
      exit 1
    fi
  else
    echo -e "${RED}Le script $script n'existe pas.${NC}"
    exit 1
  fi
}

# Exécution des scripts
execute_script "mysql_install.sh"
execute_script "init_django.sh"

echo -e "${GREEN}Tous les scripts ont été exécutés avec succès.${NC}"
