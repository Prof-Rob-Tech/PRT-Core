"""
===========================================================
PRT Labs - UI Widgets
Class: SidebarNavItem

Description:
    Componente individual para os botões do menu da Sidebar,
    com suporte a seleção ativa e badge numérico.
===========================================================
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class SidebarNavItem(QWidget):
    """Botão de item da Sidebar com suporte a Badge."""

    clicked = Signal(str)

    def __init__(self, page_key: str, text: str, badge_count: str = "", active: bool = False) -> None:
        super().__init__()
        self.page_key = page_key

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.btn = QPushButton(text)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setCheckable(True)
        self.btn.setChecked(active)
        self.btn.setStyleSheet(
            """
            QPushButton {
                text-align: left;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 13px;
                color: #A0A5B1;
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #1E2028;
                color: #FFFFFF;
            }
            QPushButton:checked {
                background-color: #1552C6;
                color: #FFFFFF;
                font-weight: bold;
            }
            """
        )
        self.btn.clicked.connect(lambda: self.clicked.emit(self.page_key))
        layout.addWidget(self.btn, stretch=1)

        if badge_count:
            lbl_badge = QLabel(badge_count)
            lbl_badge.setStyleSheet(
                """
                QLabel {
                    background-color: #1552C6;
                    color: #FFFFFF;
                    font-size: 11px;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 2px 7px;
                }
                """
            )
            layout.addWidget(lbl_badge)

    def set_active(self, active: bool) -> None:
        self.btn.setChecked(active)