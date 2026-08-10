"""
===========================================================
PRT Labs - UI / Pages
Class: ConnectorPage / PRTConnectorPage

Description:
    Página genérica e reutilizável para todos os conectores
    (YouTube, TikTok, Kiwify, Hotmart, Vimeo, Drive, Mega, Universo).
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QScrollArea
)


class ConnectorPage(QWidget):
    """Página de Conector genérica reutilizável."""

    def __init__(self, platform_key: str = "conector", connector_name: str = None, parent=None, *args, **kwargs) -> None:
        super().__init__(parent)

        if connector_name:
            self.platform_key = connector_name.lower().replace("-", "_").replace(" ", "_")
            self.display_name = connector_name
        elif isinstance(platform_key, str):
            self.platform_key = platform_key.lower().replace("-", "_").replace(" ", "_")
            self.display_name = platform_key.capitalize()
        else:
            self.platform_key = "conector"
            self.display_name = "Conector"

        NAMES_MAP = {
            "youtube": "YouTube",
            "tiktok": "TikTok",
            "kiwify": "Kiwify",
            "hotmart": "Hotmart",
            "vimeo": "Vimeo",
            "gdrive": "Google Drive",
            "google_drive": "Google Drive",
            "mega": "Mega",
            "universo": "Universo Técnico",
            "universo_tecnico": "Universo Técnico",
        }
        
        self.display_name = NAMES_MAP.get(self.platform_key, self.display_name)

        self.setStyleSheet("""
            QWidget {
                background-color: #09090B;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        self._setup_ui()

    def _setup_ui(self) -> None:
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

        # 1. Header do Conector
        header_box = QVBoxLayout()
        title = QLabel(f"Conector {self.display_name}")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; border: none; background: transparent;")
        
        subtitle = QLabel(f"Capture, extraia e gerencie conteúdos diretamente do {self.display_name}.")
        subtitle.setStyleSheet("font-size: 13px; color: #71717A; border: none; background: transparent;")
        
        header_box.addWidget(title)
        header_box.addWidget(subtitle)
        layout.addLayout(header_box)

        # 2. Card de Captura por URL
        capture_card = QFrame()
        capture_card.setObjectName("captureCard")
        capture_card.setStyleSheet("""
            QFrame#captureCard {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
            QLabel {
                border: none !important;
                background: transparent !important;
            }
        """)
        capture_layout = QVBoxLayout(capture_card)
        capture_layout.setContentsMargins(16, 16, 16, 16)
        capture_layout.setSpacing(12)

        card_title = QLabel(f"🔗 Capturar Mídia via URL - {self.display_name}")
        card_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #E4E4E7;")
        capture_layout.addWidget(card_title)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText(f"Cole o link do {self.display_name} aqui (ex: https://...)")
        self.url_input.setStyleSheet("""
            QLineEdit {
                background-color: #09090B;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 6px;
                padding: 10px 14px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #6366F1;
            }
        """)
        input_layout.addWidget(self.url_input)

        btn_fetch = QPushButton("Analisar Mídia")
        btn_fetch.setCursor(Qt.PointingHandCursor)
        btn_fetch.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """)
        input_layout.addWidget(btn_fetch)

        capture_layout.addLayout(input_layout)
        layout.addWidget(capture_card)

        # 3. Tabela de Mídias Recentes
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        table_card.setStyleSheet("""
            QFrame#tableCard {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
            QLabel {
                border: none !important;
                background: transparent !important;
            }
        """)
        table_card_layout = QVBoxLayout(table_card)
        table_card_layout.setContentsMargins(16, 16, 16, 16)
        table_card_layout.setSpacing(12)

        table_title = QLabel("📦 Mídias Recentes Capturadas neste Conector")
        table_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #E4E4E7;")
        table_card_layout.addWidget(table_title)

        # Tabela Estilizada
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Título / Nome do Arquivo", "Qualidade / Formato", "Tamanho Est.", "Ação"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setShowGrid(False)

        # Estilo CSS da Tabela
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #09090B;
                border: 1px solid #27272A;
                border-radius: 8px;
                gridline-color: transparent;
                color: #E4E4E7;
            }
            QHeaderView::section {
                background-color: #18181B;
                color: #A1A1AA;
                font-weight: bold;
                font-size: 12px;
                border: none;
                border-bottom: 1px solid #27272A;
                padding: 10px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #18181B;
                font-size: 13px;
            }
            QTableWidget::item:selected {
                background-color: #27272A;
                color: #FFFFFF;
            }
        """)

        # Configuração das Colunas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        header.setSectionResizeMode(2, QHeaderView.Interactive)
        header.setSectionResizeMode(3, QHeaderView.Fixed)

        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 130)

        # Dados Exemplo
        sample_data = [
            (f"Vídeo de Exemplo {self.display_name} #01", "1080p (MP4/HLS)", "450 MB"),
            (f"Material Complementar {self.display_name} #02", "720p (MP4)", "120 MB"),
            (f"Transmissão Gravada {self.display_name} #03", "4K Ultra HD", "1.2 GB"),
        ]

        self.table.setRowCount(len(sample_data))
        for row, (item_title, qual, size) in enumerate(sample_data):
            # Define altura confortável de 42px para cada linha
            self.table.setRowHeight(row, 42)

            t_item = QTableWidgetItem(f"  {item_title}")
            t_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            q_item = QTableWidgetItem(qual)
            q_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            s_item = QTableWidgetItem(size)
            s_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)

            self.table.setItem(row, 0, t_item)
            self.table.setItem(row, 1, q_item)
            self.table.setItem(row, 2, s_item)

            # Botão de Ação Ajustado
            btn_action = QPushButton("⬇️ Baixar")
            btn_action.setCursor(Qt.PointingHandCursor)
            btn_action.setFixedHeight(28)
            btn_action.setStyleSheet("""
                QPushButton {
                    background-color: #6366F1;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 6px;
                    padding: 0px 12px;
                    font-size: 12px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #4F46E5;
                }
            """)

            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.setContentsMargins(6, 0, 10, 0)
            cell_layout.setAlignment(Qt.AlignCenter)
            cell_layout.addWidget(btn_action)

            self.table.setCellWidget(row, 3, cell_widget)

        self.table.setFixedHeight(180)
        table_card_layout.addWidget(self.table)

        layout.addWidget(table_card)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def on_show(self) -> None:
        pass


# Alias de compatibilidade
PRTConnectorPage = ConnectorPage