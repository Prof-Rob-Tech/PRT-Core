"""
===========================================================
PRT Labs - UI / Main Window
Class: PRTMainWindow / MainWindow

Description:
    Janela Principal do PRT Nexus com gerenciamento adaptativo
    e suporte completo ao conector do TikTok.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget

# Importa a Barra Lateral
from ui.widgets.sidebar import PRTSidebar

# Imports Seguros das Páginas
try:
    from ui.pages.dashboard_page import DashboardPage
except Exception:
    DashboardPage = None

try:
    from ui.pages.browser_page import BrowserPage
except Exception:
    BrowserPage = None

try:
    from ui.pages.downloads_page import DownloadsPage
except Exception:
    DownloadsPage = None

try:
    from ui.pages.library_page import LibraryPage
except Exception:
    LibraryPage = None

try:
    from ui.pages.favorites_page import FavoritesPage
except Exception:
    FavoritesPage = None

try:
    from ui.pages.history_page import HistoryPage
except Exception:
    HistoryPage = None

try:
    from ui.pages.connector_page import ConnectorPage
except Exception:
    ConnectorPage = None

try:
    from ui.pages.settings_page import SettingsPage
except Exception:
    SettingsPage = None

try:
    from ui.pages.license_page import LicensePage
except Exception:
    LicensePage = None

try:
    from ui.pages.plugins_page import PluginsPage
except Exception:
    PluginsPage = None

try:
    from ui.pages.placeholder_page import PlaceholderPage
except Exception:
    PlaceholderPage = None


class PRTMainWindow(QMainWindow):
    """Janela Principal do PRT Nexus."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("PRT NEXUS")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 600)

        # Dicionário central de instâncias das páginas
        self.pages = {}

        self._setup_ui()

    def _instantiate_page(self, page_cls, title_fallback="Página", **kwargs):
        """Instancia qualquer página adaptando-se à assinatura de __init__."""
        if not page_cls:
            return self._create_placeholder(title_fallback)

        # 1. Tenta instanciar passando parent + kwargs
        try:
            return page_cls(parent=self, **kwargs)
        except TypeError:
            pass

        # 2. Tenta instanciar apenas com kwargs
        try:
            return page_cls(**kwargs)
        except TypeError:
            pass

        # 3. Tratamento para ConnectorPage (platform_key)
        if "platform_key" in kwargs:
            p_key = kwargs["platform_key"]
            try:
                return page_cls(p_key, parent=self)
            except TypeError:
                pass
            try:
                return page_cls(p_key)
            except TypeError:
                pass

        # 4. Tenta instanciar apenas com parent=self
        try:
            return page_cls(parent=self)
        except TypeError:
            pass

        # 5. Tenta instanciar sem argumentos
        try:
            return page_cls()
        except Exception:
            pass

        return self._create_placeholder(title_fallback)

    def _create_placeholder(self, title: str):
        """Cria uma tela de reserva caso a página falhe ao carregar."""
        if PlaceholderPage:
            try:
                return PlaceholderPage(title=title, parent=self)
            except Exception:
                try:
                    return PlaceholderPage(title)
                except Exception:
                    pass
        return QWidget(self)

    def _setup_ui(self) -> None:
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background-color: #09090B;")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Barra Lateral (Sidebar)
        self.sidebar = PRTSidebar(parent=self, on_navigate=self.navigate_to)
        main_layout.addWidget(self.sidebar)

        # 2. Gerenciador de Páginas Empilhadas
        self.stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.stacked_widget)

        # 3. Registro Adaptativo de Páginas
        self._register_pages()

        # Abre a Dashboard por padrão ao iniciar
        self.navigate_to("dashboard")

    def _register_pages(self) -> None:
        """Instancia e registra todas as telas da pasta ui/pages."""

        # Páginas Principais
        self.pages["dashboard"] = self._instantiate_page(DashboardPage, "Início", on_navigate=self.navigate_to)
        self.pages["navegador"] = self._instantiate_page(BrowserPage, "Navegador Web")
        self.pages["downloads"] = self._instantiate_page(DownloadsPage, "Downloads")
        self.pages["biblioteca"] = self._instantiate_page(LibraryPage, "Biblioteca")
        self.pages["favoritos"] = self._instantiate_page(FavoritesPage, "Favoritos")
        self.pages["historico"] = self._instantiate_page(HistoryPage, "Histórico")

        # Ferramentas
        self.pages["configuracoes"] = self._instantiate_page(SettingsPage, "Configurações")
        self.pages["licenca"] = self._instantiate_page(LicensePage, "Licença")
        self.pages["plugins"] = self._instantiate_page(PluginsPage, "Plugins")
        self.pages["atualizacoes"] = self._create_placeholder("Atualizações")

        # Conectores (Incluso o TikTok)
        connectors_map = [
            ("conn_youtube", "youtube"),
            ("conn_tiktok", "tiktok"),
            ("conn_kiwify", "kiwify"),
            ("conn_hotmart", "hotmart"),
            ("conn_vimeo", "vimeo"),
            ("conn_gdrive", "gdrive"),
            ("conn_mega", "mega"),
            ("conn_universo", "universo"),
        ]

        for route_key, conn_key in connectors_map:
            self.pages[route_key] = self._instantiate_page(
                ConnectorPage,
                title_fallback=conn_key.capitalize(),
                platform_key=conn_key,
                connector_name=conn_key
            )

        # Adiciona todas as páginas ao QStackedWidget
        for page_widget in self.pages.values():
            if page_widget:
                self.stacked_widget.addWidget(page_widget)

    def navigate_to(self, route_id: str) -> None:
        """Gerenciador central de navegação."""

        ROUTE_MAP = {
            "inicio": "dashboard",
            "home": "dashboard",
            "dashboard": "dashboard",

            "navegador": "navegador",
            "browser": "navegador",

            "downloads": "downloads",
            "biblioteca": "biblioteca",
            "library": "biblioteca",
            "favoritos": "favoritos",
            "favorites": "favoritos",
            "historico": "historico",
            "history": "historico",

            "youtube": "conn_youtube",
            "conn_youtube": "conn_youtube",
            "tiktok": "conn_tiktok",
            "conn_tiktok": "conn_tiktok",
            "kiwify": "conn_kiwify",
            "conn_kiwify": "conn_kiwify",
            "hotmart": "conn_hotmart",
            "conn_hotmart": "conn_hotmart",
            "vimeo": "conn_vimeo",
            "conn_vimeo": "conn_vimeo",
            "gdrive": "conn_gdrive",
            "conn_gdrive": "conn_gdrive",
            "mega": "conn_mega",
            "conn_mega": "conn_mega",
            "universo": "conn_universo",
            "conn_universo": "conn_universo",

            "configuracoes": "configuracoes",
            "settings": "configuracoes",
            "licenca": "licenca",
            "license": "licenca",
            "atualizacoes": "atualizacoes",
            "updates": "atualizacoes",
            "plugins": "plugins",
        }

        target_key = ROUTE_MAP.get(route_id, route_id)

        if target_key in self.pages:
            page_widget = self.pages[target_key]
            self.stacked_widget.setCurrentWidget(page_widget)

            # Sincroniza visualmente a sidebar se necessário
            if hasattr(self, "sidebar") and hasattr(self.sidebar, "set_active_route"):
                self.sidebar.set_active_route(target_key)

            if hasattr(page_widget, "on_show") and callable(page_widget.on_show):
                page_widget.on_show()


# Aliases de compatibilidade
MainWindow = PRTMainWindow
main_window = PRTMainWindow