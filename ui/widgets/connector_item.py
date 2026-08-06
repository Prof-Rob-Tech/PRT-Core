"""
===========================================================
PRT Labs - UI Widgets
Class: ConnectorItem

Description:
    Item de conector para a Sidebar com indicador
    de status (bolinha verde/cinza).
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class ConnectorItem(QWidget):
    """Linha de exibição de conector externo com status indicator."""

    def __init__(self, icon: str, name: str, online: bool = True) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(10)

        lbl_info = QLabel(f"{icon}  {name}")
        lbl_info.setStyleSheet("color: #D1D5DB; font-size: 13px; background: transparent;")

        dot_color = "#28C76F" if online else "#4B505E"
        lbl_dot = QLabel("●")
        lbl_dot.setStyleSheet(f"color: {dot_color}; font-size: 10px; background: transparent;")

        layout.addWidget(lbl_info, stretch=1)
        layout.addWidget(lbl_dot)