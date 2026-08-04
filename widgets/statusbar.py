"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTStatusBar

Description:
    Bottom status bar displaying active metrics, system stats,
    and sync status.

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class PRTStatusBar(QWidget):
    """Bottom status bar widget for system and download metrics."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._layout = QHBoxLayout(self)

        self._build_ui()

    def _build_ui(self) -> None:
        """Build and style the status bar interface."""

        self.setObjectName("PRTStatusBar")
        self.setFixedHeight(35)

        self.setStyleSheet(
            """
            QWidget#PRTStatusBar {
                background-color: #121214;
                border-top: 1px solid #26262b;
            }
            QLabel {
                color: #8E8E93;
                font-size: 12px;
                font-weight: 500;
            }
            QLabel#GreenMetric {
                color: #34C759;
                font-weight: bold;
            }
            """
        )

        self._layout.setContentsMargins(15, 0, 15, 0)
        self._layout.setSpacing(20)

        # --- Seção Esquerda: Status de Downloads ---
        self.downloads_count_label = QLabel("↑ 3 downloads ativos")
        self.download_speed_label = QLabel("6.4 MB/s")
        self.download_speed_label.setObjectName("GreenMetric")

        left_container = QHBoxLayout()
        left_container.setSpacing(10)
        left_container.addWidget(self.downloads_count_label)
        left_container.addWidget(self.download_speed_label)

        # --- Seção Central: Métricas de Hardware (CPU / RAM) ---
        self.cpu_label = QLabel("CPU: 12%")
        self.ram_label = QLabel("RAM: 45%")

        center_container = QHBoxLayout()
        center_container.setSpacing(20)
        center_container.addWidget(self.cpu_label)
        center_container.addWidget(self.ram_label)

        # --- Seção Direita: Status de Sincronização ---
        self.sync_label = QLabel("● Sincronizado")
        self.sync_label.setObjectName("GreenMetric")

        # Montagem dos blocos no layout principal
        self._layout.addLayout(left_container)
        self._layout.addStretch()
        self._layout.addLayout(center_container)
        self._layout.addStretch()
        self._layout.addWidget(self.sync_label)