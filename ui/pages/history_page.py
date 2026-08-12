"""
===========================================================
PRT Labs - UI / Pages
Class: HistoryPage
Description: Página de Histórico do PRT NEXUS adaptável a temas.
===========================================================
"""

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


class HistoryPage(QWidget):
    """Página de Histórico de Atividades."""

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

        lbl_title = QLabel("🕒 Histórico de Atividades")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        lbl_subtitle = QLabel("Registro recente de downloads efetuados e URLs navegadas.")
        lbl_subtitle.setStyleSheet("color: #8E8E93; font-size: 13px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        btn_clear = QPushButton("🗑️ Limpar Histórico")
        btn_clear.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(btn_clear)

        layout.addLayout(header_layout)

        # Barra de Pesquisa
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Filtrar histórico por título, link ou plataforma...")
        layout.addWidget(self.txt_search)

        # Exemplo de Cards do Histórico
        sample_history = [
            ("Red Hot Chili Peppers - Buenos Aires, Argentina 2023 (HD) | River Plate Stadium", "YouTube", "2026-08-11 21:46:53"),
            ("FUI NA LOJA BUSCAR MEU NOVO CARRO - JETTA GLI 2026 0KM", "YouTube", "2026-08-11 21:29:30"),
        ]

        for title, plat, dt in sample_history:
            card = QFrame()
            card.setObjectName("cardFrame")
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(15, 12, 15, 12)

            lbl_t = QLabel(f"🔗  {title}")
            lbl_t.setStyleSheet("font-weight: bold; font-size: 13px;")

            lbl_sub = QLabel(f"Plataforma: {plat}  •  Data: {dt}")
            lbl_sub.setStyleSheet("color: #8E8E93; font-size: 11px;")

            c_layout.addWidget(lbl_t)
            c_layout.addWidget(lbl_sub)
            layout.addWidget(card)

        layout.addStretch()