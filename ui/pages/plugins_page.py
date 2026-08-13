"""
===========================================================
PRT Labs - UI / Pages
Class: PluginsPage

Description:
    Gerenciador de Plugins & Conectores do PRT NEXUS
    com visual moderno, cards interativos, filtros e badges.
===========================================================
"""

from PySide6.QtCore import Qt, Signal
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

PLUGINS_DATA = [
    {
        "id": "kiwify",
        "name": "Kiwify Conector",
        "version": "v2.1.4",
        "category": "Plataformas",
        "description": "Suporte a mapeamento de módulos e vídeo.",
        "status": True,
        "icon": "💚",
    },
    {
        "id": "hotmart",
        "name": "Hotmart Club",
        "version": "v1.9.0",
        "category": "Plataformas",
        "description": "Extração de mídias e anexos do Hotmart Club v3.",
        "status": True,
        "icon": "🔥",
    },
    {
        "id": "panda",
        "name": "Panda Video Sniffer",
        "version": "v3.0.1",
        "category": "Players",
        "description": "Bypass em proteção DRM básica e captura HLS.",
        "status": True,
        "icon": "🐼",
    },
    {
        "id": "vimeo",
        "name": "Vimeo HLS Pro",
        "version": "v2.5.0",
        "category": "Players",
        "description": "Decodificação de playlists M3U8 e vídeos privados.",
        "status": True,
        "icon": "🌐",
    },
    {
        "id": "youtube",
        "name": "YouTube Downloader",
        "version": "v4.1.0",
        "category": "Players",
        "description": "Captura de vídeos públicos, unlisted e playlists.",
        "status": True,
        "icon": "🔴",
    },
    {
        "id": "gdrive_mega",
        "name": "Google Drive / Mega",
        "version": "v1.2.0",
        "category": "Plataformas",
        "description": "Download acelerado de pastas compartilhadas.",
        "status": False,
        "icon": "📁",
    },
    {
        "id": "eduzz",
        "name": "Eduzz / Nutror",
        "version": "v1.0.5",
        "category": "Plataformas",
        "description": "Mapeamento completo de aulas do Nutror.",
        "status": True,
        "icon": "🎓",
    },
    {
        "id": "memberkit",
        "name": "Memberkit Enterprise",
        "version": "v1.1.0",
        "category": "Plataformas",
        "description": "Acesso direto a áreas Memberkit.",
        "status": False,
        "icon": "💎",
    },
]


class PluginCard(QFrame):
    """Card estilizado e dinâmico para cada conector."""

    configure_clicked = Signal(str)

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.plugin_data = data
        self.setObjectName("pluginCard")
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("""
            QFrame#pluginCard {
                background-color: #121215;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
            QFrame#pluginCard:hover {
                border: 1px solid #6366F1;
                background-color: #16161A;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Cabeçalho do Card (Ícone, Nome, Badge)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        icon_lbl = QLabel(self.plugin_data["icon"])
        icon_lbl.setStyleSheet("font-size: 22px; background: transparent;")
        header_layout.addWidget(icon_lbl)

        name_box = QVBoxLayout()
        name_box.setSpacing(2)

        title_lbl = QLabel(self.plugin_data["name"])
        title_lbl.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #FFFFFF;"
        )

        ver_lbl = QLabel(f"Versão {self.plugin_data['version']}")
        ver_lbl.setStyleSheet("font-size: 11px; color: #71717A;")

        name_box.addWidget(title_lbl)
        name_box.addWidget(ver_lbl)
        header_layout.addLayout(name_box)

        header_layout.addStretch()

        # Status Badge Pill (Pílula colorida com opacidade)
        status_badge = QLabel()
        is_active = self.plugin_data["status"]
        if is_active:
            status_badge.setText("● Ativo")
            status_badge.setStyleSheet("""
                background-color: rgba(34, 197, 94, 0.12);
                color: #22C55E;
                border: 1px solid rgba(34, 197, 94, 0.3);
                border-radius: 12px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: bold;
            """)
        else:
            status_badge.setText("○ Inativo")
            status_badge.setStyleSheet("""
                background-color: rgba(113, 113, 122, 0.12);
                color: #71717A;
                border: 1px solid rgba(113, 113, 122, 0.3);
                border-radius: 12px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 500;
            """)

        header_layout.addWidget(status_badge)
        layout.addLayout(header_layout)

        # Descrição
        desc_lbl = QLabel(self.plugin_data["description"])
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet(
            "font-size: 12px; color: #A1A1AA; min-height: 34px;"
        )
        layout.addWidget(desc_lbl)

        # Botão de Ação
        btn_config = QPushButton("⚙ Configurar")
        btn_config.setCursor(Qt.PointingHandCursor)
        btn_config.setStyleSheet("""
            QPushButton {
                background-color: #18181B;
                color: #E4E4E7;
                border: 1px solid #3F3F46;
                border-radius: 6px;
                padding: 8px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #27272A;
                color: #FFFFFF;
                border-color: #6366F1;
            }
        """)
        btn_config.clicked.connect(
            lambda: self.configure_clicked.emit(self.plugin_data["id"])
        )
        layout.addWidget(btn_config)


class PluginsPage(QWidget):
    """Página de Gerenciamento de Plugins e Conectores."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards = []
        self.current_filter = "Todos"
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # --- CABEÇALHO DA PÁGINA ---
        header_layout = QVBoxLayout()
        header_layout.setSpacing(6)

        title_layout = QHBoxLayout()
        title_icon = QLabel("🧩")
        title_icon.setStyleSheet("font-size: 22px;")
        title_lbl = QLabel("Gerenciador de Plugins & Conectores")
        title_lbl.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #FFFFFF;"
        )

        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_lbl)
        title_layout.addStretch()

        subtitle_lbl = QLabel(
            "Habilite, configure ou atualize os módulos de intercepção das plataformas de membros e players."
        )
        subtitle_lbl.setStyleSheet("font-size: 13px; color: #71717A;")

        header_layout.addLayout(title_layout)
        header_layout.addWidget(subtitle_lbl)
        main_layout.addLayout(header_layout)

        # --- BARRA DE FILTROS E PESQUISA ---
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "🔍  Filtrar plugin por nome ou plataforma..."
        )
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #121215;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #6366F1;
            }
        """)
        self.search_input.textChanged.connect(self._filter_cards)
        filter_bar.addWidget(self.search_input, stretch=1)

        # Botões de Categoria
        self.filter_buttons = {}
        for cat in ["Todos", "Plataformas", "Players"]:
            btn = QPushButton(cat)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setCheckable(True)
            if cat == "Todos":
                btn.setChecked(True)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #121215;
                    color: #A1A1AA;
                    border: 1px solid #27272A;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #18181B;
                    color: #FFFFFF;
                }
                QPushButton:checked {
                    background-color: #6366F1;
                    color: #FFFFFF;
                    border-color: #6366F1;
                }
            """)
            btn.clicked.connect(lambda _, c=cat: self._set_category_filter(c))
            filter_bar.addWidget(btn)
            self.filter_buttons[cat] = btn

        main_layout.addLayout(filter_bar)

        # --- ÁREA COM SCROLL DOS CARDS ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #09090B;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #27272A;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #3F3F46;
            }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        self.grid_layout = QGridLayout(scroll_content)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(16)

        self._render_cards()

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

    def _render_cards(self):
        for card in self.cards:
            card[1].setParent(None)
        self.cards.clear()

        row = 0
        col = 0
        for item in PLUGINS_DATA:
            card = PluginCard(item)
            card.configure_clicked.connect(self._on_configure_plugin)
            self.grid_layout.addWidget(card, row, col)
            self.cards.append((item, card))

            col += 1
            if col > 1:
                col = 0
                row += 1

    def _set_category_filter(self, category: str):
        self.current_filter = category
        for cat, btn in self.filter_buttons.items():
            btn.setChecked(cat == category)
        self._filter_cards()

    def _filter_cards(self):
        search_text = self.search_input.text().lower().strip()

        for item, card in self.cards:
            matches_cat = (self.current_filter == "Todos") or (
                item["category"] == self.current_filter
            )
            matches_search = (search_text in item["name"].lower()) or (
                search_text in item["description"].lower()
            )

            if matches_cat and matches_search:
                card.show()
            else:
                card.hide()

    def _on_configure_plugin(self, plugin_id: str):
        pass