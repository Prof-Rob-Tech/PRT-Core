"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTStatCard
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from .card import PRTCard


class PRTStatCard(PRTCard):

    def __init__(
        self,
        title: str,
        value: str,
        description: str,
        parent: Optional[QWidget] = None,
    ) -> None:

        super().__init__(title, parent)

        self._value = QLabel()
        self.set_value(value)
        self._description = QLabel()
        self.set_description(description)
        self._build_ui()

    def _build_ui(self) -> None:

        self._value.setAlignment(Qt.AlignCenter)
        self._value.setStyleSheet(
            """
            font-size:32px;
            font-weight:bold;
            color:white;
            """
        )

    def set_value(
        self,
        value,
    ) -> None:

        self._value.setText(str(value))

    def set_description(self, description: str) -> None:

        self._description.setText(description)
        self._description.setAlignment(Qt.AlignCenter)
        self._description.setStyleSheet(
            """
            color:#B0B0B0;
            font-size:12px;
            """
        )

        layout: QVBoxLayout = self.layout()
        layout.addStretch()
        layout.addWidget(self._value)
        layout.addWidget(self._description)
        layout.addStretch()