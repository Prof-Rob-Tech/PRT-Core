"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTProgressBar

Description:
    Reusable progress bar used to display download,
    installation and processing progress throughout
    PRT Labs applications.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QProgressBar, QWidget

from theme.manager import ThemeManager


class PRTProgressBar(QProgressBar):
    """Standard reusable progress bar for the PRT ecosystem."""

    def __init__(
        self,
        value: int = 0,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._configure()
        self.set_progress(value)

    def _configure(self) -> None:
        """Configure the appearance and behavior of the progress bar."""

        self.setObjectName("PRTProgressBar")

        self.setRange(0, 100)
        self.setTextVisible(False)

        self.setMinimumHeight(6)
        self.setMaximumHeight(6)

        self.setOrientation(Qt.Orientation.Horizontal)

        self.setStyleSheet(
            f"""
            QProgressBar#PRTProgressBar {{
                background-color: #31363D;
                border: none;
                border-radius: 3px;
            }}

            QProgressBar#PRTProgressBar::chunk {{
                background-color: {ThemeManager.primary_color()};
                border-radius: 3px;
            }}
            """
        )

    def set_progress(self, value: int) -> None:
        """Set the progress value between zero and one hundred."""

        normalized_value = max(0, min(100, int(value)))
        self.setValue(normalized_value)

    def progress(self) -> int:
        """Return the current progress value."""

        return self.value()