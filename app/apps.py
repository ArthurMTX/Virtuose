import os
from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from . import context_processors


def check_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()

    for requirement in requirements:
        try:
            __import__(requirement)
        except ImportError:
            raise ImproperlyConfigured(f"{context_processors.MISSING_REQUIREMENT}: {requirement}")


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        required_env_vars = [
            'SECRET_KEY',
            'DB_NAME',
            'DB_USER',
            'DB_PASSWORD',
            'DB_HOST',
            'DB_PORT'
        ]

        for var in required_env_vars:
            if not os.getenv(var):
                raise ImproperlyConfigured(f"{context_processors.MISSING_ENV_VAR}: {var}")

        static_files = [
            'static/noVNC/vnc.html',
        ]

        for file in static_files:
            if not os.path.exists(file):
                raise ImproperlyConfigured(f"{context_processors.MISSING_FILE}: {file}")
