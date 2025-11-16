# 📦 Guide d'installation

## Prérequis

- Docker ou Podman installé
- 2 Go d'espace disque disponible
- Connexion internet

## Installation avec Docker

### 1. Via Docker Hub
```bash
docker pull votreusername/ytdlp-web:latest
docker run -d -p 5000:5000 --name ytdlp-web votreusername/ytdlp-web:latest
```

### 2. Build depuis les sources
```bash
git clone https://github.com/votreusername/yt-dlp-web.git
cd yt-dlp-web
docker build -t ytdlp-web .
docker run -d -p 5000:5000 --name ytdlp-web ytdlp-web
```

## Installation avec Podman

### 1. Via registre
```bash
podman pull votreusername/ytdlp-web:latest
podman run -d -p 5000:5000 --name ytdlp-web votreusername/ytdlp-web:latest
```

### 2. Build depuis les sources
```bash
git clone https://github.com/votreusername/yt-dlp-web.git
cd yt-dlp-web
podman build -t ytdlp-web .
podman run -d -p 5000:5000 --name ytdlp-web ytdlp-web
```

## Configuration avancée

### Avec volumes persistants
```bash
mkdir -p ~/ytdlp-downloads
docker run -d \
  -p 5000:5000 \
  -v ~/ytdlp-downloads:/app/downloads:Z \
  --name ytdlp-web \
  votreusername/ytdlp-web:latest
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
docker run -d -p 8080:5000 --name ytdlp-web votreusername/ytdlp-web:latest
```

### Permissions SELinux

Ajoutez `:Z` au volume :
```bash
-v ~/downloads:/app/downloads:Z
```
