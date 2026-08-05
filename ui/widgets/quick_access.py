"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTQuickAccess

Description:
    Quick access grid panel with shortcut buttons for common
    user actions, emitting signals on interaction.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class QuickActionButton(QPushButton):
    """Custom styled button for quick shortcuts."""

    def __init__(self, title: str, subtitle: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setFixedHeight(65)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(
            """
            QPushButton {
                background-color: #1A1A1E;
                border: 1px solid #28282D;
                border-radius: 10px;
                text-align: left;
                padding: 10px 15px;
            }
            QPushButton:hover {
                background-color: #24242A;
                border-color: #007ACC;
            }
            QPushButton:pressed {
                background-color: #161619;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: bold; background: transparent;")

        lbl_sub = QLabel(subtitle)
        lbl_sub.setStyleSheet("color: #8E8E93; font-size: 11px; background: transparent;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_sub)


class PRTQuickAccess(QWidget):
    """Quick access panel containing action shortcuts."""

    new_download_clicked = Signal()
    courses_clicked = Signal()
    open_folder_clicked = Signal()
    sync_clicked = Signal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._layout = QVBoxLayout(self)
        self._build_ui()

    def _build_ui(self) -> None:
        self.setObjectName("PRTQuickAccess")
        self.setStyleSheet(
            """
            QWidget#PRTQuickAccess {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 12px;
            }
            QLabel#HeaderTitle {
                color: #FFFFFF;
                font-size: 15px;
                font-weight: bold;
            }
            """
        )

        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(12)

        title = QLabel("Ações Rápidas")
        title.setObjectName("HeaderTitle")
        self._layout.addWidget(title)

        # Grade de botões 2x2
        grid = QGridLayout()
        grid.setSpacing(10)

        self.btn_new_download = QuickActionButton("⚡ Novo Download", "Adicionar URL ou link")
        self.btn_courses = QuickActionButton("📚 Meus Cursos", "Ir para biblioteca")
        self.btn_open_folder = QuickActionButton("📁 Abrir Pasta", "Acessar arquivos baixados")
        self.btn_sync = QuickActionButton("🔄 Sincronizar", "Atualizar conectores")

        # Conecta os cliques aos sinais
        self.btn_new_download.clicked.connect(self.new_download_clicked.emit)
        self.btn_courses.clicked.connect(self.courses_clicked.emit)
        self.btn_open_folder.clicked.connect(self.open_folder_clicked.emit)
        self.btn_sync.clicked.connect(self.sync_clicked.emit)

        grid.addWidget(self.btn_new_download, 0, 0)
        grid.addWidget(self.btn_courses, 0, 1)
        grid.addWidget(self.btn_open_folder, 1, 0)
        grid.addWidget(self.btn_sync, 1, 1)

        self._layout.addLayout(grid)
