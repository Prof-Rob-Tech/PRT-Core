"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTButton

Description:
    Standard push button used by PRT Labs applications.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget

from theme.manager import ThemeManager


class PRTButton(QPushButton):
    """Standard reusable push button for the PRT ecosystem."""

    def __init__(
        self,
        text: str = "",
        parent: Optional[QWidget] = None,
        icon: Optional[QIcon] = None,
    ) -> None:
        super().__init__(text, parent)

        if icon is not None:
            self.setIcon(icon)

        self._configure()

    def _configure(self) -> None:
        """Configure the default geometry and behavior."""

        self.setObjectName("PRTButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(120, 38)

        self.setStyleSheet(
        f"""
        QPushButton#PRTButton {{
            background-color: {ThemeManager.primary_color()};
            color: {ThemeManager.text_color()};
            border: none;
            border-radius: 6px;
            padding: 8px;
    }}
    """
)        