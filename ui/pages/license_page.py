"""
===========================================================
PRT Labs - UI / Pages
Class: LicensePage
Description: Página de Gestão de Licença e Planos adaptável a temas.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class LicensePage(QWidget):
    """Página de Licença e Gestão de Assinatura."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Cabeçalho
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        lbl_title = QLabel("🔑 Minha Licença & Planos")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        lbl_subtitle = QLabel("Gerencie seu plano ativo, chave de licença, HWID e opções de renovação.")
        lbl_subtitle.setStyleSheet("color: #8E8E93; font-size: 13px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        layout.addLayout(title_layout)

        # Card de Licença Ativa
        card_active = QFrame()
        card_active.setObjectName("cardFrame")
        ca_layout = QVBoxLayout(card_active)
        ca_layout.setContentsMargins(15, 15, 15, 15)
        ca_layout.setSpacing(12)

        header_active = QHBoxLayout()
        lbl_plan_name = QLabel("👑 PRT NEXUS PRO - VITALÍCIO")
        lbl_plan_name.setStyleSheet("font-size: 15px; font-weight: bold;")

        lbl_status = QLabel("● ATIVO")
        lbl_status.setStyleSheet("color: #00E676; font-weight: bold; font-size: 12px;")

        header_active.addWidget(lbl_plan_name)
        header_active.addStretch()
        header_active.addWidget(lbl_status)
        ca_layout.addLayout(header_active)

        # Detalhes HWID e Key
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)

        fields = [
            ("CHAVE DE LICENÇA", "PRT-PRO-9988-XXXX-7711"),
            ("HARDWARE ID (HWID)", "HWID-A8F2-99C1-4B02"),
            ("EXPIRA EM", "Nunca (Acesso Vitalício)"),
            ("CONEXÕES SIMULTÂNEAS", "Unlimited / Ilimitado"),
        ]

        for title, val in fields:
            box = QFrame()
            box.setObjectName("cardFrame")
            b_layout = QVBoxLayout(box)
            b_layout.setContentsMargins(10, 8, 10, 8)

            lbl_t = QLabel(title)
            lbl_t.setStyleSheet("color: #8E8E93; font-size: 10px; font-weight: bold;")
            lbl_v = QLabel(val)
            lbl_v.setStyleSheet("font-size: 12px; font-weight: bold;")

            b_layout.addWidget(lbl_t)
            b_layout.addWidget(lbl_v)
            info_layout.addWidget(box)

        ca_layout.addLayout(info_layout)
        layout.addWidget(card_active)

        # Card de Ativação
        card_activate = QFrame()
        card_activate.setObjectName("cardFrame")
        cact_layout = QVBoxLayout(card_activate)
        cact_layout.setContentsMargins(15, 15, 15, 15)
        cact_layout.setSpacing(10)

        lbl_act_title = QLabel("⚡ Ativar ou Renovar Licença")
        lbl_act_title.setStyleSheet("font-weight: bold; font-size: 13px;")

        act_form = QHBoxLayout()
        self.txt_key = QLineEdit()
        self.txt_key.setPlaceholderText("Insira sua chave de licença (Ex: PRT-NEXUS-XXXX-XXXX-XXXX)")

        btn_valid = QPushButton("Validar e Ativar Key")
        btn_valid.setCursor(Qt.PointingHandCursor)

        act_form.addWidget(self.txt_key, stretch=4)
        act_form.addWidget(btn_valid, stretch=1)

        cact_layout.addWidget(lbl_act_title)
        cact_layout.addLayout(act_form)
        layout.addWidget(card_activate)

        # Planos
        lbl_plans_title = QLabel("🚀 Conheça os Planos PRT NEXUS")
        lbl_plans_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(lbl_plans_title)

        plans_layout = QHBoxLayout()
        plans_layout.setSpacing(12)

        plans_data = [
            ("PRT STARTER", "R$ 47 /mês", ["✔ 1 Conexão Simultânea", "✔ Downloads até 1080p", "✔ Suporte Comunitário"]),
            ("PRT PRO", "R$ 97 /mês", ["✔ 3 Conexões Simultâneas", "✔ Downloads 4K Ultra HD", "✔ Sniffer Avançado HLS/M3U8"]),
            ("PRT ENTERPRISE", "R$ 297 /único", ["✔ Conexões Ilimitadas", "✔ Todas as funções PRO liberadas", "✔ Atualizações Vitalícias"]),
        ]

        for p_name, p_price, p_features in plans_data:
            p_card = QFrame()
            p_card.setObjectName("cardFrame")
            p_layout = QVBoxLayout(p_card)
            p_layout.setContentsMargins(15, 15, 15, 15)
            p_layout.setSpacing(10)

            lbl_pn = QLabel(p_name)
            lbl_pn.setStyleSheet("font-size: 14px; font-weight: bold;")

            lbl_pp = QLabel(p_price)
            lbl_pp.setStyleSheet("font-size: 18px; font-weight: bold; color: #6366F1;")

            p_layout.addWidget(lbl_pn)
            p_layout.addWidget(lbl_pp)

            for feat in p_features:
                lbl_f = QLabel(feat)
                lbl_f.setStyleSheet("font-size: 12px;")
                p_layout.addWidget(lbl_f)

            p_layout.addStretch()
            plans_layout.addWidget(p_card)

        layout.addLayout(plans_layout)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)