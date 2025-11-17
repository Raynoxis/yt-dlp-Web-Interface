# 🎬 yt-dlp Web Interface

Interface web moderne pour télécharger des vidéos YouTube avec [yt-dlp](https://github.com/yt-dlp/yt-dlp), conteneurisée avec Docker/Podman.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)

## ✨ Fonctionnalités

- 🔍 **Analyse complète** des formats vidéo et audio disponibles
- 🎯 **Sélection précise** des formats (qualité, codec, bitrate)
- ⚙️ **Options de sortie** personnalisables (MP4, MKV, WebM)
- 🎵 **Transcodage audio** (AAC, MP3, Opus) avec contrôle du bitrate
- 📦 **Interface moderne** et responsive
- 🐳 **Conteneurisé** pour un déploiement facile
- 🧹 **Nettoyage automatique** des fichiers entre les téléchargements
- 📋 **Affichage de la commande** exécutée pour transparence

## 🚀 Démarrage rapide

### Avec Docker
```bash
docker pull raynoxis/yt-dlp-web-interface:latest
docker run -d -p 5000:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface:latest
```

### Avec Podman
```bash
podman pull raynoxis/yt-dlp-web-interface:latest
podman run -d -p 5000:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface:latest
```

### Avec Docker Compose
```bash
git clone https://github.com/Raynoxis/yt-dlp-Web-Interface.git
cd yt-dlp-Web-Interface
docker-compose up -d
```

Accédez à l'interface : **http://localhost:5000**

## 📖 Documentation

- [Installation détaillée](docs/INSTALLATION.md)
- [Guide d'utilisation](docs/USAGE.md)

## 🛠️ Build depuis les sources
```bash
# Cloner le repo
git clone https://github.com/Raynoxis/yt-dlp-Web-Interface.git
cd yt-dlp-Web-Interface

# Build avec Docker
docker build -t raynoxis/yt-dlp-web-interface .

# Ou avec Podman
podman build -t raynoxis/yt-dlp-web-interface .

# Lancer
docker run -d -p 5000:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface
```

## 🎯 Utilisation

1. Collez l'URL d'une vidéo YouTube
2. Cliquez sur "Analyser la vidéo"
3. Sélectionnez les formats vidéo et audio souhaités
4. Choisissez les options de sortie (conteneur, codec audio, bitrate)
5. Cliquez sur "Télécharger"
6. Téléchargez le fichier généré

## 📸 Screenshots

![Etape 1](docs/screenshots/step1.png)
![Etape 2](docs/screenshots/step2.png)
![Etape 3](docs/screenshots/step3.png)

## 🔧 Configuration avancée

### Volumes persistants
```bash
docker run -d \
  -p 5000:5000 \
  -v ./downloads:/app/downloads \
  --name ytdlp-web \
  raynoxis/yt-dlp-web-interface:latest
```

### Variables d'environnement
```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  --name ytdlp-web \
  raynoxis/yt-dlp-web-interface:latest
```

### Compose
```bash
version: '3.8'

services:
  ytdlp-webinterface:
    image: raynoxis/yt-dlp-web-interface:latest
    container_name: ytdlp-webinterface
    ports:
      - "5000:5000"
    volumes:
      - ./downloads:/app/downloads
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```


## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Le meilleur outil de téléchargement vidéo
- [Flask](https://flask.palletsprojects.com/) - Framework web Python
- [FFmpeg](https://ffmpeg.org/) - Traitement vidéo et audio

## ⚠️ Avertissement

Cet outil est destiné à un usage personnel et éducatif. Respectez les conditions d'utilisation de YouTube et les lois sur le droit d'auteur de votre pays.

## 📧 Contact

Raynoxis - [GitHub](https://github.com/Raynoxis)

Lien du projet: [https://github.com/Raynoxis/yt-dlp-Web-Interface](https://github.com/Raynoxis/yt-dlp-Web-Interface)

Lien Docker Hub: [https://hub.docker.com/r/raynoxis/yt-dlp-web-interface](https://hub.docker.com/r/raynoxis/yt-dlp-web-interface)
