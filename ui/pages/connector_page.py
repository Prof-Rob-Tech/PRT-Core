"""
===========================================================
PRT Labs - UI / Pages
Class: ConnectorPage / PRTConnectorPage

Description:
    Página genérica para conectores com seletor de pasta de destino
    integrada ao DownloadManager e DatabaseManager.
===========================================================
"""

import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QScrollArea, QFileDialog
)

from core.download_manager import download_manager
from database.db_manager import db_manager


class ConnectorPage(QWidget):
    """Página de Conector com escolha de pasta personalizada."""

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
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical { background: #09090B; width: 8px; margin: 0px; }
            QScrollBar::handle:vertical { background: #27272A; min-height: 20px; border-radius: 4px; }
            QScrollBar::handle:vertical:hover { background: #3F3F46; }
        """)

        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # 1. Header
        header_box = QVBoxLayout()
        title = QLabel(f"Conector {self.display_name}")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; border: none; background: transparent;")
        
        subtitle = QLabel(f"Capture, extraia e gerencie conteúdos diretamente do {self.display_name}.")
        subtitle.setStyleSheet("font-size: 13px; color: #71717A; border: none; background: transparent;")
        
        header_box.addWidget(title)
        header_box.addWidget(subtitle)
        layout.addLayout(header_box)

        # 2. Card de Captura por URL + Seletor de Pasta
        capture_card = QFrame()
        capture_card.setObjectName("captureCard")
        capture_card.setStyleSheet("""
            QFrame#captureCard {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
            QLabel { border: none !important; background: transparent !important; }
        """)
        capture_layout = QVBoxLayout(capture_card)
        capture_layout.setContentsMargins(16, 16, 16, 16)
        capture_layout.setSpacing(12)

        card_title = QLabel(f"🔗 Capturar Mídia via URL - {self.display_name}")
        card_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #E4E4E7;")
        capture_layout.addWidget(card_title)

        # Campo de Input da URL
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
            QLineEdit:focus { border-color: #6366F1; }
        """)
        self.url_input.returnPressed.connect(self._on_analisar_url)
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
            QPushButton:hover { background-color: #4F46E5; }
        """)
        btn_fetch.clicked.connect(self._on_analisar_url)
        input_layout.addWidget(btn_fetch)

        capture_layout.addLayout(input_layout)

        # Seletor da Pasta de Destino
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(10)

        default_dir = os.path.join(os.path.expanduser("~"), "Downloads", "PRT_Nexus")
        os.makedirs(default_dir, exist_ok=True)

        self.folder_input = QLineEdit(default_dir)
        self.folder_input.setReadOnly(True)
        self.folder_input.setStyleSheet("""
            QLineEdit {
                background-color: #09090B;
                color: #A1A1AA;
                border: 1px solid #27272A;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
            }
        """)
        folder_layout.addWidget(self.folder_input)

        btn_browse = QPushButton("📁 Alterar Pasta")
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.setStyleSheet("""
            QPushButton {
                background-color: #27272A;
                color: #E4E4E7;
                border: 1px solid #3F3F46;
                padding: 8px 14px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3F3F46;
                color: #FFFFFF;
            }
        """)
        btn_browse.clicked.connect(self._on_select_folder)
        folder_layout.addWidget(btn_browse)

        capture_layout.addLayout(folder_layout)
        layout.addWidget(capture_card)

        # 3. Tabela de Mídias Reais do Banco
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        table_card.setStyleSheet("""
            QFrame#tableCard {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
            QLabel { border: none !important; background: transparent !important; }
        """)
        table_card_layout = QVBoxLayout(table_card)
        table_card_layout.setContentsMargins(16, 16, 16, 16)
        table_card_layout.setSpacing(12)

        table_title = QLabel(f"📦 Mídias Concluídas do {self.display_name}")
        table_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #E4E4E7;")
        table_card_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Título / Nome do Arquivo", "URL / Link", "Status"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setShowGrid(False)

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
        """)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.table.setColumnWidth(2, 120)

        table_card_layout.addWidget(self.table)
        layout.addWidget(table_card)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        self.refresh_table_data()

    def _on_select_folder(self) -> None:
        """Abre a caixa de diálogo para escolher a pasta de destino."""
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Destino", self.folder_input.text())
        if folder:
            self.folder_input.setText(folder)

    def refresh_table_data(self) -> None:
        all_downloads = db_manager.get_all_downloads()
        real_data = [d for d in all_downloads if d.get("platform") == self.platform_key]

        self.table.setRowCount(len(real_data))
        for row, item in enumerate(real_data):
            self.table.setRowHeight(row, 40)

            t_item = QTableWidgetItem(f"  {item.get('title', 'Mídia')}")
            u_item = QTableWidgetItem(item.get('url', ''))
            s_item = QTableWidgetItem(item.get('status', 'Concluído'))

            s_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(row, 0, t_item)
            self.table.setItem(row, 1, u_item)
            self.table.setItem(row, 2, s_item)

    def _on_analisar_url(self, *args) -> None:
        url = self.url_input.text().strip()
        save_path = self.folder_input.text().strip()
        if url:
            download_manager.add_download(
                url=url,
                title=f"Mídia do {self.display_name}",
                platform=self.platform_key,
                save_path=save_path
            )
            self.url_input.clear()

    def on_show(self) -> None:
        self.refresh_table_data()


PRTConnectorPage = ConnectorPage