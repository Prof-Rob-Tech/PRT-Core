"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Theme
Class......: TopBarStyle

Description:
    Styles used by the PRTTopBar widget.

Developer..: Prof Rob Tech
===========================================================
"""

from theme.manager import ThemeManager


class TopBarStyle:
    """Reusable styles for the PRTTopBar widget."""

    @staticmethod
    def container() -> str:

        return """
        QFrame#PRTTopBar {
            background-color: transparent;
            border: none;
        }
        """

    @staticmethod
    def title() -> str:

        return f"""
        QLabel#PRTLabel {{
            color: {ThemeManager.text_color()};
            font-size: 18pt;
            font-weight: 700;
            background-color: transparent;
        }}
        """

    @staticmethod
    def subtitle() -> str:

        return """
        QLabel#PRTLabel {
            color: #9AA0A8;
            font-size: 10pt;
            font-weight: 400;
            background-color: transparent;
        }
        """
