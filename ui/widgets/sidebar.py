"""
===========================================================
PRT Labs - UI / Widgets
Class: PRTSidebar

Description:
    Barra lateral de navegação do PRT NEXUS.
    Gerencia botões de navegação, lista de conectores ativos,
    ferramentas e emissão de sinais para troca de páginas.
===========================================================
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class PRTSidebar(QFrame):
    """Sidebar de navegação principal do PRT NEXUS com suporte a Conectores."""

    # Sinal emitido ao clicar em QUALQUER aba ou conector
    page_changed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedWidth(240)
        self.setStyleSheet(
            """
            QFrame#Sidebar {
                background-color: #0E0F12;
                border-right: 1px solid #18181B;
            }
        """
        )
        self.setObjectName("Sidebar")

        self.buttons_map: dict[str, QPushButton] = {}
        self.main_window = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(12)

        # 1. Header / Logo
        layout.addWidget(self._create_logo())

        # Scroll Area para os itens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 4px;
            }
            QScrollBar::handle:vertical {
                background: #27272A;
                border-radius: 2px;
            }
        """
        )

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(16)

        # 2. Menu Principal
        scroll_layout.addLayout(self._create_main_menu())

        # 3. Seção de Conectores
        scroll_layout.addLayout(self._create_connectors_menu())

        # 4. Seção de Ferramentas
        scroll_layout.addLayout(self._create_tools_menu())

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, stretch=1)

        # 5. Footer / Card do App
        layout.addWidget(self._create_footer())

        # Seleciona o item inicial por padrão
        self._select_item("navegador")

    def connect_main_window(self, main_window) -> None:
        """Conecta a Sidebar à janela principal e acopla seus sinais."""
        self.main_window = main_window

        # Conecta o sinal page_changed ao manipulador da janela principal
        if hasattr(main_window, "_on_page_changed"):
            try:
                self.page_changed.connect(main_window._on_page_changed)
            except Exception:
                pass
        elif hasattr(main_window, "on_page_changed"):
            try:
                self.page_changed.connect(main_window.on_page_changed)
            except Exception:
                pass

        # Adiciona a sidebar no layout da main window se o método existir
        if hasattr(main_window, "add_sidebar"):
            try:
                main_window.add_sidebar(self)
            except Exception:
                pass

    def _create_logo(self) -> QWidget:
        """Cria o logo do PRT NEXUS no topo da barra."""
        widget = QWidget()
        h_box = QHBoxLayout(widget)
        h_box.setContentsMargins(4, 0, 4, 8)
        h_box.setSpacing(10)

        lbl_icon = QLabel("⚡")
        lbl_icon.setStyleSheet("font-size: 22px;")

        v_box = QVBoxLayout()
        v_box.setSpacing(0)

        lbl_title = QLabel("PRT NEXUS")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")

        lbl_sub = QLabel("Content Management")
        lbl_sub.setStyleSheet("color: #71717A; font-size: 10px; font-weight: 500;")

        v_box.addWidget(lbl_title)
        v_box.addWidget(lbl_sub)

        h_box.addWidget(lbl_icon)
        h_box.addLayout(v_box)
        h_box.addStretch()

        return widget

    def _create_main_menu(self) -> QVBoxLayout:
        """Cria os botões de navegação principal."""
        menu = QVBoxLayout()
        menu.setSpacing(4)

        items = [
            ("inicio", "🏠  Início"),
            ("navegador", "🌐  Navegador"),
            ("downloads", "📥  Downloads"),
            ("biblioteca", "📁  Biblioteca"),
            ("favoritos", "⭐  Favoritos"),
            ("historico", "🕒  Histórico"),
        ]

        for page_id, text in items:
            btn = self._make_nav_button(page_id, text)
            menu.addWidget(btn)

        return menu

    def _create_connectors_menu(self) -> QVBoxLayout:
        """Cria a seção de Conectores (YouTube, Kiwify, Hotmart, Vimeo, etc.)."""
        menu = QVBoxLayout()
        menu.setSpacing(4)

        lbl_section = QLabel("CONECTORES")
        lbl_section.setStyleSheet(
            "color: #52525B; font-size: 11px; font-weight: bold; padding: 6px 8px 2px 8px;"
        )
        menu.addWidget(lbl_section)

        connectors = [
            ("youtube", "▶️  YouTube"),
            ("kiwify", "🟢  Kiwify"),
            ("hotmart", "🔥  Hotmart"),
            ("vimeo", "🔹  Vimeo"),
            ("google_drive", "🔺  Google Drive"),
            ("mega", "🔴  Mega"),
        ]

        for conn_id, text in connectors:
            btn = self._make_nav_button(conn_id, text)
            menu.addWidget(btn)

        return menu

    def _create_tools_menu(self) -> QVBoxLayout:
        """Cria a seção de Ferramentas e Configurações."""
        menu = QVBoxLayout()
        menu.setSpacing(4)

        lbl_section = QLabel("FERRAMENTAS")
        lbl_section.setStyleSheet(
            "color: #52525B; font-size: 11px; font-weight: bold; padding: 6px 8px 2px 8px;"
        )
        menu.addWidget(lbl_section)

        tools = [
            ("configuracoes", "⚙️  Configurações"),
            ("licenca", "🔑  Licença"),
            ("atualizacoes", "🔄  Atualizações"),
            ("plugins", "🧩  Plugins"),
        ]

        for tool_id, text in tools:
            btn = self._make_nav_button(tool_id, text)
            menu.addWidget(btn)

        return menu

    def _make_nav_button(self, page_id: str, text: str) -> QPushButton:
        """Cria um botão padronizado de navegação da Sidebar."""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedHeight(36)
        btn.setStyleSheet(self._get_inactive_style())

        btn.clicked.connect(lambda: self._on_item_clicked(page_id))

        self.buttons_map[page_id] = btn
        return btn

    def _on_item_clicked(self, page_id: str) -> None:
        """Trata o clique em qualquer botão da Sidebar."""
        self._select_item(page_id)
        print(f"[PRTSidebar] Navegando para a página: '{page_id}'")
        self.page_changed.emit(page_id)

    def _select_item(self, target_id: str) -> None:
        """Atualiza visualmente o estado ativo/inativo dos botões."""
        for page_id, btn in self.buttons_map.items():
            if page_id == target_id:
                btn.setChecked(True)
                btn.setStyleSheet(self._get_active_style())
            else:
                btn.setChecked(False)
                btn.setStyleSheet(self._get_inactive_style())

    def _get_active_style(self) -> str:
        """Estilo CSS do botão ativo (selecionado)."""
        return """
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding-left: 12px;
                text-align: left;
                font-weight: bold;
                font-size: 13px;
            }
        """

    def _get_inactive_style(self) -> str:
        """Estilo CSS do botão inativo."""
        return """
            QPushButton {
                background-color: transparent;
                color: #A1A1AA;
                border: none;
                border-radius: 8px;
                padding-left: 12px;
                text-align: left;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #18181B;
                color: #FFFFFF;
            }
        """

    def _create_footer(self) -> QFrame:
        """Cria o card informativo no rodapé da Sidebar."""
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 8px;
            }
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(2)

        lbl_brand = QLabel("❖ PRT Labs")
        lbl_brand.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold;")

        lbl_ver = QLabel("PRT Nexus v0.1.0-alpha")
        lbl_ver.setStyleSheet("color: #71717A; font-size: 10px;")

        layout.addWidget(lbl_brand)
        layout.addWidget(lbl_ver)

        return card


# Aliases e exportações
Sidebar = PRTSidebar
__all__ = ["PRTSidebar", "Sidebar"]