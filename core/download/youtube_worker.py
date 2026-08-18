"""
===========================================================
PRT Labs - Core / YouTube Download Worker
File: core/download/youtube_worker.py
===========================================================
"""

import os
import re
from PySide6.QtCore import QThread, Signal

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG_PATH = None


class YouTubeDownloadWorker(QThread):
    """Worker 100% isolado apenas para o YouTube."""

    progress_changed = Signal(dict)
    status_changed = Signal(str, str)
    download_finished = Signal(str)
    download_error = Signal(str)

    def __init__(self, media_url: str, output_path: str, parent=None, **kwargs):
        super().__init__(parent)
        self.media_url = media_url or ""
        self.output_path = output_path or ""

    def run(self):
        try:
            self.status_changed.emit("extracting", f"🔍 Processando mídia do YouTube: {self.media_url}...")
            os.makedirs(self.output_path, exist_ok=True)

            if not yt_dlp:
                raise Exception("A biblioteca yt-dlp não está instalada.")

            out_template = os.path.join(self.output_path, "%(title)s.%(ext)s")

            ydl_opts = {
                'outtmpl': out_template,
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'progress_hooks': [self._ydl_hook],
                'quiet': False,
                'no_warnings': True,
                'no_color': True,
                'noplaylist': True,  # Baixa apenas o vídeo individual (ignora mix/playlists)
                'extractor_args': {
                    'youtube': {
                        'player_client': ['mweb', 'android', 'web']
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
                }
            }

            if FFMPEG_PATH:
                ydl_opts['ffmpeg_location'] = FFMPEG_PATH

            print(f"🚀 [YouTube Worker] Baixando: {self.media_url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.media_url, download=True)
                if info:
                    if 'entries' in info and info['entries']:
                        info = info['entries'][0]
                    downloaded_file = ydl.prepare_filename(info)
                    final_filepath = downloaded_file

                    if not os.path.exists(final_filepath):
                        base_path = os.path.splitext(downloaded_file)[0]
                        for ext in ['.mp4', '.mkv', '.webm']:
                            if os.path.exists(base_path + ext):
                                final_filepath = base_path + ext
                                break
                else:
                    final_filepath = self.output_path

            self.download_finished.emit(final_filepath)

        except Exception as e:
            self.download_error.emit(f"Erro no download do YouTube: {str(e)}")

    def _ydl_hook(self, d):
        if d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total * 100) if total > 0 else 0
            
            speed = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_speed_str', '0 B/s'))).strip()
            eta = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_eta_str', '--:--'))).strip()
            self.progress_changed.emit({"percent": percent, "speed": speed, "eta": eta})