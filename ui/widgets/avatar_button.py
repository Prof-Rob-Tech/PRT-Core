"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTAvatarButton

Description:
    Reusable avatar button used in the application top bar.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton, QWidget

from theme.manager import ThemeManager


class PRTAvatarButton(QPushButton):
    """Reusable avatar button."""

    def __init__(
        self,
        initials: str = "RT",
        parent: Optional[QWidget] = None,
    ) -> None:

        super().__init__(parent)

        self._initials = initials

        self._configure()

    def _configure(self) -> None:

        self.setObjectName("PRTAvatarButton")

        self.setFixedSize(QSize(40, 40))

        self.setText(self._initials)

        self.setStyleSheet(
            f"""
            QPushButton#PRTAvatarButton {{
                background-color: {ThemeManager.primary_color()};
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 10pt;
                font-weight: 700;
            }}

            QPushButton#PRTAvatarButton:hover {{
                background-color: #2C86FF;
            }}

            QPushButton#PRTAvatarButton:pressed {{
                background-color: #1565C0;
            }}
            """
        )

    def set_initials(self, initials: str) -> None:
        """Update avatar initials."""

        self._initials = initials.upper()

        self.setText(self._initials)

    def initials(self) -> str:
        """Return current initials."""

        return self._initials
