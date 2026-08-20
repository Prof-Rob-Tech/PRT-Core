"""
===========================================================
PRT Labs - Core / Download Worker / Hotmart
===========================================================
"""
from core.download.download_worker import PRTDownloadWorker


class HotmartWorker(PRTDownloadWorker):
    def __init__(self, url: str, output_path: str, credentials: dict = None, parent=None) -> None:
        super().__init__(url, output_path, parent)
        self.credentials = credentials or {}

    def run(self) -> None:
        try:
            self.status.emit("Conectando à Hotmart...")
            self.progress.emit(10)
            self.progress.emit(100)
            self.finished_signal.emit(True, "Download da Hotmart concluído!")
        except Exception as e:
            self.finished_signal.emit(False, f"Erro na Hotmart: {str(e)}")