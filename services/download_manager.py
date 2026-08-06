"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Services
Class......: PRTDownloadItem / PRTDownloadManager / DownloadWorker

Description:
    Download Manager Service for PRT NEXUS powered by yt-dlp and PySide6 QThread.
    Tracks speed, size estimation, single video extraction, and Qt signals.

Developer..: Prof Rob Tech
===========================================================
"""

import os
import sys
import traceback
import yt_dlp
from dataclasses import dataclass
from PySide6.QtCore import QObject, QThread, Signal


@dataclass
class PRTDownloadItem:
    """Representa a estrutura de dados de um item na fila de downloads."""
    url: str
    id: str = ""
    title: str = "Analisando URL..."
    quality: str = "MAX"
    status: str = "Pendente"
    progress: float = 0.0
    speed: str = "---"
    size: str = "Calculando..."
    file_path: str = ""
    error: str = ""

    def __post_init__(self) -> None:
        if not self.id:
            self.id = self.url


class DownloadWorker(QThread):
    """Thread dedicada para processar o download sem travar a interface gráfica."""

    progress_updated = Signal(str, str, str, str, float, str)  # (url, title, speed, size, percentage, status)
    download_finished = Signal(str, str)                         # (url, final_file_path)
    download_failed = Signal(str, str)                           # (url, error_message)

    def __init__(self, url: str, save_folder: str, quality: str = "MAX") -> None:
        super().__init__()
        self.url = url.strip()
        self.save_folder = save_folder
        self.quality = quality
        self._is_cancelled = False

    def run(self) -> None:
        os.makedirs(self.save_folder, exist_ok=True)
        print(f"\n[PRT NEXUS] 🚀 Processando URL: {self.url}")

        ydl_opts = {
            "outtmpl": os.path.join(self.save_folder, "%(title)s.%(ext)s"),
            "progress_hooks": [self._yt_dlp_progress_hook],
            "noplaylist": True,
            "nocheckcertificate": True,
            "quiet": False,
            "no_warnings": False,
            "geo_bypass": True,
            "format": "best/bestvideo+bestaudio",
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            },
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if self._is_cancelled:
                    return

                info = ydl.extract_info(self.url, download=True)
                filename = ydl.prepare_filename(info)

                if not self._is_cancelled:
                    print(f"[PRT NEXUS] ✅ Download finalizado: {filename}")
                    self.download_finished.emit(self.url, filename)

        except yt_dlp.utils.DownloadError as e:
            clean_error = str(e).replace("ERROR: ", "").strip()
            print(f"❌ [ERRO YT-DLP]: {clean_error}")
            self.download_failed.emit(self.url, clean_error)
        except Exception as e:
            print(f"❌ [ERRO GERAL]: {e}")
            traceback.print_exc()
            self.download_failed.emit(self.url, str(e))

    def _yt_dlp_progress_hook(self, d: dict) -> None:
        if self._is_cancelled:
            raise Exception("Download cancelado pelo usuário.")

        status = d.get("status", "")
        if status == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded_bytes = d.get("downloaded_bytes", 0)

            percentage = (downloaded_bytes / total_bytes * 100) if total_bytes > 0 else 0.0
            speed_bytes = d.get("speed") or 0
            speed_str = self._format_bytes(speed_bytes) + "/s" if speed_bytes > 0 else "---"
            size_str = self._format_bytes(total_bytes) if total_bytes > 0 else "Calculando..."

            title = d.get("info_dict", {}).get("title", "Baixando vídeo...")

            self.progress_updated.emit(self.url, title, speed_str, size_str, percentage, "Baixando")

        elif status == "finished":
            total_bytes = d.get("total_bytes") or d.get("downloaded_bytes") or 0
            size_str = self._format_bytes(total_bytes) if total_bytes > 0 else "---"
            title = d.get("info_dict", {}).get("title", "Concluído")

            self.progress_updated.emit(self.url, title, "0 B/s", size_str, 100.0, "Concluído")

    def cancel(self) -> None:
        self._is_cancelled = True

    @staticmethod
    def _format_bytes(size: float) -> str:
        if not size or size <= 0:
            return "Calculando..."
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


class PRTDownloadManager(QObject):
    """Gerenciador Global de Downloads (Singleton)."""

    download_added = Signal(object)                              # Emite PRTDownloadItem
    download_removed = Signal(str)                               # Emite URL
    download_cleared = Signal()                                  # Emite quando limpa a lista
    cleared_signal = Signal()                                    # Compatibilidade
    title_updated = Signal(str, str)                             # (url, title)
    size_updated = Signal(str, str)                              # (url, size)
    speed_updated = Signal(str, str)                             # (url, speed)
    status_updated = Signal(str, str)                            # (url, status)
    progress_updated = Signal(str, str, str, str, float, str)  # (url, title, speed, size, percentage, status)
    download_finished = Signal(str, str)                         # (url, file_path)
    download_failed = Signal(str, str)                           # (url, error_message)

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = PRTDownloadManager()
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self._active_workers: dict[str, DownloadWorker] = {}
        self._download_items: dict[str, PRTDownloadItem] = {}
        self._default_download_folder = self._get_default_download_folder()

    @property
    def downloads(self) -> list[PRTDownloadItem]:
        return list(self._download_items.values())

    def _get_default_download_folder(self) -> str:
        user_home = os.path.expanduser("~")
        downloads_dir = os.path.join(user_home, "Downloads", "PRT NEXUS")
        os.makedirs(downloads_dir, exist_ok=True)
        return downloads_dir

    def get_download_folder(self) -> str:
        return self._default_download_folder

    def set_download_folder(self, folder_path: str) -> None:
        if folder_path and os.path.exists(folder_path):
            self._default_download_folder = folder_path

    def add_item(self, url: str, quality: str = "MAX") -> PRTDownloadItem:
        url = url.strip()
        if not url:
            return None

        if url in self._download_items:
            return self._download_items[url]

        item = PRTDownloadItem(url=url, id=url, quality=quality)
        self._download_items[url] = item
        self.download_added.emit(item)
        return item

    def add_download(self, url: str, quality: str = "MAX") -> PRTDownloadItem:
        url = url.strip()
        if not url:
            return None

        item = self.add_item(url, quality)
        self.start_download(url, quality)
        return item

    def get_items(self) -> list[PRTDownloadItem]:
        return self.downloads

    def remove_item(self, url: str) -> None:
        self.cancel_download(url)
        if url in self._download_items:
            del self._download_items[url]
            self.download_removed.emit(url)

    def clear_completed(self) -> None:
        to_remove = [
            url for url, item in self._download_items.items()
            if item.status in ("Concluído", "Erro")
        ]
        for url in to_remove:
            del self._download_items[url]
        self.download_cleared.emit()
        self.cleared_signal.emit()

    def pause_download(self, url: str) -> None:
        self.cancel_download(url)
        if url in self._download_items:
            self._download_items[url].status = "Pausado"
            self.status_updated.emit(url, "Pausado")

    def pause_all(self) -> None:
        for url in list(self._active_workers.keys()):
            self.pause_download(url)

    def resume_all(self) -> None:
        for url, item in self._download_items.items():
            if item.status in ("Pausado", "Pendente", "Erro"):
                self.start_download(url, item.quality)

    def start_download(
        self,
        url: str,
        quality: str = "MAX",
        on_progress=None,
        on_finished=None,
        on_failed=None,
    ) -> DownloadWorker:
        url = url.strip()
        if url in self._active_workers:
            worker = self._active_workers[url]
            if worker.isRunning():
                return worker

        if url not in self._download_items:
            self.add_item(url, quality)

        worker = DownloadWorker(url, self._default_download_folder, quality)

        worker.progress_updated.connect(self._handle_progress_updated)
        worker.download_finished.connect(self._handle_download_finished)
        worker.download_failed.connect(self._handle_download_failed)

        if on_progress:
            worker.progress_updated.connect(on_progress)
        if on_finished:
            worker.download_finished.connect(on_finished)
        if on_failed:
            worker.download_failed.connect(on_failed)

        self._active_workers[url] = worker
        worker.start()
        return worker

    def cancel_download(self, url: str) -> None:
        if url in self._active_workers:
            worker = self._active_workers[url]
            worker.cancel()
            worker.quit()
            worker.wait()
            self._cleanup_worker(url)

    def _handle_progress_updated(self, url: str, title: str, speed: str, size: str, percentage: float, status: str) -> None:
        if url in self._download_items:
            item = self._download_items[url]

            if title and item.title != title:
                item.title = title
                self.title_updated.emit(url, title)

            if status and item.status != status:
                item.status = status
                self.status_updated.emit(url, status)

            item.speed = speed
            item.size = size
            item.progress = percentage
            self.speed_updated.emit(url, speed)
            self.size_updated.emit(url, size)

        self.progress_updated.emit(url, title, speed, size, percentage, status)

    def _handle_download_finished(self, url: str, file_path: str) -> None:
        if url in self._download_items:
            item = self._download_items[url]
            item.status = "Concluído"
            item.progress = 100.0
            item.file_path = file_path
            self.status_updated.emit(url, "Concluído")

        self.download_finished.emit(url, file_path)
        self._cleanup_worker(url)

    def _handle_download_failed(self, url: str, error_message: str) -> None:
        if url in self._download_items:
            item = self._download_items[url]
            item.status = "Erro"
            item.error = error_message
            self.status_updated.emit(url, "Erro")

        self.download_failed.emit(url, error_message)
        self._cleanup_worker(url)

    def _cleanup_worker(self, url: str) -> None:
        if url in self._active_workers:
            del self._active_workers[url]


# === FIM DO ARQUIVO ===