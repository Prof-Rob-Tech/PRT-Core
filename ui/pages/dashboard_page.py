"""
===========================================================
PRT Labs - UI / Dashboard Page
Class: DashboardPage
Description: Tela inicial (Início) 100% adaptativa a qualquer tema (Light/Dark)
===========================================================
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QGridLayout, QScrollArea
)


class StatCard(QFrame):
    """Card de estatísticas com indicador lateral interno adaptável a qualquer tema."""

    def __init__(self, title: str, value: str, accent_color: str = "#2563EB", parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setFixedHeight(80)
        self.setStyleSheet("""
            QFrame#statCard {
                background-color: rgba(128, 128, 128, 0.06);
                border: 1px solid rgba(128, 128, 128, 0.18);
                border-radius: 8px;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 16, 0)
        main_layout.setSpacing(14)

        # Faixa colorida lateral embutida com cantos perfeitamente alinhados
        accent_bar = QFrame()
        accent_bar.setFixedWidth(8)
        accent_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {accent_color};
                border-top-left-radius: 7px;
                border-bottom-left-radius: 7px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                border: none;
            }}
        """)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 14, 0, 14)
        content_layout.setSpacing(4)

        lbl_title = QLabel(title.upper())
        lbl_title.setStyleSheet("font-size: 11px; font-weight: 800; opacity: 0.65; border: none; letter-spacing: 0.5px;")

        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")

        content_layout.addWidget(lbl_title)
        content_layout.addWidget(lbl_value)

        main_layout.addWidget(accent_bar)
        main_layout.addLayout(content_layout, 1)


class QuickCard(QFrame):
    """Card de atalho rápido adaptável a qualquer tema."""

    def __init__(self, title: str, desc: str, route_id: str, on_navigate=None, parent=None):
        super().__init__(parent)
        self.route_id = route_id
        self.on_navigate = on_navigate
        self.setObjectName("quickCard")
        self.setStyleSheet("""
            QFrame#quickCard {
                background-color: rgba(128, 128, 128, 0.06);
                border: 1px solid rgba(128, 128, 128, 0.18);
                border-radius: 8px;
            }
            QFrame#quickCard:hover {
                border: 1px solid rgba(37, 99, 235, 0.5);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-size: 14px; font-weight: bold; border: none;")

        lbl_desc = QLabel(desc)
        lbl_desc.setStyleSheet("font-size: 11px; opacity: 0.65; border: none;")
        lbl_desc.setWordWrap(True)

        btn_action = QPushButton("Acessar Módulo →")
        btn_action.setFixedHeight(32)
        btn_action.setCursor(Qt.PointingHandCursor)
        btn_action.setStyleSheet("""
            QPushButton {
                background-color: rgba(128, 128, 128, 0.12);
                border: 1px solid rgba(128, 128, 128, 0.2);
                border-radius: 6px;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2563EB;
                color: #FFFFFF;
                border: none;
            }
        """)
        btn_action.clicked.connect(self._handle_click)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_desc)
        layout.addStretch()
        layout.addWidget(btn_action)

    def _handle_click(self):
        if callable(self.on_navigate):
            self.on_navigate(self.route_id)


class DashboardPage(QWidget):
    """Página Inicial (Dashboard) do PRT Nexus adaptativa a temas."""

    navigate = Signal(str)

    def __init__(self, parent=None, on_navigate=None, *args, **kwargs):
        super().__init__(parent)
        self.on_navigate_callback = on_navigate
        self.setObjectName("dashboardPage")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(16)

        # 1. Cabeçalho
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        title = QLabel("Dashboard PRT Nexus")
        title.setStyleSheet("font-size: 20px; font-weight: bold; border: none;")

        subtitle = QLabel("Central de download, extração de mídias e gestão de conectores.")
        subtitle.setStyleSheet("font-size: 12px; opacity: 0.65; border: none;")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(18)

        # 2. Cards de Estatísticas
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        stats_layout.addWidget(StatCard("Conectores", "8 Módulos Prontos", "#10B981"))
        stats_layout.addWidget(StatCard("Downloads Ativos", "0 em andamento", "#3B82F6"))
        stats_layout.addWidget(StatCard("Mídias Salvas", "0 arquivos", "#F59E0B"))
        stats_layout.addWidget(StatCard("Sistema Core", "100% Operacional", "#06B6D4"))

        content_layout.addLayout(stats_layout)

        # 3. Seção Atalhos Rápido
        sec_title = QLabel("Atalhos Rápido de Conectores")
        sec_title.setStyleSheet("font-size: 13px; font-weight: 800; opacity: 0.8; margin-top: 6px; border: none; letter-spacing: 0.5px;")
        content_layout.addWidget(sec_title)

        # Grid de Atalhos
        grid = QGridLayout()
        grid.setSpacing(12)

        shortcuts = [
            ("Navegador Web", "Navegar e extrair URLs direto de sites", "navegador"),
            ("Downloads", "Ver gerenciador e histórico de downloads", "downloads"),
            ("YouTube", "Download de vídeos, playlists e áudio", "conn_youtube"),
            ("TikTok", "Extrair vídeos e Reels sem marca d'água", "conn_tiktok"),
            ("Kiwify", "Acessar conteúdos da plataforma Kiwify", "conn_kiwify"),
            ("Hotmart", "Acessar áreas de membros da Hotmart", "conn_hotmart"),
            ("Google Drive", "Baixar arquivos e pastas do Drive", "conn_gdrive"),
            ("Universo Técnico", "Extrair aulas do Universo Técnico", "conn_universo"),
        ]

        row, col = 0, 0
        for item_title, desc, route_id in shortcuts:
            card = QuickCard(item_title, desc, route_id, on_navigate=self._trigger_navigate)
            grid.addWidget(card, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1

        content_layout.addLayout(grid)
        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def _trigger_navigate(self, route_id: str):
        self.navigate.emit(route_id)
        if callable(self.on_navigate_callback):
            self.on_navigate_callback(route_id)