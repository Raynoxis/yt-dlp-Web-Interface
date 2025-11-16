from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import json
import os
import re
from pathlib import Path

app = Flask(__name__)
DOWNLOAD_DIR = Path('/app/downloads')
DOWNLOAD_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_video():
    """Analyse une URL YouTube et retourne les formats disponibles"""
    try:
        # Nettoyage des anciens fichiers lors d'une nouvelle analyse
        for file in DOWNLOAD_DIR.glob('*'):
            if file.is_file():
                try:
                    file.unlink()
                except:
                    pass
        
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL manquante'}), 400
        
        # Commande yt-dlp pour lister les formats
        cmd = ['yt-dlp', '-J', url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return jsonify({'error': f'Erreur yt-dlp: {result.stderr}'}), 400
        
        video_info = json.loads(result.stdout)
        
        # Extraction des informations
        title = video_info.get('title', 'Sans titre')
        duration = video_info.get('duration', 0)
        thumbnail = video_info.get('thumbnail', '')
        
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
            tbr = fmt.get('tbr', 0)
            
            # Formats vidéo (avec vidéo)
            if vcodec != 'none' and resolution != 'audio only':
                size_mb = f"{filesize / (1024*1024):.1f} MB" if filesize else "N/A"
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
                size_mb = f"{filesize / (1024*1024):.1f} MB" if filesize else "N/A"
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
        return jsonify({'error': 'Timeout lors de l\'analyse'}), 408
    except json.JSONDecodeError:
        return jsonify({'error': 'Erreur de parsing JSON'}), 500
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@app.route('/api/download', methods=['POST'])
def download_video():
    """Télécharge la vidéo avec les paramètres spécifiés"""
    try:
        # Nettoyage des anciens fichiers avant nouveau téléchargement
        for file in DOWNLOAD_DIR.glob('*'):
            if file.is_file():
                try:
                    file.unlink()
                except:
                    pass
        
        data = request.get_json()
        url = data.get('url', '').strip()
        video_format = data.get('video_format', '')
        audio_format = data.get('audio_format', '')
        output_container = data.get('output_container', 'mp4')
        audio_codec = data.get('audio_codec', 'aac')
        audio_bitrate = data.get('audio_bitrate', '192k')
        
        if not url:
            return jsonify({'error': 'URL manquante'}), 400
        
        # Construction de la chaîne de format
        if video_format and audio_format:
            format_string = f"{video_format}+{audio_format}"
        elif video_format:
            format_string = f"{video_format}+ba"
        elif audio_format:
            format_string = f"bv+{audio_format}"
        else:
            format_string = "bv+ba/best"
        
        # Nom de fichier sécurisé avec timestamp pour éviter les conflits
        import time
        timestamp = int(time.time())
        output_template = str(DOWNLOAD_DIR / f'%(title)s_{timestamp}.%(ext)s')
        
        # Construction de la commande yt-dlp
        cmd = [
            'yt-dlp',
            '-f', format_string,
            '--merge-output-format', output_container,
            '-o', output_template
        ]
        
        # Ajout des arguments de post-processing pour l'audio
        postproc_added = False
        if audio_codec and audio_codec != 'copy':
            postproc_args = f"-c:a {audio_codec}"
            if audio_bitrate:
                postproc_args += f" -b:a {audio_bitrate}"
            cmd.extend(['--postprocessor-args', f'ffmpeg:{postproc_args}'])
            postproc_added = True
        # Si copy est sélectionné, on ne réencode pas du tout
        # Le bitrate est ignoré car on ne peut pas changer le bitrate sans réencoder
        
        # Ajout de l'URL à la fin
        cmd.append(url)
        
        # Conversion de la commande en string pour affichage
        cmd_string = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in cmd)
        
        # Exécution du téléchargement
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        
        if result.returncode != 0:
            return jsonify({
                'error': f'Erreur téléchargement: {result.stderr}',
                'command': cmd_string
            }), 400
        
        # Recherche du fichier téléchargé
        downloaded_files = list(DOWNLOAD_DIR.glob(f'*.{output_container}'))
        if not downloaded_files:
            downloaded_files = list(DOWNLOAD_DIR.glob('*'))
        
        if not downloaded_files:
            return jsonify({
                'error': 'Fichier téléchargé introuvable',
                'command': cmd_string
            }), 404
        
        # Dernier fichier modifié
        latest_file = max(downloaded_files, key=lambda p: p.stat().st_mtime)
        
        return jsonify({
            'success': True,
            'filename': latest_file.name,
            'size': latest_file.stat().st_size,
            'command': cmd_string,
            'stdout': result.stdout,
            'format_used': format_string,
            'postproc_applied': postproc_added,
            'audio_codec': audio_codec if audio_codec != 'copy' else 'original (copy)',
            'audio_bitrate': audio_bitrate if audio_codec != 'copy' else 'original'
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Timeout lors du téléchargement'}), 408
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@app.route('/api/download-file/<filename>')
def download_file(filename):
    """Télécharge le fichier généré"""
    try:
        file_path = DOWNLOAD_DIR / filename
        if not file_path.exists():
            return jsonify({'error': 'Fichier introuvable'}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """Nettoie les fichiers téléchargés"""
    try:
        for file in DOWNLOAD_DIR.glob('*'):
            if file.is_file():
                file.unlink()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
