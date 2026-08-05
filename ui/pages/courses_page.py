"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: CoursesPage

Description:
    Media and courses gallery displaying downloaded videos
    with playback, organization, and real-time search filtering.

Developer..: Prof Rob Tech
===========================================================
"""

import os
from typing import List
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from services.download_manager import PRTDownloadManager
from ui.pages.base_page import BasePage


class VideoCard(QFrame):
    """Card visual para representar um vídeo/curso baixado."""

    def __init__(self, file_path: str, parent=None) -> None:
        super().__init__(parent)
        self.file_path = file_path
        self.filename = os.path.basename(file_path)

        self._build_ui()

    def _build_ui(self) -> None:
        self.setFixedWidth(240)
        self.setFixedHeight(220)
        self.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 10px;
            }
            QFrame:hover {
                border-color: #007ACC;
                background-color: #1A1A1E;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Thumbnail / Ícone
        thumb_container = QFrame()
        thumb_container.setStyleSheet(
            """
            background-color: #1F1F24;
            border-radius: 6px;
            border: none;
            """
        )
        thumb_layout = QVBoxLayout(thumb_container)
        thumb_layout.setAlignment(Qt.AlignCenter)

        icon_lbl = QLabel("🎬")
        icon_lbl.setStyleSheet("font-size: 36px; background: transparent;")
        thumb_layout.addWidget(icon_lbl)

        layout.addWidget(thumb_container, stretch=1)

        # Título
        name_lbl = QLabel(self.filename)
        name_lbl.setWordWrap(True)
        name_lbl.setStyleSheet(
            "color: #FFFFFF; font-size: 12px; font-weight: bold; border: none;"
        )
        name_lbl.setToolTip(self.filename)
        layout.addWidget(name_lbl)

        # Tamanho
        size_bytes = os.path.getsize(self.file_path) if os.path.exists(self.file_path) else 0
        size_str = self._format_size(size_bytes)
        info_lbl = QLabel(f"Tamanho: {size_str}")
        info_lbl.setStyleSheet("color: #8E8E93; font-size: 11px; border: none;")
        layout.addWidget(info_lbl)

        # Botão Play
        btn_play = QPushButton("▶ Assistir")
        btn_play.setCursor(Qt.PointingHandCursor)
        btn_play.setStyleSheet(
            """
            QPushButton {
                background-color: #007ACC;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            """
        )
        btn_play.clicked.connect(self._play_video)
        layout.addWidget(btn_play)

    def _play_video(self) -> None:
        if os.path.exists(self.file_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(self.file_path)))

    def _format_size(self, size_bytes: float) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"


class CoursesPage(BasePage):
    """Página de galeria de cursos e vídeos baixados com suporte a busca."""

    def __init__(self) -> None:
        super().__init__()
        self._cards: List[VideoCard] = []

        self._layout = QVBoxLayout(self)
        self._configure()
        self._build_ui()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.reload_media()

    def _configure(self) -> None:
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(20)

    def _build_ui(self) -> None:
        top_layout = QHBoxLayout()
        title = QLabel("Cursos e Mídias Baixadas")
        title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")
        top_layout.addWidget(title)

        top_layout.addStretch()

        btn_refresh = QPushButton("🔄 Atualizar")
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.setStyleSheet(
            """
            QPushButton {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #28282D;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #24242A;
                border-color: #007ACC;
            }
            """
        )
        btn_refresh.clicked.connect(self.reload_media)
        top_layout.addWidget(btn_refresh)

        self._layout.addLayout(top_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #141416;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: #28282D;
                border-radius: 4px;
            }
            """
        )

        self.container_widget = QWidget()
        self.container_widget.setStyleSheet("background-color: transparent;")
        self.grid_layout = QGridLayout(self.container_widget)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.scroll_area.setWidget(self.container_widget)
        self._layout.addWidget(self.scroll_area)

    def reload_media(self) -> None:
        """Carrega e renderiza todos os vídeos encontrados na pasta de downloads."""
        self._cards.clear()
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        folder_path = PRTDownloadManager.instance().get_download_folder()
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        video_extensions = (".mp4", ".mkv", ".webm", ".avi", ".mov", ".ts", ".m4a")
        files: List[str] = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(video_extensions)
        ]

        if not files:
            empty_lbl = QLabel("Nenhum vídeo ou curso encontrado na pasta de downloads.")
            empty_lbl.setStyleSheet("color: #8E8E93; font-size: 14px; padding: 20px;")
            self.grid_layout.addWidget(empty_lbl, 0, 0)
            return

        cols = 4
        for idx, file_path in enumerate(files):
            card = VideoCard(file_path)
            self._cards.append(card)
            row = idx // cols
            col = idx % cols
            self.grid_layout.addWidget(card, row, col)

    def filter_media(self, query: str) -> None:
        """Filtra os cards visíveis com base na pesquisa em tempo real."""
        clean_q = query.lower().strip()
        visible_count = 0

        for card in self._cards:
            if not clean_q or clean_q in card.filename.lower():
                card.show()
                visible_count += 1
            else:
                card.hide()