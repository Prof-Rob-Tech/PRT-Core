"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTNewDownloadDialog

Description:
    Dialog to prompt user for a URL with automatic
    clipboard link detection.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class PRTNewDownloadDialog(QDialog):
    """Dialog to input video URLs with smart clipboard auto-fill."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Novo Download")
        self.setMinimumWidth(480)
        
        self.setStyleSheet(
            """
            QDialog {
                background-color: #1A1A1E;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 13px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #141416;
                border: 1px solid #28282D;
                border-radius: 6px;
                color: #FFFFFF;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #007ACC;
            }
            QPushButton {
                background-color: #24242A;
                color: #FFFFFF;
                border: 1px solid #28282D;
                border-radius: 6px;
                padding: 8px 18px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2C2C32;
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

        self._build_ui()
        self._check_clipboard()

    def _build_ui(self) -> None:
        """Constrói a interface visual do Dialog."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        lbl = QLabel("Cole a URL do vídeo (YouTube, Vimeo, etc):")
        layout.addWidget(lbl)

        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("https://www.youtube.com/watch?v=...")
        layout.addWidget(self.input_url)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.clicked.connect(self.reject)

        btn_download = QPushButton("⚡ Baixar")
        btn_download.setObjectName("Primary")
        btn_download.setCursor(Qt.PointingHandCursor)
        btn_download.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_download)

        layout.addLayout(btn_layout)

    def _check_clipboard(self) -> None:
        """Lê a área de transferência do SO e cola se for um link web válido."""
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()

        # Verifica se o texto copiado é uma URL de internet
        if text.startswith("http://") or text.startswith("https://"):
            self.input_url.setText(text)
            self.input_url.selectAll()  # Deixa o texto pré-selecionado

    def get_url(self) -> str:
        """Retorna o texto digitado/colado."""
        return self.input_url.text().strip()