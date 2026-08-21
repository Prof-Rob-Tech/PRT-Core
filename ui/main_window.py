"""
===========================================================
PRT Labs - UI / Main Window
Class: PRTMainWindow / MainWindow

Description:
    Janela Principal do PRT Nexus com suporte global completo 
    a temas (Escuro, Claro, Cyber), navegação entre páginas,
    gerenciamento de tray icon e integração com a UpdatesPage.
===========================================================
"""

import ctypes
import sys

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QStackedWidget,
    QStyle,
    QSystemTrayIcon,
    QWidget,
)

from ui.widgets.sidebar import PRTSidebar

# --- IMPORTAÇÃO SEGURA DAS PÁGINAS ---
try:
    from ui.pages.dashboard_page import DashboardPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR DashboardPage: {e}")
    DashboardPage = None

try:
    from ui.pages.browser_page import BrowserPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR BrowserPage: {e}")
    BrowserPage = None

try:
    from ui.pages.downloads_page import DownloadsPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR DownloadsPage: {e}")
    DownloadsPage = None

try:
    from ui.pages.library_page import LibraryPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR LibraryPage: {e}")
    LibraryPage = None

try:
    from ui.pages.favorites_page import FavoritesPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR FavoritesPage: {e}")
    FavoritesPage = None

try:
    from ui.pages.history_page import HistoryPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR HistoryPage: {e}")
    HistoryPage = None

try:
    from ui.pages.connector_page import ConnectorPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR ConnectorPage: {e}")
    ConnectorPage = None

try:
    from ui.pages.settings_page import SettingsPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR SettingsPage: {e}")
    SettingsPage = None

try:
    from ui.pages.license_page import LicensePage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR LicensePage: {e}")
    LicensePage = None

try:
    from ui.pages.plugins_page import PluginsPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR PluginsPage: {e}")
    PluginsPage = None

try:
    from ui.pages.updates_page import UpdatesPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR UpdatesPage: {e}")
    UpdatesPage = None

try:
    from ui.pages.placeholder_page import PlaceholderPage
except Exception as e:
    print(f"❌ ERRO AO IMPORTAR PlaceholderPage: {e}")
    PlaceholderPage = None


THEME_STYLES = {
    "dark": """
        QMainWindow, QWidget#centralWidget, QStackedWidget {
            background-color: #09090B;
            color: #F4F4F5;
            font-family: 'Segoe UI', sans-serif;
        }
        PRTSidebar {
            background-color: #121215;
            border-right: 1px solid #27272A;
            color: #A1A1AA;
        }
        PRTSidebar QPushButton {
            text-align: left;
            padding: 8px 12px;
            border-radius: 6px;
            background-color: transparent;
            color: #A1A1AA;
            border: none;
            font-weight: 500;
        }
        PRTSidebar QPushButton:hover {
            background-color: #18181B;
            color: #FFFFFF;
        }
        PRTSidebar QPushButton:checked {
            background-color: #2563EB; /* Botão Azul de Destaque */
            color: #FFFFFF;
            font-weight: bold;
        }
        PRTSidebar QLabel#sectionHeader { color: #52525B; }
        PRTSidebar QLabel#subText { color: #71717A; }

        QFrame#cardFrame {
            background-color: #141416;
            border: 1px solid #26262B;
            border-radius: 8px;
        }
        QLabel { color: #F4F4F5; }
        QLineEdit, QComboBox {
            background-color: #18181B;
            color: #FFFFFF;
            border: 1px solid #27272A;
            border-radius: 6px;
            padding: 8px 12px;
        }
        QPushButton {
            background-color: #27272A;
            color: #FFFFFF;
            border: 1px solid #3F3F46;
            border-radius: 6px;
            padding: 8px 14px;
            font-weight: 500;
        }
        QPushButton:hover { background-color: #3F3F46; }
        QTableWidget {
            background-color: #141416;
            color: #F4F4F5;
            gridline-color: #27272A;
            border: 1px solid #27272A;
            border-radius: 6px;
        }
        QHeaderView::section {
            background-color: #18181B;
            color: #A1A1AA;
            border: none;
            padding: 6px;
        }
        QProgressBar {
            background-color: #18181B;
            border: 1px solid #27272A;
            border-radius: 6px;
            height: 20px;
            text-align: center;
            color: #ffffff;
            font-weight: bold;
        }
        QProgressBar::chunk {
            background-color: #6366f1;
            border-radius: 5px;
        }
    """,
    "light": """
        QMainWindow, QWidget#centralWidget, QStackedWidget {
            background-color: #F8FAFC;
            color: #0F172A;
            font-family: 'Segoe UI', sans-serif;
        }
        PRTSidebar {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
            color: #475569;
        }
        PRTSidebar QPushButton {
            text-align: left;
            padding: 8px 12px;
            border-radius: 6px;
            background-color: transparent;
            color: #475569;
            border: none;
            font-weight: 500;
        }
        PRTSidebar QPushButton:hover {
            background-color: #F1F5F9;
            color: #0F172A;
        }
        PRTSidebar QPushButton:checked {
            background-color: #2563EB;
            color: #FFFFFF;
            font-weight: bold;
        }
        PRTSidebar QLabel#sectionHeader { color: #94A3B8; }
        PRTSidebar QLabel#subText { color: #64748B; }

        QFrame#cardFrame {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
        }
        QLabel { color: #0F172A; }
        QLineEdit, QComboBox {
            background-color: #FFFFFF;
            color: #0F172A;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 8px 12px;
        }
        QPushButton {
            background-color: #E2E8F0;
            color: #0F172A;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            padding: 8px 14px;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #CBD5E1;
            color: #0F172A;
        }
        QTableWidget {
            background-color: #FFFFFF;
            color: #0F172A;
            gridline-color: #E2E8F0;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
        }
        QHeaderView::section {
            background-color: #F1F5F9;
            color: #475569;
            border: none;
            padding: 6px;
        }
        QProgressBar {
            background-color: #E2E8F0;
            border: 1px solid #CBD5E1;
            border-radius: 6px;
            height: 20px;
            text-align: center;
            color: #0F172A;
            font-weight: bold;
        }
        QProgressBar::chunk {
            background-color: #3b82f6;
            border-radius: 5px;
        }
    """,
    "cyber": """
        QMainWindow, QWidget#centralWidget, QStackedWidget {
            background-color: #0B0518;
            color: #00F0FF;
            font-family: 'Segoe UI', sans-serif;
        }
        PRTSidebar {
            background-color: #150A2A;
            border-right: 1px solid #FF007F;
            color: #8A72B2;
        }
        PRTSidebar QPushButton {
            text-align: left;
            padding: 8px 12px;
            border-radius: 6px;
            background-color: transparent;
            color: #8A72B2;
            border: none;
            font-weight: 500;
        }
        PRTSidebar QPushButton:hover {
            background-color: #24114A;
            color: #00F0FF;
        }
        PRTSidebar QPushButton:checked {
            background-color: #2563EB;
            color: #FFFFFF;
            font-weight: bold;
        }
        PRTSidebar QLabel#sectionHeader { color: #FF007F; }
        PRTSidebar QLabel#subText { color: #8A72B2; }

        QFrame#cardFrame {
            background-color: #150A2A;
            border: 1px solid #FF007F;
            border-radius: 8px;
        }
        QLabel { color: #00F0FF; }
        QLineEdit, QComboBox {
            background-color: #1A0D36;
            color: #00F0FF;
            border: 1px solid #FF007F;
            border-radius: 6px;
            padding: 8px 12px;
        }
        QPushButton {
            background-color: #24114A;
            color: #00F0FF;
            border: 1px solid #00F0FF;
            border-radius: 6px;
            padding: 8px 14px;
            font-weight: 500;
        }
        QPushButton:hover { background-color: #381A72; }
        QTableWidget {
            background-color: #150A2A;
            color: #00F0FF;
            gridline-color: #FF007F;
            border: 1px solid #FF007F;
            border-radius: 6px;
        }
        QHeaderView::section {
            background-color: #1A0D36;
            color: #FF007F;
            border: none;
            padding: 6px;
        }
        QProgressBar {
            background-color: #1A0D36;
            border: 1px solid #FF007F;
            border-radius: 6px;
            height: 20px;
            text-align: center;
            color: #00F0FF;
            font-weight: bold;
        }
        QProgressBar::chunk {
            background-color: #FF007F;
            border-radius: 5px;
        }
    """,
}


class PRTMainWindow(QMainWindow):
    """Janela Principal do PRT Nexus."""

    def __init__(self) -> None:
        super().__init__()

        # --- REGISTRA O APP NO WINDOWS PARA PERMITIR NOTIFICAÇÕES ---
        if sys.platform == "win32":
            try:
                myappid = "prtlabs.prtnexus.desktop.1.0"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception:
                pass

        self.setWindowTitle("PRT NEXUS")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 600)

        self.settings = QSettings("PRTLabs", "PRTNexus")
        self.pages = {}

        self._setup_ui()
        self._setup_system_tray()

        saved_theme = self.settings.value("theme", "dark")
        self.apply_theme(saved_theme)

    def apply_theme(self, theme_id: str) -> None:
        """Aplica o tema CSS globalmente na aplicação."""
        style = THEME_STYLES.get(theme_id, THEME_STYLES["dark"])
        self.setStyleSheet(style)

    def _instantiate_page(self, page_cls, title_fallback="Página", **kwargs):
        if not page_cls:
            print(f"⚠️ AVISO: A classe da página '{title_fallback}' está NULA (Falhou no import lá no topo!)")
            return self._create_placeholder(title_fallback)

        try:
            return page_cls(parent=self, **kwargs)
        except Exception as e:
            print(f"❌ ERRO CRÍTICO ao instanciar '{title_fallback}': {e}")
            import traceback
            traceback.print_exc()
            return self._create_placeholder(title_fallback)

    def _create_placeholder(self, title: str):
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
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = PRTSidebar(parent=self, on_navigate=self.navigate_to)
        main_layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.stacked_widget)

        self._register_pages()
        self.navigate_to("dashboard")

    def _setup_system_tray(self) -> None:
        """Configura o ícone na bandeja do sistema (System Tray)."""
        self.tray_icon = QSystemTrayIcon(self)

        # 1. Tenta carregar do arquivo local de assets
        icon = QIcon("assets/icon.png")

        # 2. Se falhar, usa o ícone atribuído à janela
        if icon.isNull():
            icon = self.windowIcon()

        # 3. Se falhar, tenta o ícone padrão do sistema
        if icon.isNull():
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)

        # 4. Fallback infalível: desenha um ícone simples em memória
        if icon.isNull():
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor("#00F0FF"))
            icon = QIcon(pixmap)

        self.tray_icon.setIcon(icon)

        # Configura o menu da bandeja (botão direito)
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Abrir PRT NEXUS")
        show_action.triggered.connect(self.show_from_tray)

        tray_menu.addSeparator()

        quit_action = tray_menu.addAction("Sair do PRT NEXUS")
        quit_action.triggered.connect(self.force_quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_tray_icon_activated)
        self.tray_icon.show()

    def _on_tray_icon_activated(self, reason) -> None:
        """Restaura a janela ao clicar no ícone da bandeja."""
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_from_tray()

    def show_from_tray(self) -> None:
        """Exibe a janela novamente e traz para a frente."""
        self.show()
        self.activateWindow()
        self.raise_()

    def force_quit(self) -> None:
        """Encerra a aplicação de verdade."""
        if hasattr(self, "tray_icon"):
            self.tray_icon.hide()
        QApplication.quit()

    def closeEvent(self, event) -> None:
        """Intercepta o clique no botão de fechar (X)."""
        val = self.settings.value("minimize_to_tray", True)

        # Tratamento seguro contra strings do Registro do Windows ("false"/"true")
        if isinstance(val, str):
            minimize_to_tray = val.lower() in ("true", "1")
        else:
            minimize_to_tray = bool(val)

        if minimize_to_tray:
            event.ignore()
            self.hide()

            if hasattr(self, "tray_icon") and self.tray_icon.isVisible():
                self.tray_icon.showMessage(
                    "PRT NEXUS",
                    "O aplicativo continua rodando em segundo plano.",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000,
                )
        else:
            event.accept()
            self.force_quit()

    def _register_pages(self) -> None:
        self.pages["dashboard"] = self._instantiate_page(
            DashboardPage, "Início", on_navigate=self.navigate_to
        )
        self.pages["navegador"] = self._instantiate_page(BrowserPage, "Navegador Web")
        self.pages["downloads"] = self._instantiate_page(DownloadsPage, "Downloads")
        self.pages["biblioteca"] = self._instantiate_page(LibraryPage, "Biblioteca")
        self.pages["favoritos"] = self._instantiate_page(FavoritesPage, "Favoritos")
        self.pages["historico"] = self._instantiate_page(HistoryPage, "Histórico")

        # Conectar Sinal de Download do Navegador
        browser_widget = self.pages.get("navegador")
        if browser_widget and hasattr(browser_widget, "download_requested"):
            browser_widget.download_requested.connect(self._handle_browser_download)

        settings_widget = self._instantiate_page(SettingsPage, "Configurações")
        self.pages["configuracoes"] = settings_widget

        if hasattr(settings_widget, "theme_changed"):
            settings_widget.theme_changed.connect(self.apply_theme)

        self.pages["licenca"] = self._instantiate_page(LicensePage, "Licença")
        self.pages["plugins"] = self._instantiate_page(PluginsPage, "Plugins")
        self.pages["atualizacoes"] = self._instantiate_page(
            UpdatesPage, "Atualizações"
        )

        # Mapeamento com (chave_rota, chave_plataforma, nome_de_exibicao)
        connectors_map = [
            ("conn_youtube", "youtube", "YouTube"),
            ("conn_tiktok", "tiktok", "TikTok"),
            ("conn_kiwify", "kiwify", "Kiwify"),
            ("conn_hotmart", "hotmart", "Hotmart"),
            ("conn_vimeo", "vimeo", "Vimeo"),
            ("conn_gdrive", "gdrive", "Google Drive"),
            ("conn_mega", "mega", "Mega"),
            ("conn_universo", "universo", "Universo Técnico"),
        ]

        for route_key, conn_key, display_name in connectors_map:
            self.pages[route_key] = self._instantiate_page(
                ConnectorPage,
                title_fallback=display_name,
                platform_key=conn_key,
                connector_name=display_name,
            )

        for page_widget in self.pages.values():
            if page_widget:
                self.stacked_widget.addWidget(page_widget)

    def _handle_browser_download(
        self, url: str, media_type: str, quality: str, title: str = None
    ) -> None:
        """Recebe a solicitação do navegador e repassa o título real para a página de downloads."""
        downloads_widget = self.pages.get("downloads")
        if downloads_widget and hasattr(downloads_widget, "add_download"):
            downloads_widget.add_download(url, media_type, quality, title)

        self.navigate_to("downloads")

    def navigate_to(self, route_id: str) -> None:
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

            if hasattr(self, "sidebar") and hasattr(
                self.sidebar, "set_active_route"
            ):
                self.sidebar.set_active_route(target_key)

            if hasattr(page_widget, "on_show") and callable(page_widget.on_show):
                page_widget.on_show()


MainWindow = PRTMainWindow
main_window = PRTMainWindow