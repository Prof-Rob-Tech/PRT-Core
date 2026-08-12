"""
===========================================================
PRT Labs - UI / Pages
Class: LibraryPage
Description: Página de Biblioteca de Mídias adaptativa para
             todos os temas (Escuro, Claro, Cyber).
===========================================================
"""

import os
import subprocess
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LibraryPage(QWidget):
    """Página de Biblioteca do PRT NEXUS."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 1. Cabeçalho (Título e Botões de Ação)
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        lbl_title = QLabel("📁 Biblioteca de Mídias")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        lbl_subtitle = QLabel("Gerencie e visualize todas as mídias salvas localmente no computador.")
        lbl_subtitle.setStyleSheet("color: #8E8E93; font-size: 13px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        # Botões do Topo
        btn_clear = QPushButton("🗑️ Limpar Biblioteca")
        btn_clear.setCursor(Qt.PointingHandCursor)

        btn_open_folder = QPushButton("📁 Abrir Pasta no Windows")
        btn_open_folder.setCursor(Qt.PointingHandCursor)
        btn_open_folder.clicked.connect(self._open_downloads_folder)

        header_layout.addWidget(btn_clear)
        header_layout.addWidget(btn_open_folder)
        layout.addLayout(header_layout)

        # 2. Barra de Pesquisa
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Pesquisar mídias na biblioteca...")
        layout.addWidget(self.txt_search)

        # 3. Container da Biblioteca / Estado Vazio
        self.card_empty = QFrame()
        self.card_empty.setObjectName("cardFrame")

        empty_layout = QVBoxLayout(self.card_empty)
        empty_layout.setContentsMargins(30, 40, 30, 40)
        empty_layout.setSpacing(10)

        lbl_empty_icon = QLabel("🎬")
        lbl_empty_icon.setAlignment(Qt.AlignCenter)
        lbl_empty_icon.setStyleSheet("font-size: 36px;")

        lbl_empty_title = QLabel("Sua biblioteca está vazia")
        lbl_empty_title.setAlignment(Qt.AlignCenter)
        lbl_empty_title.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_empty_desc = QLabel("Os vídeos e conteúdos baixados através dos conectores e do navegador aparecerão listados aqui.")
        lbl_empty_desc.setAlignment(Qt.AlignCenter)
        lbl_empty_desc.setStyleSheet("color: #8E8E93; font-size: 13px;")

        empty_layout.addWidget(lbl_empty_icon)
        empty_layout.addWidget(lbl_empty_title)
        empty_layout.addWidget(lbl_empty_desc)

        layout.addWidget(self.card_empty)
        layout.addStretch()

    def _open_downloads_folder(self) -> None:
        """Abre a pasta de downloads no Explorer do Windows."""
        folder_path = os.path.abspath("downloads")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
        try:
            os.startfile(folder_path)
        except Exception:
            subprocess.Popen(["explorer", folder_path])