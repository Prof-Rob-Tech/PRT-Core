"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Application
Class......: Application

Description:
    Main application lifecycle controller.

Developer..: Prof Rob Tech
===========================================================
"""

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import PRTMainWindow
from ui.widgets.sidebar import PRTSidebar


class Application:
    """Main application lifecycle controller."""

    def __init__(self) -> None:
        self.qt_app = QApplication(sys.argv)

        self.main_window = PRTMainWindow()

        # Instancia e conecta o menu lateral à janela principal
        self.sidebar = PRTSidebar()
        self.sidebar.connect_main_window(self.main_window)
        self.main_window.add_sidebar(self.sidebar)

    def run(self) -> int:
        self.main_window.show()
        return self.qt_app.exec()
