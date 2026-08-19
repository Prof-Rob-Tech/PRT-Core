"""
===========================================================
PRT Labs - Core / Download Router & Bridge
File: core/download/download_worker.py
===========================================================
"""

from PySide6.QtCore import QThread, Signal
from .youtube_worker import YouTubeDownloadWorker
from .universo_worker import UniversoDownloadWorker, UniversoCourseMapper


class PRTDownloadWorker(QThread):
    """
    Roteador transparente de downloads.
    Identifica se a URL é YouTube e redireciona com parâmetros sanitizados.
    """

    progress_changed = Signal(dict)
    status_changed = Signal(str, str)
    download_finished = Signal(str)
    download_error = Signal(str)

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

        url_clean = str(media_url or "").strip().lower()
        is_youtube = any(domain in url_clean for domain in ["youtube.com", "youtu.be", "yt.be"])

        if is_youtube:
            print(f"🔀 [Router] Link do YouTube detectado: {media_url}. Enviando para YouTubeDownloadWorker...")
            self.internal_worker = YouTubeDownloadWorker(
                media_url=media_url,
                output_path=output_path,
                parent=parent
            )
        else:
            print(f"🔀 [Router] Link de Plataforma detectado. Enviando para UniversoDownloadWorker...")
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
                parent=parent
            )

        # Repassa os sinais para a interface gráfica
        self.internal_worker.progress_changed.connect(self.progress_changed.emit)
        self.internal_worker.status_changed.connect(self.status_changed.emit)
        self.internal_worker.download_finished.connect(self.download_finished.emit)
        self.internal_worker.download_error.connect(self.download_error.emit)

    def run(self):
        self.internal_worker.run()


__all__ = [
    "PRTDownloadWorker",
    "YouTubeDownloadWorker",
    "UniversoDownloadWorker",
    "UniversoCourseMapper"
]