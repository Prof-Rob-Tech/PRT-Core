"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Services
Class......: PRTDownloadManager

Description:
    Singleton download manager supporting active tasks management,
    progress tracking, cancellation, pause/resume, and tray control.

Developer..: Prof Rob Tech
===========================================================
"""

import os
import uuid
from typing import Dict, List, Optional
from PySide6.QtCore import QObject, Signal

from services.yt_dlp_worker import PRTYtDlpWorker


class DownloadItem:
    """Modelo de dados para representar um item de download."""

    def __init__(self, url: str, title: str, save_path: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.url: str = url
        self.title: str = title
        self.save_path: str = save_path
        self.progress: int = 0
        self.speed: str = "-"
        self.size_mb: str = "0.0 MB"
        self.status: str = "Aguardando"  # Aguardando, Baixando, Pausado, Concluído, Erro, Cancelado
        self.worker: Optional[PRTYtDlpWorker] = None


class PRTDownloadManager(QObject):
    """Gerenciador central de downloads (Singleton)."""

    _instance: Optional["PRTDownloadManager"] = None

    progress_updated = Signal(str, int, str, str)  # id, progress, speed, status
    download_completed = Signal(str)               # title
    cleared_signal = Signal()                      # emitido ao limpar concluídos

    def __init__(self) -> None:
        super().__init__()
        self.downloads: List[DownloadItem] = []
        self._download_folder = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "downloads")
        )
        if not os.path.exists(self._download_folder):
            os.makedirs(self._download_folder, exist_ok=True)

    @classmethod
    def instance(cls) -> "PRTDownloadManager":
        if cls._instance is None:
            cls._instance = PRTDownloadManager()
        return cls._instance

    def get_download_folder(self) -> str:
        return self._download_folder

    def set_download_folder(self, path: str) -> None:
        if path and os.path.exists(path):
            self._download_folder = path

    def add_download(self, url: str) -> DownloadItem:
        title = url.split("/")[-1] or "Download"
        item = DownloadItem(url, title, self._download_folder)
        self.downloads.append(item)
        self.start_download(item.id)
        return item

    def start_download(self, download_id: str) -> None:
        item = self._get_item_by_id(download_id)
        if not item:
            return

        item.status = "Baixando"

        worker = PRTYtDlpWorker(item.url, item.save_path)
        item.worker = worker

        worker.progress_signal.connect(
            lambda prog, spd, title, d_id=download_id: self._on_worker_progress(d_id, prog, spd, title)
        )
        worker.finished_signal.connect(
            lambda success, msg, title, d_id=download_id: self._on_worker_finished(d_id, success, msg, title)
        )

        worker.start()

    def pause_download(self, download_id: str) -> None:
        item = self._get_item_by_id(download_id)
        if item and item.worker and item.status == "Baixando":
            item.status = "Pausado"
            item.worker.cancel()
            self.progress_updated.emit(item.id, item.progress, "-", "Pausado")

    def resume_download(self, download_id: str) -> None:
        item = self._get_item_by_id(download_id)
        if item and item.status == "Pausado":
            self.start_download(download_id)

    def pause_all(self) -> None:
        """Pausa todos os downloads que estão em andamento."""
        for item in self.downloads:
            if item.status == "Baixando":
                self.pause_download(item.id)

    def resume_all(self) -> None:
        """Retoma todos os downloads pausados."""
        for item in self.downloads:
            if item.status == "Pausado":
                self.resume_download(item.id)

    def cancel_download(self, download_id: str) -> None:
        item = self._get_item_by_id(download_id)
        if item:
            if item.worker:
                item.worker.cancel()
            item.status = "Cancelado"
            self.progress_updated.emit(item.id, item.progress, "-", "Cancelado")

    def clear_completed(self) -> None:
        self.downloads = [d for d in self.downloads if d.status not in ["Concluído", "Cancelado"]]
        self.cleared_signal.emit()

    def _on_worker_progress(self, download_id: str, progress: int, speed: str, title: str) -> None:
        item = self._get_item_by_id(download_id)
        if item:
            item.progress = progress
            item.speed = speed
            if title and item.title != title:
                item.title = title
            self.progress_updated.emit(item.id, item.progress, item.speed, item.status)

    def _on_worker_finished(self, download_id: str, success: bool, msg: str, title: str) -> None:
        item = self._get_item_by_id(download_id)
        if item:
            if title:
                item.title = title

            if success:
                item.status = "Concluído"
                item.progress = 100
                item.speed = "-"
                self.download_completed.emit(item.title)
            elif item.status != "Pausado" and item.status != "Cancelado":
                item.status = "Erro"

            self.progress_updated.emit(item.id, item.progress, item.speed, item.status)

    def _get_item_by_id(self, download_id: str) -> Optional[DownloadItem]:
        for d in self.downloads:
            if d.id == download_id:
                return d
        return None