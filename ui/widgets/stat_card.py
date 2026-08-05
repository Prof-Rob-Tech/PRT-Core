"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTStatCard

Description:
    Reusable statistics card for displaying a title,
    a highlighted value and a short description.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from theme.manager import ThemeManager
from ui.widgets.card import PRTCard


class PRTStatCard(PRTCard):
    """Reusable card for displaying statistical information."""

    def __init__(
        self,
        title: str,
        value: str,
        description: str,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(title, parent)

        self._value_label = QLabel()
        self._description_label = QLabel()

        self._build_ui()

        self.set_value(value)
        self.set_description(description)

    def _build_ui(self) -> None:
        """Build and configure the visual structure of the card."""

        self.setMinimumSize(180, 130)

        self._value_label.setObjectName("PRTStatCardValue")
        self._value_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter
            | Qt.AlignmentFlag.AlignVCenter
        )

        self._value_label.setStyleSheet(
            f"""
            QLabel#PRTStatCardValue {{
                color: {ThemeManager.text_color()};
                font-size: 26pt;
                font-weight: 700;
                background-color: transparent;
            }}
            """
        )

        self._description_label.setObjectName(
            "PRTStatCardDescription"
        )

        self._description_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter
            | Qt.AlignmentFlag.AlignVCenter
        )

        self._description_label.setStyleSheet(
            """
            QLabel#PRTStatCardDescription {
                color: #A8AFB9;
                font-size: 10pt;
                font-weight: 400;
                background-color: transparent;
            }
            """
        )

        layout: QVBoxLayout = self.layout()

        layout.addStretch()
        layout.addWidget(self._value_label)
        layout.addWidget(self._description_label)
        layout.addStretch()

    def set_value(self, value: str) -> None:
        """Update the highlighted value displayed by the card."""

        self._value_label.setText(str(value))

    def value(self) -> str:
        """Return the current highlighted value."""

        return self._value_label.text()

    def set_description(self, description: str) -> None:
        """Update the description displayed below the value."""

        self._description_label.setText(description)

    def description(self) -> str:
        """Return the current card description."""

        return self._description_label.text()
