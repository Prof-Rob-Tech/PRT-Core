"""
===============================================================================
 PRT Core
-------------------------------------------------------------------------------
 Project.....: PRT Core
 Module......: Main Window
 Description.: Base reusable application window.

 Organization: PRT Labs
 Developer...: Prof Rob Tech
===============================================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow


class MainWindow(QMainWindow):
    """Base main window provided by PRT Core."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("PRT Core")
        self.resize(1000, 650)

        label = QLabel(
        "PRT Core\n\n"
        "Engineering first.\n"
        "Code second.\n\n"
        "Build once.\n"
        "Reuse forever."
)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)