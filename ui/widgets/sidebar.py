"""
===========================================================
PRT Labs - UI Widgets
Class: PRTSidebar

Description:
    Sidebar modular principal do PRT NEXUS. Unifica
    navegação, conectores e rodapé da aplicação.
===========================================================
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QWidget

from ui.widgets.connector_item import ConnectorItem
from ui.widgets.footer_card import SidebarFooterCard
from ui.widgets.sidebar_item import SidebarNavItem


class PRTSidebar(QWidget):
    """Barra lateral modular e responsiva do PRT NEXUS."""

    page_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setFixedWidth(240)
        self._nav_items: dict[str, SidebarNavItem] = {}
        self.main_window = None
        self._build_ui()

    def connect_main_window(self, main_window) -> None:
        """Conecta os sinais da Sidebar com a Janela Principal."""
        self.main_window = main_window
        if hasattr(main_window, "_on_page_changed"):
            self.page_changed.connect(main_window._on_page_changed)
        elif hasattr(main_window, "on_page_changed"):
            self.page_changed.connect(main_window.on_page_changed)

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(16)

        # 1. CABEÇALHO COM LOGO SVG
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        logo_widget = QSvgWidget("assets/nexus_logo.svg")
        logo_widget.setFixedSize(28, 28)

        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(0)

        lbl_title = QLabel("PRT NEXUS")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")

        lbl_sub = QLabel("Content Management")
        lbl_sub.setStyleSheet("color: #6C727F; font-size: 10px;")

        title_vbox.addWidget(lbl_title)
        title_vbox.addWidget(lbl_sub)

        header_layout.addWidget(logo_widget)
        header_layout.addLayout(title_vbox)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # 2. ÁREA ROLÁVEL DE CONTEÚDO
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        c_layout = QVBoxLayout(container)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_layout.setSpacing(18)

        # Grupo: Menu Principal
        nav_group = QVBoxLayout()
        nav_group.setSpacing(4)

        for key, text, badge, active in [
            ("inicio", "🏠  Início", "", True),
            ("navegador", "🌐  Navegador", "", False),
            ("downloads", "📥  Downloads", "3", False),
            ("biblioteca", "📁  Biblioteca", "", False),
            ("favoritos", "⭐  Favoritos", "", False),
            ("historico", "🕒  Histórico", "", False),
        ]:
            item = SidebarNavItem(key, text, badge_count=badge, active=active)
            item.clicked.connect(self._on_item_clicked)
            self._nav_items[key] = item
            nav_group.addWidget(item)

        c_layout.addLayout(nav_group)

        # Grupo: Conectores
        c_layout.addLayout(self._create_header("CONECTORES", show_plus=True))
        conn_group = QVBoxLayout()
        conn_group.setSpacing(2)
        conn_group.addWidget(ConnectorItem("▶️", "YouTube", online=True))
        conn_group.addWidget(ConnectorItem("🟢", "Kiwify", online=True))
        conn_group.addWidget(ConnectorItem("🔥", "Hotmart", online=True))
        conn_group.addWidget(ConnectorItem("🔷", "Vimeo", online=False))
        conn_group.addWidget(ConnectorItem("🔺", "Google Drive", online=False))
        conn_group.addWidget(ConnectorItem("🔴", "Mega", online=False))
        c_layout.addLayout(conn_group)

        # Grupo: Ferramentas
        c_layout.addLayout(self._create_header("FERRAMENTAS"))
        tool_group = QVBoxLayout()
        tool_group.setSpacing(4)
        for key, text in [
            ("configuracoes", "⚙️  Configurações"),
            ("licenca", "🛡️  Licença"),
            ("atualizacoes", "🔄  Atualizações"),
            ("plugins", "🧩  Plugins"),
        ]:
            item = SidebarNavItem(key, text)
            item.clicked.connect(self._on_item_clicked)
            self._nav_items[key] = item
            tool_group.addWidget(item)

        c_layout.addLayout(tool_group)
        c_layout.addStretch()

        scroll.setWidget(container)
        layout.addWidget(scroll)

        # 3. RODAPÉ
        layout.addWidget(SidebarFooterCard())

    def _create_header(self, title: str, show_plus: bool = False) -> QHBoxLayout:
        lay = QHBoxLayout()
        lay.setContentsMargins(4, 4, 4, 0)

        lbl = QLabel(title)
        lbl.setStyleSheet("color: #525663; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        lay.addWidget(lbl)
        lay.addStretch()

        if show_plus:
            lbl_plus = QLabel("+")
            lbl_plus.setCursor(Qt.PointingHandCursor)
            lbl_plus.setStyleSheet("color: #525663; font-size: 14px; font-weight: bold;")
            lay.addWidget(lbl_plus)

        return lay

    def _on_item_clicked(self, selected_key: str) -> None:
        for key, item in self._nav_items.items():
            item.set_active(key == selected_key)
        self.page_changed.emit(selected_key)