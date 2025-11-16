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
docker pull votreusername/ytdlp-web:latest
docker run -d -p 5000:5000 --name ytdlp-web votreusername/ytdlp-web:latest
```

### Avec Podman
```bash
podman pull votreusername/ytdlp-web:latest
podman run -d -p 5000:5000 --name ytdlp-web votreusername/ytdlp-web:latest
```

### Avec Docker Compose
```bash
git clone https://github.com/votreusername/yt-dlp-web.git
cd yt-dlp-web
docker-compose up -d
```

Accédez à l'interface : **http://localhost:5000**

## 📖 Documentation

- [Installation détaillée](docs/INSTALLATION.md)
- [Guide d'utilisation](docs/USAGE.md)

## 🛠️ Build depuis les sources
```bash
# Cloner le repo
git clone https://github.com/votreusername/yt-dlp-web.git
cd yt-dlp-web

# Build avec Docker
docker build -t ytdlp-web .

# Ou avec Podman
podman build -t ytdlp-web .

# Lancer
docker run -d -p 5000:5000 --name ytdlp-web ytdlp-web
```

## 🎯 Utilisation

1. Collez l'URL d'une vidéo YouTube
2. Cliquez sur "Analyser la vidéo"
3. Sélectionnez les formats vidéo et audio souhaités
4. Choisissez les options de sortie (conteneur, codec audio, bitrate)
5. Cliquez sur "Télécharger"
6. Téléchargez le fichier généré

## 📸 Screenshots

![Interface principale](docs/screenshots/main.png)
![Sélection des formats](docs/screenshots/formats.png)

## 🔧 Configuration avancée

### Volumes persistants
```bash
docker run -d \
  -p 5000:5000 \
  -v ./downloads:/app/downloads \
  --name ytdlp-web \
  votreusername/ytdlp-web:latest
```

### Variables d'environnement
```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  --name ytdlp-web \
  votreusername/ytdlp-web:latest
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

