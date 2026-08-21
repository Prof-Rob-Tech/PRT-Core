"""
===========================================================
PRT Labs - UI / Connector Page
Class: ConnectorPage
Description: Página de Conector Genérica adaptável aos temas do PRT Nexus
===========================================================
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QProgressBar, QGridLayout
)


class ConnectorPage(QWidget):
    """Página de Conector Genérica adaptável aos temas do PRT Nexus."""

    def __init__(self, platform_key: str = "conector", connector_name: str = "Conector", parent=None, *args, **kwargs):
        super().__init__(parent)
        self.platform_key = platform_key
        self.connector_name = connector_name.title() if connector_name else "Conector"
        self.setObjectName("connectorPage")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(14)

        # 1. Cabeçalho Adaptativo
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        self.lbl_title = QLabel(f"Conector {self.connector_name}")
        self.lbl_title.setObjectName("connectorTitle")
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; border: none;")

        self.lbl_subtitle = QLabel(f"Capture, extraia e gerencie conteúdos diretamente do {self.connector_name}.")
        self.lbl_subtitle.setObjectName("connectorSubtitle")
        self.lbl_subtitle.setStyleSheet("font-size: 12px; opacity: 0.7; border: none;")

        header_layout.addWidget(self.lbl_title)
        header_layout.addWidget(self.lbl_subtitle)
        main_layout.addLayout(header_layout)

        # 2. Card: Captura de Mídia
        card_captura = self._create_card()
        captura_layout = QVBoxLayout(card_captura)
        captura_layout.setSpacing(10)

        lbl_captura_title = QLabel(f"🔗 Captura de Mídia - {self.connector_name}")
        lbl_captura_title.setStyleSheet("font-weight: bold; font-size: 13px; border: none;")
        captura_layout.addWidget(lbl_captura_title)

        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("Cole o link do vídeo, áudio ou curso / playlist aqui...")
        self.input_url.setFixedHeight(36)
        captura_layout.addWidget(self.input_url)

        opt_box = QHBoxLayout()
        opt_box.setSpacing(10)

        lbl_qual = QLabel("Qualidade:")
        lbl_qual.setStyleSheet("font-size: 12px; font-weight: 500; border: none;")
        self.combo_quality = QComboBox()
        self.combo_quality.setFixedHeight(34)
        self.combo_quality.addItems([
            "📹 Vídeo - Max Qualidade (MP4)",
            "📹 Vídeo - 1080p (MP4)",
            "📹 Vídeo - 720p (MP4)",
            "🎵 Áudio - Max Qualidade (MP3)",
        ])

        self.btn_download_single = QPushButton("📥 Baixar Mídia Avulsa")
        self.btn_download_single.setFixedHeight(34)
        self.btn_download_single.setCursor(Qt.PointingHandCursor)
        self.btn_download_single.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: #FFFFFF;
                font-weight: 600;
                border-radius: 6px;
                padding: 0 14px;
                border: none;
            }
            QPushButton:hover { background-color: #1D4ED8; }
        """)

        self.btn_map_course = QPushButton("🗺️ Mapear e Baixar Curso / Playlist")
        self.btn_map_course.setFixedHeight(34)
        self.btn_map_course.setCursor(Qt.PointingHandCursor)
        self.btn_map_course.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: #FFFFFF;
                font-weight: 600;
                border-radius: 6px;
                padding: 0 14px;
                border: none;
            }
            QPushButton:hover { background-color: #059669; }
        """)

        opt_box.addWidget(lbl_qual)
        opt_box.addWidget(self.combo_quality, 1)
        opt_box.addWidget(self.btn_download_single)
        opt_box.addWidget(self.btn_map_course)
        captura_layout.addLayout(opt_box)

        main_layout.addWidget(card_captura)

        # 3. Grid: Autenticação + Organização de Pastas
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(14)

        # Card Auth
        card_auth = self._create_card()
        auth_layout = QVBoxLayout(card_auth)
        auth_layout.setSpacing(8)

        lbl_auth_title = QLabel("🔐 Autenticação (Áreas Pagas / Privadas)")
        lbl_auth_title.setStyleSheet("font-weight: bold; font-size: 12px; border: none;")
        auth_layout.addWidget(lbl_auth_title)

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("E-mail / Usuário")
        self.input_user.setFixedHeight(32)

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Senha")
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setFixedHeight(32)

        auth_layout.addWidget(self.input_user)
        auth_layout.addWidget(self.input_pass)
        grid_layout.addWidget(card_auth, 1)

        # Card Organização
        card_org = self._create_card()
        org_layout = QVBoxLayout(card_org)
        org_layout.setSpacing(8)

        lbl_org_title = QLabel("🔰 Organização de Pastas (Curso / Playlist)")
        lbl_org_title.setStyleSheet("font-weight: bold; font-size: 12px; border: none;")
        org_layout.addWidget(lbl_org_title)

        self.input_course_name = QLineEdit()
        self.input_course_name.setPlaceholderText("Nome do Conteúdo / Curso / Playlist")
        self.input_course_name.setFixedHeight(32)

        row_mod = QHBoxLayout()
        self.combo_mod = QComboBox()
        self.combo_mod.addItems([f"Mod {i}" for i in range(1, 21)])
        self.combo_mod.setFixedWidth(80)
        self.combo_mod.setFixedHeight(32)

        self.input_mod_name = QLineEdit()
        self.input_mod_name.setPlaceholderText("Nome do Módulo / Seção")
        self.input_mod_name.setFixedHeight(32)

        row_mod.addWidget(self.combo_mod)
        row_mod.addWidget(self.input_mod_name)

        row_item = QHBoxLayout()
        self.combo_item = QComboBox()
        self.combo_item.addItems([f"Item {i}" for i in range(1, 51)])
        self.combo_item.setFixedWidth(80)
        self.combo_item.setFixedHeight(32)

        self.input_item_name = QLineEdit()
        self.input_item_name.setPlaceholderText("Nome da Aula / Item")
        self.input_item_name.setFixedHeight(32)

        row_item.addWidget(self.combo_item)
        row_item.addWidget(self.input_item_name)

        org_layout.addWidget(self.input_course_name)
        org_layout.addLayout(row_mod)
        org_layout.addLayout(row_item)

        grid_layout.addWidget(card_org, 1)
        main_layout.addLayout(grid_layout)

        # 4. Card: Pasta de Destino + Progress Bar
        card_dest = self._create_card()
        dest_layout = QVBoxLayout(card_dest)
        dest_layout.setSpacing(8)

        lbl_dest_title = QLabel("📁 Pasta de Destino")
        lbl_dest_title.setStyleSheet("font-weight: bold; font-size: 12px; border: none;")
        dest_layout.addWidget(lbl_dest_title)

        path_box = QHBoxLayout()
        self.input_dest_path = QLineEdit("C:\\Users\\Downloads\\PRT_Nexus")
        self.input_dest_path.setReadOnly(True)
        self.input_dest_path.setFixedHeight(32)

        self.btn_change_dest = QPushButton("Alterar")
        self.btn_change_dest.setFixedHeight(32)
        self.btn_change_dest.setCursor(Qt.PointingHandCursor)

        path_box.addWidget(self.input_dest_path, 1)
        path_box.addWidget(self.btn_change_dest)
        dest_layout.addLayout(path_box)

        # Barra de Progresso e Status
        prog_box = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.lbl_status = QLabel("Aguardando link de download...")
        self.lbl_status.setStyleSheet("font-size: 11px; opacity: 0.7; border: none;")

        prog_box.addWidget(self.lbl_status)
        prog_box.addStretch()
        prog_box.addWidget(QLabel("0%"))

        dest_layout.addWidget(self.progress_bar)
        dest_layout.addLayout(prog_box)

        main_layout.addWidget(card_dest)

        # 5. Card: Mídias Concluídas (Tabela)
        card_table = self._create_card()
        table_layout = QVBoxLayout(card_table)
        table_layout.setSpacing(8)

        lbl_table_title = QLabel(f"📦 Mídias Concluídas do {self.connector_name}")
        lbl_table_title.setStyleSheet("font-weight: bold; font-size: 12px; border: none;")
        table_layout.addWidget(lbl_table_title)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["#", "Título / Nome do Arquivo", "Caminho Salvo", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: 1px solid rgba(128, 128, 128, 0.2);
                border-radius: 6px;
                gridline-color: rgba(128, 128, 128, 0.15);
            }
            QHeaderView::section {
                background-color: rgba(128, 128, 128, 0.1);
                padding: 6px;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid rgba(128, 128, 128, 0.2);
            }
        """)

        table_layout.addWidget(self.table)
        main_layout.addWidget(card_table, 1)

    def _create_card(self) -> QFrame:
        """Cria um card container adaptativo aos temas Claro e Escuro."""
        card = QFrame()
        card.setObjectName("connectorCard")
        card.setStyleSheet("""
            QFrame#connectorCard {
                background-color: rgba(128, 128, 128, 0.05);
                border: 1px solid rgba(128, 128, 128, 0.18);
                border-radius: 8px;
                padding: 10px;
            }
            QLineEdit, QComboBox {
                background-color: rgba(128, 128, 128, 0.08);
                border: 1px solid rgba(128, 128, 128, 0.25);
                border-radius: 6px;
                padding: 4px 8px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #2563EB;
            }
            QPushButton {
                border-radius: 6px;
                padding: 4px 12px;
            }
        """)
        return card