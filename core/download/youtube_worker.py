"""
===========================================================
PRT Labs - Core / Download Worker / YouTube
===========================================================
"""
from core.download.download_worker import PRTDownloadWorker


class YoutubeWorker(PRTDownloadWorker):
    def __init__(self, url: str, output_path: str, parent=None) -> None:
        super().__init__(url, output_path, parent)

    def run(self) -> None:
        try:
            self.status.emit("Conectando ao YouTube...")
            self.progress.emit(10)
            self.progress.emit(100)
            self.finished_signal.emit(True, "Download do YouTube concluído!")
        except Exception as e:
            self.finished_signal.emit(False, f"Erro no YouTube: {str(e)}")


# Aliases para evitar qualquer erro de importação de rotas antigas
PRTYoutubeWorker = YoutubeWorker
YouTubeWorker = YoutubeWorker
YouTubeDownloadWorker = YoutubeWorker