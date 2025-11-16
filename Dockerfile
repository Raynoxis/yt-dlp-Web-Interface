FROM python:3.11-slim

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Installation de yt-dlp
RUN wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp \
    && chmod +x /usr/local/bin/yt-dlp

# Installation de Flask
RUN pip install --no-cache-dir flask flask-cors

# Création des répertoires
WORKDIR /app
RUN mkdir -p /app/downloads /app/templates

# Copie des fichiers de l'application
COPY app.py /app/
COPY templates/index.html /app/templates/

# Exposition du port
EXPOSE 5000

# Variables d'environnement
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Commande de démarrage
CMD ["python", "-u", "app.py"]
