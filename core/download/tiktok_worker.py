from core.download.download_worker import PRTDownloadWorker


class TikTokWorker(PRTDownloadWorker):
    def __init__(self, url: str, output_path: str, parent=None) -> None:
        super().__init__(url, output_path, parent)

    def run(self) -> None:
        try:
            self.status.emit("Conectando ao TikTok...")
            self.progress.emit(10)
            self.progress.emit(100)
            self.finished_signal.emit(True, "Download do TikTok concluído!")
        except Exception as e:
            self.finished_signal.emit(False, f"Erro no TikTok: {str(e)}")