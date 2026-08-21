"""
===========================================================
PRT Labs - UI / Placeholder Page
Class: PlaceholderPage
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PlaceholderPage(QWidget):
    """Página temporária exibida quando uma aba ainda não possui conteúdo."""

    def __init__(self, title: str = "Página em Desenvolvimento", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        label = QLabel(f"🚧 {title}\n\nEsta seção está em desenvolvimento.", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #71717A; font-size: 14px; font-weight: 500;")

        layout.addWidget(label)