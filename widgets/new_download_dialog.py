"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTNewDownloadDialog

Description:
    Modal pop-up dialog to capture new download URLs and
    trigger download tasks.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PRTNewDownloadDialog(QDialog):
    """Modal dialog for pasting download URLs."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Novo Download")
        self.setFixedSize(520, 240)
        self.setModal(True)

        self._build_ui()

    def _build_ui(self) -> None:
        self.setStyleSheet(
            """
            QDialog {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 12px;
            }
            QLabel#TitleLabel {
                color: #FFFFFF;
                font-size: 17px;
                font-weight: bold;
            }
            QLabel#FieldLabel {
                color: #8E8E93;
                font-size: 12px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #1A1A1E;
                border: 1px solid #28282D;
                border-radius: 6px;
                color: #FFFFFF;
                padding: 10px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #007ACC;
            }
            QPushButton {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #28282D;
                border-radius: 6px;
                padding: 8px 18px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #24242A;
                border-color: #007ACC;
            }
            QPushButton#Primary {
                background-color: #007ACC;
                border-color: #007ACC;
            }
            QPushButton#Primary:hover {
                background-color: #005A9E;
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Título do Modal
        title = QLabel("⚡ Adicionar Novo Download")
        title.setObjectName("TitleLabel")
        layout.addWidget(title)

        # Campo de entrada da URL
        url_label = QLabel("Cole a URL do vídeo, playlist ou arquivo abaixo:")
        url_label.setObjectName("FieldLabel")

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=... ou Kiwify / Hotmart link")

        layout.addWidget(url_label)
        layout.addWidget(self.url_input)

        # Botões de Ação (Cancelar e Iniciar)
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.clicked.connect(self.reject)

        btn_start = QPushButton("Iniciar Download")
        btn_start.setObjectName("Primary")
        btn_start.setCursor(Qt.PointingHandCursor)
        btn_start.clicked.connect(self.accept)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_start)

        layout.addStretch()
        layout.addLayout(btn_layout)

    def get_url(self) -> str:
        """Returns the entered URL string."""
        return self.url_input.text().strip()