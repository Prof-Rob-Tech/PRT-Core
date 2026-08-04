"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTStatusBadge

Description:
    Reusable status indicator used by PRT Labs applications.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from theme.manager import ThemeManager


class PRTStatusBadge(QWidget):

    _STATUS_COLORS = {
        "disponível": "#22C55E",
        "baixando": "#3B82F6",
        "pausado": "#F59E0B",
        "concluído": "#9CA3AF",
        "erro": "#EF4444",
    }

    def __init__(
        self,
        status: str = "Disponível",
        parent: Optional[QWidget] = None,
    ) -> None:

        super().__init__(parent)

        self._status = status

        self._dot_label = QLabel(self)
        self._text_label = QLabel(self)

        self._layout = QHBoxLayout(self)

        self._configure()
        self._build_ui()
        self.set_status(status)

    def _configure(self) -> None:

        self.setObjectName("PRTStatusBadge")

        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(6)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self._dot_label.setObjectName("PRTStatusBadgeDot")
        self._dot_label.setFixedSize(10, 10)

        self._text_label.setObjectName("PRTStatusBadgeText")
        self._text_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        self._text_label.setStyleSheet(
            f"""
            QLabel#PRTStatusBadgeText {{
                color: {ThemeManager.text_color()};
                font-size: 10pt;
            }}
            """
        )

    def _build_ui(self) -> None:

        self._layout.addWidget(self._dot_label)
        self._layout.addWidget(self._text_label)

    def set_status(self, status: str) -> None:

        normalized_status = status.strip().lower()

        self._status = status

        color = self._STATUS_COLORS.get(
            normalized_status,
            ThemeManager.text_color(),
        )

        self._text_label.setText(status)

        self._dot_label.setStyleSheet(
            f"""
            QLabel#PRTStatusBadgeDot {{
                background-color: {color};
                border: none;
                border-radius: 5px;
            }}
            """
        )

    def status(self) -> str:

        return self._status