import os
import traceback
from PySide6.QtCore import QThread, Signal


class GDriveWorker(QThread):
    progress_changed = Signal(dict)
    status_changed = Signal(str, str)
    download_finished = Signal(str)
    download_error = Signal(str)

    def __init__(self, media_url, output_path, parent=None, **kwargs):
        super().__init__(parent)
        self.media_url = media_url
        self.output_path = output_path
        self.kwargs = kwargs

    def run(self):
        try:
            self.status_changed.emit("START", "Conectando ao Google Drive...")
            # TODO: Implementar download de arquivos/pastas (gdown ou PyDrive2)
            os.makedirs(self.output_path, exist_ok=True)
            
            self.progress_changed.emit({"percent": 100, "speed": "0KB/s", "eta": "00:00"})
            self.download_finished.emit(self.output_path)
        except Exception as e:
            traceback.print_exc()
            self.download_error.emit(f"Erro Google Drive: {str(e)}")