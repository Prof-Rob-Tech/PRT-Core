"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: PRTMainWindow

Description:
    Main Application Window for PRT NEXUS with direct explicit module loading,
    navigation handlers, system tray integration, and startup maximized mode.

Developer..: Prof Rob Tech
===========================================================
"""

import os
import sys
import traceback

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QStackedWidget,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

# --- GARANTE QUE A RAIZ DO PROJETO ESTÁ NO PATH DO PYTHON ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# --- IMPORTAÇÃO DIRETA E TRANSPARENTE DAS PÁGINAS ---

def _safe_import(module_path: str, class_name: str, fallback_title: str):
    """Importa uma classe de página exibindo o erro exato no terminal caso falhe."""
    try:
        mod = __import__(module_path, fromlist=[class_name])
        page_cls = getattr(mod, class_name)
        print(f"✅ Módulo '{module_path}' carregado com sucesso.")
        return page_cls
    except Exception as e:
        print(f"❌ [ERRO AO CARREGAR {fallback_title}] do arquivo '{module_path}':")
        traceback.print_exc()
        return None


DashboardPage = _safe_import("ui.pages.dashboard_page", "DashboardPage", "Dashboard")
DownloadsPage = _safe_import("ui.pages.downloads_page", "DownloadsPage", "Downloads")
CoursesPage = _safe_import("ui.pages.courses_page", "CoursesPage", "Cursos")
SettingsPage = _safe_import("ui.pages.settings_page", "SettingsPage", "Configurações")

# Tenta carregar Licença se existir
LicensePage = _safe_import("ui.pages.license_page", "LicensePage", "Licença")


class PRTMainWindow(QMainWindow):
    """Janela Principal do PRT NEXUS."""

    def __init__(self) -> None:
        super().__init__()
        self.settings = QSettings("PRTLabs", "PRTNexus")
        self.sidebar = None

        self.setWindowTitle("PRT NEXUS")
        self.resize(1100, 700)
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #0B0B0C;")

        self._build_ui()
        self._setup_tray_icon()

        # Inicia maximizado em tela cheia
        self.showMaximized()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.stacked_widget = QStackedWidget()

        # Instancia as páginas da interface (com fallback visual caso haja erro no arquivo)
        self.page_dashboard = DashboardPage() if DashboardPage else self._create_placeholder_page("Dashboard")
        self.page_downloads = DownloadsPage() if DownloadsPage else self._create_placeholder_page("Downloads")
        self.page_courses = CoursesPage() if CoursesPage else self._create_placeholder_page("Aulas / Cursos")
        self.page_settings = SettingsPage() if SettingsPage else self._create_placeholder_page("Configurações")
        self.page_license = LicensePage() if LicensePage else self._create_placeholder_page("Licença / Sobre")

        self.stacked_widget.addWidget(self.page_dashboard)
        self.stacked_widget.addWidget(self.page_downloads)
        self.stacked_widget.addWidget(self.page_courses)
        self.stacked_widget.addWidget(self.page_settings)
        self.stacked_widget.addWidget(self.page_license)

        self.main_layout.addWidget(self.stacked_widget, stretch=1)

    def add_sidebar(self, sidebar_widget: QWidget) -> None:
        """Adiciona o componente de Sidebar à janela principal."""
        if self.sidebar is not None:
            self.main_layout.removeWidget(self.sidebar)
            self.sidebar.deleteLater()

        self.sidebar = sidebar_widget

        if hasattr(self.sidebar, "navigation_requested"):
            self.sidebar.navigation_requested.connect(self._navigate_to_page)

        self.main_layout.insertWidget(0, self.sidebar)

    # --- MÉTODOS DE NAVEGAÇÃO CHAMADOS PELA SIDEBAR ---

    def show_dashboard(self) -> None:
        self.stacked_widget.setCurrentWidget(self.page_dashboard)

    def show_downloads(self) -> None:
        self.stacked_widget.setCurrentWidget(self.page_downloads)

    def show_courses(self) -> None:
        self.stacked_widget.setCurrentWidget(self.page_courses)

    def show_settings(self) -> None:
        self.stacked_widget.setCurrentWidget(self.page_settings)

    def show_license(self) -> None:
        self.stacked_widget.setCurrentWidget(self.page_license)

    def _navigate_to_page(self, page_index: int) -> None:
        if 0 <= page_index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(page_index)

    def _create_placeholder_page(self, title: str) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        lbl = QLabel(f"📄 Página: {title}")
        lbl.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold;")
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl)
        return page

    def _setup_tray_icon(self) -> None:
        self.tray_icon = QSystemTrayIcon(self)
        default_icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray_icon.setIcon(default_icon)

        tray_menu = QMenu()
        action_show = QAction("Mostrar PRT NEXUS", self)
        action_show.triggered.connect(self.showNormal)

        action_quit = QAction("Sair", self)
        action_quit.triggered.connect(self._force_quit)

        tray_menu.addAction(action_show)
        tray_menu.addSeparator()
        tray_menu.addAction(action_quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_tray_icon_activated)
        self.tray_icon.show()

    def _on_tray_icon_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()
                self.activateWindow()

    def _force_quit(self) -> None:
        if hasattr(self, "tray_icon") and self.tray_icon:
            self.tray_icon.hide()
        QApplication.quit()

    def closeEvent(self, event: QCloseEvent) -> None:
        close_to_tray = self.settings.value("close_to_tray", True, type=bool)

        if close_to_tray and hasattr(self, "tray_icon") and self.tray_icon and self.tray_icon.isVisible():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "PRT NEXUS",
                "O aplicativo continua rodando em segundo plano.",
                QSystemTrayIcon.Information,
                2500,
            )
        else:
            if hasattr(self, "tray_icon") and self.tray_icon:
                self.tray_icon.hide()
            event.accept()
            QApplication.quit()


# Alias para garantir compatibilidade
MainWindow = PRTMainWindow