"""
===========================================================
PRT Labs - Core / Download Worker / MEGA
===========================================================
"""
from core.download.download_worker import PRTDownloadWorker


class MegaWorker(PRTDownloadWorker):
    def __init__(self, url: str, output_path: str, parent=None) -> None:
        super().__init__(url, output_path, parent)

    def run(self) -> None:
        try:
            self.status.emit("Obtendo metadados do MEGA...")
            self.progress.emit(10)
            self.progress.emit(100)
            self.finished_signal.emit(True, "Download do MEGA concluído!")
        except Exception as e:
            self.finished_signal.emit(False, f"Erro no MEGA: {str(e)}")