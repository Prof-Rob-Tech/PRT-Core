"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Services
Class......: YTDLWorker

Description:
    Background QThread executing yt-dlp with single-stream format
    selection (no FFmpeg dependency), pause, and cancellation.

Developer..: Prof Rob Tech
===========================================================
"""

import os
import re
from PySide6.QtCore import QThread, Signal

try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False


class YTDLWorker(QThread):
    """Worker thread running yt-dlp smoothly in background."""

    progress_signal = Signal(str, int, str, str)  # (id, progress_percent, speed_str, status_str)
    title_signal = Signal(str, str)               # (id, title)
    size_signal = Signal(str, str)                # (id, size_str)
    finished_signal = Signal(str, str)            # (id, final_status)

    def __init__(self, download_id: str, url: str, output_dir: str) -> None:
        super().__init__()
        self.download_id = download_id
        self.url = url
        self.output_dir = output_dir

        self._is_paused = False
        self._is_cancelled = False
        self._title_extracted = False

    def pause(self) -> None:
        """Solicita a pausa da execução."""
        self._is_paused = True

    def cancel(self) -> None:
        """Solicita o cancelamento da execução."""
        self._is_cancelled = True

    def run(self) -> None:
        if not HAS_YTDLP:
            self.finished_signal.emit(self.download_id, "Erro: yt-dlp não instalado")
            return

        out_template = os.path.join(self.output_dir, "%(title)s.%(ext)s")

        # 'best' pega o melhor arquivo pré-combinado (vídeo + áudio num único stream)
        # dispensando 100% a necessidade de ter o FFmpeg instalado na máquina!
        ydl_opts = {
            "outtmpl": out_template,
            "progress_hooks": [self._progress_hook],
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "no_color": True,
            "nocheckcertificate": True,
            "format": "best",
        }

        try:
            self.progress_signal.emit(self.download_id, 0, "0.0 KB/s", "Conectando...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            if not self._is_paused and not self._is_cancelled:
                self.finished_signal.emit(self.download_id, "Concluído")

        except Exception as e:
            err_msg = str(e)
            if "USER_PAUSED" in err_msg:
                self.finished_signal.emit(self.download_id, "Pausado")
            elif "USER_CANCELLED" in err_msg:
                self.finished_signal.emit(self.download_id, "Cancelado")
            else:
                clean_err = re.sub(r"\x1b\[[0-9;]*m", "", err_msg)
                clean_err = clean_err.replace("ERROR:", "").replace("\n", " ").strip()[:40]
                self.finished_signal.emit(self.download_id, f"Erro: {clean_err}")

    def _progress_hook(self, d: dict) -> None:
        """Hook chamado a cada bloco baixado pelo yt-dlp."""
        if self._is_cancelled:
            raise Exception("USER_CANCELLED")
        if self._is_paused:
            raise Exception("USER_PAUSED")

        # Puxa o título real na primeira oportunidade
        if not self._title_extracted:
            info = d.get("info_dict", {})
            title = info.get("title")
            if title:
                self.title_signal.emit(self.download_id, title)
                self._title_extracted = True

        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)

            if total > 0:
                percent = int((downloaded / total) * 100)
                size_mb = total / (1024 * 1024)
                self.size_signal.emit(self.download_id, f"{size_mb:.1f} MB")
            else:
                percent = 0

            speed = d.get("speed", 0)
            speed_str = self._format_speed(speed) if speed else "0.0 KB/s"

            self.progress_signal.emit(self.download_id, percent, speed_str, "Baixando")

        elif d["status"] == "finished":
            self.progress_signal.emit(self.download_id, 100, "-", "Concluído")

    def _format_speed(self, speed_bytes: float) -> str:
        if speed_bytes >= 1024 * 1024:
            return f"{speed_bytes / (1024 * 1024):.1f} MB/s"
        elif speed_bytes >= 1024:
            return f"{speed_bytes / 1024:.1f} KB/s"
        return f"{speed_bytes:.1f} B/s"