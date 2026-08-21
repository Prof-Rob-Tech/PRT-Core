"""
===========================================================
PRT Labs - UI / Sidebar Widget
Class: PRTSidebar
Description: Barra lateral minimalista com ícones em tamanho legível e proporções fiéis
===========================================================
"""

import os
from PySide6.QtCore import Qt, Signal, QSize, QByteArray
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QStackedWidget, QApplication
)

# Vetores SVG corrigidos e proporções ajustadas (stroke-width: 1.6px)
ICONS_SVG = {
    # Principal
    "dashboard": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A0A5B5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>''',
    "navegador": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#818CF8" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>''',
    "downloads": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A0A5B5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>''',
    "biblioteca": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A0A5B5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>''',
    "favoritos": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A0A5B5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>''',
    "historico": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A0A5B5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>''',
    
    # Conectores
    "conn_youtube": '''<svg width="24" height="24" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="3" fill="#FF0000"/><polygon points="10,9 15,12 10,15" fill="#FFFFFF"/></svg>''',
    "conn_tiktok": '''<svg width="24" height="24" viewBox="0 0 24 24"><path d="M12 2v10.5a2.5 2.5 0 1 1-2.5-2.5c.3 0 .6.05.9.15V7.1A6.5 6.5 0 1 0 15 13.5V8.2a8.07 8.07 0 0 0 4 1.8V7.1a4.1 4.1 0 0 1-3-1.4A4.1 4.1 0 0 1 14.7 2H12z" fill="#EE1D52"/></svg>''',
    "conn_kiwify": '''<svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="#00E676"/><polygon points="10,8 15,12 10,16" fill="#FFFFFF"/></svg>''',
    "conn_hotmart": '''<svg width="24" height="24" viewBox="0 0 24 24"><path d="M12 2C12 2 7 7 7 12a5 5 0 0 0 10 0c0-3-2-6-5-10z" fill="#FF5252"/><path d="M12 8c0 0-2 2-2 4a2 2 0 0 0 4 0c0-1.5-1-3-2-4z" fill="#FFD700"/></svg>''',
    "conn_vimeo": '''<svg width="24" height="24" viewBox="0 0 24 24"><path d="M22.4 7c-.2 1.8-1.6 4.3-4.1 7.6-2.6 3.4-4.8 5.1-6.6 5.1-1.1 0-2.1-.5-2.9-1.5C8 17.2 7.1 14.2 6.2 9.2 5.5 5.8 4.7 4.1 3.8 4.1c-.2 0-.8.3-1.8 1L1 3.8C2.2 2.7 3.6 1.6 5.1 1.5c1.8-.2 3 .9 3.5 3.3.6 3.9 1 6.3 1.3 7.2.5 1.5 1.2 2.2 2 2.2.6 0 1.5-.7 2.6-2.1 1.1-1.4 1.7-2.8 1.8-4.2.1-1.2-.3-1.8-1.3-1.8-.5 0-1 .1-1.6.3 1-.8 2.2-2.1 3.6-2.1 1.8 0 2.6 1.1 2.4 2.7z" fill="#00ADEF"/></svg>''',
    "conn_gdrive": '''<svg width="24" height="24" viewBox="0 0 24 24"><path fill="#34A853" d="M7.7 3.5L1.5 14.2l3.1 5.3 6.2-10.7z"/><path fill="#4285F4" d="M22.5 14.2H10.1l3.1 5.3h9.3z"/><path fill="#FBBC05" d="M16.3 3.5H3.9l3.1 5.3h12.4z"/><path fill="#EA4335" d="M16.3 3.5L10.1 14.2l3.1 5.3 6.2-10.7z"/></svg>''',
    "conn_mega": '''<svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="#D92727"/><path d="M7.5 15V9l4.5 3.5L16.5 9v6" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>''',
    "conn_universo": '''<svg width="24" height="24" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="#A855F7"/><circle cx="12" cy="12" r="5" fill="none" stroke="#FFFFFF" stroke-width="1.4"/><line x1="3" y1="12" x2="21" y2="12" stroke="#FFFFFF" stroke-width="1.4"/></svg>''',

    # Ferramentas
    "settings": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A0A5B5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>''',
    "license": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A0A5B5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>''',
    "updates": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A0A5B5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>''',
    "plugins": '''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#A0A5B5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/></svg>''',
}


def render_svg_icon(route_id: str) -> QIcon:
    """Renderiza os ícones em resolução nítida de 20x20px."""
    clean_id = route_id.replace("conn_", "")
    svg_data = ICONS_SVG.get(route_id) or ICONS_SVG.get(clean_id)
    
    if svg_data:
        renderer = QSvgRenderer(QByteArray(svg_data.encode("utf-8")))
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)

    return QIcon()


class PRTSidebarButton(QPushButton):
    """Botão flat sem caixas de fundo e com ícones no tamanho correto."""

    def __init__(self, text: str, route_id: str, parent=None):
        super().__init__(parent)
        self.route_id = route_id
        self.setCheckable(True)
        self.setFixedHeight(32)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(f"  {text}")

        icon = render_svg_icon(route_id)
        if not icon.isNull():
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))

        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding-left: 2px;
                text-align: left;
                font-size: 13px;
                font-weight: 400;
                color: #A0A5B5;
            }
            QPushButton:hover {
                background-color: transparent;
                color: #FFFFFF;
            }
            QPushButton:checked {
                background-color: transparent !important;
                color: #FFFFFF !important;
                font-weight: 700;
            }
        """)


class PRTSidebar(QWidget):
    """Sidebar original com espaçamentos e ícones fiéis ao PRT Nexus."""

    navigate = Signal(str)
    page_changed = Signal(str)
    navigation_requested = Signal(str)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(210)
        self.main_window = None
        self._buttons = []
        
        self.setStyleSheet("QWidget#sidebar { background-color: #0F1015; border: none; }")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 14, 12, 12)
        main_layout.setSpacing(6)

        # Header / Brand
        brand_layout = QHBoxLayout()
        brand_layout.setContentsMargins(2, 2, 0, 6)
        
        bolt_svg = '''<svg width="20" height="20" viewBox="0 0 24 24"><polygon points="13,2 3,14 12,14 11,22 21,10 12,10" fill="#F97316"/></svg>'''
        bolt_icon = QLabel()
        r = QSvgRenderer(QByteArray(bolt_svg.encode("utf-8")))
        px = QPixmap(20, 20)
        px.fill(Qt.transparent)
        p = QPainter(px)
        r.render(p)
        p.end()
        bolt_icon.setPixmap(px)
        
        brand_label = QLabel("PRT NEXUS")
        brand_label.setStyleSheet("font-size: 14px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.5px; border: none; background: transparent;")
        
        brand_layout.addWidget(bolt_icon)
        brand_layout.addWidget(brand_label)
        brand_layout.addStretch()
        main_layout.addLayout(brand_layout)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; } QScrollBar:vertical { width: 0px; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(2)

        # Seções do Menu
        sections = [
            ("PRINCIPAL", [
                ("Início", "dashboard"),
                ("Navegador", "navegador"),
                ("Downloads", "downloads"),
                ("Biblioteca", "biblioteca"),
                ("Favoritos", "favoritos"),
                ("Histórico", "historico"),
            ]),
            ("CONECTORES", [
                ("YouTube", "conn_youtube"),
                ("TikTok", "conn_tiktok"),
                ("Kiwify", "conn_kiwify"),
                ("Hotmart", "conn_hotmart"),
                ("Vimeo", "conn_vimeo"),
                ("Google Drive", "conn_gdrive"),
                ("Mega", "conn_mega"),
                ("Universo Técnico", "conn_universo"),
            ]),
            ("FERRAMENTAS", [
                ("Configurações", "settings"),
                ("Licença", "license"),
                ("Atualizações", "updates"),
                ("Plugins", "plugins"),
            ])
        ]

        for sec_title, items in sections:
            lbl_sec = QLabel(sec_title)
            lbl_sec.setStyleSheet("font-size: 10px; font-weight: 800; color: #4B5162; letter-spacing: 0.8px; border: none; margin-top: 10px; margin-bottom: 2px; padding-left: 2px; background: transparent;")
            content_layout.addWidget(lbl_sec)

            for label_str, route_id in items:
                btn = PRTSidebarButton(label_str, route_id)
                btn.clicked.connect(self._make_click_handler(route_id))
                content_layout.addWidget(btn)
                self._buttons.append((btn, route_id))

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Selecionar "Início" por padrão
        self.set_active("dashboard")

    def _make_click_handler(self, route_id: str):
        return lambda checked=False: self._on_btn_clicked(route_id)

    def connect_main_window(self, main_window):
        self.main_window = main_window
        nav_methods = ['navigate_to', 'switch_page', 'change_page', 'set_page', 'show_page', 'on_navigate', 'navigate']

        for method_name in nav_methods:
            method = getattr(main_window, method_name, None)
            if method and callable(method):
                for sig in (self.navigate, self.page_changed, self.navigation_requested):
                    try:
                        sig.connect(method)
                    except Exception:
                        pass

    def _on_btn_clicked(self, route_id: str):
        self.set_active(route_id)
        self.navigate.emit(route_id)
        self.page_changed.emit(route_id)
        self.navigation_requested.emit(route_id)

        targets = [self.main_window, self.window(), self.parent()]
        if hasattr(QApplication, "activeWindow"):
            targets.append(QApplication.activeWindow())

        route_candidates = [
            route_id,
            route_id.replace("conn_", ""),
            f"conn_{route_id}",
            "inicio" if route_id == "dashboard" else route_id,
            "dashboard" if route_id == "inicio" else route_id
        ]

        nav_methods = ['navigate_to', 'switch_page', 'change_page', 'set_page', 'show_page', 'on_navigate', 'navigate']

        for target in targets:
            if not target:
                continue
            for method_name in nav_methods:
                method = getattr(target, method_name, None)
                if method and callable(method):
                    for rc in route_candidates:
                        try:
                            method(rc)
                            return
                        except Exception:
                            pass

        for target in targets:
            if not target:
                continue
            stacked_widgets = target.findChildren(QStackedWidget)
            for stacked in stacked_widgets:
                for i in range(stacked.count()):
                    w = stacked.widget(i)
                    w_name = w.objectName().lower()
                    cls_name = w.__class__.__name__.lower()
                    for rc in route_candidates:
                        rc_clean = rc.lower()
                        if (rc_clean in w_name or w_name in rc_clean or rc_clean in cls_name or cls_name in rc_clean):
                            stacked.setCurrentIndex(i)
                            return

    def set_active(self, route_id: str):
        for btn, rid in self._buttons:
            btn.setChecked(rid == route_id)


Sidebar = PRTSidebar