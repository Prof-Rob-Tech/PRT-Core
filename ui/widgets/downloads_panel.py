"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTDownloadsPanel

Description:
    Reusable panel for grouping download widgets under
    a common header with an optional "View all" action.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from theme.manager import ThemeManager
from ui.widgets.card import PRTCard
from ui.widgets.label import PRTLabel


class PRTDownloadsPanel(PRTCard):
    """Reusable panel for displaying a list of download items."""

    view_all_clicked = Signal()

    def __init__(
        self,
        title: str = "Downloads ativos",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent=parent)

        self._title = title
        self._item_count = 0

        self._title_label = PRTLabel(self._title)
        self._view_all_label = PRTLabel("Ver todos →")

        self._items_container = QWidget()
        self._items_layout = QVBoxLayout(self._items_container)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        """Build the visual structure of the downloads panel."""

        content = QWidget()

        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(18)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        self._title_label.setStyleSheet(
            f"""
            QLabel#PRTLabel {{
                color: {ThemeManager.text_color()};
                font-size: 12pt;
                font-weight: 600;
                background-color: transparent;
            }}
            """
        )

        self._view_all_label.setStyleSheet(
            f"""
            QLabel#PRTLabel {{
                color: {ThemeManager.primary_color()};
                font-size: 9pt;
                font-weight: 600;
                background-color: transparent;
            }}
            """
        )

        self._view_all_label.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self._items_container.setObjectName(
            "PRTDownloadsPanelItems"
        )

        self._items_container.setStyleSheet(
            """
            QWidget#PRTDownloadsPanelItems {
                background-color: transparent;
            }
            """
        )

        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(0)

        header_layout.addWidget(self._title_label)
        header_layout.addStretch()
        header_layout.addWidget(self._view_all_label)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self._items_container)

        self.add_widget(content)

    def _connect_signals(self) -> None:
        """Connect the panel interaction signals."""

        self._view_all_label.mousePressEvent = (
            self._handle_view_all_click
        )

    def _handle_view_all_click(self, event) -> None:
        """Emit the view-all signal after a left mouse click."""

        if event.button() == Qt.MouseButton.LeftButton:
            self.view_all_clicked.emit()

        event.accept()

    def _create_separator(self) -> QFrame:
        """Create a visual separator between download items."""

        separator = QFrame()

        separator.setObjectName(
            "PRTDownloadsPanelSeparator"
        )

        separator.setFrameShape(
            QFrame.Shape.HLine
        )

        separator.setFrameShadow(
            QFrame.Shadow.Plain
        )

        separator.setFixedHeight(1)

        separator.setStyleSheet(
            """
            QFrame#PRTDownloadsPanelSeparator {
                background-color: #343A42;
                border: none;
                margin-left: 8px;
                margin-right: 8px;
            }
            """
        )

        return separator

    def add_item(self, item: QWidget) -> None:
        """Add a download widget to the panel."""

        if self._item_count > 0:
            self._items_layout.addWidget(
                self._create_separator()
            )

        self._items_layout.addWidget(item)

        self._item_count += 1

    def clear_items(self) -> None:
        """Remove all download widgets and separators."""

        while self._items_layout.count():
            layout_item = self._items_layout.takeAt(0)
            widget = layout_item.widget()

            if widget is not None:
                widget.deleteLater()

        self._item_count = 0

    def set_title(self, title: str) -> None:
        """Update the panel title."""

        self._title = title
        self._title_label.setText(self._title)

    def title(self) -> str:
        """Return the current panel title."""

        return self._title

    def item_count(self) -> int:
        """Return the number of download items in the panel."""

        return self._item_count
