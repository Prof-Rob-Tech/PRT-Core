"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTSearchBox

Description:
    Reusable search box used throughout
    PRT Labs applications.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QWidget,
)

from theme.manager import ThemeManager


class PRTSearchBox(QWidget):
    """Reusable search box."""

    search_changed = Signal(str)

    def __init__(
        self,
        placeholder: str = "Pesquisar...",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._edit = QLineEdit()

        self._build_ui()

        self.set_placeholder(placeholder)

        self._edit.textChanged.connect(
            self.search_changed.emit
        )

    def _build_ui(self) -> None:

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        self._edit.setMinimumWidth(320)
        self._edit.setMinimumHeight(38)

        self._edit.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: #343A42;
                border: 1px solid #454C55;
                border-radius: 10px;
                padding-left: 12px;
                padding-right: 12px;
                color: {ThemeManager.text_color()};
                selection-background-color: {ThemeManager.primary_color()};
            }}

            QLineEdit:focus {{
                border: 1px solid {ThemeManager.primary_color()};
            }}
            """
        )

        layout.addWidget(self._edit)

    def set_placeholder(self, text: str) -> None:
        """Update the placeholder text."""

        self._edit.setPlaceholderText(text)

    def text(self) -> str:
        """Return the current search text."""

        return self._edit.text()

    def clear(self) -> None:
        """Clear the search box."""

        self._edit.clear()

    def set_text(self, text: str) -> None:
        """Set the current search text."""

        self._edit.setText(text)
