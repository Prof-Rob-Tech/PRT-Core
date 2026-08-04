from theme import ThemeColors


class SidebarButtonStyle:

    @staticmethod
    def normal() -> str:
        return f"""
        QPushButton {{
            background-color: {ThemeColors.CARD};
            color: {ThemeColors.TEXT};
            border: none;
            text-align: left;
            padding: 10px;
        }}

        QPushButton:hover {{
            background-color: {ThemeColors.HOVER};
        }}
        """

    @staticmethod
    def selected() -> str:
        return f"""
        QPushButton {{
            background-color: {ThemeColors.PRIMARY};
            color: {ThemeColors.TEXT};
            border: none;
            border-left: 4px solid {ThemeColors.PRIMARY_LIGHT};
            text-align: left;
            padding: 10px;
        }}
        """