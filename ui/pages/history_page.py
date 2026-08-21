"""
===========================================================
PRT Labs - UI / History Page
Class: HistoryPage
Description: Tela de histórico de atividades e downloads dinâmico.
===========================================================
"""

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QScrollArea
)

# Ícone SVG de relógio minimalista e vetorial
CLOCK_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FAFAFA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="10"></circle>
    <polyline points="12 6 12 12 16 14"></polyline>
</svg>
"""


def get_svg_pixmap(svg_code: str, width: int = 22, height: int = 22) -> QPixmap:
    """Gera um QPixmap em memória a partir do código SVG."""
    renderer = QSvgRenderer(QByteArray(svg_code.encode("utf-8")))
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


class HistoryItemWidget(QFrame):
    """Widget para renderizar cada registro de histórico."""
    def __init__(self, title: str, platform: str, date: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #09090B;
                border: 1px solid #27272A;
                border-radius: 8px;
            }
            QFrame:hover {
                border-color: #3F3F46;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: bold; border: none;")

        lbl_info = QLabel(f"Plataforma: {platform}  •  Data: {date}")
        lbl_info.setStyleSheet("color: #71717A; font-size: 11px; border: none;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_info)


class HistoryPage(QWidget):
    """Página de histórico de downloads e navegação."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history_items = []
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # 1. Cabeçalho
        header_layout = QHBoxLayout()

        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        # Linha do Título com Ícone SVG
        title_row = QHBoxLayout()
        title_row.setSpacing(10)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(get_svg_pixmap(CLOCK_SVG, 22, 22))
        icon_lbl.setStyleSheet("border: none;")

        title = QLabel("Histórico de Atividades")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")

        title_row.addWidget(icon_lbl)
        title_row.addWidget(title)
        title_row.addStretch()

        subtitle = QLabel("Registro recente de downloads efetuados e URLs navegadas.")
        subtitle.setStyleSheet("font-size: 13px; color: #A1A1AA;")

        title_box.addLayout(title_row)
        title_box.addWidget(subtitle)

        btn_clear = QPushButton("Limpar Histórico")
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #18181B;
                color: #FAFAFA;
                border: 1px solid #27272A;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27272A;
                border-color: #EF4444;
                color: #EF4444;
            }
        """)
        btn_clear.clicked.connect(self.clear_history)

        header_layout.addLayout(title_box)
        header_layout.addStretch()
        header_layout.addWidget(btn_clear)

        main_layout.addLayout(header_layout)

        # 2. Campo de Filtro
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filtrar histórico por título, link ou plataforma...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #09090B;
                border: 1px solid #27272A;
                border-radius: 6px;
                padding: 10px 14px;
                color: #FFFFFF;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
            }
        """)
        self.search_input.textChanged.connect(self._filter_history)
        main_layout.addWidget(self.search_input)

        # 3. Lista Rolável
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.list_container = QWidget()
        self.list_container.setStyleSheet("background: transparent;")
        self.list_layout = QVBoxLayout(self.list_container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)

        self.scroll_area.setWidget(self.list_container)
        main_layout.addWidget(self.scroll_area)

        self.refresh_list()

    def refresh_list(self, filter_text: str = ""):
        """Atualiza a lista visualmente ou mostra o estado de histórico vazio."""
        while self.list_layout.count():
            child = self.list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        filtered = [
            item for item in self.history_items
            if filter_text.lower() in item['title'].lower() or filter_text.lower() in item['platform'].lower()
        ]

        if not filtered:
            empty_lbl = QLabel("Nenhum histórico registrado até o momento.")
            empty_lbl.setAlignment(Qt.AlignCenter)
            empty_lbl.setStyleSheet("color: #71717A; font-size: 13px; margin-top: 50px;")
            self.list_layout.addWidget(empty_lbl)
        else:
            for item in filtered:
                widget = HistoryItemWidget(item['title'], item['platform'], item['date'])
                self.list_layout.addWidget(widget)

        self.list_layout.addStretch()

    def _filter_history(self, text: str):
        self.refresh_list(text)

    def clear_history(self):
        """Esvazia o histórico e redesenha a tela."""
        self.history_items.clear()
        self.refresh_list()

    def add_entry(self, title: str, platform: str, date: str):
        """Método público para o backend inserir um item real no topo do histórico."""
        self.history_items.insert(0, {
            "title": title,
            "platform": platform,
            "date": date
        })
        self.refresh_list(self.search_input.text())