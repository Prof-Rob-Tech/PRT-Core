"""
===========================================================
PRT Labs - Core / YouTube Download Worker
File: core/download/youtube_worker.py
===========================================================
"""

import html
import os
import re
import time
from PySide6.QtCore import QThread, Signal, QTimer

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_PATH = None

# Mantém referências fortes às threads ativas para evitar destruição prematura pelo Garbage Collector do Python
GLOBAL_YOUTUBE_REGISTRY = set()


class YouTubeDownloadWorker(QThread):
    """Worker de download altamente resistente a bloqueios do YouTube e erros de ciclo de vida de QThread."""

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
        self._is_cancelled = False

        # Registra na memória global para impedir que a thread seja destruída antes da hora
        GLOBAL_YOUTUBE_REGISTRY.add(self)
        self.finished.connect(self._on_qt_finished)

    def _on_qt_finished(self):
        """MANTÉM a referência viva por 15 segundos após o término para evitar 'QThread: Destroyed while thread is still running'."""
        QTimer.singleShot(15000, lambda: GLOBAL_YOUTUBE_REGISTRY.discard(self))

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        if not yt_dlp:
            self.progress_changed.emit({"percent": 0, "speed": "0 B/s", "eta": "00:00"})
            self.status_changed.emit("error", "Erro")
            self.download_error.emit("yt-dlp não está instalado.")
            return

        try:
            self.status_changed.emit("extracting", "🔍 Analisando vídeo...")

            target_dir = self.output_path or os.path.expanduser("~/Downloads")
            os.makedirs(target_dir, exist_ok=True)

            if self.custom_title:
                safe_title = self._sanitize(self.custom_title)
                out_template = os.path.join(target_dir, f"{safe_title}.%(ext)s")
            else:
                out_template = os.path.join(target_dir, "%(title)s.%(ext)s")

            # Formato flexível para garantir compatibilidade e mesclagem
            if self.media_type == "audio":
                format_opt = "bestaudio[ext=m4a]/bestaudio/best"
            else:
                format_opt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/bestvideo+bestaudio/best"

            ydl_opts = {
                'outtmpl': out_template,
                'format': format_opt,
                'merge_output_format': 'mp4',
                'progress_hooks': [self._ydl_hook],
                'postprocessor_hooks': [self._pp_hook],
                'quiet': True,
                'no_warnings': True,
                'no_color': True,
                'noplaylist': True,
                'overwrites': True,
                'force_overwrites': True,
                'nocheckcertificate': True,
                'geo_bypass': True,
                'retries': 10,
                'fragment_retries': 10,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['mweb', 'ios', 'android', 'web', 'tv'],
                        'player_skip': ['webpage', 'configs']
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                }
            }

            if FFMPEG_PATH and os.path.exists(FFMPEG_PATH):
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

            if self._is_cancelled:
                self.progress_changed.emit({"percent": 0, "speed": "0 B/s", "eta": "00:00"})
                self.status_changed.emit("error", "Cancelado")
                return

            # Procura pelo arquivo baixado (com fallbacks inteligentes)
            final_filepath = self._find_downloaded_file(target_dir, extracted_filename)

            if final_filepath and os.path.exists(final_filepath) and os.path.getsize(final_filepath) > 0:
                # EMITE OS SINAIS DE SUCESSO
                self.progress_changed.emit({"percent": 100, "speed": "0 B/s", "eta": "00:00"})
                self.status_changed.emit("finished", "Concluído")
                self.download_finished.emit(final_filepath)
                # PAUSA DE 300ms PARA GARANTIR QUE A MAIN THREAD DA INTERFACE PROCESSE OS SINAIS ANTES DA THREAD ENCERRAR
                self.msleep(300)
                return

            # Trata falha se não encontrou o arquivo final
            err_msg = download_exception or "Não foi possível encontrar o arquivo baixado."
            if "rate-limited" in err_msg.lower() or "this content isn't available" in err_msg.lower():
                err_msg = "Bloqueio temporário do YouTube (Rate Limit). Tente novamente em instantes."

            self.progress_changed.emit({"percent": 0, "speed": "0 B/s", "eta": "00:00"})
            self.status_changed.emit("error", "Erro no Download")
            self.download_error.emit(err_msg)
            self.msleep(200)

        except Exception as e:
            self.progress_changed.emit({"percent": 0, "speed": "0 B/s", "eta": "00:00"})
            self.status_changed.emit("error", "Erro no Download")
            self.download_error.emit(f"Erro no download: {str(e)}")
            self.msleep(200)

    def _find_downloaded_file(self, target_dir: str, prepared_filename: str = None) -> str:
        # 1. Título customizado
        if self.custom_title:
            safe_title = self._sanitize(self.custom_title)
            for ext in ['.mp4', '.mkv', '.webm', '.m4a', '.mp3']:
                candidate = os.path.join(target_dir, f"{safe_title}{ext}")
                if os.path.exists(candidate) and os.path.getsize(candidate) > 0:
                    return candidate

        # 2. Nome retornado pelo yt-dlp diretamente
        if prepared_filename and os.path.exists(prepared_filename) and os.path.getsize(prepared_filename) > 0:
            return prepared_filename

        # 3. Nome sem sufixos temporários (.f399, etc)
        if prepared_filename:
            clean_path = re.sub(r'\.f\d+', '', prepared_filename)
            clean_path = os.path.splitext(clean_path)[0]
            for ext in ['.mp4', '.mkv', '.webm', '.m4a', '.mp3']:
                candidate = clean_path + ext
                if os.path.exists(candidate) and os.path.getsize(candidate) > 0:
                    return candidate

        # 4. Fallback de Segurança: Arquivo mais recente criado na pasta nos últimos 5 minutos
        try:
            now = time.time()
            candidates = []
            for fname in os.listdir(target_dir):
                fpath = os.path.join(target_dir, fname)
                if os.path.isfile(fpath) and not fname.endswith('.part') and not fname.endswith('.ytdl'):
                    mtime = os.path.getmtime(fpath)
                    if (now - mtime) < 300:
                        candidates.append((mtime, fpath))
            if candidates:
                candidates.sort(key=lambda x: x[0], reverse=True)
                return candidates[0][1]
        except Exception:
            pass

        return None

    def _ydl_hook(self, d):
        if self._is_cancelled:
            raise Exception("Download cancelado pelo usuário.")

        status = d.get('status')
        if status == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total * 90.0) if total > 0 else 0

            speed = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_speed_str', '0 B/s'))).strip()
            eta = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_eta_str', '--:--'))).strip()
            self.progress_changed.emit({"percent": percent, "speed": speed, "eta": eta})

        elif status == 'finished':
            self.progress_changed.emit({"percent": 92.0, "speed": "FFmpeg", "eta": "00:01"})
            self.status_changed.emit("processing", "⚡ Mesclando áudio e vídeo...")

    def _pp_hook(self, d):
        if self._is_cancelled:
            raise Exception("Download cancelado pelo usuário.")

        status = d.get('status')
        if status == 'finished':
            self.progress_changed.emit({"percent": 98.0, "speed": "Finalizando", "eta": "00:00"})
            self.status_changed.emit("processing", "💾 Salvando mídia...")

    def _sanitize(self, text: str) -> str:
        if not text:
            return "Video"
        text = html.unescape(str(text))
        sanitized = re.sub(r'[\\/*?:"<>|]', "", text).strip()
        return sanitized if sanitized else "Video"