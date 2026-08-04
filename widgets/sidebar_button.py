"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTSidebarButton

Description:
    Sidebar navigation button.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QWidget
from theme import Style


class PRTSidebarButton(QPushButton):
    """Navigation button used by the sidebar."""

    def __init__(
        self,
        text: str,
        parent: Optional[QWidget] = None,
    ) -> None:

        super().__init__(text, parent)

        self._selected = False

        self._build_ui()

    def _build_ui(self) -> None:

        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(42)

        self.setStyleSheet(
            Style.sidebar.normal()
        )

    def set_selected(self, selected: bool) -> None:

        self._selected = selected

        if selected:
            self.setStyleSheet(
                Style.sidebar.selected()
            )
        else:
            self.setStyleSheet(
                Style.sidebar.normal()
            )