"""
══════════════════════════════════════════════════════════════

                           PRT Core

                    Engineering Framework

                    Engineering first.
                      Code second.

                      Build once.
                    Reuse forever.

Framework developed by Prof Rob Tech.

Used by PRT Labs software.

══════════════════════════════════════════════════════════════

Module:
    Application

Description:
    Main application lifecycle controller.

══════════════════════════════════════════════════════════════
"""

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


class Application:
    """Main application lifecycle controller."""

    def __init__(self) -> None:
        self.qt_app = QApplication(sys.argv)
        self.main_window = MainWindow()

    def run(self) -> int:
        self.main_window.show()
        return self.qt_app.exec()