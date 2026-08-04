"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTTopBar

Description:
    Global top navigation bar featuring a search input and
    user profile indicator.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget


class PRTTopBar(QWidget):
    """Top navigation and search bar widget."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._layout = QHBoxLayout(self)
        self._build_ui()

    def _build_ui(self) -> None:
        self.setObjectName("PRTTopBar")
        self.setFixedHeight(60)
        
        self.setStyleSheet(
            """
            QWidget#PRTTopBar {
                background-color: transparent;
            }
            QLineEdit {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
                color: #FFFFFF;
                padding: 8px 15px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #007ACC;
            }
            QLabel#ProfileIcon {
                background-color: #007ACC;
                color: #FFFFFF;
                border-radius: 18px;
                font-weight: bold;
                font-size: 14px;
            }
            """
        )

        self._layout.setContentsMargins(0, 0, 0, 15)
        self._layout.setSpacing(20)

        # Barra de Pesquisa Central
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Pesquisar cursos, arquivos ou conectores... (Ctrl+K)")
        self.search_bar.setFixedWidth(450)

        # Ícone de Perfil (Simulado)
        self.profile_icon = QLabel("RT")
        self.profile_icon.setObjectName("ProfileIcon")
        self.profile_icon.setFixedSize(36, 36)
        self.profile_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._layout.addStretch()
        self._layout.addWidget(self.search_bar)
        self._layout.addStretch()
        self._layout.addWidget(self.profile_icon)