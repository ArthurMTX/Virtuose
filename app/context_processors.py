# General
PROJECT_NAME = "Virtuose"

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
CREATE_VM_DISK_LABEL = "Taille du disque"
CREATE_VM_DISK_LABEL_10GB = "10GB"
CREATE_VM_DISK_LABEL_20GB = "20GB"
CREATE_VM_DISK_LABEL_50GB = "50GB"
CREATE_VM_DISK_LABEL_100GB = "100GB"
CREATE_VM_DISK_LABEL_250GB = "250GB"
CREATE_VM_DISK_LABEL_500GB = "500GB"
CREATE_VM_OS_LABEL = "Système d'exploitation"
CREATE_VM_OS_LABEL_WINDOWS = "Windows"
CREATE_VM_OS_LABEL_LINUX = "Linux"
CREATE_VM_NAME_LABEL = "Nom de la VM"
CREATE_VM_SUCCESS = "La machine virtuelle a été créée avec succès."
CREATE_VM_ERROR = "Erreur lors de la machine virtuelle."
CREATE_VM_ERROR_NAME_NOT_ALPHANUMERIC = "Le nom de la machine virtuelle doit être alphanumérique."
CREATE_VM_ERROR_NAME_SPACE = "Le nom de la machine virtuelle ne doit pas contenir d'espaces."
CREATE_VM_ERROR_WINDOWS_RAM = "Windows requiert au moins 2GB de RAM."
CREATE_VM_ERROR_LINUX_RAM = "Linux requiert au moins 1GB de RAM."
CREATE_VM_ERROR_DISK = "Le disque doit être au moins de 10GB."
CREATE_VM_ERROR_RAM_GENERIC = "La RAM n'est pas valide."
CREATE_VM_ERROR_CPU_GENERIC = "Le CPU n'est pas valide."
CREATE_VM_ERROR_DISK_GENERIC = "Le disque n'est pas valide."
CREATE_VM_ERROR_OS_GENERIC = "Le système d'exploitation n'est pas valide."



def constants_processor(request):
    all_globals = globals()
    constants = {k: v for k, v in all_globals.items() if k.isupper()}
    return constants
