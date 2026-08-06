"""
===========================================================
PRT Labs - UI Widgets
Class: SidebarFooterCard

Description:
    Card informativo do rodapé da barra lateral com
    branding da PRT Labs e versão da aplicação.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class SidebarFooterCard(QFrame):
    """Card do rodapé da Sidebar com logo e versão."""

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(
            """
            QFrame {
                background-color: #14151A;
                border: 1px solid #23252E;
                border-radius: 8px;
                padding: 4px;
            }
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        lbl_icon = QLabel("❖")
        lbl_icon.setStyleSheet("color: #2F80ED; font-size: 16px; border: none;")

        vbox = QVBoxLayout()
        vbox.setSpacing(1)

        lbl_title = QLabel("PRT Labs")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: bold; border: none;")

        lbl_version = QLabel("PRT Nexus v0.1.0-alpha")
        lbl_version.setStyleSheet("color: #6C727F; font-size: 10px; border: none;")

        vbox.addWidget(lbl_title)
        vbox.addWidget(lbl_version)

        layout.addWidget(lbl_icon)
        layout.addLayout(vbox)
        layout.addStretch()