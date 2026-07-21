"""
===========================================================
PRT Labs

Project....: PRT Core
Class......: PRTMainWindow

Description:
    Base window for all PRT Labs applications.

Developer..: Prof Rob Tech
===========================================================
"""
from ui.pages import (
    DashboardPage,
    DownloadsPage,
    CoursesPage,
    SettingsPage,
    LicensePage,
)

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class PRTMainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()

    def _build_ui(self) -> None:

        self.setWindowTitle("PRT Application")

        self.resize(1200, 700)

        central = QWidget()

        self.setCentralWidget(central)

        # Layout principal (Sidebar + Workspace)
        self._layout = QHBoxLayout(central)

        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.setSpacing(0)

        # Área central
        self._workspace = QWidget()

        self._workspace_layout = QVBoxLayout(self._workspace)

        self._workspace_layout.setContentsMargins(20, 20, 20, 20)

        self._workspace_layout.setSpacing(15)

        self._layout.addWidget(self._workspace)

        self._current_page = None

        self.show_dashboard()

    def add_sidebar(self, sidebar: QWidget) -> None:

        self._layout.insertWidget(0, sidebar)

    def add_widget(self, widget: QWidget) -> None:

        if self._current_page is not None:

            self._workspace_layout.removeWidget(self._current_page)

            self._current_page.deleteLater()

        self._current_page = widget

        self._workspace_layout.addWidget(widget)

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