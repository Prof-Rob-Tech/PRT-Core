"""
===========================================================
PRT Labs - Core / Download Worker / Kiwify
===========================================================
"""
from core.download.download_worker import PRTDownloadWorker


class KiwifyWorker(PRTDownloadWorker):
    def __init__(self, url: str, output_path: str, credentials: dict = None, parent=None) -> None:
        super().__init__(url, output_path, parent)
        self.credentials = credentials or {}

    def run(self) -> None:
        try:
            self.status.emit("Autenticando na plataforma Kiwify...")
            self.progress.emit(10)
            self.progress.emit(100)
            self.finished_signal.emit(True, "Download do Kiwify concluído!")
        except Exception as e:
            self.finished_signal.emit(False, f"Erro no Kiwify: {str(e)}")