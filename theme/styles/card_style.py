"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Theme Styles
Class......: CardStyle

Description:
    Style definitions for PRTCard.

Developer..: Prof Rob Tech
===========================================================
"""

from theme import ThemeColors


class CardStyle:
    """Provide stylesheet definitions for card components."""

    @staticmethod
    def normal() -> str:
        """Return the default card stylesheet."""

        return f"""
        QFrame#PRTCard {{
            background-color: {ThemeColors.CARD};
            border: 1px solid {ThemeColors.BORDER};
            border-radius: 12px;
        }}
        """

    @staticmethod
    def title() -> str:
        """Return the card title stylesheet."""

        return f"""
        QLabel {{
            color: {ThemeColors.TEXT};
            font-size: 16px;
            font-weight: bold;
            border: none;
            background-color: transparent;
        }}
        """
