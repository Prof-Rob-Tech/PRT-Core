"""
===========================================================
PRT Labs - Core / Download
Class: PRTDownloadManager

Description:
    Gerenciador global de downloads. Controla a fila de tarefas,
    limite de downloads simultâneos e histórico de mídias baixadas.
===========================================================
"""

import os
from PySide6.QtCore import QObject, Signal
from core.download.download_worker import PRTDownloadWorker


class PRTDownloadManager(QObject):
    """Gerenciador centralizado de fila de downloads do PRT NEXUS."""

    task_added = Signal(dict)
    task_updated = Signal(str, dict)  # (task_id, info)
    task_finished = Signal(str, str)  # (task_id, file_path)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.download_folder = os.path.join(
            os.path.expanduser("~"), "Downloads", "PRT_Nexus"
        )
        self.active_workers: dict[str, PRTDownloadWorker] = {}
        self.tasks: dict[str, dict] = {}

    def add_download(
        self, 
        url: str, 
        title: str = "Mídia Capturada",
        cookie_string: str = "",
        cookies_list: list = None,
        course_name: str = "Curso",
        module_name: str = "Módulo 1",
        module_index: int = 1,
        lesson_index: int = 1
    ) -> str:
        """Adiciona e inicia um novo download na fila com suporte a sessão e metadados."""
        import uuid

        task_id = str(uuid.uuid4())[:8]

        task_info = {
            "id": task_id,
            "title": title,
            "url": url,
            "course_name": course_name,
            "module_name": module_name,
            "percent": 0.0,
            "speed": "0 KB/s",
            "eta": "--:--",
            "status": "QUEUED",
        }

        self.tasks[task_id] = task_info
        self.task_added.emit(task_info)

        # 🎯 Instancia o worker passando TODOS os dados de sessão e hierarquia
        worker = PRTDownloadWorker(
            media_url=url,
            output_path=self.download_folder,
            media_type="video",
            quality="best",
            cookie_string=cookie_string,
            cookies_list=cookies_list or [],
            course_name=course_name,
            module_name=module_name,
            module_index=module_index,
            lesson_index=lesson_index,
            lesson_name=title,
            parent=self
        )

        worker.progress_changed.connect(
            lambda prog: self._on_progress(task_id, prog)
        )
        worker.status_changed.connect(
            lambda st_code, st_msg: self._on_status_changed(
                task_id, st_code, st_msg
            )
        )
        worker.download_finished.connect(
            lambda filepath: self._on_finished(task_id, filepath)
        )
        worker.download_error.connect(
            lambda err_msg: self._on_error(task_id, err_msg)
        )

        self.active_workers[task_id] = worker
        worker.start()

        return task_id

    def _on_progress(self, task_id: str, progress_data: dict) -> None:
        if task_id in self.tasks:
            self.tasks[task_id].update(progress_data)
            self.tasks[task_id]["status"] = "DOWNLOADING"
            self.task_updated.emit(task_id, self.tasks[task_id])

    def _on_status_changed(
        self, task_id: str, status_code: str, message: str
    ) -> None:
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status_code
            self.tasks[task_id]["status_msg"] = message
            self.task_updated.emit(task_id, self.tasks[task_id])

    def _on_finished(self, task_id: str, filepath: str) -> None:
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "COMPLETED"
            self.tasks[task_id]["filepath"] = filepath
            self.task_finished.emit(task_id, filepath)

        if task_id in self.active_workers:
            del self.active_workers[task_id]

    def _on_error(self, task_id: str, error_message: str) -> None:
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "ERROR"
            self.tasks[task_id]["error"] = error_message
            self.task_updated.emit(task_id, self.tasks[task_id])

        if task_id in self.active_workers:
            del self.active_workers[task_id]