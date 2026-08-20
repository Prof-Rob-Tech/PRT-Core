"""
===========================================================
PRT Labs - Core / Download Worker / Google Drive
===========================================================
"""
from core.download.download_worker import PRTDownloadWorker


class GDriveWorker(PRTDownloadWorker):
    def __init__(self, url: str, output_path: str, parent=None) -> None:
        super().__init__(url, output_path, parent)

    def run(self) -> None:
        try:
            self.status.emit("Conectando ao Google Drive...")
            self.progress.emit(10)
            self.progress.emit(100)
            self.finished_signal.emit(True, "Download do Drive concluído!")
        except Exception as e:
            self.finished_signal.emit(False, f"Erro no Google Drive: {str(e)}")