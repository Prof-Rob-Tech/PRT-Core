"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Pages
Class......: CoursesPage

Description:
    Courses and Media Player page. Auto-discovers media files in
    downloads folder, supports search filtering, and embeds video player.

Developer..: Prof Rob Tech
===========================================================
"""

import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QSplitter,
    QFrame
)

from services.download_manager import PRTDownloadManager
from ui.widgets.video_player_widget import PRTVideoPlayerWidget


class CoursesPage(QWidget):
    """Página de Cursos e Player de Vídeos."""

    MEDIA_EXTENSIONS = (".mp4", ".mkv", ".webm", ".avi", ".mov", ".m4v", ".mp3")

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()
        self.refresh_media_list()

        # Atualiza a lista automaticamente se um novo download for concluído
        PRTDownloadManager.instance().download_completed.connect(lambda *_: self.refresh_media_list())

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Splitter permitindo redimensionar a lista e o player
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(
            """
            QSplitter::handle {
                background-color: #18181B;
                width: 2px;
            }
            """
        )

        # Painel Esquerdo: Lista de Vídeos Baixados
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)

        lbl_title = QLabel("Aulas & Arquivos Baixados")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: bold;")
        left_layout.addWidget(lbl_title)

        self.list_media = QListWidget()
        self.list_media.setStyleSheet(
            """
            QListWidget {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 6px;
                color: #FFFFFF;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #1C1C1F;
            }
            QListWidget::item:selected {
                background-color: #007ACC;
                color: #FFFFFF;
                border-radius: 4px;
            }
            QListWidget::item:hover:!selected {
                background-color: #1A1A1E;
            }
            """
        )
        self.list_media.itemClicked.connect(self._on_media_selected)
        left_layout.addWidget(self.list_media)

        splitter.addWidget(left_panel)

        # Painel Direito: Player de Vídeo
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        self.video_player = PRTVideoPlayerWidget()
        right_layout.addWidget(self.video_player)

        splitter.addWidget(right_panel)

        # Proporção inicial: 30% lista, 70% player
        splitter.setSizes([300, 700])

        layout.addWidget(splitter)

    def refresh_media_list(self) -> None:
        """Escaneia a pasta de downloads e preenche a lista de arquivos."""
        self.list_media.clear()
        download_folder = PRTDownloadManager.instance().get_download_folder()

        if not os.path.exists(download_folder):
            return

        for file_name in sorted(os.listdir(download_folder)):
            if file_name.lower().endswith(self.MEDIA_EXTENSIONS):
                full_path = os.path.join(download_folder, file_name)
                item = QListWidgetItem(f"🎥  {file_name}")
                item.setData(Qt.UserRole, full_path)
                self.list_media.addItem(item)

        if self.list_media.count() == 0:
            item = QListWidgetItem("Nenhuma aula encontrada na pasta downloads.")
            item.setFlags(Qt.NoItemFlags)
            self.list_media.addItem(item)

    def filter_media(self, text: str) -> None:
        """Filtra as aulas exibidas de acordo com a busca (Ctrl+K)."""
        clean_text = text.lower().strip()
        for i in range(self.list_media.count()):
            item = self.list_media.item(i)
            item_text = item.text().lower()
            item.setHidden(clean_text not in item_text and clean_text != "")

    def _on_media_selected(self, item: QListWidgetItem) -> None:
        file_path = item.data(Qt.UserRole)
        if file_path and os.path.exists(file_path):
            clean_title = item.text().replace("🎥  ", "")
            self.video_player.load_video(file_path, title=clean_title)
