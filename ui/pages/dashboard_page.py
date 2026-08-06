"""
===========================================================
PRT Labs

Project....: PRT Core
Module.....: UI / Pages
Class......: DashboardPage

Description:
    Main Dashboard Page for PRT NEXUS displaying system status,
    quick stats cards, and shortcut buttons with clean CSS targeting.

Developer..: Prof Rob Tech
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class DashboardPage(QWidget):
    """Página Inicial / Dashboard do PRT NEXUS."""

    def __init__(self) -> None:
        super().__init__()
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # 1. Cabeçalho de Boas-Vindas
        lbl_welcome = QLabel("🚀 PRT NEXUS — Painel Geral")
        lbl_welcome.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: bold; border: none; background: transparent;")
        layout.addWidget(lbl_welcome)

        # 2. Cards de Métricas e Status
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        cards_layout.addWidget(self._create_card("⚡ Status do Core", "ONLINE", "#28A745"))
        cards_layout.addWidget(self._create_card("📥 Gerenciador de Downloads", "PRONTO", "#007ACC"))
        cards_layout.addWidget(self._create_card("🎓 Player de Vídeos", "ATIVO", "#FFC107"))

        layout.addLayout(cards_layout)

        # 3. Painel de Ações Rápidas
        actions_card = QFrame()
        actions_card.setObjectName("ActionsCard")
        actions_card.setStyleSheet(
            """
            QFrame#ActionsCard {
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
            }
            QLabel {
                border: none;
                background: transparent;
            }
            """
        )
        actions_layout = QVBoxLayout(actions_card)
        actions_layout.setContentsMargins(20, 20, 20, 20)
        actions_layout.setSpacing(10)

        lbl_actions = QLabel("Acesso Rápido")
        lbl_actions.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: bold;")
        actions_layout.addWidget(lbl_actions)

        lbl_desc = QLabel("Selecione um dos módulos na barra lateral para começar a utilizar o sistema.")
        lbl_desc.setStyleSheet("color: #8E8E93; font-size: 12px;")
        actions_layout.addWidget(lbl_desc)

        layout.addWidget(actions_card)
        layout.addStretch()

    def _create_card(self, title: str, status_text: str, color: str) -> QFrame:
        """Cria um card visual de status sem bordas nos textos internos."""
        card = QFrame()
        card.setObjectName("StatusCard")
        card.setStyleSheet(
            f"""
            QFrame#StatusCard {{
                background-color: #141416;
                border: 1px solid #26262B;
                border-radius: 8px;
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
            """
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #8E8E93; font-size: 12px; font-weight: bold;")

        lbl_val = QLabel(status_text)
        lbl_val.setStyleSheet(f"color: {color}; font-size: 16px; font-weight: bold; margin-top: 5px;")

        card_layout.addWidget(lbl_title)
        card_layout.addWidget(lbl_val)
        return card


# Alias de compatibilidade
DashboardView = DashboardPage
DashboardWidget = DashboardPage