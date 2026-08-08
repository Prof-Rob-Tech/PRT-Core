"""
===========================================================
PRT Labs - Core / Download
Class: PRTDownloadWorker

Description:
    Worker assíncrono (QThread) para download de vídeos e streams
    utilizando yt-dlp e FFmpeg. Emite sinais de progresso,
    velocidade, tempo restante e alteração de estado.
===========================================================
"""

import os
from PySide6.QtCore import QThread, Signal
import yt_dlp


class PRTDownloadWorker(QThread):
    """Worker de download executado em thread separada para não congelar a UI."""

    # Sinais Qt para atualizar a barra de progresso e status na UI
    progress_changed = Signal(dict)  # {"percent": float, "speed": str, "eta": str}
    status_changed = Signal(str, str)  # (status_code, status_message)
    download_finished = Signal(str)  # filepath final
    download_error = Signal(str)  # mensagem de erro

    def __init__(self, media_url: str, output_path: str, parent=None) -> None:
        super().__init__(parent)
        self.media_url = media_url
        self.output_path = output_path
        self._is_cancelled = False

    def run(self) -> None:
        """Execução assíncrona do download."""
        self.status_changed.emit("DOWNLOADING", "Iniciando download...")

        # Certifica que a pasta de destino existe
        os.makedirs(self.output_path, exist_ok=True)

        ydl_opts = {
            "outtmpl": os.path.join(self.output_path, "%(title)s.%(ext)s"),
            "progress_hooks": [self._yt_dlp_hook],
            "quiet": True,
            "no_warnings": True,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.media_url, download=True)
                filename = ydl.prepare_filename(info)

                # Se juntou em mp4
                base_name, _ = os.path.splitext(filename)
                final_file = (
                    f"{base_name}.mp4"
                    if os.path.exists(f"{base_name}.mp4")
                    else filename
                )

                if not self._is_cancelled:
                    self.status_changed.emit(
                        "COMPLETED", "Download concluído com sucesso!"
                    )
                    self.download_finished.emit(final_file)

        except Exception as e:
            if not self._is_cancelled:
                err_msg = str(e)
                print(f"❌ [PRT Downloader Error]: {err_msg}")
                self.status_changed.emit("ERROR", err_msg)
                self.download_error.emit(err_msg)

    def _yt_dlp_hook(self, d: dict) -> None:
        """Hook chamado pelo yt-dlp para reportar progresso."""
        if self._is_cancelled:
            raise Exception("Download cancelado pelo usuário.")

        if d.get("status") == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded_bytes = d.get("downloaded_bytes") or 0

            percent = (
                (downloaded_bytes / total_bytes * 100) if total_bytes > 0 else 0.0
            )
            speed = d.get("_speed_str", "N/A")
            eta = d.get("_eta_str", "N/A")

            self.progress_changed.emit(
                {
                    "percent": percent,
                    "speed": speed,
                    "eta": eta,
                    "downloaded_bytes": downloaded_bytes,
                    "total_bytes": total_bytes,
                }
            )

    def cancel(self) -> None:
        """Cancela o download em andamento."""
        self._is_cancelled = True
        self.status_changed.emit("CANCELLED", "Download cancelado.")