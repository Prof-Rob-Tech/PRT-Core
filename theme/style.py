"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Theme
Class......: Style

Description:
    Central access point for all application styles.

Developer..: Prof Rob Tech
===========================================================
"""

from theme.styles import (
    CardStyle,
    SidebarButtonStyle,
    TopBarStyle,
)


class Style:
    """Facade for all application styles."""

    card = CardStyle

    sidebar = SidebarButtonStyle

    top_bar = TopBarStyle