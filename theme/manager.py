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

from typing import Type

from theme.themes import BaseTheme, DarkTheme


class ThemeManager:
    """Centralized theme manager."""

    _themes: dict[str, Type[BaseTheme]] = {
        "dark": DarkTheme,
    }

    _current_theme_name = "dark"

    @classmethod
    def set_theme(cls, theme_name: str) -> None:
        """Set the active application theme."""

        normalized_name = theme_name.strip().lower()

        if normalized_name not in cls._themes:
            raise ValueError(
                f"Theme '{theme_name}' is not available."
            )

        cls._current_theme_name = normalized_name

    @classmethod
    def current_theme(cls) -> str:
        """Return the name of the active theme."""

        return cls._current_theme_name

    @classmethod
    def colors(cls) -> Type[BaseTheme]:
        """Return the active theme color palette."""

        return cls._themes[cls._current_theme_name]

    @classmethod
    def primary_color(cls) -> str:
        """Return the primary color of the active theme."""

        return cls.colors().PRIMARY

    @classmethod
    def background_color(cls) -> str:
        """Return the background color of the active theme."""

        return cls.colors().BACKGROUND

    @classmethod
    def text_color(cls) -> str:
        """Return the primary text color of the active theme."""

        return cls.colors().TEXT

    @classmethod
    def initialize(cls) -> None:
        """Initialize the theme system."""

        cls.set_theme("dark")
