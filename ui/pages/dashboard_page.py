"""
===========================================================
PRT Labs - UI / Dashboard Page
Class: DashboardPage
Description: Tela inicial com resumo de métricas e
             grid de atalhos rápidos para conectores.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QGridLayout, QPushButton, QScrollArea
)


class DashboardPage(QWidget):
    """Página Dashboard principal do PRT Nexus."""

    def __init__(self, parent=None, on_navigate=None) -> None:
        super().__init__(parent)
        self.on_navigate_callback = on_navigate

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
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        container = QWidget()
        container.setStyleSheet("background-color: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # 1. Header de Boas-Vindas
        header_box = QVBoxLayout()
        title = QLabel("Dashboard PRT Nexus")
        title.setStyleSheet("font-size: 26px; font-weight: bold; color: #FFFFFF; border: none; background: transparent;")
        subtitle = QLabel("Central de download, extração de mídias e gestão de conectores.")
        subtitle.setStyleSheet("font-size: 14px; color: #71717A; border: none; background: transparent;")
        header_box.addWidget(title)
        header_box.addWidget(subtitle)
        layout.addLayout(header_box)

        # 2. Resumo de Métricas (8 Módulos Prontos)
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(16)

        metrics_layout.addWidget(self._create_stat_card("Conectores", "8 Módulos Prontos", "#10B981"))
        metrics_layout.addWidget(self._create_stat_card("Downloads Ativos", "0 em andamento", "#6366F1"))
        metrics_layout.addWidget(self._create_stat_card("Mídias Salvas", "0 arquivos", "#F59E0B"))
        metrics_layout.addWidget(self._create_stat_card("Sistema Core", "100% Operacional", "#3B82F6"))

        layout.addLayout(metrics_layout)

        # 3. Título da Seção Conectores
        sec_title = QLabel("Atalhos Rápidos de Conectores")
        sec_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #E4E4E7; margin-top: 12px; border: none; background: transparent;")
        layout.addWidget(sec_title)

        # 4. Grid de Cards dos Módulos (com TikTok incluso)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(16)

        cards_data = [
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
        for name, desc, route_id in cards_data:
            card = self._create_module_card(name, desc, route_id)
            grid_layout.addWidget(card, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        layout.addLayout(grid_layout)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _create_stat_card(self, title: str, value: str, accent_color: str) -> QFrame:
        card = QFrame()
        card.setObjectName("statCard")
        card.setStyleSheet(f"""
            QFrame#statCard {{
                background-color: #18181B;
                border: 1px solid #27272A;
                border-left: 4px solid {accent_color};
                border-radius: 8px;
            }}
            QFrame#statCard QLabel {{
                border: none !important;
                background: transparent !important;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #A1A1AA; font-size: 12px;")
        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold; margin-top: 4px;")

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        return card

    def _create_module_card(self, name: str, desc: str, route_id: str) -> QFrame:
        card = QFrame()
        card.setObjectName("moduleCard")
        card.setStyleSheet("""
            QFrame#moduleCard {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
            QFrame#moduleCard:hover {
                border: 1px solid #3F3F46;
                background-color: #202023;
            }
            QFrame#moduleCard QLabel {
                border: none !important;
                background: transparent !important;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)

        lbl_name = QLabel(name)
        lbl_name.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        
        lbl_desc = QLabel(desc)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("font-size: 12px; color: #A1A1AA; margin-top: 4px;")

        btn = QPushButton("Acessar Módulo →")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #27272A;
                color: #FFFFFF;
                border: 1px solid #3F3F46;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: 500;
                margin-top: 12px;
            }
            QPushButton:hover {
                background-color: #3F3F46;
            }
        """)
        btn.clicked.connect(lambda checked=False, r=route_id: self._navigate(r))

        layout.addWidget(lbl_name)
        layout.addWidget(lbl_desc)
        layout.addWidget(btn)
        return card

    def _navigate(self, route_id: str) -> None:
        if callable(self.on_navigate_callback):
            self.on_navigate_callback(route_id)