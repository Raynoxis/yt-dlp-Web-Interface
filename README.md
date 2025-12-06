# 🎬 yt-dlp Web Interface

Modern, hardened web UI for downloading YouTube videos with conversion options and detailed status. Built on the excellent [yt-dlp](https://github.com/yt-dlp/yt-dlp) and fully containerized with Docker/Podman. Coded with my friend: Claude AI

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Security](https://img.shields.io/badge/security-hardened-green.svg)

## ✨ Highlights
- 🎯 Choose exact video/audio formats with custom containers and codecs
- 📈 Real-time progress via SSE; shows speed, ETA, and the yt-dlp command used
- 🛡️ Hardened: strict URL validation, path traversal protection, non-root container, full logging
- ⚡ Concurrent, non-blocking downloads with automatic cleanup after 1h
- 🐳 Ready-to-run images for Docker and Podman

## 🚀 Deploy

### Docker
```bash
docker pull raynoxis/yt-dlp-web-interface:latest
docker run -d -p 5000:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface:latest
```

### Docker Compose (recommended)
```bash
git clone https://github.com/Raynoxis/yt-dlp-Web-Interface.git
cd yt-dlp-Web-Interface

docker-compose up -d
```

Access the UI: **http://localhost:5001** (Compose) or **http://localhost:5000** (direct run).

Persist downloads:
```bash
docker run -d -p 5000:5000 \
  -v ./downloads:/app/downloads \
  --name ytdlp-web \
  raynoxis/yt-dlp-web-interface:latest
```

Build from source (optional):
```bash
git clone https://github.com/Raynoxis/yt-dlp-Web-Interface.git
cd yt-dlp-Web-Interface
docker build -t raynoxis/yt-dlp-web-interface .
docker run -d -p 5000:5000 --name ytdlp-web raynoxis/yt-dlp-web-interface
```

## 📸 Screenshots
### Step 1 - Analysis
![Step 1](docs/screenshots/step1.png)

### Step 2 - Format selection
![Step 2](docs/screenshots/step2.png)


## 🎯 How it works
1. Paste a YouTube URL and click **Analyze video** to list available streams.
2. Pick video and audio formats; choose container, codec, and bitrate.
3. Click **Download** and follow live progress (speed, ETA, executed yt-dlp command).
4. Download the generated file when it completes.


## 📝 License

This project is under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Credits

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The best video download tool
- [Flask](https://flask.palletsprojects.com/) - Python web framework
- [FFmpeg](https://ffmpeg.org/) - Audio/video processing
- [Claude AI](https://claude.ai) - Development assistant

## ⚠️ Disclaimer

This tool is for personal and educational use. Respect YouTube's terms of service and your local copyright laws.

## 📧 Contact

Raynoxis - [GitHub](https://github.com/Raynoxis)

Project link: [https://github.com/Raynoxis/yt-dlp-Web-Interface](https://github.com/Raynoxis/yt-dlp-Web-Interface)

Docker Hub link: [https://hub.docker.com/r/raynoxis/yt-dlp-web-interface](https://hub.docker.com/r/raynoxis/yt-dlp-web-interface)
