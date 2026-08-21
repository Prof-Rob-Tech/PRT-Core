"""
===========================================================
PRT Labs - UI / History Page
Class: HistoryPage
Description: Tela de Histórico adaptativa a temas do PRT Nexus
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QHeaderView
)


class HistoryPage(QWidget):
    """Página de Histórico adaptativa aos temas Claro e Escuro."""

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setObjectName("historyPage")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(14)

        # 1. Cabeçalho (Título, Subtítulo e Botão Limpar)
        header_layout = QHBoxLayout()

        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        self.lbl_title = QLabel("Histórico de Atividades")
        self.lbl_title.setObjectName("historyTitle")
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; border: none;")

        self.lbl_subtitle = QLabel("Registro recente de downloads efetuados e URLs navegadas.")
        self.lbl_subtitle.setObjectName("historySubtitle")
        self.lbl_subtitle.setStyleSheet("font-size: 12px; opacity: 0.65; border: none;")

        title_box.addWidget(self.lbl_title)
        title_box.addWidget(self.lbl_subtitle)

        self.btn_clear = QPushButton("Limpar Histórico")
        self.btn_clear.setFixedHeight(34)
        self.btn_clear.setCursor(Qt.PointingHandCursor)
        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: rgba(239, 68, 68, 0.12);
                color: #EF4444;
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 6px;
                padding: 0 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #EF4444;
                color: #FFFFFF;
            }
        """)

        header_layout.addLayout(title_box)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_clear)
        main_layout.addLayout(header_layout)

        # 2. Campo de Pesquisa / Filtro
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("Filtrar histórico por título, link ou plataforma...")
        self.input_search.setFixedHeight(36)
        self.input_search.setStyleSheet("""
            QLineEdit {
                background-color: rgba(128, 128, 128, 0.08);
                border: 1px solid rgba(128, 128, 128, 0.22);
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #2563EB;
            }
        """)
        main_layout.addWidget(self.input_search)

        # 3. Conteúdo / Tabela e Estado Vazio
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Data / Hora", "Título / Item", "Plataforma", "Ação / Link"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: 1px solid rgba(128, 128, 128, 0.18);
                border-radius: 6px;
                gridline-color: rgba(128, 128, 128, 0.15);
            }
            QHeaderView::section {
                background-color: rgba(128, 128, 128, 0.08);
                padding: 6px;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid rgba(128, 128, 128, 0.2);
            }
        """)

        self.lbl_empty = QLabel("Nenhum histórico registrado até o momento.")
        self.lbl_empty.setAlignment(Qt.AlignCenter)
        self.lbl_empty.setStyleSheet("font-size: 13px; opacity: 0.55; margin: 40px 0; border: none;")

        main_layout.addWidget(self.lbl_empty)
        main_layout.addWidget(self.table)
        self.table.hide()

        main_layout.addStretch()