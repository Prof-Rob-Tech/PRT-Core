"""
===========================================================
PRT Labs - UI / Pages
Class: ConnectorPage
Description: Template genérico para conectores (TikTok, YouTube, etc.) adaptável.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)


class ConnectorPage(QWidget):
    """Página de Conector Genérica adaptável aos temas do PRT Nexus."""

    def __init__(self, platform_key: str = "conector", connector_name: str = "Conector", parent=None) -> None:
        super().__init__(parent)
        self.platform_key = platform_key
        self.connector_name = connector_name.capitalize()
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Cabeçalho
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        lbl_title = QLabel(f"Conector {self.connector_name}")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        lbl_subtitle = QLabel(f"Capture, extraia e gerencie conteúdos diretamente do {self.connector_name}.")
        lbl_subtitle.setStyleSheet("color: #8E8E93; font-size: 13px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        layout.addLayout(title_layout)

        # Card de Captura por URL
        card_capture = QFrame()
        card_capture.setObjectName("cardFrame")
        c_layout = QVBoxLayout(card_capture)
        c_layout.setContentsMargins(15, 15, 15, 15)
        c_layout.setSpacing(12)

        lbl_cap_title = QLabel(f"🔗 Capturar Mídia via URL - {self.connector_name}")
        lbl_cap_title.setStyleSheet("font-weight: bold; font-size: 13px;")
        c_layout.addWidget(lbl_cap_title)

        input_layout = QHBoxLayout()
        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText(f"Cole o link do {self.connector_name} aqui (ex: https://...)")

        self.combo_format = QComboBox()
        self.combo_format.addItems(["📹 Vídeo (Melhor Qualidade)", "🎵 Apenas Áudio (MP3)"])

        btn_analyze = QPushButton("Analisar Mídia")
        btn_analyze.setCursor(Qt.PointingHandCursor)

        input_layout.addWidget(self.txt_url, stretch=3)
        input_layout.addWidget(self.combo_format, stretch=1)
        input_layout.addWidget(btn_analyze)

        c_layout.addLayout(input_layout)

        # Pasta de Saída
        folder_layout = QHBoxLayout()
        self.txt_folder = QLineEdit("C:\\Users\\Public\\Downloads\\PRT_Nexus")
        btn_folder = QPushButton("📁 Alterar Pasta")
        btn_folder.setCursor(Qt.PointingHandCursor)

        folder_layout.addWidget(self.txt_folder, stretch=4)
        folder_layout.addWidget(btn_folder, stretch=1)
        c_layout.addLayout(folder_layout)

        layout.addWidget(card_capture)

        # Tabela de Mídias Concluídas
        card_table = QFrame()
        card_table.setObjectName("cardFrame")
        t_layout = QVBoxLayout(card_table)
        t_layout.setContentsMargins(15, 15, 15, 15)

        lbl_tbl_title = QLabel(f"📦 Mídias Concluídas do {self.connector_name}")
        lbl_tbl_title.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 8px;")
        t_layout.addWidget(lbl_tbl_title)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Título / Nome do Arquivo", "URL / Fonte", "Ações"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFixedHeight(180)

        t_layout.addWidget(self.table)
        layout.addWidget(card_table)

        layout.addStretch()