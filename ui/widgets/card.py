"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTCard

Description:
    Reusable card container with optional title.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from theme import Style
from ui.widgets.label import PRTLabel


class PRTCard(QFrame):
    """Reusable card container for PRT Labs applications."""

    def __init__(
        self,
        title: str = "",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._title = title
        self._layout = QVBoxLayout(self)

        self._configure()
        self._build_title()

    def _configure(self) -> None:
        """Configure the card appearance and internal layout."""

        self.setObjectName("PRTCard")

        self.setStyleSheet(
            Style.card.normal()
        )

        self._layout.setContentsMargins(15, 15, 15, 15)
        self._layout.setSpacing(10)

    def _build_title(self) -> None:
        """Create the title label when a title was provided."""

        if not self._title:
            return

        title_label = PRTLabel(self._title)

        title_label.setStyleSheet(
        """
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: white;
            }
         """
        )
        
        self._layout.addWidget(title_label)

    def add_widget(self, widget: QWidget) -> None:
        """Add a widget to the card content area."""

        self._layout.addWidget(widget)
