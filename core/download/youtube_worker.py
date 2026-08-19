"""
===========================================================
PRT Labs - Core / YouTube Download Worker
File: core/download/youtube_worker.py
===========================================================
"""

import html
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
    """Worker para download de vídeos do YouTube."""

    progress_changed = Signal(dict)
    status_changed = Signal(str, str)
    download_finished = Signal(str)
    download_error = Signal(str)

    def __init__(
        self,
        media_url: str,
        output_path: str = "",
        media_type: str = "video",
        quality: str = "best",
        title: str = "",
        parent=None,
        **kwargs
    ):
        super().__init__(parent)
        self.media_url = media_url or ""
        self.output_path = output_path or ""
        self.media_type = media_type or "video"
        self.quality = quality or "best"
        self.custom_title = title or ""

    def run(self):
        if not yt_dlp:
            self.download_error.emit("yt-dlp não está instalado.")
            return

        try:
            self.status_changed.emit("extracting", "🔍 Analisando link do YouTube...")

            target_dir = self.output_path or os.path.expanduser("~/Downloads")
            os.makedirs(target_dir, exist_ok=True)

            if self.custom_title:
                safe_title = self._sanitize(self.custom_title)
                out_template = os.path.join(target_dir, f"{safe_title}.%(ext)s")
            else:
                out_template = os.path.join(target_dir, "%(title)s.%(ext)s")

            if self.media_type == "audio":
                format_opt = "bestaudio/best"
            else:
                if self.quality == "1080p":
                    format_opt = "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
                elif self.quality == "720p":
                    format_opt = "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
                elif self.quality == "480p":
                    format_opt = "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
                else:
                    format_opt = "bestvideo+bestaudio/best"

            ydl_opts = {
                'outtmpl': out_template,
                'format': format_opt,
                'progress_hooks': [self._ydl_hook],
                'quiet': False,
                'no_warnings': True,
                'no_color': True,
                'noplaylist': True,
                'overwrites': True,           # Sobrescreve sem travar
                'force_overwrites': True,     # Força autorização sem prompt
                'ignoreerrors': 'only_download',
                'postprocessor_args': {
                    'ffmpeg': ['-y']          # Responde 'Sim' automaticamente para o FFmpeg
                },
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'ios', 'mweb', 'web']
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                }
            }

            if FFMPEG_PATH:
                ydl_opts['ffmpeg_location'] = FFMPEG_PATH

            self.status_changed.emit("downloading", "⬇️ Baixando mídia...")

            download_exception = None
            extracted_filename = None

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(self.media_url, download=True)
                    if info:
                        extracted_filename = ydl.prepare_filename(info)
            except Exception as e:
                download_exception = str(e)

            # Verifica se o arquivo físico foi gravado no disco
            final_filepath = self._find_downloaded_file(target_dir, extracted_filename)

            if final_filepath and os.path.exists(final_filepath) and os.path.getsize(final_filepath) > 0:
                self.progress_changed.emit({"percent": 100, "speed": "0 B/s", "eta": "00:00"})
                self.status_changed.emit("finished", "Concluído")
                self.download_finished.emit(final_filepath)
            else:
                err_msg = download_exception or "Não foi possível salvar o arquivo."
                self.download_error.emit(err_msg)

        except Exception as e:
            self.download_error.emit(f"Erro no download: {str(e)}")

    def _find_downloaded_file(self, target_dir: str, prepared_filename: str = None) -> str:
        """Verifica se o arquivo de vídeo foi salvo na pasta."""
        if prepared_filename and os.path.exists(prepared_filename):
            return prepared_filename

        if prepared_filename:
            base_path = os.path.splitext(prepared_filename)[0]
            for ext in ['.mp4', '.mkv', '.webm', '.m4a', '.mp3']:
                if os.path.exists(base_path + ext):
                    return base_path + ext

        if os.path.exists(target_dir):
            files = [
                os.path.join(target_dir, f) for f in os.listdir(target_dir)
                if f.endswith(('.mp4', '.mkv', '.webm', '.mp3', '.m4a')) and not f.endswith('.part') and not f.endswith('.ytdl')
            ]
            if files:
                files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                return files[0]

        return None

    def _ydl_hook(self, d):
        status = d.get('status')
        if status == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total * 100) if total > 0 else 0

            if percent >= 99.0:
                percent = 99.0
                self.status_changed.emit("processing", "⚡ Mesclando áudio e vídeo...")

            speed = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_speed_str', '0 B/s'))).strip()
            eta = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_eta_str', '--:--'))).strip()
            self.progress_changed.emit({"percent": percent, "speed": speed, "eta": eta})

        elif status == 'finished':
            self.status_changed.emit("processing", "⚡ Finalizando e salvando arquivo...")

    def _sanitize(self, text: str) -> str:
        if not text:
            return "Video"
        text = html.unescape(str(text))
        sanitized = re.sub(r'[\\/*?:"<>|]', "", text).strip()
        return sanitized if sanitized else "Video"