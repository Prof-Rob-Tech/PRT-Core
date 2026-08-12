"""
===========================================================
PRT Labs - UI / Pages
Class: DashboardPage
Description: Dashboard Principal do PRT NEXUS adaptável a temas.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class DashboardPage(QWidget):
    """Página Dashboard / Início do PRT NEXUS."""

    def __init__(self, parent=None, on_navigate=None) -> None:
        super().__init__(parent)
        self.on_navigate_callback = on_navigate
        self._build_ui()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Cabeçalho
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        lbl_title = QLabel("Dashboard PRT Nexus")
        lbl_title.setStyleSheet("font-size: 22px; font-weight: bold;")

        lbl_subtitle = QLabel("Central de download, extração de mídias e gestão de conectores.")
        lbl_subtitle.setStyleSheet("color: #8E8E93; font-size: 13px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        layout.addLayout(title_layout)

        # Cards de Status
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        stats = [
            ("Conectores", "8 Módulos Prontos", "#00E676"),
            ("Downloads Ativos", "0 em andamento", "#6366F1"),
            ("Mídias Salvas", "0 arquivos", "#FF9800"),
            ("Sistema Core", "100% Operacional", "#00F0FF"),
        ]

        for title, value, border_color in stats:
            card = QFrame()
            card.setObjectName("cardFrame")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(15, 12, 15, 12)

            lbl_t = QLabel(title)
            lbl_t.setStyleSheet("color: #8E8E93; font-size: 11px; font-weight: bold;")

            lbl_v = QLabel(value)
            lbl_v.setStyleSheet("font-size: 15px; font-weight: bold;")

            card_layout.addWidget(lbl_t)
            card_layout.addWidget(lbl_v)
            stats_layout.addWidget(card)

        layout.addLayout(stats_layout)

        # Seção Conectores
        lbl_sec = QLabel("Atalhos Rápido de Conectores")
        lbl_sec.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(lbl_sec)

        grid = QGridLayout()
        grid.setSpacing(12)

        connectors = [
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
        for name, desc, route in connectors:
            card = QFrame()
            card.setObjectName("cardFrame")
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(15, 15, 15, 15)

            lbl_n = QLabel(name)
            lbl_n.setStyleSheet("font-size: 14px; font-weight: bold;")

            lbl_d = QLabel(desc)
            lbl_d.setStyleSheet("color: #8E8E93; font-size: 12px;")

            btn = QPushButton("Acessar Módulo →")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, r=route: self._navigate(r))

            c_layout.addWidget(lbl_n)
            c_layout.addWidget(lbl_d)
            c_layout.addSpacing(8)
            c_layout.addWidget(btn)

            grid.addWidget(card, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        layout.addLayout(grid)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _navigate(self, route: str) -> None:
        if callable(self.on_navigate_callback):
            self.on_navigate_callback(route)