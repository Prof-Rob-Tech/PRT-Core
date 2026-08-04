"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTTopBar

Description:
    Standard top navigation bar composed exclusively
    of reusable PRT Core widgets.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from theme.manager import ThemeManager
from widgets.avatar_button import PRTAvatarButton
from widgets.icon_button import PRTIconButton
from widgets.label import PRTLabel
from widgets.search_box import PRTSearchBox


class PRTTopBar(QFrame):
    """Reusable top navigation bar."""

    search_changed = Signal(str)
    notifications_clicked = Signal()
    profile_clicked = Signal()

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        search_placeholder: str = "Pesquisar...",
        user_initials: str = "RT",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._title_text = title
        self._subtitle_text = subtitle

        self._title_label = PRTLabel(title)
        self._subtitle_label = PRTLabel(subtitle)

        self._search_box = PRTSearchBox(
            placeholder=search_placeholder,
        )

        self._notifications_button = PRTIconButton(
            icon="🔔",
            tooltip="Notificações",
        )

        self._avatar_button = PRTAvatarButton(
            initials=user_initials,
        )

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        """Build the visual structure of the top bar."""

        self.setObjectName("PRTTopBar")
        self.setFixedHeight(72)

        self.setStyleSheet(
            """
            QFrame#PRTTopBar {
                background-color: transparent;
                border: none;
            }
            """
        )

        self._title_label.setStyleSheet(
            f"""
            QLabel#PRTLabel {{
                color: {ThemeManager.text_color()};
                font-size: 18pt;
                font-weight: 700;
                background-color: transparent;
            }}
            """
        )

        self._subtitle_label.setStyleSheet(
            """
            QLabel#PRTLabel {
                color: #9AA0A8;
                font-size: 10pt;
                font-weight: 400;
                background-color: transparent;
            }
            """
        )

        self._search_box.setFixedWidth(320)

        titles_layout = QVBoxLayout()
        titles_layout.setContentsMargins(0, 0, 0, 0)
        titles_layout.setSpacing(2)

        titles_layout.addWidget(self._title_label)

        if self._subtitle_text:
            titles_layout.addWidget(self._subtitle_label)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(12)

        main_layout.addLayout(titles_layout)
        main_layout.addStretch()
        main_layout.addWidget(self._search_box)
        main_layout.addWidget(self._notifications_button)
        main_layout.addWidget(self._avatar_button)

    def _connect_signals(self) -> None:
        """Connect internal widgets to the public top-bar signals."""

        self._search_box.search_changed.connect(
            self.search_changed.emit
        )

        self._notifications_button.clicked.connect(
            self.notifications_clicked.emit
        )

        self._avatar_button.clicked.connect(
            self.profile_clicked.emit
        )

    def set_title(self, title: str) -> None:
        """Update the top-bar title."""

        self._title_text = title
        self._title_label.setText(title)

    def title(self) -> str:
        """Return the current top-bar title."""

        return self._title_text

    def set_subtitle(self, subtitle: str) -> None:
        """Update the top-bar subtitle."""

        self._subtitle_text = subtitle
        self._subtitle_label.setText(subtitle)
        self._subtitle_label.setVisible(bool(subtitle))

    def subtitle(self) -> str:
        """Return the current top-bar subtitle."""

        return self._subtitle_text

    def set_search_placeholder(self, text: str) -> None:
        """Update the search-box placeholder."""

        self._search_box.set_placeholder(text)

    def search_text(self) -> str:
        """Return the current search text."""

        return self._search_box.text()

    def clear_search(self) -> None:
        """Clear the search box."""

        self._search_box.clear()

    def set_user_initials(self, initials: str) -> None:
        """Update the initials displayed in the avatar."""

        self._avatar_button.set_initials(initials)