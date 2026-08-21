"""
===========================================================
PRT Labs - UI / Dashboard Page
Class: DashboardPage
Description: Tela inicial do PRT Nexus com métricas e atalhos rápidos.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGridLayout
)


class StatCard(QFrame):
    """Card de métrica do Dashboard com faixa lateral encorpada."""
    def __init__(self, title: str, value: str, border_color: str, parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.setStyleSheet("""
            QFrame {
                background-color: #09090B;
                border: 1px solid #27272A;
                border-radius: 8px;
            }
        """)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Faixa colorida mais larga (10px) colada na borda esquerda
        bar = QFrame()
        bar.setFixedWidth(10)
        bar.setStyleSheet(f"""
            QFrame {{
                background-color: {border_color};
                border-top-left-radius: 7px;
                border-bottom-left-radius: 7px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                border: none;
            }}
        """)

        content = QWidget()
        content.setStyleSheet("background: transparent; border: none;")
        text_layout = QVBoxLayout(content)
        text_layout.setContentsMargins(18, 16, 18, 16)
        text_layout.setSpacing(10)

        lbl_title = QLabel(title.upper())
        lbl_title.setStyleSheet("color: #A1A1AA; font-size: 11px; font-weight: bold; border: none;")

        lbl_val = QLabel(value)
        lbl_val.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold; border: none;")

        text_layout.addWidget(lbl_title)
        text_layout.addWidget(lbl_val)
        text_layout.addStretch()

        main_layout.addWidget(bar)
        main_layout.addWidget(content, 1)


class ShortcutCard(QFrame):
    """Card de atalho rápido de conector."""
    def __init__(self, title: str, desc: str, route_id: str, on_navigate=None, parent=None):
        super().__init__(parent)
        self.setFixedHeight(110)
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
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: bold; border: none;")

        lbl_desc = QLabel(desc)
        lbl_desc.setStyleSheet("color: #71717A; font-size: 11px; border: none;")

        btn = QPushButton("Acessar Módulo →")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #18181B;
                color: #FAFAFA;
                border: 1px solid #27272A;
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
                font-weight: bold;
                margin-top: 4px;
            }
            QPushButton:hover {
                background-color: #27272A;
            }
        """)

        if callable(on_navigate):
            btn.clicked.connect(lambda: on_navigate(route_id))

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_desc)
        layout.addWidget(btn)


class DashboardPage(QWidget):
    """Página principal do Dashboard."""
    def __init__(self, parent=None, on_navigate=None):
        super().__init__(parent)
        self.on_navigate = on_navigate
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 18, 24, 18)
        main_layout.setSpacing(14)

        # 1. Cabeçalho
        header_box = QVBoxLayout()
        header_box.setSpacing(2)

        title = QLabel("Dashboard PRT Nexus")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")

        subtitle = QLabel("Central de download, extração de mídias e gestão de conectores.")
        subtitle.setStyleSheet("font-size: 13px; color: #A1A1AA;")

        header_box.addWidget(title)
        header_box.addWidget(subtitle)
        main_layout.addLayout(header_box)

        # 2. Grid de Métricas
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(14)

        stats_layout.addWidget(StatCard("Conectores", "8 Módulos Prontos", "#00E676"))
        stats_layout.addWidget(StatCard("Downloads Ativos", "0 em andamento", "#6366F1"))
        stats_layout.addWidget(StatCard("Mídias Salvas", "0 arquivos", "#F59E0B"))
        stats_layout.addWidget(StatCard("Sistema Core", "100% Operacional", "#00BCD4"))

        main_layout.addLayout(stats_layout)

        # 3. Título dos Atalhos
        sec_title = QLabel("Atalhos Rápido de Conectores")
        sec_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #FFFFFF; margin-top: 4px;")
        main_layout.addWidget(sec_title)

        # 4. Grid de Atalhos
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)

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
        for item in shortcuts:
            card = ShortcutCard(item[0], item[1], item[2], on_navigate=self.on_navigate)
            grid_layout.addWidget(card, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        main_layout.addLayout(grid_layout)
        main_layout.addStretch()