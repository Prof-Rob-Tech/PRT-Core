"""
===========================================================
PRT Labs - UI / Pages
Class: HistoryPage / PRTHistoryPage

Description:
    Histórico de Downloads e Navegação do PRT Nexus.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QScrollArea
)

try:
    from ui.pages.base_page import BasePage
except Exception:
    class BasePage(QWidget):
        pass


class HistoryPage(BasePage):
    """Página de Histórico do PRT Nexus."""

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

        self.title = "Histórico"
        self.subtitle = "Registro de Atividades"
        self.icon = "🕒"
        self.page_id = "historico"

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
        lbl_title = QLabel("🕒 Histórico de Atividades")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; border: none; background: transparent;")
        lbl_subtitle = QLabel("Registro recente de downloads efetuados e URLs navegadas.")
        lbl_subtitle.setStyleSheet("font-size: 13px; color: #71717A; border: none; background: transparent;")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_subtitle)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        btn_clear = QPushButton("🗑️ Limpar Histórico")
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #27272A;
                color: #EF4444;
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
        header_layout.addWidget(btn_clear)

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

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Filtrar histórico por título, link ou data...")
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

        # 3. Estado Vazio (Card)
        empty_card = QFrame()
        empty_card.setObjectName("emptyCard")
        empty_card.setStyleSheet("""
            QFrame#emptyCard {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 12px;
            }
            QLabel {
                border: none !important;
                background: transparent !important;
            }
        """)

        card_layout = QVBoxLayout(empty_card)
        card_layout.setContentsMargins(40, 60, 40, 60)
        card_layout.setAlignment(Qt.AlignCenter)

        icon_empty = QLabel("🕒")
        icon_empty.setStyleSheet("font-size: 48px;")
        icon_empty.setAlignment(Qt.AlignCenter)

        title_empty = QLabel("Nenhum histórico registrado")
        title_empty.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF; margin-top: 12px;")
        title_empty.setAlignment(Qt.AlignCenter)

        desc_empty = QLabel("As buscas, downloads concluídos e ações nos conectores serão registrados aqui automaticamente.")
        desc_empty.setStyleSheet("font-size: 13px; color: #71717A; margin-top: 4px;")
        desc_empty.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(icon_empty)
        card_layout.addWidget(title_empty)
        card_layout.addWidget(desc_empty)

        layout.addWidget(empty_card)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def on_show(self) -> None:
        pass


# Aliases para compatibilidade total
PRTHistoryPage = HistoryPage