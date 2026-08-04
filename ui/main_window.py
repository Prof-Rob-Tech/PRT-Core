"""
===========================================================
PRT Labs

Project....: PRT Core
Class......: PRTMainWindow

Description:
    Base window for all PRT Labs applications, featuring a
    sidebar, fixed topbar, dynamic workspace area, and
    bottom status bar.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from ui.pages import (
    CoursesPage,
    DashboardPage,
    DownloadsPage,
    LicensePage,
    SettingsPage,
)
from widgets.statusbar import PRTStatusBar
from widgets.topbar import PRTTopBar


class PRTMainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()

    def _build_ui(self) -> None:

        self.setWindowTitle("PRT Application")
        self.resize(1200, 750)

        central = QWidget()
        self.setCentralWidget(central)

        # Layout Vertical Principal (Área Superior + Barra de Status)
        self._root_layout = QVBoxLayout(central)
        self._root_layout.setContentsMargins(0, 0, 0, 0)
        self._root_layout.setSpacing(0)

        # Container para a Área Superior (Sidebar + Workspace)
        self._top_container = QWidget()
        self._layout = QHBoxLayout(self._top_container)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # Área de Conteúdo Central (Workspace = TopBar Fixa + Páginas Dinâmicas)
        self._workspace = QWidget()
        self._workspace_layout = QVBoxLayout(self._workspace)
        self._workspace_layout.setContentsMargins(20, 20, 20, 20)
        self._workspace_layout.setSpacing(0)

        # 1. Adiciona a Barra Superior Fixa
        self._top_bar = PRTTopBar()
        self._workspace_layout.addWidget(self._top_bar)

        # 2. Adiciona o Container Dinâmico de Páginas
        self._page_container = QWidget()
        self._page_layout = QVBoxLayout(self._page_container)
        self._page_layout.setContentsMargins(0, 0, 0, 0)
        self._workspace_layout.addWidget(self._page_container)

        self._layout.addWidget(self._workspace)

        # Instancia e posiciona a barra de status no rodapé
        self._status_bar = PRTStatusBar()

        self._root_layout.addWidget(self._top_container)
        self._root_layout.addWidget(self._status_bar)

        self._current_page = None

        self.show_dashboard()

    def add_sidebar(self, sidebar: QWidget) -> None:

        self._layout.insertWidget(0, sidebar)

    def add_widget(self, widget: QWidget) -> None:

        # Remove a página atual apenas do container de páginas
        if self._current_page is not None:
            self._page_layout.removeWidget(self._current_page)
            self._current_page.deleteLater()

        self._current_page = widget
        self._page_layout.addWidget(widget)

    def show_dashboard(self) -> None:

        self.add_widget(DashboardPage())

    def show_downloads(self) -> None:

        self.add_widget(DownloadsPage())

    def show_courses(self) -> None:

        self.add_widget(CoursesPage())

    def show_settings(self) -> None:

        self.add_widget(SettingsPage())

    def show_license(self) -> None:

        self.add_widget(LicensePage())