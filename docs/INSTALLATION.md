# 📦 Guide d'installation

## Prérequis

- Docker ou Podman installé
- 2 Go d'espace disque disponible
- Connexion internet

## Installation avec Docker

### 1. Via Docker Hub
```bash
docker pull raynoxis/yt-dlp-web-interface:latest
docker run -d -p 5000:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface:latest
```

### 2. Build depuis les sources
```bash
git clone https://github.com/Raynoxis/yt-dlp-Web-Interface.git
cd yt-dlp-Web-Interface
docker build -t raynoxis/yt-dlp-web-interface .
docker run -d -p 5000:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface
```

## Installation avec Podman

### 1. Via registre
```bash
podman pull raynoxis/yt-dlp-web-interface:latest
podman run -d -p 5000:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface:latest
```

### 2. Build depuis les sources
```bash
git clone https://github.com/Raynoxis/yt-dlp-Web-Interface.git
cd yt-dlp-Web-Interface
podman build -t raynoxis/yt-dlp-web-interface .
podman run -d -p 5000:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface
```

## Configuration avancée

### Avec volumes persistants
```bash
mkdir -p ~/ytdlp-downloads
docker run -d \
  -p 5000:5000 \
  -v ~/ytdlp-downloads:/app/downloads:Z \
  --name ytdlp-web \
  raynoxis/yt-dlp-web-interface:latest
```

### Avec Docker Compose
```bash
docker-compose up -d
```

## Vérification

Accédez à http://localhost:5000 dans votre navigateur.

## Dépannage

### Le conteneur ne démarre pas
```bash
docker logs ytdlp-web
```

### Port déjà utilisé

Changez le port :
```bash
docker run -d -p 8080:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface:latest
```

### Permissions SELinux

Ajoutez `:Z` au volume :
```bash
-v ~/downloads:/app/downloads:Z
```
