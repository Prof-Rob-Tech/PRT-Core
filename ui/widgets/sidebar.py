"""
===========================================================
PRT Labs - UI / Sidebar Widget
Class: PRTSidebar
Description: Barra lateral de navegação adaptativa aos temas do PRT Nexus
===========================================================
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QStackedWidget, QApplication
)


class PRTSidebarButton(QPushButton):
    """Botão de navegação lateral adaptativo aos temas Claro e Escuro."""

    def __init__(self, icon_str: str, text: str, route_id: str, parent=None):
        super().__init__(parent)
        self.route_id = route_id
        self.setCheckable(True)
        self.setFixedHeight(38)
        self.setCursor(Qt.PointingHandCursor)
        self.setText(f"{icon_str}  {text}")

        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
                padding-left: 12px;
                text-align: left;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.18);
            }
            QPushButton:checked {
                background-color: #2563EB;
                color: #FFFFFF !important;
                font-weight: bold;
            }
        """)


class PRTSidebar(QWidget):
    """Barra lateral de navegação principal do PRT Nexus com navegação direta e suporte a sinais."""

    navigate = Signal(str)
    page_changed = Signal(str)
    navigation_requested = Signal(str)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(230)
        self.main_window = None
        self._buttons = []
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 16, 12, 16)
        main_layout.setSpacing(16)

        # Header / Brand
        brand_label = QLabel("⚡ PRT NEXUS")
        brand_label.setStyleSheet("font-size: 16px; font-weight: bold; border: none; padding-left: 4px;")
        main_layout.addWidget(brand_label)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        # Seções do Menu
        sections = [
            ("PRINCIPAL", [
                ("🏠", "Início", "dashboard"),
                ("🌐", "Navegador", "navegador"),
                ("📥", "Downloads", "downloads"),
                ("📁", "Biblioteca", "biblioteca"),
                ("⭐", "Favoritos", "favoritos"),
                ("🕒", "Histórico", "historico"),
            ]),
            ("CONECTORES", [
                ("▶️", "YouTube", "conn_youtube"),
                ("🎵", "TikTok", "conn_tiktok"),
                ("🟢", "Kiwify", "conn_kiwify"),
                ("🔥", "Hotmart", "conn_hotmart"),
                ("🔷", "Vimeo", "conn_vimeo"),
                ("▲", "Google Drive", "conn_gdrive"),
                ("Ⓜ️", "Mega", "conn_mega"),
                ("🌐", "Universo Técnico", "conn_universo"),
            ]),
            ("FERRAMENTAS", [
                ("⚙️", "Configurações", "settings"),
                ("🔒", "Licença", "license"),
                ("🔄", "Atualizações", "updates"),
            ])
        ]

        for sec_title, items in sections:
            lbl_sec = QLabel(sec_title)
            lbl_sec.setStyleSheet("font-size: 10px; font-weight: 800; opacity: 0.65; letter-spacing: 0.5px; border: none; margin-top: 6px;")
            content_layout.addWidget(lbl_sec)

            for icon_str, label_str, route_id in items:
                btn = PRTSidebarButton(icon_str, label_str, route_id)
                btn.clicked.connect(self._make_click_handler(route_id))
                content_layout.addWidget(btn)
                self._buttons.append((btn, route_id))

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Ativar "Início" por padrão
        self.set_active("dashboard")

    def _make_click_handler(self, route_id: str):
        return lambda checked=False: self._on_btn_clicked(route_id)

    def connect_main_window(self, main_window):
        """Conecta a barra lateral com a janela principal do sistema."""
        self.main_window = main_window

        nav_methods = [
            'navigate_to', 'switch_page', 'change_page', 'set_page', 
            'show_page', 'on_navigate', 'navigate', 'goto_page'
        ]

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

        # Emissão dos sinais
        self.navigate.emit(route_id)
        self.page_changed.emit(route_id)
        self.navigation_requested.emit(route_id)

        # Lista de candidatos a janela e rotas
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

        nav_methods = [
            'navigate_to', 'switch_page', 'change_page', 'set_page', 
            'show_page', 'on_navigate', 'navigate', 'goto_page',
            'load_page', 'open_page', 'select_page', 'handle_navigation'
        ]

        # 1. Tentar métodos diretos nas janelas encontradas
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

        # 2. Varredura direta na árvore de widgets para encontrar o QStackedWidget
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
                        if (rc_clean in w_name or w_name in rc_clean or 
                            rc_clean in cls_name or cls_name in rc_clean):
                            stacked.setCurrentIndex(i)
                            return


    def set_active(self, route_id: str):
        for btn, rid in self._buttons:
            btn.setChecked(rid == route_id)


# Alias para compatibilidade
Sidebar = PRTSidebar