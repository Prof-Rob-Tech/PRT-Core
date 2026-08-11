"""
===========================================================
PRT Labs - Core
Class: DownloadManager / DownloadTask

Description:
    Gerenciador global de fila de downloads assíncronos com PySide6 QThread,
    suporte a cancelamento, seleção de qualidade e múltiplos status.
===========================================================
"""

import uuid
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, List, Callable
from PySide6.QtCore import QObject, QThread, Signal, Slot


class TaskStatus(Enum):
    QUEUED = "Aguardando..."
    DOWNLOADING = "Baixando..."
    COMPLETED = "Concluído"
    FAILED = "Erro no Download"
    CANCELLED = "Cancelado"


@dataclass
class DownloadTask:
    task_id: str
    url: str
    title: str = "Aguardando..."
    platform: str = "web"
    progress: int = 0
    speed: str = "0 KB/s"
    eta: str = "--:--"
    file_size: str = "-- MB"
    format_type: str = "video"  # "video" ou "audio"
    quality: str = "best"        # "best", "1080p", "720p", "audio"
    status: TaskStatus = TaskStatus.QUEUED
    save_path: str = ""
    is_cancelled: bool = False


class DownloadWorker(QThread):
    """Worker Thread responsável por executar a extração em background sem travar a UI."""

    task_started = Signal(object)
    task_updated = Signal(object)
    task_completed = Signal(object)
    task_failed = Signal(object, str)

    def __init__(self, task: DownloadTask, engine: Optional[Callable] = None, parent=None) -> None:
        super().__init__(parent)
        self.task = task
        self.engine = engine

    def run(self) -> None:
        if self.task.is_cancelled:
            self.task.status = TaskStatus.CANCELLED
            self.task_failed.emit(self.task, "Download cancelado pelo usuário.")
            return

        self.task.status = TaskStatus.DOWNLOADING
        self.task_started.emit(self.task)

        try:
            # Se um motor específico foi registrado, utiliza ele, senão faz fallback para o extractor_service
            if self.engine:
                extractor_func = self.engine
            else:
                from services.extractor_service import extractor_service
                extractor_func = extractor_service.download_media_task
            
            def progress_callback(pct: int, speed: str, eta: str, size: str = "-- MB"):
                if self.task.is_cancelled:
                    raise RuntimeError("CANCELLED_BY_USER")
                self.task.progress = pct
                self.task.speed = speed
                self.task.eta = eta
                self.task.file_size = size
                self.task_updated.emit(self.task)

            final_file = extractor_func(self.task, progress_callback)
            
            if self.task.is_cancelled:
                self.task.status = TaskStatus.CANCELLED
                self.task_failed.emit(self.task, "Download cancelado pelo usuário.")
            else:
                self.task.save_path = final_file
                self.task.status = TaskStatus.COMPLETED
                self.task.progress = 100
                self.task_completed.emit(self.task)

        except RuntimeError as re:
            if "CANCELLED_BY_USER" in str(re):
                self.task.status = TaskStatus.CANCELLED
                self.task_failed.emit(self.task, "Download cancelado pelo usuário.")
            else:
                self.task.status = TaskStatus.FAILED
                self.task_failed.emit(self.task, str(re))
        except Exception as e:
            self.task.status = TaskStatus.FAILED
            self.task_failed.emit(self.task, str(e))


class DownloadManager(QObject):
    """Gerenciador central de downloads do PRT Nexus."""

    task_added = Signal(object)
    task_updated = Signal(object)
    task_completed = Signal(object)
    task_failed = Signal(object, str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.tasks: Dict[str, DownloadTask] = {}
        self.workers: Dict[str, DownloadWorker] = {}
        self.engine: Optional[Callable] = None

    def register_engine(self, engine_func: Callable) -> None:
        """Registra o motor de extração (chamado pelo application.py)."""
        self.engine = engine_func

    def add_download(
        self,
        url: str,
        title: str = "Nova Mídia",
        platform: str = "web",
        save_path: str = "",
        format_type: str = "video",
        quality: str = "best"
    ) -> DownloadTask:
        task_id = str(uuid.uuid4())[:8]
        task = DownloadTask(
            task_id=task_id,
            url=url,
            title=title,
            platform=platform,
            save_path=save_path,
            format_type=format_type,
            quality=quality
        )
        self.tasks[task_id] = task
        self.task_added.emit(task)

        # Inicia worker assíncrono
        worker = DownloadWorker(task, engine=self.engine)
        worker.task_updated.connect(self.task_updated.emit)
        worker.task_completed.connect(self._on_worker_completed)
        worker.task_failed.connect(self._on_worker_failed)

        self.workers[task_id] = worker
        worker.start()
        return task

    def cancel_download(self, task_id: str) -> bool:
        """Sinaliza e cancela o download ativo."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.is_cancelled = True
            task.status = TaskStatus.CANCELLED
            self.task_updated.emit(task)
            return True
        return False

    @Slot(object)
    def _on_worker_completed(self, task: DownloadTask) -> None:
        if task.task_id in self.workers:
            del self.workers[task.task_id]
        self.task_completed.emit(task)

    @Slot(object, str)
    def _on_worker_failed(self, task: DownloadTask, error_msg: str) -> None:
        if task.task_id in self.workers:
            del self.workers[task.task_id]
        self.task_failed.emit(task, error_msg)


# Instância Singleton
download_manager = DownloadManager()