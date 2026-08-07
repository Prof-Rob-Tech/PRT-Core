"""
===========================================================
PRT Labs - UI / Pages
Class: PluginsPage

Description:
    Tela de Gerenciamento de Plugins e Conectores de Mídias.
    Exibe os conectores suportados (Kiwify, Hotmart, YouTube, Vimeo, 
    Panda, etc.), seus status de ativação, versões e configurações.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
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
    """Página de Gerenciamento de Plugins e Conectores de Plataformas."""

    def __init__(self) -> None:
        super().__init__()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: #0E0F12;
                border: none;
            }
            QScrollBar:vertical {
                background: #121318;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #27272A;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3F3F46;
            }
        """
        )

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(20)

        # 1. Cabeçalho
        container_layout.addLayout(self._create_header())

        # 2. Barra de Busca e Filtros
        container_layout.addLayout(self._create_search_bar())

        # 3. Grid de Plugins/Conectores
        container_layout.addLayout(self._create_plugins_grid())

        container_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _create_header(self) -> QVBoxLayout:
        """Cria o cabeçalho da página."""
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        lbl_title = QLabel("🧩 Gerenciador de Plugins & Conectores")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")

        lbl_subtitle = QLabel(
            "Habilite, configure ou atualize os módulos de interceptação das plataformas de membros e players."
        )
        lbl_subtitle.setStyleSheet("color: #A1A1AA; font-size: 14px;")

        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_subtitle)

        return header_layout

    def _create_search_bar(self) -> QHBoxLayout:
        """Cria a barra de pesquisa e filtros por categoria."""
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Filtrar plugin por nome ou plataforma...")
        self.txt_search.setStyleSheet(
            """
            QLineEdit {
                background-color: #18181B;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #6366F1;
            }
        """
        )

        btn_all = QPushButton("Todos")
        btn_platforms = QPushButton("Plataformas")
        btn_players = QPushButton("Players")
        btn_cloud = QPushButton("Nuvem")

        filter_buttons = [btn_all, btn_platforms, btn_players, btn_cloud]
        for idx, btn in enumerate(filter_buttons):
            is_active = idx == 0
            bg_color = "#6366F1" if is_active else "#18181B"
            text_color = "#FFFFFF" if is_active else "#A1A1AA"
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {bg_color};
                    color: {text_color};
                    border: 1px solid #27272A;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    background-color: #27272A;
                    color: #FFFFFF;
                }}
            """
            )

        layout.addWidget(self.txt_search, stretch=1)
        for btn in filter_buttons:
            layout.addWidget(btn)

        return layout

    def _create_plugins_grid(self) -> QGridLayout:
        """Cria a grade contendo os cartões de cada conector."""
        grid = QGridLayout()
        grid.setSpacing(16)

        plugins_list = [
            {
                "name": "Kiwify Conector",
                "category": "Plataforma",
                "desc": "Suporte a mapeamento de módulos, aulas e vídeos hospedados na Kiwify/Nutror.",
                "version": "v2.1.4",
                "active": True,
                "icon": "🟢",
            },
            {
                "name": "Hotmart Club",
                "category": "Plataforma",
                "desc": "Extração de mídias, anexos e estrutura de módulos do Hotmart Club v3.",
                "version": "v1.9.0",
                "active": True,
                "icon": "🔥",
            },
            {
                "name": "Panda Video Sniffer",
                "category": "Player",
                "desc": "Bypass em proteção DRM básica e captura de streams HLS de alta qualidade.",
                "version": "v3.0.1",
                "active": True,
                "icon": "🐼",
            },
            {
                "name": "Vimeo HLS Pro",
                "category": "Player",
                "desc": "Decodificação de playlists M3U8 e extração de vídeos restritos/privados.",
                "version": "v2.5.0",
                "active": True,
                "icon": "🔹",
            },
            {
                "name": "YouTube Downloader",
                "category": "Player",
                "desc": "Captura de vídeos públicos, unlisted, playlists e lives gravadas em até 4K.",
                "version": "v4.1.0",
                "active": True,
                "icon": "▶️",
            },
            {
                "name": "Google Drive / Mega",
                "category": "Nuvem",
                "desc": "Download acelerado de arquivos grandes e pastas compartilhadas.",
                "version": "v1.2.0",
                "active": False,
                "icon": "☁️",
            },
            {
                "name": "Eduzz / Nutror",
                "category": "Plataforma",
                "desc": "Integração para extração de cursos e materiais da plataforma Eduzz.",
                "version": "v1.0.5",
                "active": True,
                "icon": "🎯",
            },
            {
                "name": "Memberkit Enterprise",
                "category": "Plataforma",
                "desc": "Mapeador completo de áreas de membros customizadas Memberkit.",
                "version": "v1.1.0",
                "active": False,
                "icon": "⚙️",
            },
        ]

        row, col = 0, 0
        max_cols = 2  # 2 cartões por linha

        for p in plugins_list:
            card = self._build_plugin_card(p)
            grid.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        return grid

    def _build_plugin_card(self, plugin: dict) -> QFrame:
        """Constrói o widget visual de um conector específico."""
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 12px;
            }
            QFrame:hover {
                border: 1px solid #3F3F46;
            }
        """
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        # Topo: Ícone + Nome + Toggle Switch
        top = QHBoxLayout()
        top.setSpacing(10)

        lbl_icon = QLabel(plugin["icon"])
        lbl_icon.setStyleSheet("font-size: 20px;")

        v_info = QVBoxLayout()
        v_info.setSpacing(2)
        lbl_name = QLabel(plugin["name"])
        lbl_name.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")

        lbl_cat = QLabel(f"{plugin['category']} • {plugin['version']}")
        lbl_cat.setStyleSheet("color: #71717A; font-size: 11px;")

        v_info.addWidget(lbl_name)
        v_info.addWidget(lbl_cat)

        chk_toggle = QCheckBox("Ativo" if plugin["active"] else "Inativo")
        chk_toggle.setChecked(plugin["active"])
        chk_toggle.setStyleSheet(
            """
            QCheckBox {
                color: #A1A1AA;
                font-size: 12px;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #3F3F46;
                background-color: #0E0F12;
            }
            QCheckBox::indicator:checked {
                background-color: #22C55E;
                border: 1px solid #22C55E;
            }
        """
        )

        top.addWidget(lbl_icon)
        top.addLayout(v_info, stretch=1)
        top.addWidget(chk_toggle)

        layout.addLayout(top)

        # Descrição
        lbl_desc = QLabel(plugin["desc"])
        lbl_desc.setStyleSheet("color: #A1A1AA; font-size: 12px;")
        lbl_desc.setWordWrap(True)
        layout.addWidget(lbl_desc)

        # Rodapé do Card
        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 4, 0, 0)

        lbl_status = QLabel("● Ativo & Pronto" if plugin["active"] else "○ Desativado")
        color = "#22C55E" if plugin["active"] else "#71717A"
        lbl_status.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")

        btn_config = QPushButton("⚙️ Configurar")
        btn_config.setStyleSheet(
            """
            QPushButton {
                background-color: #27272A;
                color: #FFFFFF;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3F3F46;
            }
        """
        )

        bottom.addWidget(lbl_status)
        bottom.addStretch()
        bottom.addWidget(btn_config)

        layout.addLayout(bottom)

        return card