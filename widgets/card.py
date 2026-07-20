"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTCard

Description:
    Reusable card container.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from theme.manager import ThemeManager


class PRTCard(QFrame):

    def __init__(
        self,
        parent: Optional[QWidget] = None,
    ) -> None:

        super().__init__(parent)

        self._configure()

    def _configure(self) -> None:

        self.setObjectName("PRTCard")

        self.setStyleSheet(
            f"""
            QFrame#PRTCard {{

                background-color: {ThemeManager.background_color()};

                border: 1px solid #404040;

                border-radius: 10px;

            }}
            """
        )

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(15, 15, 15, 15)

        self.layout.setSpacing(10)

    def add_widget(self, widget):

        self.layout.addWidget(widget)