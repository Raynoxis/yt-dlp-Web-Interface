from flask import Flask, render_template, request, jsonify, send_file, Response
import subprocess
import json
import os
import re
import logging
import uuid
import time
from pathlib import Path
from urllib.parse import urlparse
import threading

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
DOWNLOAD_DIR = Path('/app/downloads')
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Configuration
BYTES_PER_MB = 1024 * 1024
TIMEOUT_ANALYZE = 30
TIMEOUT_DOWNLOAD = 600

# Validation YouTube URL
YOUTUBE_REGEX = re.compile(
    r'^(https?://)?(www\.)?(youtube\.com/(watch\?v=|shorts/|embed/)|youtu\.be/)[\w-]+([?&].*)?$'
)

# Ensembles de valeurs valides
VALID_CONTAINERS = {'mp4', 'mkv', 'webm', 'm4a', 'mp3'}
VALID_AUDIO_CODECS = {'aac', 'mp3', 'opus', 'copy'}

# Stockage des sessions de téléchargement pour le suivi de progression
download_sessions = {}
download_lock = threading.Lock()


def validate_youtube_url(url: str) -> bool:
    """Valide qu'une URL est bien une URL YouTube valide"""
    if not url:
        return False
    return bool(YOUTUBE_REGEX.match(url))


def validate_container(container: str) -> bool:
    """Valide le format de conteneur"""
    return container in VALID_CONTAINERS


def validate_audio_codec(codec: str) -> bool:
    """Valide le codec audio"""
    return codec in VALID_AUDIO_CODECS


def create_session_dir(session_id: str) -> Path:
    """Crée un répertoire unique pour la session"""
    session_dir = DOWNLOAD_DIR / session_id
    session_dir.mkdir(exist_ok=True)
    return session_dir


def cleanup_old_sessions(max_age_seconds: int = 3600):
    """Nettoie les répertoires de session de plus de max_age_seconds"""
    try:
        current_time = time.time()
        for item in DOWNLOAD_DIR.iterdir():
            if item.is_dir():
                # Vérifier l'âge du répertoire
                dir_age = current_time - item.stat().st_mtime
                if dir_age > max_age_seconds:
                    try:
                        for file in item.iterdir():
                            if file.is_file():
                                file.unlink()
                        item.rmdir()
                        logger.info(f"Cleaned up old session directory: {item.name}")
                    except Exception as e:
                        logger.error(f"Error cleaning up {item.name}: {e}")
    except Exception as e:
        logger.error(f"Error in cleanup_old_sessions: {e}")


@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """Analyse une URL YouTube et retourne les formats disponibles"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()

        if not url:
            logger.warning("Analyze request with missing URL")
            return jsonify({'error': 'URL manquante'}), 400

        # Validation de l'URL
        if not validate_youtube_url(url):
            logger.warning(f"Invalid YouTube URL attempted: {url}")
            return jsonify({'error': 'URL YouTube invalide'}), 400

        logger.info(f"Analyzing video: {url}")

        # Commande yt-dlp pour lister les formats
        cmd = ['yt-dlp', '-J', url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_ANALYZE)

        if result.returncode != 0:
            logger.error(f"yt-dlp analyze failed: {result.stderr}")
            return jsonify({'error': 'Erreur lors de l\'analyse de la vidéo'}), 400

        video_info = json.loads(result.stdout)

        # Extraction des informations
        title = video_info.get('title', 'Sans titre')
        duration = video_info.get('duration', 0)
        thumbnail = video_info.get('thumbnail', '')

        logger.info(f"Successfully analyzed: {title}")

        # Traitement des formats
        formats = video_info.get('formats', [])
        video_formats = []
        audio_formats = []

        for fmt in formats:
            format_id = fmt.get('format_id', '')
            ext = fmt.get('ext', '')
            resolution = fmt.get('resolution', 'audio only')
            filesize = fmt.get('filesize', 0) or fmt.get('filesize_approx', 0)
            vcodec = fmt.get('vcodec', 'none')
            acodec = fmt.get('acodec', 'none')
            fps = fmt.get('fps', 0)

            # Formats vidéo (avec vidéo)
            if vcodec != 'none' and resolution != 'audio only':
                size_mb = f"{filesize / BYTES_PER_MB:.1f} MB" if filesize else "N/A"
                video_formats.append({
                    'id': format_id,
                    'label': f"{resolution} - {ext} - {vcodec} - {fps}fps - {size_mb}",
                    'ext': ext,
                    'resolution': resolution,
                    'vcodec': vcodec,
                    'filesize': filesize
                })

            # Formats audio (sans vidéo)
            if acodec != 'none' and vcodec == 'none':
                abr = fmt.get('abr', 0)
                size_mb = f"{filesize / BYTES_PER_MB:.1f} MB" if filesize else "N/A"
                audio_formats.append({
                    'id': format_id,
                    'label': f"{acodec} - {abr}kbps - {ext} - {size_mb}",
                    'ext': ext,
                    'acodec': acodec,
                    'abr': abr,
                    'filesize': filesize
                })

        # Tri par qualité
        video_formats.sort(key=lambda x: x.get('filesize', 0), reverse=True)
        audio_formats.sort(key=lambda x: x.get('filesize', 0), reverse=True)

        return jsonify({
            'title': title,
            'duration': duration,
            'thumbnail': thumbnail,
            'video_formats': video_formats,
            'audio_formats': audio_formats
        })

    except subprocess.TimeoutExpired:
        logger.error(f"Analyze timeout for URL: {url}")
        return jsonify({'error': 'Timeout lors de l\'analyse'}), 408
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return jsonify({'error': 'Erreur de parsing JSON'}), 500
    except Exception as e:
        logger.error(f"Unexpected error in analyze_video: {e}", exc_info=True)
        return jsonify({'error': 'Erreur serveur'}), 500


@app.route('/api/download', methods=['POST'])
def download_video():
    """Télécharge la vidéo avec les paramètres spécifiés"""
    postproc_added = False  # Initialisation au début

    try:
        # Nettoyage des anciennes sessions
        cleanup_old_sessions()

        data = request.get_json()
        url = data.get('url', '').strip()
        video_format = data.get('video_format', '')
        audio_format = data.get('audio_format', '')
        output_container = data.get('output_container', 'mp4')
        audio_codec = data.get('audio_codec', 'aac')
        audio_bitrate = data.get('audio_bitrate', '192k')
        audio_only = data.get('audio_only', False)

        # Validation des entrées
        if not url:
            logger.warning("Download request with missing URL")
            return jsonify({'error': 'URL manquante'}), 400

        if not validate_youtube_url(url):
            logger.warning(f"Invalid YouTube URL attempted: {url}")
            return jsonify({'error': 'URL YouTube invalide'}), 400

        if not validate_container(output_container):
            logger.warning(f"Invalid container attempted: {output_container}")
            return jsonify({'error': f'Format de conteneur invalide: {output_container}'}), 400

        if not validate_audio_codec(audio_codec):
            logger.warning(f"Invalid audio codec attempted: {audio_codec}")
            return jsonify({'error': f'Codec audio invalide: {audio_codec}'}), 400

        # Créer une session unique pour ce téléchargement
        session_id = str(uuid.uuid4())
        session_dir = create_session_dir(session_id)

        logger.info(f"Starting download for session {session_id}: {url}")

        # Construction de la chaîne de format
        if audio_only:
            # Mode audio seulement
            if audio_format:
                format_string = audio_format
            else:
                format_string = "ba/best"
        else:
            # Mode vidéo + audio
            if video_format and audio_format:
                format_string = f"{video_format}+{audio_format}"
            elif video_format:
                format_string = f"{video_format}+ba"
            elif audio_format:
                format_string = f"bv+{audio_format}"
            else:
                format_string = "bv+ba/best"

        # Nom de fichier sécurisé avec timestamp
        timestamp = int(time.time())
        output_template = str(session_dir / f'%(title)s_{timestamp}.%(ext)s')

        # Construction de la commande yt-dlp
        cmd = ['yt-dlp', '-f', format_string, '-o', output_template]

        # Pour l'audio seulement, utiliser -x pour extraction
        if audio_only:
            cmd.extend(['-x'])  # Extraire l'audio

            # Spécifier le format audio de sortie
            if output_container == 'mp3':
                cmd.extend(['--audio-format', 'mp3'])
            elif output_container == 'm4a':
                cmd.extend(['--audio-format', 'm4a'])
            else:
                cmd.extend(['--audio-format', 'best'])

            # Gérer la qualité audio
            if audio_codec == 'copy':
                cmd.extend(['--audio-quality', '0'])
            else:
                if audio_bitrate:
                    cmd.extend(['--audio-quality', audio_bitrate.upper()])
                else:
                    cmd.extend(['--audio-quality', '0'])
                postproc_added = True
        else:
            # Mode vidéo + audio : utiliser merge-output-format
            cmd.extend(['--merge-output-format', output_container])

            # Ajout des arguments de post-processing pour l'audio
            if audio_codec and audio_codec != 'copy':
                postproc_args = f"-c:a {audio_codec}"
                if audio_bitrate:
                    postproc_args += f" -b:a {audio_bitrate}"
                cmd.extend(['--postprocessor-args', f'ffmpeg:{postproc_args}'])
                postproc_added = True

        # Ajout de l'URL à la fin
        cmd.append(url)

        # Conversion de la commande en string pour affichage
        cmd_string = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in cmd)

        logger.info(f"Executing download command for session {session_id}")

        # Exécution du téléchargement
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_DOWNLOAD)

        if result.returncode != 0:
            logger.error(f"Download failed for session {session_id}: {result.stderr}")
            return jsonify({'error': 'Erreur lors du téléchargement'}), 400

        # Recherche du fichier téléchargé dans le répertoire de session
        if audio_only and output_container in ['mp3', 'm4a']:
            downloaded_files = list(session_dir.glob(f'*.{output_container}'))
        else:
            downloaded_files = list(session_dir.glob(f'*.{output_container}'))

        if not downloaded_files:
            downloaded_files = list(session_dir.glob('*'))

        if not downloaded_files:
            logger.error(f"No downloaded file found for session {session_id}")
            return jsonify({'error': 'Fichier téléchargé introuvable'}), 404

        # Dernier fichier modifié
        latest_file = max(downloaded_files, key=lambda p: p.stat().st_mtime)

        logger.info(f"Download successful for session {session_id}: {latest_file.name}")

        return jsonify({
            'success': True,
            'session_id': session_id,
            'filename': latest_file.name,
            'size': latest_file.stat().st_size,
            'command': cmd_string,
            'format_used': format_string,
            'postproc_applied': postproc_added,
            'audio_codec': audio_codec if audio_codec != 'copy' else 'original (copy)',
            'audio_bitrate': audio_bitrate if audio_codec != 'copy' else 'original',
            'audio_only': audio_only
        })

    except subprocess.TimeoutExpired:
        logger.error(f"Download timeout for session {session_id}")
        return jsonify({'error': 'Timeout lors du téléchargement'}), 408
    except Exception as e:
        logger.error(f"Unexpected error in download_video: {e}", exc_info=True)
        return jsonify({'error': 'Erreur serveur'}), 500


@app.route('/api/download-file/<session_id>/<filename>')
def download_file(session_id, filename):
    """Télécharge le fichier généré - sécurisé contre path traversal"""
    try:
        # Validation du nom de fichier pour éviter path traversal
        safe_filename = os.path.basename(filename)
        safe_session_id = os.path.basename(session_id)

        if '..' in filename or '/' in filename or '\\' in filename:
            logger.warning(f"Path traversal attempt detected: {filename}")
            return jsonify({'error': 'Nom de fichier invalide'}), 400

        session_dir = DOWNLOAD_DIR / safe_session_id
        file_path = session_dir / safe_filename

        # Vérifier que le fichier est bien dans le répertoire de session
        if not file_path.resolve().is_relative_to(session_dir.resolve()):
            logger.warning(f"Path traversal attempt detected: {file_path}")
            return jsonify({'error': 'Chemin de fichier invalide'}), 400

        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return jsonify({'error': 'Fichier introuvable'}), 404

        logger.info(f"Serving file: {file_path}")
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        logger.error(f"Error in download_file: {e}", exc_info=True)
        return jsonify({'error': 'Erreur serveur'}), 500


@app.route('/api/cleanup/<session_id>', methods=['POST'])
def cleanup_session(session_id):
    """Nettoie les fichiers d'une session spécifique"""
    try:
        safe_session_id = os.path.basename(session_id)
        session_dir = DOWNLOAD_DIR / safe_session_id

        if not session_dir.exists():
            return jsonify({'success': True, 'message': 'Session déjà nettoyée'})

        # Supprimer tous les fichiers du répertoire
        for file in session_dir.iterdir():
            if file.is_file():
                file.unlink()
                logger.info(f"Deleted file: {file}")

        # Supprimer le répertoire
        session_dir.rmdir()
        logger.info(f"Cleaned up session: {session_id}")

        return jsonify({'success': True})

    except Exception as e:
        logger.error(f"Error in cleanup_session: {e}", exc_info=True)
        return jsonify({'error': 'Erreur lors du nettoyage'}), 500


@app.route('/api/cleanup-all', methods=['POST'])
def cleanup_all():
    """Nettoie tous les fichiers téléchargés"""
    try:
        count = 0
        for item in DOWNLOAD_DIR.iterdir():
            if item.is_dir():
                for file in item.iterdir():
                    if file.is_file():
                        file.unlink()
                        count += 1
                item.rmdir()

        logger.info(f"Cleaned up {count} files from all sessions")
        return jsonify({'success': True, 'files_deleted': count})

    except Exception as e:
        logger.error(f"Error in cleanup_all: {e}", exc_info=True)
        return jsonify({'error': 'Erreur lors du nettoyage'}), 500


if __name__ == '__main__':
    logger.info("Starting yt-dlp Web Interface")
    app.run(host='0.0.0.0', port=5000, debug=False)
