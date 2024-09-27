# General
PROJECT_NAME = "Virtuose"
MISSING_ENV_VAR = "Variable d'environnement manquante"
MISSING_FILE = "Fichier manquant"
MISSING_REQUIREMENT = "Module Python manquant"

# Header
NAVBAR_HOME = "Accueil"
NAVBAR_PROFILE = "Profil"
NAVBAR_LOGOUT = "Déconnexion"
NAVBAR_LOGIN = "Connexion"
NAVBAR_REGISTER = "Inscription"

# Login and register pages
LOGIN_PAGE_TITLE = "Connexion"
REGISTER_PAGE_TITLE = "Inscription"
GO_TO_HOME = "← Retour à l'accueil"
GO_TO_REGISTER = "Pas de compte ?"
GO_TO_LOGIN = "Déjà un compte ?"
CREATE_ACCOUNT = "Inscrivez-vous"
LOG_TO_ACCOUNT = "Connectez-vous"
LOGIN_BUTTON = "Se connecter"
REGISTER_BUTTON = "S'inscrire"
USERNAME_LABEL = "Nom d'utilisateur"
PASSWORD_LABEL = "Mot de passe"
CONFIRM_PASSWORD_LABEL = "Confirmer le mot de passe"
EMAIL_LABEL = "Adresse email"
ERROR_EMAIL_EXISTS = "Un utilisateur avec cet email existe déjà."

# Profile pages
ACCOUNT_SECTION = "Compte"
INFORMATIONS_PAGE_TITLE = "Informations"
INFORMATIONS_PAGE_USERNAME = "Nom d'utilisateur"
INFORMATIONS_PAGE_EMAIL = "Adresse email"

# Security pages
SECURITY_PAGE_TITLE = "Sécurité"

# Virtual Machines pages
VM_SECTION = "Machines Virtuelles"

# List VM page
LIST_VM_PAGE_TITLE = "Liste des machines virtuelles"
LIST_VM_OS_LABEL = "Système d'exploitation"
LIST_VM_NAME_LABEL = "Nom"
LIST_VM_RAM_LABEL = "RAM"
LIST_VM_CPU_LABEL = "CPU"

# Create VM page
CREATE_VM_PAGE_TITLE = "Créer une machine virtuelle"
CREATE_VM_BUTTON = "Créer la machine virtuelle"
TEMPLATE_LABEL = "Templates"
TEMPLATE_TEXT = "Envie d'une VM déjà prête à l'emploi ? Choisissez parmi nos templates !"
CREATE_VM_RAM_LABEL = "RAM"
CREATE_VM_RAM_LABEL_4GB = "4GB"
CREATE_VM_RAM_LABEL_8GB = "8GB"
CREATE_VM_RAM_LABEL_16GB = "16GB"
CREATE_VM_RAM_LABEL_32GB = "32GB"
CREATE_VM_CPU_LABEL = "CPU"
CREATE_VM_CPU_LABEL_1 = "1"
CREATE_VM_CPU_LABEL_2 = "2"
CREATE_VM_CPU_LABEL_4 = "4"
CREATE_VM_CPU_LABEL_8 = "8"
CREATE_VM_OS_LABEL = "Image système"
CREATE_VM_OS_LABEL_WINDOWS = "Windows"
CREATE_VM_OS_LABEL_LINUX = "Linux"
CREATE_VM_NAME_LABEL = "Nom de la VM"
LIST_VM_STATE_LABEL = "État"
CREATE_VM_SUCCESS = "La machine virtuelle a été créée avec succès."
CREATE_VM_ERROR = "Erreur lors de la machine virtuelle."
CREATE_VM_ERROR_NAME_NOT_ALPHANUMERIC = "Le nom de la machine virtuelle doit être alphanumérique."
CREATE_VM_ERROR_NAME_SPACE = "Le nom de la machine virtuelle ne doit pas contenir d'espaces."
CREATE_VM_ERROR_WINDOWS_RAM = "Windows requiert au moins 2GB de RAM."
CREATE_VM_ERROR_LINUX_RAM = "Linux requiert au moins 1GB de RAM."
CREATE_VM_ERROR_RAM_GENERIC = "La RAM n'est pas valide."
CREATE_VM_ERROR_CPU_GENERIC = "Le CPU n'est pas valide."
CREATE_VM_ERROR_OS_GENERIC = "Le système d'exploitation n'est pas valide."

DOMAIN_NOT_FOUND = "Domaine introuvable"
FAILED_TO_GET_DOMAIN_NAMES = "Échec de récupération des noms de domaine"
FAILED_TO_GET_DOMAIN_IDS = "Échec de récupération des IDs de domaine"
NO_POOLS_STORAGE = "Aucun pool de stockage"
FAILED_TO_GET_STORAGE_POOL = "Échec de récupération du pool de stockage"
FAILED_TO_GET_DOMAIN_UUID = "Échec de récupération de la VM. Merci de vérifier l'UUID."

VM_NO_STATE = "no state"
VM_STATE_RUNNING = "running"
VM_STATE_BLOCKED = "blocked"
VM_STATE_PAUSED = "paused"
VM_STATE_SHUTDOWN = "shutdown"
VM_STATE_SHUTOFF = "shutoff"
VM_STATE_CRASHED = "crashed"
VM_STATE_PMSUSPENDED = "pmsuspended"
UNKNOWN = "unknown"

VM_ALREADY_RUNNING = "La machine virtuelle est déjà en cours d'exécution"
VM_ALREADY_STOPPED = "La machine virtuelle est déjà arrêtée"
VM_NOT_RUNNING = "La machine virtuelle n'est pas en cours d'exécution"
VM_INVALID_ACTION = "Action non valide"
VM_INVALID_METHOD = "Méthode non valide"
VM_ERROR = "Erreur lors de l'exécution de l'action"
VM_STARTED = "La machine virtuelle a été démarrée"
VM_RESTARTED = "La machine virtuelle a été redémarrée"
VM_STOPPED = "La machine virtuelle a été arrêtée"
VM_KILLED = "La machine virtuelle a été tuée"
VM_DESTROYED = "La machine virtuelle a été détruite"
VM_DELETED = "La machine virtuelle a été supprimée"
VM_INFO = "Récupération des informations de la machine virtuelle"

VOLUME_FILE = "VOLUME_FILE"
VOLUME_BLOCK = "VOLUME_BLOCK"
VOLUME_DIR = "VOLUME_DIR"
VOLUME_NETWORK = "VOLUME_NETWORK"
VOLUME_NETDIR = "VOLUME_NETDIR"


# TEMPLATE NAME AND VOLUME NAME
# todo: IL FAUT METTRE CES INFOS DANS LA BDD VM
DOMAIN_TEMPLATE = {
    "centos9" : "centos-stream9"
}

TEMPLATE_PATH_POOL = "/var/lib/libvirt/images/"

def constants_processor(request):
    all_globals = globals()
    constants = {k: v for k, v in all_globals.items() if k.isupper()}
    return constants
