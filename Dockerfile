FROM python:3.11

# Empêcher Python d'écrire des fichiers pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /frontend

# Installer les dépendances système nécessaires
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libvirt-dev \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances Python
COPY requirements.txt /frontend/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . /frontend/
