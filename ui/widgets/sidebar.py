"""
===========================================================
PRT Labs - UI / Sidebar Widget
Class: PRTSidebar
Description: Barra lateral de navegação completa do PRT Nexus
===========================================================
"""

from PySide6.QtCore import Qt, QSize, QByteArray, Signal
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea
)

# Mapa de Ícones SVG das Plataformas e Menus
SVG_ICONS = {
    "logo": """<svg viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>""",
    "dashboard": """<svg viewBox="0 0 24 24" fill="none" stroke="#A1A1AA" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>""",
    "navegador": """<svg viewBox="0 0 24 24" fill="none" stroke="#6366F1" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10z"/></svg>""",
    "downloads": """<svg viewBox="0 0 24 24" fill="none" stroke="#A1A1AA" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>""",
    "biblioteca": """<svg viewBox="0 0 24 24" fill="none" stroke="#A1A1AA" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>""",
    "favoritos": """<svg viewBox="0 0 24 24" fill="none" stroke="#A1A1AA" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>""",
    "historico": """<svg viewBox="0 0 24 24" fill="none" stroke="#A1A1AA" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>""",
    "conn_youtube": """<svg viewBox="0 0 24 24" fill="#FF0000"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>""",
    "conn_tiktok": """<svg viewBox="0 0 24 24" fill="#FE2C55"><path d="M16.6 5.82a4.27 4.27 0 0 1-3.07-3.47h-3.08v13.06a2.47 2.47 0 1 1-2.47-2.47c.27 0 .53.04.78.13V9.8a5.55 5.55 0 0 0-.78-.06 5.55 5.55 0 1 0 5.55 5.55V8.2a7.28 7.28 0 0 0 4.07 1.22V6.28a4.25 4.25 0 0 1-1-.46z"/></svg>""",
    "conn_kiwify": """<svg viewBox="0 0 24 24" fill="#00E676"><circle cx="12" cy="12" r="10"/><path d="M10 8l6 4-6 4V8z" fill="#09090B"/></svg>""",
    "conn_hotmart": """<svg viewBox="0 0 24 24" fill="#FF5722"><path d="M13.5 1.5s0 4.5-3 6.5C8 10 5.5 12 5.5 15a6.5 6.5 0 0 0 13 0c0-4.5-5-13.5-5-13.5z"/></svg>""",
    "conn_vimeo": """<svg viewBox="0 0 24 24" fill="#00ADEF"><path d="M22.4 7.16c-.09 2.02-1.5 4.8-4.22 8.33-2.82 3.68-5.2 5.52-7.14 5.52-1.2 0-2.22-1.11-3.06-3.33L5.3 8.87C4.7 6.64 4.05 5.52 3.35 5.52c-.15 0-.68.32-1.6.96L0 4.79C1.16 3.77 2.41 2.5 3.75 1c1.86-1.5 3.24-1.5 4.14 0 1.2 2 1.8 3.5 1.8 4.5 0 1.25-.45 2.5-1.35 3.75-.9 1.25-1.5 2-1.8 2.25-.3.25-.45.52-.45.82 0 .6.45.9 1.35.9 1.2 0 2.55-.9 4.05-2.7 1.5-1.8 2.25-3.3 2.25-4.5 0-1.05-.45-1.58-1.35-1.58-.45 0-1.05.15-1.8.45.9-2.85 2.7-4.28 5.4-4.28 1.95 0 2.85 1.16 2.7 3.48z"/></svg>""",
    "conn_gdrive": """<svg viewBox="0 0 24 24" fill="#0F9D58"><path d="M7.71 3.5L1.15 15l3.43 6 6.56-11.5H7.71z"/><path d="M16.29 3.5H7.71l6.56 11.5h8.58L16.29 3.5z"/><path d="M14.27 15L10.84 21h12.01l3.43-6H14.27z"/></svg>""",
    "conn_mega": """<svg viewBox="0 0 24 24" fill="#D9272E"><circle cx="12" cy="12" r="10"/><path d="M7 16V8l5 4 5-4v8" stroke="#FFFFFF" stroke-width="2" fill="none"/></svg>""",
    "conn_universo": """<svg viewBox="0 0 24 24" fill="none" stroke="#E040FB" stroke-width="2"><circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="10" ry="4"/><line x1="12" y1="2" x2="12" y2="22"/></svg>""",
    "configuracoes": """<svg viewBox="0 0 24 24" fill="none" stroke="#A1A1AA" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>""",
    "licenca": """<svg viewBox="0 0 24 24" fill="none" stroke="#A1A1AA" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>""",
    "atualizacoes": """<svg viewBox="0 0 24 24" fill="none" stroke="#A1A1AA" stroke-width="2"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>""",
}


def create_svg_icon(svg_code: str, width: int = 18, height: int = 18) -> QIcon:
    """Renderiza a string SVG como um QIcon."""
    if not svg_code:
        return QIcon()
    renderer = QSvgRenderer(QByteArray(svg_code.encode("utf-8")))
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


class SidebarButton(QPushButton):
    """Botão estilizado com ícone vetorial."""

    def __init__(self, text: str, route_id: str, icon_key: str = "", active: bool = False, parent=None):
        super().__init__(f"  {text}", parent)
        self.route_id = route_id
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(38)
        self.setIconSize(QSize(18, 18))

        if icon_key in SVG_ICONS:
            self.setIcon(create_svg_icon(SVG_ICONS[icon_key]))

        self.set_active(active)

    def set_active(self, active: bool):
        if active:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2563EB;
                    color: #FFFFFF;
                    border: none;
                    border-radius: 6px;
                    text-align: left;
                    padding-left: 12px;
                    font-size: 13px;
                    font-weight: 600;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #A1A1AA;
                    border: none;
                    border-radius: 6px;
                    text-align: left;
                    padding-left: 12px;
                    font-size: 13px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #18181B;
                    color: #FAFAFA;
                }
            """)


class PRTSidebar(QWidget):
    """Barra lateral de navegação."""

    navigate = Signal(str)

    def __init__(self, parent=None, on_navigate=None, *args, **kwargs):
        super().__init__(parent)
        self.on_navigate_callback = on_navigate
        self.setFixedWidth(220)
        self.buttons = {}
        self._setup_ui()

    def connect_main_window(self, main_window) -> None:
        if hasattr(main_window, "navigate_to") and callable(main_window.navigate_to):
            self.on_navigate_callback = main_window.navigate_to

    def _setup_ui(self):
        self.setStyleSheet("background-color: #09090B; border-right: 1px solid #18181B;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(12)

        # 1. Logo do Topo
        logo_box = QHBoxLayout()
        logo_box.setContentsMargins(4, 4, 4, 8)
        logo_box.setSpacing(10)

        icon_badge = QFrame()
        icon_badge.setFixedSize(32, 32)
        icon_badge.setStyleSheet("""
            QFrame {
                background-color: rgba(59, 130, 246, 0.12);
                border: 1px solid rgba(59, 130, 246, 0.25);
                border-radius: 8px;
            }
        """)
        badge_layout = QVBoxLayout(icon_badge)
        badge_layout.setContentsMargins(0, 0, 0, 0)
        badge_layout.setAlignment(Qt.AlignCenter)

        icon_lbl = QLabel()
        logo_icon = create_svg_icon(SVG_ICONS["logo"], 18, 18)
        icon_lbl.setPixmap(logo_icon.pixmap(18, 18))
        icon_lbl.setStyleSheet("background: transparent; border: none;")
        badge_layout.addWidget(icon_lbl)

        logo_text = QLabel("PRT NEXUS")
        logo_text.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold; border: none;")

        logo_box.addWidget(icon_badge)
        logo_box.addWidget(logo_text)
        logo_box.addStretch()

        layout.addLayout(logo_box)

        # 2. Lista de Menus Rolável
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        menu_container = QWidget()
        menu_container.setStyleSheet("background: transparent;")
        self.menu_layout = QVBoxLayout(menu_container)
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.setSpacing(4)

        # PRINCIPAL
        self._add_section("PRINCIPAL")
        self._add_button("Início", "dashboard", icon_key="dashboard", active=True)
        self._add_button("Navegador", "navegador", icon_key="navegador")
        self._add_button("Downloads", "downloads", icon_key="downloads")
        self._add_button("Biblioteca", "biblioteca", icon_key="biblioteca")
        self._add_button("Favoritos", "favoritos", icon_key="favoritos")
        self._add_button("Histórico", "historico", icon_key="historico")

        # CONECTORES
        self._add_section("CONECTORES")
        self._add_button("YouTube", "conn_youtube", icon_key="conn_youtube")
        self._add_button("TikTok", "conn_tiktok", icon_key="conn_tiktok")
        self._add_button("Kiwify", "conn_kiwify", icon_key="conn_kiwify")
        self._add_button("Hotmart", "conn_hotmart", icon_key="conn_hotmart")
        self._add_button("Vimeo", "conn_vimeo", icon_key="conn_vimeo")
        self._add_button("Google Drive", "conn_gdrive", icon_key="conn_gdrive")
        self._add_button("Mega", "conn_mega", icon_key="conn_mega")
        self._add_button("Universo Técnico", "conn_universo", icon_key="conn_universo")

        # FERRAMENTAS
        self._add_section("FERRAMENTAS")
        self._add_button("Configurações", "configuracoes", icon_key="configuracoes")
        self._add_button("Licença", "licenca", icon_key="licenca")
        self._add_button("Atualizações", "atualizacoes", icon_key="atualizacoes")

        self.menu_layout.addStretch()
        scroll.setWidget(menu_container)
        layout.addWidget(scroll)

    def _add_section(self, title: str):
        lbl = QLabel(title)
        lbl.setStyleSheet("color: #52525B; font-size: 10px; font-weight: bold; margin-top: 12px; margin-left: 6px; border: none;")
        self.menu_layout.addWidget(lbl)

    def _add_button(self, text: str, route_id: str, icon_key: str = "", active: bool = False):
        btn = SidebarButton(text, route_id, icon_key=icon_key, active=active)
        btn.clicked.connect(lambda: self._on_btn_click(route_id))
        self.buttons[route_id] = btn
        self.menu_layout.addWidget(btn)

    def _on_btn_click(self, route_id: str):
        self.set_active_route(route_id)
        self.navigate.emit(route_id)
        if callable(self.on_navigate_callback):
            self.on_navigate_callback(route_id)

    def set_active_route(self, route_id: str):
        for r_id, btn in self.buttons.items():
            btn.set_active(r_id == route_id)


# Alias de compatibilidade
Sidebar = PRTSidebar