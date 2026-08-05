"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTIconButton

Description:
    Standard icon button used throughout
    PRT Labs applications.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton, QWidget

from theme.manager import ThemeManager


class PRTIconButton(QPushButton):
    """Reusable icon button."""

    def __init__(
        self,
        icon: str = "",
        tooltip: str = "",
        parent: Optional[QWidget] = None,
    ) -> None:

        super().__init__(parent)

        self.setText(icon)
        self.setToolTip(tooltip)

        self._configure()

    def _configure(self) -> None:

        self.setObjectName("PRTIconButton")

        self.setFixedSize(QSize(40, 40))

        self.setStyleSheet(
            f"""
            QPushButton#PRTIconButton {{
                background-color:#343A42;
                border:1px solid #454C55;
                border-radius:10px;
                color:{ThemeManager.text_color()};
                font-size:13pt;
            }}

            QPushButton#PRTIconButton:hover {{
                background-color:#404854;
                border:1px solid {ThemeManager.primary_color()};
            }}

            QPushButton#PRTIconButton:pressed {{
                background-color:{ThemeManager.primary_color()};
                color:white;
            }}
            """
        )
