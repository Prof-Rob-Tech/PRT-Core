"""
===========================================================
PRT Labs - Core / Download Router & Bridge
File: core/download/download_worker.py
===========================================================
"""

from PySide6.QtCore import QObject, Signal, QTimer
from .youtube_worker import YouTubeDownloadWorker
from .universo_worker import UniversoDownloadWorker, UniversoCourseMapper

GLOBAL_WORKER_REGISTRY = set()


class PRTDownloadWorker(QObject):
    """
    Roteador transparente de downloads.
    Mantém o worker seguro na memória até a finalização real da Thread.
    """

    progress_changed = Signal(dict)
    status_changed = Signal(str, str)
    download_finished = Signal(str)
    download_error = Signal(str)
    finished = Signal()

    def __init__(
        self,
        media_url: str,
        output_path: str = "",
        media_type: str = "video",
        quality: str = "best",
        cookie_string: str = "",
        cookies_list: list = None,
        course_name: str = "Curso",
        module_name: str = "Módulo 1",
        module_index: int = 1,
        lesson_index: int = 1,
        lesson_name: str = "Aula",
        username: str = "",
        password: str = "",
        parent=None,
        **kwargs
    ):
        super().__init__(parent)

        GLOBAL_WORKER_REGISTRY.add(self)

        url_clean = str(media_url or "").strip().lower()
        is_youtube = any(domain in url_clean for domain in ["youtube.com", "youtu.be", "yt.be"])

        if is_youtube:
            self.internal_worker = YouTubeDownloadWorker(
                media_url=media_url,
                output_path=output_path,
                media_type=media_type,
                quality=quality,
                title=lesson_name or "",
                parent=None
            )
        else:
            self.internal_worker = UniversoDownloadWorker(
                media_url=media_url,
                output_path=output_path,
                media_type=media_type,
                quality=quality,
                cookie_string=cookie_string or "",
                cookies_list=cookies_list or [],
                course_name=course_name or "Curso",
                module_name=module_name or "Módulo 1",
                module_index=module_index,
                lesson_index=lesson_index,
                lesson_name=lesson_name or "Aula",
                username=username or "",
                password=password or "",
                parent=None
            )

        self.internal_worker.progress_changed.connect(self.progress_changed.emit)
        self.internal_worker.status_changed.connect(self.status_changed.emit)
        self.internal_worker.download_finished.connect(self.download_finished.emit)
        self.internal_worker.download_error.connect(self.download_error.emit)
        
        if hasattr(self.internal_worker, "finished"):
            self.internal_worker.finished.connect(self._on_internal_finished)

    def _on_internal_finished(self):
        """Dispara o sinal final e limpa a memória com segurança."""
        self.finished.emit()
        QTimer.singleShot(1000, lambda: GLOBAL_WORKER_REGISTRY.discard(self))

    def start(self):
        if hasattr(self.internal_worker, "start"):
            self.internal_worker.start()

    def run(self):
        self.start()

    def terminate(self):
        if hasattr(self.internal_worker, "terminate"):
            self.internal_worker.terminate()

    def isRunning(self):
        if hasattr(self.internal_worker, "isRunning"):
            return self.internal_worker.isRunning()
        return False


__all__ = [
    "PRTDownloadWorker",
    "YouTubeDownloadWorker",
    "UniversoDownloadWorker",
    "UniversoCourseMapper"
]