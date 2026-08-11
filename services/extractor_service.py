"""
===========================================================
PRT Labs - Services
Class: ExtractorService / extractor_service

Description:
    Serviço de extração avançado via yt-dlp com suporte a cancelamento,
    limpeza de temporários e seleção de qualidade/áudio.
===========================================================
"""

import os
import glob
from typing import Callable, Optional

try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    yt_dlp = None
    HAS_YTDLP = False


class ExtractorService:
    """Serviço responsável pela execução dos downloads via yt-dlp."""

    def __init__(self, download_dir: Optional[str] = None) -> None:
        if download_dir is None:
            user_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
            self.download_dir = os.path.join(user_downloads, "PRT_Nexus")
        else:
            self.download_dir = download_dir

        os.makedirs(self.download_dir, exist_ok=True)

    def _cleanup_temp_files(self, target_dir: str) -> None:
        """Remove arquivos temporários (.part, .ytdl) em caso de cancelamento."""
        try:
            temp_files = glob.glob(os.path.join(target_dir, "*.part")) + glob.glob(os.path.join(target_dir, "*.ytdl"))
            for temp_f in temp_files:
                if os.path.exists(temp_f):
                    os.remove(temp_f)
        except Exception as e:
            print(f"⚠️ Erro ao limpar arquivos temporários: {e}")

    def download_media_task(self, task, progress_hook: Callable) -> str:
        if not HAS_YTDLP:
            raise RuntimeError("A biblioteca 'yt-dlp' não está instalada no ambiente.")

        target_dir = task.save_path if task.save_path and os.path.exists(task.save_path) else self.download_dir
        out_template = os.path.join(target_dir, "%(title)s.%(ext)s")

        def _fmt_size(bytes_val: float) -> str:
            if not bytes_val or bytes_val <= 0:
                return "-- MB"
            if bytes_val >= 1024 * 1024 * 1024:
                return f"{bytes_val / (1024 * 1024 * 1024):.2f} GB"
            return f"{bytes_val / (1024 * 1024):.1f} MB"

        def _yt_dlp_progress_callback(d: dict):
            # 1. Checa interrupção/cancelamento
            if getattr(task, "is_cancelled", False):
                raise RuntimeError("CANCELLED_BY_USER")

            # 2. Captura o título real
            info = d.get('info_dict', {})
            real_title = info.get('title') or info.get('fulltitle')
            if real_title:
                task.title = real_title

            if d.get('status') == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

                pct = int((downloaded / total) * 100) if total > 0 else 0
                size_str = f"{_fmt_size(downloaded)} / {_fmt_size(total)}"

                speed_bytes = d.get('speed') or 0
                if speed_bytes > 1024 * 1024:
                    speed_str = f"{speed_bytes / (1024 * 1024):.1f} MB/s"
                elif speed_bytes > 1024:
                    speed_str = f"{speed_bytes / 1024:.0f} KB/s"
                else:
                    speed_str = "0 KB/s"

                eta_sec = d.get('eta')
                if eta_sec is not None:
                    m, s = divmod(int(eta_sec), 60)
                    eta_str = f"{m:02d}:{s:02d}"
                else:
                    eta_str = "--:--"

                try:
                    progress_hook(pct, speed_str, eta_str, size_str)
                except TypeError:
                    progress_hook(pct, speed_str, eta_str)

        # Seleção Dinâmica de Qualidade e Formato
        format_spec = 'b[ext=mp4]/b/best'
        if getattr(task, 'format_type', 'video') == 'audio':
            format_spec = 'bestaudio/best'
        elif getattr(task, 'quality', 'best') == '1080p':
            format_spec = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]'
        elif getattr(task, 'quality', 'best') == '720p':
            format_spec = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]'

        ydl_opts = {
            'outtmpl': out_template,
            'progress_hooks': [_yt_dlp_progress_callback],
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'format': format_spec,
            'concurrent_fragment_downloads': 4,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(task.url, download=True)
                filename = ydl.prepare_filename(info)
                return filename
        except Exception as e:
            # Se for cancelamento, limpa resíduos temporários do disco
            if "CANCELLED_BY_USER" in str(e) or getattr(task, "is_cancelled", False):
                self._cleanup_temp_files(target_dir)
                raise RuntimeError("CANCELLED_BY_USER")
            raise e


# Instância Singleton
extractor_service = ExtractorService()