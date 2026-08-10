"""
===========================================================
PRT Labs - UI / Pages
Class: LibraryPage / PRTLibraryPage

Description:
    Gerenciador da Biblioteca de Mídias local do PRT Nexus.
===========================================================
"""

import os
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QScrollArea
)

try:
    from ui.pages.base_page import BasePage
except Exception:
    class BasePage(QWidget):
        pass


class LibraryPage(BasePage):
    """Página de Biblioteca do PRT Nexus."""

    def __init__(self, parent=None, *args, **kwargs) -> None:
        try:
            super().__init__()
        except TypeError:
            try:
                super().__init__(parent)
            except Exception:
                QWidget.__init__(self)

        if parent is not None and isinstance(parent, QWidget):
            try:
                self.setParent(parent)
            except Exception:
                pass

        self.title = "Biblioteca"
        self.subtitle = "Gerenciador de Mídias"
        self.icon = "📁"
        self.page_id = "biblioteca"

        # Caminho padrão da pasta de downloads do usuário
        self.download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(self.download_dir):
            try:
                os.makedirs(self.download_dir, exist_ok=True)
            except Exception:
                pass

        self._setup_ui()

    def _setup_ui(self) -> None:
        main_layout = self.layout()
        if main_layout is None:
            main_layout = QVBoxLayout(self)
        
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #09090B;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #27272A;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3F3F46;
            }
        """)

        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # 1. Header principal
        header_layout = QHBoxLayout()
        
        title_box = QVBoxLayout()
        lbl_title = QLabel("📁 Biblioteca de Mídias")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; border: none; background: transparent;")
        lbl_subtitle = QLabel("Gerencie e visualize todas as mídias salvas localmente no computador.")
        lbl_subtitle.setStyleSheet("font-size: 13px; color: #71717A; border: none; background: transparent;")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_subtitle)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        btn_open_folder = QPushButton("📂 Abrir Pasta no Windows")
        btn_open_folder.setCursor(Qt.PointingHandCursor)
        btn_open_folder.setStyleSheet("""
            QPushButton {
                background-color: #27272A;
                color: #FFFFFF;
                border: 1px solid #3F3F46;
                padding: 10px 16px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3F3F46;
            }
        """)
        btn_open_folder.clicked.connect(self._open_downloads_folder)
        header_layout.addWidget(btn_open_folder)

        layout.addLayout(header_layout)

        # 2. Barra de Busca
        filter_card = QFrame()
        filter_card.setObjectName("filterCard")
        filter_card.setStyleSheet("""
            QFrame#filterCard {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
        """)
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(12, 12, 12, 12)
        filter_layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Pesquisar mídias na biblioteca...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #09090B;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #6366F1;
            }
        """)
        filter_layout.addWidget(self.search_input)

        layout.addWidget(filter_card)

        # 3. Estado de Biblioteca
        self.media_container = QFrame()
        self.media_container.setObjectName("mediaContainer")
        self.media_container.setStyleSheet("""
            QFrame#mediaContainer {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 12px;
            }
            QLabel {
                border: none !important;
                background: transparent !important;
            }
        """)
        
        media_layout = QVBoxLayout(self.media_container)
        media_layout.setContentsMargins(40, 60, 40, 60)
        media_layout.setAlignment(Qt.AlignCenter)

        icon_empty = QLabel("🎬")
        icon_empty.setStyleSheet("font-size: 48px;")
        icon_empty.setAlignment(Qt.AlignCenter)

        title_empty = QLabel("Sua biblioteca está pronta")
        title_empty.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF; margin-top: 12px;")
        title_empty.setAlignment(Qt.AlignCenter)

        desc_empty = QLabel("Os vídeos e conteúdos baixados através dos conectores e do navegador aparecerão listados aqui.")
        desc_empty.setStyleSheet("font-size: 13px; color: #71717A; margin-top: 4px;")
        desc_empty.setAlignment(Qt.AlignCenter)

        media_layout.addWidget(icon_empty)
        media_layout.addWidget(title_empty)
        media_layout.addWidget(desc_empty)

        layout.addWidget(self.media_container)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _open_downloads_folder(self) -> None:
        """Abre a pasta de downloads no sistema operacional."""
        try:
            if os.name == 'nt':
                os.startfile(self.download_dir)
            else:
                QDesktopServices.openUrl(QUrl.fromLocalFile(self.download_dir))
        except Exception:
            pass

    def on_show(self) -> None:
        pass

    def refresh(self) -> None:
        pass


# Aliases para compatibilidade total
PRTLibraryPage = LibraryPage