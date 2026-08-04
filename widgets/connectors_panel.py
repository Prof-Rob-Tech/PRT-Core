"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: Widgets
Class......: PRTConnectorsPanel

Description:
    Side panel displaying real-time connector statuses
    (YouTube, Kiwify, Hotmart, Google Drive, etc.).

Developer..: Prof Rob Tech
===========================================================
"""

from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class ConnectorItem(QWidget):
    """Individual connector status row."""

    def __init__(
        self,
        name: str,
        status_text: str = "Conectado",
        is_active: bool = True,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(12, 10, 12, 10)

        self.setStyleSheet(
            """
            QWidget {
                background-color: #1F1F23;
                border-radius: 8px;
            }
            QLabel#NameLabel {
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 600;
            }
            QLabel#StatusLabel {
                color: #8E8E93;
                font-size: 11px;
            }
            """
        )

        # Nome da plataforma
        name_label = QLabel(name)
        name_label.setObjectName("NameLabel")

        # Indicador visual (LED) + Texto de Status
        status_color = "#34C759" if is_active else "#FF3B30"
        led_label = QLabel("●")
        led_label.setStyleSheet(f"color: {status_color}; font-size: 10px;")

        status_label = QLabel(status_text)
        status_label.setObjectName("StatusLabel")

        status_container = QHBoxLayout()
        status_container.setSpacing(6)
        status_container.addWidget(led_label)
        status_container.addWidget(status_label)

        self._layout.addWidget(name_label)
        self._layout.addStretch()
        self._layout.addLayout(status_container)


class PRTConnectorsPanel(QWidget):
    """Panel holding all platform integrations and connectors."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self._layout = QVBoxLayout(self)
        self._build_ui()

    def _build_ui(self) -> None:
        self.setObjectName("PRTConnectorsPanel")
        self.setStyleSheet(
            """
            QWidget#PRTConnectorsPanel {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 12px;
            }
            QLabel#TitleLabel {
                color: #FFFFFF;
                font-size: 15px;
                font-weight: bold;
            }
            """
        )

        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(10)

        # Título do Painel
        title = QLabel("Conectores Ativos")
        title.setObjectName("TitleLabel")
        self._layout.addWidget(title)

        # Lista de Plataformas / Conectores
        self._layout.addWidget(ConnectorItem("YouTube", "Conectado", True))
        self._layout.addWidget(ConnectorItem("Kiwify", "Conectado", True))
        self._layout.addWidget(ConnectorItem("Hotmart", "Autenticando", True))
        self._layout.addWidget(ConnectorItem("Google Drive", "Desconectado", False))

        self._layout.addStretch()