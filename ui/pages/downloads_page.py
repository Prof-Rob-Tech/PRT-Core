"""
===========================================================
PRT Labs - UI / Pages
Class: DownloadsPage
Description: Página de Downloads adaptável a temas.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DownloadsPage(QWidget):
    """Página de Gerenciamento de Downloads."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Cabeçalho
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        lbl_title = QLabel("⬇️ Fila de Downloads")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        lbl_subtitle = QLabel("Acompanhe a extração e o download de conteúdos em tempo real.")
        lbl_subtitle.setStyleSheet("color: #8E8E93; font-size: 13px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        btn_clear = QPushButton("🗑️ Limpar Finalizados")
        btn_clear.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(btn_clear)

        layout.addLayout(header_layout)

        # Card Vazio
        self.card_empty = QFrame()
        self.card_empty.setObjectName("cardFrame")

        empty_layout = QVBoxLayout(self.card_empty)
        empty_layout.setContentsMargins(30, 40, 30, 40)
        empty_layout.setSpacing(10)

        lbl_empty_icon = QLabel("📦")
        lbl_empty_icon.setAlignment(Qt.AlignCenter)
        lbl_empty_icon.setStyleSheet("font-size: 36px;")

        lbl_empty_title = QLabel("Nenhum download ativo no momento")
        lbl_empty_title.setAlignment(Qt.AlignCenter)
        lbl_empty_title.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_empty_desc = QLabel("Utilize o Navegador ou os Conectores laterais para adicionar links à fila.")
        lbl_empty_desc.setAlignment(Qt.AlignCenter)
        lbl_empty_desc.setStyleSheet("color: #8E8E93; font-size: 13px;")

        empty_layout.addWidget(lbl_empty_icon)
        empty_layout.addWidget(lbl_empty_title)
        empty_layout.addWidget(lbl_empty_desc)

        layout.addWidget(self.card_empty)
        layout.addStretch()