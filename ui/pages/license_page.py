"""
===========================================================
PRT Labs - UI / Pages
Class: LicensePage

Description:
    Tela de Gestão de Licença e Planos do PRT NEXUS.
    Exibe os detalhes da licença ativa, campo para ativação/renovação
    de chaves de licença, ID da máquina (HWID) e cartões de planos.
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
    """Página de Gerenciamento de Licenças e Assinatura do Usuário."""

    def __init__(self) -> None:
        super().__init__()

        # Layout Principal com Scroll Area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: #0E0F12;
                border: none;
            }
            QScrollBar:vertical {
                background: #121318;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #27272A;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #3F3F46;
            }
        """
        )

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(20)

        # 1. Cabeçalho da Página
        container_layout.addLayout(self._create_header())

        # 2. Card de Status da Licença Atual
        container_layout.addWidget(self._create_active_license_card())

        # 3. Card de Ativação de Nova Chave (Redeem Key)
        container_layout.addWidget(self._create_activation_card())

        # 4. Seção de Planos e Upgrades
        container_layout.addLayout(self._create_plans_section())

        container_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _create_header(self) -> QVBoxLayout:
        """Cria o cabeçalho da página."""
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        lbl_title = QLabel("🔑 Minha Licença & Planos")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")

        lbl_subtitle = QLabel("Gerencie seu plano ativo, chave de licença, HWID e opções de renovação.")
        lbl_subtitle.setStyleSheet("color: #A1A1AA; font-size: 14px;")

        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_subtitle)

        return header_layout

    def _create_active_license_card(self) -> QFrame:
        """Cria o card contendo as informações da licença atual em uso."""
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 12px;
            }
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Topo do Card: Plano + Status Badge
        top_layout = QHBoxLayout()

        lbl_plan_title = QLabel("👑 PRT NEXUS PRO - VITALÍCIO")
        lbl_plan_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold;")

        lbl_status = QLabel(" ● ATIVO ")
        lbl_status.setStyleSheet(
            """
            QLabel {
                background-color: rgba(34, 197, 94, 0.15);
                color: #22C55E;
                font-weight: bold;
                font-size: 12px;
                padding: 4px 10px;
                border-radius: 10px;
                border: 1px solid #22C55E;
            }
        """
        )

        top_layout.addWidget(lbl_plan_title)
        top_layout.addStretch()
        top_layout.addWidget(lbl_status)
        layout.addLayout(top_layout)

        # Linha Divisória
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #27272A; max-height: 1px;")
        layout.addWidget(line)

        # Grid de Informações
        info_layout = QHBoxLayout()
        info_layout.setSpacing(20)

        def make_info_box(title: str, value: str) -> QVBoxLayout:
            vbox = QVBoxLayout()
            vbox.setSpacing(4)
            t = QLabel(title)
            t.setStyleSheet("color: #71717A; font-size: 12px; font-weight: bold;")
            v = QLabel(value)
            v.setStyleSheet("color: #E4E4E7; font-size: 14px; font-weight: 500;")
            vbox.addWidget(t)
            vbox.addWidget(v)
            return vbox

        info_layout.addLayout(make_info_box("CHAVE DE LICENÇA", "PRT-PRO-9988-XXXX-7711"))
        info_layout.addLayout(make_info_box("HARDWARE ID (HWID)", "HWID-A8F2-99C1-4B02"))
        info_layout.addLayout(make_info_box("EXPIRA EM", "Nunca (Acesso Vitalício)"))
        info_layout.addLayout(make_info_box("CONEXÕES SIMULTÂNEAS", "Unlimited / Ilimitado"))

        layout.addLayout(info_layout)

        return card

    def _create_activation_card(self) -> QFrame:
        """Cria a seção para inserir e validar novas chaves de licença."""
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 12px;
            }
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        lbl_section = QLabel("⚡ Ativar ou Renovar Licença")
        lbl_section.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.txt_key = QLineEdit()
        self.txt_key.setPlaceholderText("Insira sua chave de licença (Ex: PRT-NEXUS-XXXX-XXXX-XXXX)")
        self.txt_key.setStyleSheet(
            """
            QLineEdit {
                background-color: #0E0F12;
                color: #FFFFFF;
                border: 1px solid #3F3F46;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #6366F1;
            }
        """
        )

        btn_activate = QPushButton(" Validar & Ativar Key ")
        btn_activate.setStyleSheet(
            """
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """
        )
        btn_activate.clicked.connect(self._on_activate_clicked)

        input_layout.addWidget(self.txt_key, stretch=1)
        input_layout.addWidget(btn_activate)

        layout.addWidget(lbl_section)
        layout.addLayout(input_layout)

        return card

    def _create_plans_section(self) -> QVBoxLayout:
        """Cria o grid comparativo de planos do PRT NEXUS."""
        plans_vbox = QVBoxLayout()
        plans_vbox.setSpacing(12)

        lbl_section = QLabel("🚀 Conheça os Planos PRT NEXUS")
        lbl_section.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold;")
        plans_vbox.addWidget(lbl_section)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)

        plans_data = [
            {
                "name": "PRT STARTER",
                "price": "R$ 47 /mês",
                "desc": "Ideal para iniciantes no uso do gerenciador.",
                "features": ["1 Conexão Simultânea", "Downloads até 1080p", "Suporte Comunitário"],
                "highlight": False,
                "btn_text": "Fazer Upgrade",
            },
            {
                "name": "PRT PRO",
                "price": "R$ 97 /mês",
                "desc": "O plano ideal para criadores e produtores.",
                "features": [
                    "3 Conexões Simultâneas",
                    "Downloads 4K Ultra HD",
                    "Sniffer Avançado HLS/M3U8",
                    "Mapeador Automático de Cursos",
                    "Suporte Prioritário VIP",
                ],
                "highlight": True,
                "btn_text": "Plano Atual",
            },
            {
                "name": "PRT ENTERPRISE",
                "price": "R$ 297 /único",
                "desc": "Acesso Vitalício completo para equipes e agências.",
                "features": [
                    "Conexões Ilimitadas",
                    "Todas as funções PRO liberadas",
                    "Atualizações Vitalícias",
                    "Acesso Direto aos Desenvolvedores",
                ],
                "highlight": False,
                "btn_text": "Obter Vitalício",
            },
        ]

        for p in plans_data:
            cards_layout.addWidget(self._build_plan_card(p))

        plans_vbox.addLayout(cards_layout)
        return plans_vbox

    def _build_plan_card(self, data: dict) -> QFrame:
        """Constrói o widget de um cartão individual de plano."""
        card = QFrame()
        border_color = "#6366F1" if data["highlight"] else "#27272A"
        bg_color = "#121318" if not data["highlight"] else "#18181B"

        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
            }}
        """
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        if data["highlight"]:
            lbl_badge = QLabel(" RECOMENDADO ")
            lbl_badge.setAlignment(Qt.AlignCenter)
            lbl_badge.setStyleSheet(
                """
                background-color: #6366F1;
                color: #FFFFFF;
                font-weight: bold;
                font-size: 10px;
                padding: 3px 8px;
                border-radius: 8px;
            """
            )
            layout.addWidget(lbl_badge, alignment=Qt.AlignRight)

        lbl_name = QLabel(data["name"])
        lbl_name.setStyleSheet("color: #FFFFFF; font-size: 16px; font-weight: bold;")

        lbl_price = QLabel(data["price"])
        lbl_price.setStyleSheet("color: #6366F1; font-size: 20px; font-weight: bold;")

        lbl_desc = QLabel(data["desc"])
        lbl_desc.setStyleSheet("color: #A1A1AA; font-size: 12px;")
        lbl_desc.setWordWrap(True)

        layout.addWidget(lbl_name)
        layout.addWidget(lbl_price)
        layout.addWidget(lbl_desc)

        # Divisor
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #27272A; max-height: 1px;")
        layout.addWidget(line)

        # Lista de Recursos
        v_feat = QVBoxLayout()
        v_feat.setSpacing(6)

        for feat in data["features"]:
            lbl_f = QLabel(f"✓ {feat}")
            lbl_f.setStyleSheet("color: #D4D4D8; font-size: 12px;")
            v_feat.addWidget(lbl_f)

        layout.addLayout(v_feat)
        layout.addStretch()

        btn = QPushButton(data["btn_text"])
        btn_style = (
            """
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """
            if data["highlight"]
            else """
            QPushButton {
                background-color: #27272A;
                color: #A1A1AA;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3F3F46;
                color: #FFFFFF;
            }
        """
        )
        btn.setStyleSheet(btn_style)
        layout.addWidget(btn)

        return card

    def _on_activate_clicked(self) -> None:
        """Handler do botão de validação de licença."""
        key = self.txt_key.text().strip()
        if key:
            print(f"[PRT NEXUS] Tentando validar chave: {key}")
            self.txt_key.clear()
            self.txt_key.setPlaceholderText("✅ Licença validada com sucesso!")