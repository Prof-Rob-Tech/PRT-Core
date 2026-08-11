"""
===========================================================
PRT Labs - Core / Download Manager
Classes: TaskStatus, DownloadTask, DownloadWorker, DownloadManager

Description:
    Gerenciador assíncrono de downloads em segundo plano.
    Utiliza QThread e Signals para não congelar a UI.
===========================================================
"""

import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
from PySide6.QtCore import QObject, QThread, Signal, Slot


class TaskStatus(Enum):
    PENDING = "Pendente"
    DOWNLOADING = "Baixando"
    PAUSED = "Pausado"
    FINISHED = "Concluído"
    FAILED = "Erro"
    CANCELLED = "Cancelado"


@dataclass
class DownloadTask:
    """Modelo de dados de uma tarefa de download."""
    task_id: str
    url: str
    title: str
    platform: str
    save_path: str
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0
    speed: str = "0 MB/s"
    eta: str = "--:--"
    file_size: str = "-- MB"
    error_msg: str = ""


class DownloadWorker(QThread):
    """Worker que executa o download em segundo plano fora da thread principal de UI."""

    progress_signal = Signal(str, int, str, str)  # (task_id, progress_pct, speed, eta)
    status_signal = Signal(str, str)              # (task_id, status_str)
    finished_signal = Signal(str, str)            # (task_id, final_file_path)
    error_signal = Signal(str, str)               # (task_id, error_message)

    def __init__(self, task: DownloadTask, download_func=None, parent=None) -> None:
        super().__init__(parent)
        self.task = task
        self.download_func = download_func
        self._is_cancelled = False

    def cancel(self) -> None:
        self._is_cancelled = True

    def run(self) -> None:
        """Execução paralela na Thread secundária."""
        self.status_signal.emit(self.task.task_id, TaskStatus.DOWNLOADING.value)

        try:
            if self.download_func:
                # Executa a função de extração/download (hook do yt-dlp / extractor_service)
                self.download_func(self.task, self._progress_hook)
            else:
                # Callback genérico para fallback/testes
                self.finished_signal.emit(self.task.task_id, self.task.save_path)
                return

            if not self._is_cancelled:
                self.finished_signal.emit(self.task.task_id, self.task.save_path)

        except Exception as e:
            self.error_signal.emit(self.task.task_id, str(e))

    def _progress_hook(self, pct: int, speed: str, eta: str, file_size: str = "-- MB") -> None:
        """Callback invocado pelos motores de extração durante o progresso."""
        if not self._is_cancelled:
            self.task.progress = pct
            self.task.speed = speed
            self.task.eta = eta
            self.task.file_size = file_size  # 👈 Atualiza o tamanho na task
            
            # Se o seu sinal envia a task ou os atributos:
            self.progress_signal.emit(self.task.task_id, pct, speed, eta)


class DownloadManager(QObject):
    """Gerenciador central de fila e controle de downloads (Singleton)."""

    # Sinais globais retransmitidos para as telas (DownloadsPage, Dashboard, etc.)
    task_added = Signal(object)
    task_updated = Signal(object)
    task_completed = Signal(object)
    task_failed = Signal(object, str)

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DownloadManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent=None) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        super().__init__(parent)
        self._initialized = True

        self.tasks: Dict[str, DownloadTask] = {}
        self.workers: Dict[str, DownloadWorker] = {}
        self.max_concurrent_downloads: int = 3
        self.download_engine_func = None  # Receberá a função do extractor_service

    def register_engine(self, engine_func) -> None:
        """Registra a função do motor de extração (ex: ExtractorService)."""
        self.download_engine_func = engine_func

    def add_download(self, url: str, title: str, platform: str = "geral", save_path: str = "") -> DownloadTask:
        """Adiciona uma nova tarefa na fila."""
        task_id = str(uuid.uuid4())[:8]
        task = DownloadTask(
            task_id=task_id,
            url=url,
            title=title if title else "Mídia sem título",
            platform=platform,
            save_path=save_path
        )

        self.tasks[task_id] = task
        self.task_added.emit(task)
        self._process_queue()
        return task

    def _process_queue(self) -> None:
        """Gerencia os slots da fila e inicia os próximos da lista."""
        active_workers = sum(1 for w in self.workers.values() if w.isRunning())
        if active_workers >= self.max_concurrent_downloads:
            return

        for task_id, task in self.tasks.items():
            if task.status == TaskStatus.PENDING and task_id not in self.workers:
                worker = DownloadWorker(task, download_func=self.download_engine_func)
                worker.progress_signal.connect(self._on_worker_progress)
                worker.status_signal.connect(self._on_worker_status)
                worker.finished_signal.connect(self._on_worker_finished)
                worker.error_signal.connect(self._on_worker_error)

                self.workers[task_id] = worker
                worker.start()
                break

    @Slot(str, int, str, str)
    def _on_worker_progress(self, task_id: str, progress: int, speed: str, eta: str) -> None:
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.progress = progress
            task.speed = speed
            task.eta = eta
            self.task_updated.emit(task)

    @Slot(str, str)
    def _on_worker_status(self, task_id: str, status_str: str) -> None:
        if task_id in self.tasks:
            task = self.tasks[task_id]
            for s in TaskStatus:
                if s.value == status_str:
                    task.status = s
                    break
            self.task_updated.emit(task)

    @Slot(str, str)
    def _on_worker_finished(self, task_id: str, file_path: str) -> None:
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.FINISHED
            task.progress = 100
            task.save_path = file_path
            self.task_completed.emit(task)

        self._cleanup_worker(task_id)
        self._process_queue()

    @Slot(str, str)
    def _on_worker_error(self, task_id: str, error_msg: str) -> None:
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = TaskStatus.FAILED
            task.error_msg = error_msg
            self.task_failed.emit(task, error_msg)

        self._cleanup_worker(task_id)
        self._process_queue()

    def _cleanup_worker(self, task_id: str) -> None:
        if task_id in self.workers:
            self.workers[task_id].deleteLater()
            del self.workers[task_id]


# Instância global do Gerenciador de Downloads
download_manager = DownloadManager()