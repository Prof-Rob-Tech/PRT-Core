"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTStoragePanel

Description:
    Side panel displaying local disk storage usage with a
    progress bar.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QVBoxLayout, QWidget


class PRTStoragePanel(QWidget):
    """Panel displaying local storage statistics."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._layout = QVBoxLayout(self)
        self._build_ui()

    def _build_ui(self) -> None:
        self.setObjectName("PRTStoragePanel")
        self.setStyleSheet(
            """
            QWidget#PRTStoragePanel {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 12px;
            }
            QLabel#TitleLabel {
                color: #FFFFFF;
                font-size: 15px;
                font-weight: bold;
            }
            QLabel#StatsLabel {
                color: #8E8E93;
                font-size: 12px;
            }
            QProgressBar {
                background-color: #1F1F23;
                border: none;
                border-radius: 4px;
                height: 8px;
                text-align: center;
                color: transparent;
            }
            QProgressBar::chunk {
                background-color: #007ACC;
                border-radius: 4px;
            }
            """
        )

        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(12)

        # Título
        title = QLabel("Armazenamento Local")
        title.setObjectName("TitleLabel")
        self._layout.addWidget(title)

        # Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(68)  # Simulando 68% de uso
        self.progress_bar.setTextVisible(False)
        self._layout.addWidget(self.progress_bar)

        # Textos de Uso (Usado vs Total)
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        
        used_label = QLabel("Usado: 340 GB")
        used_label.setObjectName("StatsLabel")
        
        total_label = QLabel("Total: 500 GB")
        total_label.setObjectName("StatsLabel")
        total_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        stats_layout.addWidget(used_label)
        stats_layout.addStretch()
        stats_layout.addWidget(total_label)

        self._layout.addLayout(stats_layout)