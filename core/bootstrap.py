"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Core
Class......: Bootstrap

Description:
    Initializes all application managers.

Developer..: Prof Rob Tech
===========================================================
"""

from theme.manager import ThemeManager


class Bootstrap:
    """Initialize the application."""

    @staticmethod
    def initialize() -> None:

        ThemeManager.initialize()