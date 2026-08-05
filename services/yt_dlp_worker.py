"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Services
Class......: YTDLWorker

Description:
    Robust QThread worker for yt-dlp with clean speed formatting,
    ANSI escape code stripping, and fallback for systems without FFmpeg.

Developer..: Prof Rob Tech
===========================================================
"""

import os
import re
from typing import Any, Dict
from PySide6.QtCore import QThread, Signal
import yt_dlp


def clean_ansi(text: str) -> str:
    """Remove códigos de cores ANSI (ex: \x1b[0;32m) do texto."""
    return re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text).strip()


class YTDLWorker(QThread):
    """Worker de execução em segundo plano do yt-dlp."""

    progress_signal = Signal(str, int, str, str)  # (id, progress %, speed, status)
    title_signal = Signal(str, str)               # (id, title)
    size_signal = Signal(str, str)                # (id, size_str)
    finished_signal = Signal(str, str)            # (id, final_status)

    def __init__(
        self,
        download_id: str,
        url: str,
        output_dir: str,
        quality: str = "best"
    ) -> None:
        super().__init__()
        self.download_id = download_id
        self.url = url
        self.output_dir = output_dir
        self.quality = quality
        self._is_cancelled = False

    def run(self) -> None:
        """Executa o download usando yt-dlp com fallback sem necessidade de FFmpeg."""
        outtmpl = os.path.join(self.output_dir, "%(title)s.%(ext)s")

        # Configuração de formato seguro
        if self.quality == "1080p":
            format_selector = "best[height<=1080]/b[height<=1080]/bestvideo+bestaudio/best"
        elif self.quality == "720p":
            format_selector = "best[height<=720]/b[height<=720]/bestvideo+bestaudio/best"
        elif self.quality == "480p":
            format_selector = "best[height<=480]/b[height<=480]/bestvideo+bestaudio/best"
        elif self.quality == "mp3":
            format_selector = "bestaudio/best"
        else:
            format_selector = "b/best/bestvideo+bestaudio"

        ydl_opts: Dict[str, Any] = {
            "format": format_selector,
            "outtmpl": outtmpl,
            "progress_hooks": [self._progress_hook],
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "color": "never",
            "nocolor": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                if info:
                    title = info.get("title", "Vídeo sem título")
                    self.title_signal.emit(self.download_id, title)

                ydl.download([self.url])

            if not self._is_cancelled:
                self.finished_signal.emit(self.download_id, "Concluído")
        except Exception as e:
            err_msg = str(e)
            print(f"[YTDL Error Full Trace]: {err_msg}")

            if self._is_cancelled:
                self.finished_signal.emit(self.download_id, "Cancelado")
            elif "ffmpeg" in err_msg.lower():
                self.finished_signal.emit(self.download_id, "Erro: Requer FFmpeg")
            else:
                short_err = clean_ansi(err_msg.split("\n")[0])[:25]
                self.finished_signal.emit(self.download_id, f"Erro: {short_err}")

    def _progress_hook(self, d: Dict[str, Any]) -> None:
        if self._is_cancelled:
            raise Exception("Download cancelado pelo usuário.")

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)

            if total > 0:
                percent = int((downloaded / total) * 100)
                size_mb = total / (1024 * 1024)
                size_str = f"{size_mb:.1f} MB"
                self.size_signal.emit(self.download_id, size_str)
            else:
                percent = 0

            # Formatação limpa de velocidade sem códigos ANSI
            speed_bytes = d.get("speed")
            if speed_bytes and isinstance(speed_bytes, (int, float)):
                if speed_bytes >= 1024 * 1024:
                    speed = f"{speed_bytes / (1024 * 1024):.2f} MB/s"
                elif speed_bytes >= 1024:
                    speed = f"{speed_bytes / 1024:.1f} KB/s"
                else:
                    speed = f"{speed_bytes:.0f} B/s"
            else:
                raw_speed = d.get("_speed_str", "")
                speed = clean_ansi(raw_speed) if raw_speed else "0.0 KB/s"

            self.progress_signal.emit(self.download_id, percent, speed, "Baixando")

        elif d["status"] == "finished":
            self.progress_signal.emit(self.download_id, 100, "-", "Processando...")

    def cancel(self) -> None:
        self._is_cancelled = True