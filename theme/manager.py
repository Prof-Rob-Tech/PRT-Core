"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Theme
Class......: ThemeManager

Description:
    Manages the application visual theme.

Developer..: Prof Rob Tech
===========================================================
"""


class ThemeManager:
    """Centralized theme manager."""

    @staticmethod
    def primary_color() -> str:
        return "#0078D4"

    @staticmethod
    def background_color() -> str:
        return "#202020"

    @staticmethod
    def text_color() -> str:
        return "#FFFFFF"