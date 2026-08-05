"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Services
Class......: PRTDownloadManager

Description:
    Singleton download manager supporting active tasks management,
    quality options, progress tracking, cancellation, and tray control.

Developer..: Prof Rob Tech
===========================================================
"""

import os
from typing import Dict, List, Optional
from PySide6.QtCore import QObject, Signal

from services.yt_dlp_worker import YTDLWorker


class PRTDownloadItem:
    """Representa uma tarefa de download."""

    def __init__(self, download_id: str, url: str, name: str, size_str: str, quality: str = "best") -> None:
        self.id = download_id
        self.url = url
        self.name = name
        self.size_str = size_str
        self.quality = quality
        self.progress = 0
        self.status = "Iniciando..."
        self.speed = "0.0 KB/s"


class PRTDownloadManager(QObject):
    """Gerenciador central de downloads (Singleton)."""

    download_added = Signal(object)
    progress_updated = Signal(str, int, str, str)
    title_updated = Signal(str, str)
    size_updated = Signal(str, str)
    download_completed = Signal(str)
    cleared_signal = Signal()

    _instance: Optional["PRTDownloadManager"] = None

    @classmethod
    def instance(cls) -> "PRTDownloadManager":
        if cls._instance is None:
            cls._instance = PRTDownloadManager()
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.downloads: List[PRTDownloadItem] = []
        self._workers: Dict[str, YTDLWorker] = {}

        self._download_folder = os.path.join(
            os.path.expanduser("~"), "Downloads", "PRT NEXUS"
        )
        os.makedirs(self._download_folder, exist_ok=True)

    def get_download_folder(self) -> str:
        return self._download_folder

    def set_download_folder(self, folder_path: str) -> None:
        if folder_path and os.path.exists(folder_path):
            self._download_folder = folder_path
            os.makedirs(self._download_folder, exist_ok=True)

    def add_download(self, url_or_name: str, quality: str = "best") -> PRTDownloadItem:
        """Adiciona um novo download com qualidade especificada."""
        download_id = f"dl_{len(self.downloads) + 1}"
        is_real_url = url_or_name.startswith("http://") or url_or_name.startswith("https://")

        display_name = url_or_name.split("/")[-1] if "/" in url_or_name else url_or_name
        if not display_name or is_real_url:
            display_name = "Analisando URL..."

        item = PRTDownloadItem(download_id, url_or_name, display_name, "Calculando...", quality)
        self.downloads.append(item)
        self.download_added.emit(item)

        if is_real_url:
            self._start_worker(item)

        return item

    def pause_download(self, download_id: str) -> None:
        if download_id in self._workers:
            self._workers[download_id].pause()

    def resume_download(self, download_id: str) -> None:
        for item in self.downloads:
            if item.id == download_id and item.status in ["Pausado", "Erro"]:
                item.status = "Iniciando..."
                self.progress_updated.emit(download_id, item.progress, "0.0 KB/s", "Iniciando...")
                self._start_worker(item)
                break

    def pause_all(self) -> None:
        for item in self.downloads:
            if item.status == "Baixando":
                self.pause_download(item.id)

    def resume_all(self) -> None:
        for item in self.downloads:
            if item.status in ["Pausado", "Erro"]:
                self.resume_download(item.id)

    def cancel_download(self, download_id: str) -> None:
        if download_id in self._workers:
            self._workers[download_id].cancel()

        self.downloads = [item for item in self.downloads if item.id != download_id]
        self.cleared_signal.emit()

    def clear_completed(self) -> None:
        self.downloads = [
            item for item in self.downloads
            if item.status not in ["Concluído", "Concluido", "Cancelado"] and not item.status.startswith("Erro")
        ]
        self.cleared_signal.emit()

    def _start_worker(self, item: PRTDownloadItem) -> None:
        worker = YTDLWorker(
            download_id=item.id,
            url=item.url,
            output_dir=self.get_download_folder(),
            quality=item.quality
        )
        worker.progress_signal.connect(self._on_worker_progress)
        worker.title_signal.connect(self._on_worker_title)
        worker.size_signal.connect(self._on_worker_size)
        worker.finished_signal.connect(self._on_worker_finished)

        self._workers[item.id] = worker
        worker.start()

    def _on_worker_progress(self, download_id: str, progress: int, speed: str, status: str) -> None:
        for item in self.downloads:
            if item.id == download_id:
                item.progress = progress
                item.speed = speed
                item.status = status
                self.progress_updated.emit(download_id, progress, speed, status)
                break

    def _on_worker_title(self, download_id: str, title: str) -> None:
        for item in self.downloads:
            if item.id == download_id:
                item.name = title
                self.title_updated.emit(download_id, item.name)
                break

    def _on_worker_size(self, download_id: str, size_str: str) -> None:
        for item in self.downloads:
            if item.id == download_id:
                if item.size_str != size_str:
                    item.size_str = size_str
                    self.size_updated.emit(download_id, size_str)
                break

    def _on_worker_finished(self, download_id: str, status: str) -> None:
        for item in self.downloads:
            if item.id == download_id:
                item.status = status
                item.speed = "-"
                if status == "Concluído":
                    item.progress = 100
                    self.download_completed.emit(item.name)
                self.progress_updated.emit(download_id, item.progress, "-", status)
                break

        if download_id in self._workers:
            del self._workers[download_id]