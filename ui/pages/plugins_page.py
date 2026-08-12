"""
===========================================================
PRT Labs - UI / Pages
Class: PluginsPage
Description: Gerenciador de Plugins e Conectores adaptável a temas.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class PluginsPage(QWidget):
    """Página de Gerenciamento de Plugins do PRT NEXUS."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
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
        layout.setSpacing(15)

        # Cabeçalho
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        lbl_title = QLabel("🧩 Gerenciador de Plugins & Conectores")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        lbl_subtitle = QLabel("Habilite, configure ou atualize os módulos de intercepção das plataformas de membros e players.")
        lbl_subtitle.setStyleSheet("color: #8E8E93; font-size: 13px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        layout.addLayout(title_layout)

        # Barra de Pesquisa e Filtros
        filter_layout = QHBoxLayout()
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Filtrar plugin por nome ou plataforma...")

        btn_all = QPushButton("Todos")
        btn_plat = QPushButton("Plataformas")
        btn_play = QPushButton("Players")

        for btn in (btn_all, btn_plat, btn_play):
            btn.setCursor(Qt.PointingHandCursor)

        filter_layout.addWidget(self.txt_search, stretch=3)
        filter_layout.addWidget(btn_all)
        filter_layout.addWidget(btn_plat)
        filter_layout.addWidget(btn_play)

        layout.addLayout(filter_layout)

        # Lista de Plugins (Grid)
        grid = QGridLayout()
        grid.setSpacing(12)

        plugins_list = [
            ("Kiwify Conector", "v2.1.4", "Suporte a mapeamento de módulos e vídeo.", True),
            ("Hotmart Club", "v1.9.0", "Extração de mídias e anexos do Hotmart Club v3.", True),
            ("Panda Video Sniffer", "v3.0.1", "Bypass em proteção DRM básica e captura HLS.", True),
            ("Vimeo HLS Pro", "v2.5.0", "Decodificação de playlists M3U8 e vídeos privados.", True),
            ("YouTube Downloader", "v4.1.0", "Captura de vídeos públicos, unlisted e playlists.", True),
            ("Google Drive / Mega", "v1.2.0", "Download acelerado de pastas compartilhadas.", False),
            ("Eduzz / Nutror", "v1.0.5", "Mapeamento completo de aulas do Nutror.", True),
            ("Memberkit Enterprise", "v1.1.0", "Acesso direto a áreas Memberkit.", False),
        ]

        row, col = 0, 0
        for name, ver, desc, active in plugins_list:
            card = QFrame()
            card.setObjectName("cardFrame")
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(15, 15, 15, 15)
            c_layout.setSpacing(8)

            head = QHBoxLayout()
            lbl_n = QLabel(name)
            lbl_n.setStyleSheet("font-weight: bold; font-size: 13px;")

            status_txt = "● Ativo" if active else "○ Inativo"
            status_color = "#00E676" if active else "#8E8E93"
            lbl_s = QLabel(status_txt)
            lbl_s.setStyleSheet(f"color: {status_color}; font-weight: bold; font-size: 11px;")

            head.addWidget(lbl_n)
            head.addStretch()
            head.addWidget(lbl_s)

            lbl_v = QLabel(f"Versão {ver}")
            lbl_v.setStyleSheet("color: #8E8E93; font-size: 11px;")

            lbl_d = QLabel(desc)
            lbl_d.setStyleSheet("font-size: 12px;")
            lbl_d.setWordWrap(True)

            btn_cfg = QPushButton("⚙️ Configurar")
            btn_cfg.setCursor(Qt.PointingHandCursor)

            c_layout.addLayout(head)
            c_layout.addWidget(lbl_v)
            c_layout.addWidget(lbl_d)
            c_layout.addSpacing(6)
            c_layout.addWidget(btn_cfg)

            grid.addWidget(card, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        layout.addLayout(grid)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)