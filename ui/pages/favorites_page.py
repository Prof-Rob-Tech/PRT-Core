"""
===========================================================
PRT Labs - UI / Pages
Class: FavoritesPage
Description: Página de Favoritos do PRT NEXUS adaptável a temas.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)


class FavoritesPage(QWidget):
    """Página de Favoritos do PRT NEXUS."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Cabeçalho
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        lbl_title = QLabel("⭐ Seus Favoritos")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        lbl_subtitle = QLabel("Acesso rápido às suas mídias, vídeos e conectores salvos.")
        lbl_subtitle.setStyleSheet("color: #8E8E93; font-size: 13px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        layout.addLayout(title_layout)

        # Barra de Pesquisa
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Pesquisar nos favoritos...")
        layout.addWidget(self.txt_search)

        # Container do Estado Vazio
        self.card_empty = QFrame()
        self.card_empty.setObjectName("cardFrame")

        empty_layout = QVBoxLayout(self.card_empty)
        empty_layout.setContentsMargins(30, 40, 30, 40)
        empty_layout.setSpacing(10)

        lbl_empty_icon = QLabel("⭐")
        lbl_empty_icon.setAlignment(Qt.AlignCenter)
        lbl_empty_icon.setStyleSheet("font-size: 36px;")

        lbl_empty_title = QLabel("Nenhum favorito salvo ainda")
        lbl_empty_title.setAlignment(Qt.AlignCenter)
        lbl_empty_title.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_empty_desc = QLabel("Você pode favoritar links no Navegador ou conteúdos capturados nos conectores para acessar rapidamente por aqui.")
        lbl_empty_desc.setAlignment(Qt.AlignCenter)
        lbl_empty_desc.setStyleSheet("color: #8E8E93; font-size: 13px;")

        empty_layout.addWidget(lbl_empty_icon)
        empty_layout.addWidget(lbl_empty_title)
        empty_layout.addWidget(lbl_empty_desc)

        layout.addWidget(self.card_empty)
        layout.addStretch()