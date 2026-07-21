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
            """
            QPushButton {

                background: transparent;

                border: none;

                color: white;

                text-align: left;

                padding-left: 14px;

                font-size: 14px;

            }

            QPushButton:hover {

                background-color: #2A2A2A;

                border-radius: 6px;

            }

            QPushButton:pressed {

                background-color: #0066CC;

            }

            """
        )

    def set_selected(self, selected: bool) -> None:
        self._selected = selected

        if selected:

            self.setStyleSheet(
                """
                QPushButton {

                    background-color: #0066CC;

                    border-left: 4px solid #4EA3FF;

                    color: white;

                    text-align: left;

                    padding-left: 10px;

                    border-top-right-radius:6px;

                    border-bottom-right-radius:6px;

                }
                """
            )

        else:

            self._build_ui()