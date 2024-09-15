import os
from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from . import context_processors


"""
Initialisation de l'application, vérification des variables d'environnement et des fichiers statiques
"""


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        REQUIRED_ENV_VARS = [
            'SECRET_KEY',
            'DB_NAME',
            'DB_USER',
            'DB_PASSWORD',
            'DB_HOST',
            'DB_PORT'
        ]
        STATIC_FILES = [
            'static/noVNC/vnc.html',
        ]

        # Vérification des variables d'environnement dans le fichier .env
        for var in REQUIRED_ENV_VARS:
            if not os.getenv(var):
                raise ImproperlyConfigured(f"{context_processors.MISSING_ENV_VAR}: {var}")

        # Vérification des fichiers statiques dans le dossier static
        for file in STATIC_FILES:
            if not os.path.exists(file):
                raise ImproperlyConfigured(f"{context_processors.MISSING_FILE}: {file}")
