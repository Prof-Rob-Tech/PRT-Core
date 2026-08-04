"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Services
Class......: PRTDownloadManager

Description:
    Centralized singleton manager for tracking download state
    and simulating real-time download progress via QTimer.

Developer..: Prof Rob Tech
===========================================================
"""

import random
from typing import List, Optional
from PySide6.QtCore import QObject, QTimer, Signal


class PRTDownloadItem:
    """Represents a single download task."""

    def __init__(self, download_id: str, name: str, size_str: str) -> None:
        self.id = download_id
        self.name = name
        self.size_str = size_str
        self.progress = 0
        self.status = "Baixando"
        self.speed = "0.0 MB/s"


class PRTDownloadManager(QObject):
    """Singleton service for managing active downloads and simulation ticks."""

    download_added = Signal(object)
    progress_updated = Signal(str, int, str, str)  # (id, progress, speed, status)

    _instance: Optional["PRTDownloadManager"] = None

    @classmethod
    def instance(cls) -> "PRTDownloadManager":
        if cls._instance is None:
            cls._instance = PRTDownloadManager()
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.downloads: List[PRTDownloadItem] = []

        # Timer para atualizar a barra de progresso em tempo real
        self._timer = QTimer(self)
        self._timer.setInterval(700)  # Atualiza a cada 700ms
        self._timer.timeout.connect(self._simulate_tick)

        self._populate_initial_data()
        self._timer.start()

    def _populate_initial_data(self) -> None:
        """Carrega os downloads iniciais de demonstração."""
        item1 = PRTDownloadItem("dl_1", "Curso_Python_Completo_Aula01.mp4", "1.2 GB")
        item1.progress = 45
        item1.status = "Baixando"
        item1.speed = "6.4 MB/s"

        item2 = PRTDownloadItem("dl_2", "Design_System_Figma.zip", "350 MB")
        item2.progress = 100
        item2.status = "Concluído"
        item2.speed = "-"

        item3 = PRTDownloadItem("dl_3", "Apostila_DevOps.pdf", "15 MB")
        item3.progress = 12
        item3.status = "Pausado"
        item3.speed = "-"

        self.downloads.extend([item1, item2, item3])

    def add_download(self, url_or_name: str) -> PRTDownloadItem:
        """Adiciona um novo download e dispara os sinais da interface."""
        name = url_or_name.split("/")[-1] if "/" in url_or_name else url_or_name
        if not name or len(name) < 3 or name.startswith("http"):
            name = f"Curso_Download_{len(self.downloads) + 1}.mp4"

        download_id = f"dl_{len(self.downloads) + 1}"
        size_mb = random.randint(200, 1800)
        size_str = f"{size_mb} MB" if size_mb < 1000 else f"{round(size_mb / 1024, 1)} GB"

        item = PRTDownloadItem(download_id, name, size_str)
        item.progress = 0
        item.status = "Baixando"
        item.speed = "2.1 MB/s"

        self.downloads.append(item)
        self.download_added.emit(item)
        return item

    def _simulate_tick(self) -> None:
        """Simula a evolução do progresso de downloads ativos."""
        for item in self.downloads:
            if item.status == "Baixando":
                item.progress += random.randint(2, 6)
                speed_val = round(random.uniform(4.0, 9.8), 1)
                item.speed = f"{speed_val} MB/s"

                if item.progress >= 100:
                    item.progress = 100
                    item.status = "Concluído"
                    item.speed = "-"

                self.progress_updated.emit(
                    item.id, item.progress, item.speed, item.status
                )