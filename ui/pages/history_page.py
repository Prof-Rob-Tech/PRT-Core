"""
===========================================================
PRT Labs - UI / Pages
Class: HistoryPage / PRTHistoryPage

Description:
    Página de Histórico de Atividades conectada ao SQLite
    (db_manager) com suporte a busca e limpeza.
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

from database.db_manager import db_manager


class HistoryPage(BasePage):
    """Página de Histórico de Atividades e Downloads."""

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
        self.subtitle = "Atividades Recentes"
        self.icon = "🕒"
        self.page_id = "history"

        self.all_items = []

        self.setStyleSheet("""
            QWidget {
                background-color: #09090B;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
        """)

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
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical { background: #09090B; width: 8px; margin: 0px; }
            QScrollBar::handle:vertical { background: #27272A; min-height: 20px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #3F3F46; }
        """)

        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        self.cards_layout = QVBoxLayout(container)
        self.cards_layout.setContentsMargins(24, 24, 24, 24)
        self.cards_layout.setSpacing(20)

        # 1. Header + Botão Limpar
        header_layout = QHBoxLayout()
        header_box = QVBoxLayout()
        lbl_title = QLabel("🕒 Histórico de Atividades")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; border: none;")
        lbl_subtitle = QLabel("Registro recente de downloads efetuados e URLs navegadas.")
        lbl_subtitle.setStyleSheet("font-size: 13px; color: #71717A; border: none;")
        header_box.addWidget(lbl_title)
        header_box.addWidget(lbl_subtitle)

        btn_clear = QPushButton("🗑️ Limpar Histórico")
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #27272A;
                color: #EF4444;
                border: 1px solid #3F3F46;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7F1D1D;
                color: #FFFFFF;
                border-color: #EF4444;
            }
        """)
        btn_clear.clicked.connect(self._on_clear_history)

        header_layout.addLayout(header_box)
        header_layout.addStretch()
        header_layout.addWidget(btn_clear)
        self.cards_layout.addLayout(header_layout)

        # 2. Barra de Pesquisa
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Filtrar histórico por título, link ou plataforma...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #18181B;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
            }
            QLineEdit:focus { border-color: #6366F1; }
        """)
        self.search_input.textChanged.connect(self._filter_items)
        self.cards_layout.addWidget(self.search_input)

        # 3. Estado Vazio
        self.empty_card = QFrame()
        self.empty_card.setStyleSheet("""
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 12px;
            }
            QLabel { border: none; background: transparent; }
        """)
        empty_layout = QVBoxLayout(self.empty_card)
        empty_layout.setContentsMargins(40, 50, 40, 50)
        empty_layout.setAlignment(Qt.AlignCenter)

        lbl_icon = QLabel("🕒")
        lbl_icon.setStyleSheet("font-size: 40px;")
        lbl_icon.setAlignment(Qt.AlignCenter)

        lbl_empty_t = QLabel("Nenhum histórico registrado")
        lbl_empty_t.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF; margin-top: 8px;")
        lbl_empty_t.setAlignment(Qt.AlignCenter)

        lbl_empty_d = QLabel("As buscas, downloads concluídos e ações nos conectores serão registrados aqui automaticamente.")
        lbl_empty_d.setStyleSheet("font-size: 13px; color: #71717A; margin-top: 4px;")
        lbl_empty_d.setAlignment(Qt.AlignCenter)

        empty_layout.addWidget(lbl_icon)
        empty_layout.addWidget(lbl_empty_t)
        empty_layout.addWidget(lbl_empty_d)

        self.cards_layout.addWidget(self.empty_card)

        # Container dinâmico
        self.items_container = QWidget()
        self.items_container.setStyleSheet("background: transparent;")
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setContentsMargins(0, 0, 0, 0)
        self.items_layout.setSpacing(10)

        self.cards_layout.addWidget(self.items_container)
        self.cards_layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        self.refresh_history()

    def refresh_history(self) -> None:
        """Carrega os dados do SQLite e renderiza na tela."""
        if hasattr(db_manager, "get_all_history"):
            self.all_items = db_manager.get_all_history()
        elif hasattr(db_manager, "get_history"):
            self.all_items = db_manager.get_history()
        else:
            self.all_items = db_manager.get_all_downloads()

        if not self.all_items:
            self.empty_card.setVisible(True)
            self.items_container.setVisible(False)
        else:
            self.empty_card.setVisible(False)
            self.items_container.setVisible(True)
            self._render_items(self.all_items)

    def _render_items(self, items: list) -> None:
        for i in reversed(range(self.items_layout.count())):
            widget = self.items_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for item in items:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #18181B;
                    border: 1px solid #27272A;
                    border-radius: 8px;
                }
                QLabel { border: none; background: transparent; }
            """)
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            card_layout.setSpacing(12)

            icon = QLabel("🔗")
            icon.setStyleSheet("font-size: 16px;")
            card_layout.addWidget(icon)

            info_box = QVBoxLayout()
            info_box.setSpacing(2)

            title_text = item.get("title") or item.get("url") or "Ação sem título"
            lbl_title = QLabel(title_text)
            lbl_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #E4E4E7;")

            platform = item.get("platform", "web").capitalize()
            url_str = item.get("url", "")
            time_str = item.get("created_at") or item.get("timestamp") or "Recente"

            sub_text = f"Plataforma: {platform} • Link: {url_str[:65]}... • Data: {time_str}" if len(url_str) > 65 else f"Plataforma: {platform} • Link: {url_str} • Data: {time_str}"
            lbl_sub = QLabel(sub_text)
            lbl_sub.setStyleSheet("font-size: 11px; color: #71717A;")

            info_box.addWidget(lbl_title)
            info_box.addWidget(lbl_sub)
            card_layout.addLayout(info_box, stretch=1)

            self.items_layout.addWidget(card)

    def _on_clear_history(self) -> None:
        """Limpa o histórico do banco de dados."""
        if hasattr(db_manager, "clear_history"):
            db_manager.clear_history()
        elif hasattr(db_manager, "clear_all_history"):
            db_manager.clear_all_history()
        
        self.refresh_history()

    def _filter_items(self, text: str) -> None:
        query = text.strip().lower()
        if not query:
            self._render_items(self.all_items)
        else:
            filtered = [
                item for item in self.all_items
                if query in (item.get("title") or "").lower()
                or query in (item.get("url") or "").lower()
                or query in (item.get("platform") or "").lower()
            ]
            self._render_items(filtered)

    def on_show(self) -> None:
        self.refresh_history()


PRTHistoryPage = HistoryPage