#!/bin/bash

# Couleurs pour les messages
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Fichier de log
LOG_FILE="installation.log"

# Vérification des droits de superutilisateur
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Veuillez exécuter ce script en tant que superutilisateur (root).${NC}" | tee -a "$LOG_FILE"
  exit 1
fi

# Fonction pour exécuter un script et vérifier son succès
execute_script() {
  local script=$1

  if [ -f "$script" ]; alors
    echo -e "${NC}#############################################${NC}" | tee -a "$LOG_FILE"
    echo -e "${GREEN}Exécution de $script...${NC}" | tee -a "$LOG_FILE"
    echo -e "${NC}#############################################${NC}" | tee -a "$LOG_FILE"
    if bash "$script" >> "$LOG_FILE" 2>&1; then
      echo -e "${GREEN}$script terminé avec succès.${NC}" | tee -a "$LOG_FILE"
    else
      echo -e "${RED}Erreur lors de l'exécution de $script. Consultez $LOG_FILE pour plus de détails.${NC}" | tee -a "$LOG_FILE"
      exit 1
    fi
  else
    echo -e "${RED}Le script $script n'existe pas.${NC}" | tee -a "$LOG_FILE"
    exit 1
  fi
}

# Exécution des scripts dans l'ordre
execute_script "mysql_install.sh"
execute_script "init_django.sh"

echo -e "${GREEN}Tous les scripts ont été exécutés avec succès.${NC}" | tee -a "$LOG_FILE"
