"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTSidebar

Description:
    Left navigation panel used by PRT Labs applications.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional
from PySide6.QtWidgets import QVBoxLayout, QWidget
from widgets.label import PRTLabel
from widgets.sidebar_button import PRTSidebarButton


class PRTSidebar(QWidget):
    """Left navigation panel for PRT Labs applications."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._layout = QVBoxLayout(self)

        self._build_ui()

    def _build_ui(self) -> None:
        """Build and style the sidebar interface."""

        self.setObjectName("PRTSidebar")
        self.setFixedWidth(230)

        self.setStyleSheet(
            """
            QWidget#PRTSidebar {
                background-color: #181818;
                border-right: 1px solid #303030;
            }
            """
        )

        self._layout.setContentsMargins(15, 20, 15, 20)
        self._layout.setSpacing(10)
        self._build_header()
        self._build_navigation()
        self._build_footer()

    def _build_header(self) -> None:
        """Create the application name displayed at the top."""

        logo = PRTLabel("PRT NEXUS")

        logo.setStyleSheet(
            """
            QLabel {
                color: #FFFFFF;
                font-size: 20px;
                font-weight: bold;
            }
            """
        )

        self._layout.addWidget(logo)
        self._layout.addSpacing(20)

    def _build_navigation(self) -> None:
        """Create the initial navigation items."""

        self.dashboard = PRTSidebarButton("Dashboard")
        self.downloads = PRTSidebarButton("Downloads")
        self.courses = PRTSidebarButton("Cursos")
        self.settings = PRTSidebarButton("Configurações")
        self.license = PRTSidebarButton("Licença")

        self.dashboard.set_selected(True)

        self._layout.addWidget(self.dashboard)
        self._layout.addWidget(self.downloads)
        self._layout.addWidget(self.courses)
        self._layout.addWidget(self.settings)
        self._layout.addWidget(self.license)
        
    def connect_main_window(self, window) -> None:

        self.dashboard.clicked.connect(
            lambda: self._navigate(
                self.dashboard,
                window.show_dashboard,
            )
        )

        self.downloads.clicked.connect(
            lambda: self._navigate(
                self.downloads,
                window.show_downloads,
            )
        )

        self.courses.clicked.connect(
            lambda: self._navigate(
                self.courses,
                window.show_courses,
            )
        )

        self.settings.clicked.connect(
            lambda: self._navigate(
                self.settings,
                window.show_settings,
            )
        )

        self.license.clicked.connect(
            lambda: self._navigate(
                self.license,
                window.show_license,
            )
        )

        self.set_selected_button(self.dashboard)

    def _navigate(self, button, page_callback) -> None:

        self.set_selected_button(button)

        page_callback()
    
    def set_selected_button(self, selected_button) -> None:

        buttons = (
            self.dashboard,
            self.downloads,
            self.courses,
            self.settings,
            self.license,
        )

        for button in buttons:

            button.set_selected(button is selected_button)

    def _build_footer(self) -> None:
        """Create the version label at the bottom."""

        self._layout.addStretch()

        version = PRTLabel("v0.1 Alpha")

        version.setStyleSheet(
            """
            QLabel {
                color: #777777;
                font-size: 11px;
            }
            """
        )

        self._layout.addWidget(version)

    def add_widget(self, widget: QWidget) -> None:
        """Add an external widget to the sidebar."""

        self._layout.addWidget(widget)