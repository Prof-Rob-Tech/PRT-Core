"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Pages
Class......: SettingsPage

Description:
    Settings Page for PRT NEXUS allowing application preferences management,
    such as toggling background/system tray close behavior.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QLabel, QVBoxLayout, QWidget


class SettingsPage(QWidget):
    """Página de Configurações do PRT NEXUS."""

    def __init__(self) -> None:
        super().__init__()
        self.settings = QSettings("PRTLabs", "PRTNexus")
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título da Página
        lbl_title = QLabel("⚙️ Configurações do Sistema")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_title)

        # Card de Preferências de Sistema
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
            }
            """
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(12)

        lbl_card_title = QLabel("Comportamento do Aplicativo")
        lbl_card_title.setStyleSheet("color: #8E8E93; font-size: 12px; font-weight: bold; text-transform: uppercase;")
        card_layout.addWidget(lbl_card_title)

        # Checkbox: Fechar para a bandeja
        self.chk_minimize_to_tray = QCheckBox("Manter aplicativo rodando na bandeja do sistema ao fechar (X)")
        self.chk_minimize_to_tray.setCursor(Qt.PointingHandCursor)
        self.chk_minimize_to_tray.setStyleSheet(
            """
            QCheckBox {
                color: #FFFFFF;
                font-size: 13px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #323238;
                background-color: #1C1C1F;
            }
            QCheckBox::indicator:hover {
                border-color: #007ACC;
            }
            QCheckBox::indicator:checked {
                background-color: #007ACC;
                border-color: #007ACC;
            }
            """
        )

        # Carrega o estado salvo (Padrão: True = envia para a bandeja)
        close_to_tray = self.settings.value("close_to_tray", True, type=bool)
        self.chk_minimize_to_tray.setChecked(close_to_tray)
        self.chk_minimize_to_tray.toggled.connect(self._on_close_to_tray_toggled)

        card_layout.addWidget(self.chk_minimize_to_tray)
        layout.addWidget(card)

        layout.addStretch()

    def _on_close_to_tray_toggled(self, checked: bool) -> None:
        """Salva a preferência do usuário no registro do sistema."""
        self.settings.setValue("close_to_tray", checked)