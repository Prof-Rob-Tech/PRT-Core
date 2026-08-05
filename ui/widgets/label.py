"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTLabel

Description:
    Standard label used by PRT Labs applications.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget

from theme.manager import ThemeManager


class PRTLabel(QLabel):

    def __init__(
        self,
        text: str = "",
        parent: Optional[QWidget] = None,
    ) -> None:

        super().__init__(text, parent)

        self._configure()

    def _configure(self) -> None:

        self.setObjectName("PRTLabel")

        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.setStyleSheet(
            f"""
            QLabel#PRTLabel {{
                color: {ThemeManager.text_color()};
                font-size: 12pt;
            }}
            """
        )
