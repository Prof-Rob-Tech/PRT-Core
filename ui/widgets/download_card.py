"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTDownloadCard

Description:
    Reusable card for displaying downloadable content,
    including title, description, category, status and
    an action button.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional

from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from theme.manager import ThemeManager
from ui.widgets.button import PRTButton
from ui.widgets.card import PRTCard
from ui.widgets.label import PRTLabel
from ui.widgets.status_badge import PRTStatusBadge


class PRTDownloadCard(PRTCard):
    """Reusable card for displaying downloadable content."""

    def __init__(
        self,
        title: str,
        description: str,
        category: str,
        status: str,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent=parent)

        self._title = title
        self._description = description
        self._category = category
        self._status = status

        self._status_badge = PRTStatusBadge(self._status)
        self._action_button = PRTButton()

        self._build_content()
        self._configure_status()

    def _build_content(self) -> None:
        """Build the visual structure of the download card."""

        content = QWidget()

        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_label = PRTLabel(self._title)

        title_label.setStyleSheet(
            f"""
            QLabel#PRTLabel {{
                color: {ThemeManager.text_color()};
                font-size: 15pt;
                font-weight: 700;
            }}
            """
        )

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self._status_badge)

        description_label = PRTLabel(self._description)

        description_label.setStyleSheet(
            """
            QLabel#PRTLabel {
                font-size: 11pt;
                color: #BFBFBF;
            }
            """
        )

        category_label = PRTLabel(
            f"Categoria: {self._category}"
        )

        category_label.setStyleSheet(
            """
            QLabel#PRTLabel {
                font-size: 10pt;
                color: #8C8C8C;
            }
            """
        )

        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 0, 0, 0)

        footer_layout.addStretch()
        footer_layout.addWidget(self._action_button)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(description_label)
        main_layout.addWidget(category_label)
        main_layout.addLayout(footer_layout)

        self.add_widget(content)

    def _configure_status(self) -> None:
        """Configure the action button according to the status."""

        actions = {
            "Disponível": "Baixar",
            "Baixando": "Pausar",
            "Pausado": "Continuar",
            "Concluído": "Abrir",
            "Erro": "Tentar novamente",
        }

        button_text = actions.get(
            self._status,
            "Baixar",
        )

        self._action_button.setText(button_text)
