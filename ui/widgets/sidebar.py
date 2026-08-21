"""
===========================================================
PRT Labs - UI / Sidebar Widget
Class: PRTSidebar
Description: Barra lateral de navegação adaptativa aos temas do PRT Nexus
===========================================================
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
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

        # Herda dinamicamente a cor do tema ativo (claro ou escuro)
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
    """Barra lateral de navegação principal do PRT Nexus."""

    navigate = Signal(str)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setObjectName("sidebar")
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
                btn.clicked.connect(lambda checked=False, rid=route_id: self._on_btn_clicked(rid))
                content_layout.addWidget(btn)
                self._buttons.append((btn, route_id))

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Ativar "Início" por padrão
        self.set_active("dashboard")

    def _on_btn_clicked(self, route_id: str):
        self.set_active(route_id)
        self.navigate.emit(route_id)

    def set_active(self, route_id: str):
        for btn, rid in self._buttons:
            btn.setChecked(rid == route_id)


# Alias para compatibilidade
Sidebar = PRTSidebar