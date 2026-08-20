"""
===========================================================
PRT Labs - Core / Download Worker Base
===========================================================
"""
from PySide6.QtCore import QThread, Signal


class PRTDownloadWorker(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished_signal = Signal(bool, str)

    def __init__(self, url: str, output_path: str, parent=None) -> None:
        super().__init__(parent)
        self.url = url
        self.output_path = output_path
        self.is_cancelled = False

    def cancel() -> None:
        self.is_cancelled = True


# Aliases para compatibilidade
DownloadWorker = PRTDownloadWorker