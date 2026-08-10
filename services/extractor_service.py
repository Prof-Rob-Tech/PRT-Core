"""
===========================================================
PRT Labs - Services / Extractor Service
Class: ExtractorService

Description:
    Motor central de extração e download de mídias usando
    yt-dlp. Suporta YouTube, TikTok (sem marca d'água),
    Vimeo e links diretos.
===========================================================
"""

import os
import sys
from typing import Dict, Any, Callable, Optional

try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False


class ExtractorService:
    """Serviço de extração de mídias e conversão via yt-dlp."""

    def __init__(self, default_download_dir: Optional[str] = None) -> None:
        if default_download_dir:
            self.download_dir = default_download_dir
        else:
            self.download_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        if not os.path.exists(self.download_dir):
            try:
                os.makedirs(self.download_dir, exist_ok=True)
            except Exception:
                pass

    def extract_info(self, url: str) -> Dict[str, Any]:
        """Analisador de URL: Obtém títulos, thumbs e formatos sem realizar o download."""
        if not HAS_YTDLP:
            return {"error": "Biblioteca 'yt-dlp' não instalada no ambiente virtual."}

        opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'extract_flat': 'in_playlist',
        }

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    "title": info.get("title", "Mídia sem título"),
                    "uploader": info.get("uploader") or info.get("extractor", "Desconhecido"),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail", ""),
                    "formats_count": len(info.get("formats", [])),
                    "raw": info
                }
        except Exception as e:
            return {"error": str(e)}

    def download_media_task(self, task, progress_hook: Callable[[int, str, str], None]) -> str:
        """
        Executa o download real do vídeo/mídia e envia atualização via progress_hook.
        
        Args:
            task: Instância de DownloadTask contendo url, save_path, etc.
            progress_hook: Função callback (pct: int, speed: str, eta: str) -> None
        """
        if not HAS_YTDLP:
            raise RuntimeError("Biblioteca 'yt-dlp' não está instalada.")

        target_dir = task.save_path if task.save_path and os.path.exists(task.save_path) else self.download_dir

        # Callback interno do yt-dlp para conversão de métricas
        def _yt_dlp_progress_callback(d: dict):
            if d.get('status') == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

                # Porcentagem de progresso
                pct = int((downloaded / total) * 100) if total > 0 else 0

                # Velocidade de Download
                speed_bytes = d.get('speed') or 0
                if speed_bytes > 1024 * 1024:
                    speed_str = f"{speed_bytes / (1024 * 1024):.1f} MB/s"
                elif speed_bytes > 1024:
                    speed_str = f"{speed_bytes / 1024:.0f} KB/s"
                else:
                    speed_str = "0 KB/s"

                # Tempo Estimado (ETA)
                eta_sec = d.get('eta')
                if eta_sec is not None:
                    m, s = divmod(int(eta_sec), 60)
                    eta_str = f"{m:02d}:{s:02d}"
                else:
                    eta_str = "--:--"

                # Envia as métricas limpas para a QThread do DownloadManager
                progress_hook(pct, speed_str, eta_str)

        out_template = os.path.join(target_dir, "%(title)s.%(ext)s")

        ydl_opts = {
            'outtmpl': out_template,
            'progress_hooks': [_yt_dlp_progress_callback],
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo+bestaudio/best',
            'concurrent_fragment_downloads': 4,
            # Configurações específicas para extração limpa do TikTok sem marca d'água
            'extractor_args': {
                'tiktok': {
                    'app_version': '20.2.1',
                    'manifest_app_version': '20.2.1',
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(task.url, download=True)
            filename = ydl.prepare_filename(info)
            return filename


# Instância global do serviço
extractor_service = ExtractorService()