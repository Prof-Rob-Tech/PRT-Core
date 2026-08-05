"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI
Class......: LicensePage

Description:
    License management page displaying plan details, active
    status, activation key info, and hardware ID.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.pages.base_page import BasePage


class LicensePage(BasePage):
    """License details and subscription page."""

    def __init__(self) -> None:
        super().__init__()

        self._layout = QVBoxLayout(self)

        self._configure()
        self._build_ui()

    def _configure(self) -> None:
        """Configure page margins and spacing."""
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(20)

    def _build_ui(self) -> None:
        """Build the user interface."""

        # Título
        title = QLabel("Informações de Licença")
        title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")
        self._layout.addWidget(title)

        # Card Principal de Licença
        card = QWidget()
        card.setObjectName("LicenseCard")
        card.setStyleSheet(
            """
            QWidget#LicenseCard {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 12px;
            }
            QLabel#PlanTitle {
                color: #FFFFFF;
                font-size: 17px;
                font-weight: bold;
            }
            QLabel#StatusBadge {
                background-color: #1C3829;
                color: #34C759;
                border: 1px solid #235436;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
                padding: 4px 12px;
            }
            QLabel#FieldLabel {
                color: #8E8E93;
                font-size: 13px;
            }
            QLabel#FieldValue {
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton {
                background-color: #1A1A1E;
                color: #FFFFFF;
                border: 1px solid #28282D;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #007ACC;
                border-color: #007ACC;
            }
            """
        )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(18)

        # Header do Card (Plano + Badge de Status)
        header_layout = QHBoxLayout()
        plan_title = QLabel("PRT NEXUS - Plano Enterprise / Vitalício")
        plan_title.setObjectName("PlanTitle")

        status_badge = QLabel("● LICENÇA ATIVA")
        status_badge.setObjectName("StatusBadge")

        header_layout.addWidget(plan_title)
        header_layout.addStretch()
        header_layout.addWidget(status_badge)

        card_layout.addLayout(header_layout)

        # Linha Divisória
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #26262B;")
        card_layout.addWidget(line)

        # Detalhes da Licença
        details_layout = QVBoxLayout()
        details_layout.setSpacing(12)

        fields = [
            ("Proprietário:", "Prof Rob Tech (robso@prtlabs.com)"),
            ("Chave de Ativação:", "PRT-NEXUS-8890-XKL9-2026-PRO"),
            ("Hardware ID (HWID):", "A4B9-8F12-330C-9E2F"),
            ("Validade:", "Vitalícia (Atualizações inclusas)"),
            ("Dispositivos Ativos:", "1 / 3 Máquinas Autorizadas"),
        ]

        for label_text, val_text in fields:
            row = QHBoxLayout()
            lbl_widget = QLabel(label_text)
            lbl_widget.setObjectName("FieldLabel")
            lbl_widget.setFixedWidth(160)

            val_widget = QLabel(val_text)
            val_widget.setObjectName("FieldValue")

            row.addWidget(lbl_widget)
            row.addWidget(val_widget)
            row.addStretch()
            details_layout.addLayout(row)

        card_layout.addLayout(details_layout)

        # Botão de Validação
        btn_layout = QHBoxLayout()
        btn_renew = QPushButton("🔄 Validar Licença Novamente")
        btn_renew.setCursor(Qt.PointingHandCursor)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_renew)

        card_layout.addLayout(btn_layout)

        self._layout.addWidget(card)
        self._layout.addStretch()
