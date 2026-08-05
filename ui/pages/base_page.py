"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: BasePage

Description:
    Base class for all application pages.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtWidgets import QWidget


class BasePage(QWidget):
    """Base class for all application pages."""

    def __init__(self) -> None:
        super().__init__()

    def _build_ui(self) -> None:
        """Build the user interface."""
        raise NotImplementedError

    def _connect_signals(self) -> None:
        """Connect widget signals."""

    def _initialize(self) -> None:
        """Initialize the page."""
