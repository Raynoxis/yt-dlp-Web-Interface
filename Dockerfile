FROM python:3.11-slim

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installation de yt-dlp
RUN wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp \
    && chmod +x /usr/local/bin/yt-dlp

# Installation de Flask
RUN pip install --no-cache-dir flask

# Création d'un utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/downloads /app/templates && \
    chown -R appuser:appuser /app

# Création des répertoires
WORKDIR /app

# Copie des fichiers de l'application
COPY --chown=appuser:appuser app.py /app/
COPY --chown=appuser:appuser templates/index.html /app/templates/

# Passer à l'utilisateur non-root
USER appuser

# Exposition du port
EXPOSE 5000

# Variables d'environnement
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Commande de démarrage
CMD ["python", "-u", "app.py"]
