"""
===========================================================
PRT Labs - UI / Pages
Class: ConnectorPage

Description:
    Tela genérica e dinâmica para gerenciamento individual
    de cada Conector (YouTube, Kiwify, Hotmart, Vimeo, 
    Google Drive, Mega, etc.).
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ConnectorPage(QWidget):
    """Página detalhada de controle e extração de um Conector específico."""

    CONNECTORS_CONFIG = {
        "youtube": {
            "name": "YouTube",
            "category": "Player & Streaming",
            "icon": "▶️",
            "color": "#FF0000",
            "default_url": "https://www.youtube.com",
            "desc": "Conector para extração de vídeos públicos, não listados, playlists e transmissões.",
            "placeholder": "Cole a URL do vídeo ou playlist do YouTube...",
            "status": "Conectado",
        },
        "kiwify": {
            "name": "Kiwify",
            "category": "Área de Membros / Cursos",
            "icon": "🟢",
            "color": "#22C55E",
            "default_url": "https://dashboard.kiwify.com.br",
            "desc": "Conector automático para áreas de membros Kiwify e Nutror com suporte a HLS e M3U8.",
            "placeholder": "Cole a URL do curso ou aula da Kiwify...",
            "status": "Conectado",
        },
        "hotmart": {
            "name": "Hotmart",
            "category": "Área de Membros / Cursos",
            "icon": "🔥",
            "color": "#F97316",
            "default_url": "https://club.hotmart.com",
            "desc": "Mapeador e extrator completo para Hotmart Club v3, vídeos embutidos e anexos.",
            "placeholder": "Cole a URL da área de alunos do Hotmart Club...",
            "status": "Conectado",
        },
        "vimeo": {
            "name": "Vimeo",
            "category": "Player HLS / Privado",
            "icon": "🔹",
            "color": "#00ADEF",
            "default_url": "https://vimeo.com",
            "desc": "Decodificador de vídeos privados do Vimeo, M3U8 master playlist e chaves HLS.",
            "placeholder": "Cole a URL do vídeo Vimeo ou player embutido...",
            "status": "Standby",
        },
        "google_drive": {
            "name": "Google Drive",
            "category": "Armazenamento em Nuvem",
            "icon": "🔺",
            "color": "#EA4335",
            "default_url": "https://drive.google.com",
            "desc": "Download de arquivos grandes, pastas inteiras e mídias hospedadas no Google Drive.",
            "placeholder": "Cole o link da pasta ou arquivo do Google Drive...",
            "status": "Standby",
        },
        "mega": {
            "name": "Mega",
            "category": "Armazenamento em Nuvem",
            "icon": "🔴",
            "color": "#D9252A",
            "default_url": "https://mega.nz",
            "desc": "Extrator e gerenciador de downloads para links e pastas do Mega.nz.",
            "placeholder": "Cole a URL de download ou pasta do Mega...",
            "status": "Standby",
        },
    }

    def __init__(self, platform_key: str = "youtube", parent=None) -> None:
        super().__init__(parent)
        self.platform_key = platform_key.lower().replace("-", "_")
        self.config = self.CONNECTORS_CONFIG.get(
            self.platform_key,
            {
                "name": platform_key.capitalize(),
                "category": "Conector Personalizado",
                "icon": "⚡",
                "color": "#6366F1",
                "default_url": "https://google.com",
                "desc": "Gerenciamento e captura de mídias para esta plataforma.",
                "placeholder": "Cole a URL para extração...",
                "status": "Desconhecido",
            },
        )

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
        """
        )

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(20)

        # 1. Cabeçalho do Conector
        container_layout.addWidget(self._create_header_card())

        # 2. Extrator Direto por Link
        container_layout.addWidget(self._create_extractor_card())

        # 3. Painel de Autenticação / Configuração
        container_layout.addWidget(self._create_auth_card())

        # 4. Tabela de Mídias Detectadas / Histórico
        container_layout.addWidget(self._create_history_card())

        container_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _create_header_card(self) -> QFrame:
        """Cria o card de apresentação do conector com ações rápidas."""
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
        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        lbl_icon = QLabel(self.config["icon"])
        lbl_icon.setStyleSheet("font-size: 32px;")

        v_info = QVBoxLayout()
        v_info.setSpacing(4)

        lbl_name = QLabel(f"{self.config['name']} Conector")
        lbl_name.setStyleSheet("color: #FFFFFF; font-size: 20px; font-weight: bold;")

        lbl_desc = QLabel(f"{self.config['category']} • {self.config['desc']}")
        lbl_desc.setStyleSheet("color: #A1A1AA; font-size: 13px;")

        v_info.addWidget(lbl_name)
        v_info.addWidget(lbl_desc)

        # Badges & Botão de Abrir no Navegador
        v_actions = QVBoxLayout()
        v_actions.setSpacing(8)
        v_actions.setAlignment(Qt.AlignRight)

        status_str = self.config["status"]
        is_conn = status_str == "Conectado"
        bg_status = "rgba(34, 197, 94, 0.15)" if is_conn else "rgba(234, 179, 8, 0.15)"
        border_status = "#22C55E" if is_conn else "#EAB308"
        text_status = "#22C55E" if is_conn else "#EAB308"

        lbl_badge = QLabel(f" ● {status_str.upper()} ")
        lbl_badge.setStyleSheet(
            f"""
            QLabel {{
                background-color: {bg_status};
                color: {text_status};
                font-weight: bold;
                font-size: 11px;
                padding: 4px 10px;
                border-radius: 10px;
                border: 1px solid {border_status};
            }}
        """
        )

        btn_open_browser = QPushButton("🌐 Abrir no Navegador PRT")
        btn_open_browser.setStyleSheet(
            """
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                font-weight: bold;
                font-size: 12px;
                padding: 8px 14px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """
        )

        v_actions.addWidget(lbl_badge, alignment=Qt.AlignRight)
        v_actions.addWidget(btn_open_browser)

        layout.addWidget(lbl_icon)
        layout.addLayout(v_info, stretch=1)
        layout.addLayout(v_actions)

        return card

    def _create_extractor_card(self) -> QFrame:
        """Cria a seção para inserção direta de link para extração."""
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

        lbl_title = QLabel("⚡ Analisador & Extrator Rápido de Mídias")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")

        h_input = QHBoxLayout()
        h_input.setSpacing(10)

        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText(self.config["placeholder"])
        self.txt_url.setStyleSheet(
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

        btn_analyze = QPushButton("🔍 Capturar Mídia")
        btn_analyze.setStyleSheet(
            """
            QPushButton {
                background-color: #22C55E;
                color: #FFFFFF;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #16A34A;
            }
        """
        )

        h_input.addWidget(self.txt_url, stretch=1)
        h_input.addWidget(btn_analyze)

        layout.addWidget(lbl_title)
        layout.addLayout(h_input)

        return card

    def _create_auth_card(self) -> QFrame:
        """Cria o painel para gerenciar cookies de sessão / credenciais do conector."""
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

        lbl_title = QLabel("🔐 Autenticação & Sessão (Session Cookies)")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")

        lbl_desc = QLabel(
            "Caso a plataforma exija login para acessar o conteúdo privado, "
            "o PRT NEXUS sincroniza os cookies automaticamente através do navegador embutido."
        )
        lbl_desc.setStyleSheet("color: #A1A1AA; font-size: 12px;")

        h_actions = QHBoxLayout()
        h_actions.setSpacing(10)

        btn_sync = QPushButton("🔄 Sincronizar Cookies do Navegador")
        btn_sync.setStyleSheet(
            """
            QPushButton {
                background-color: #27272A;
                color: #FFFFFF;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3F3F46;
            }
        """
        )

        btn_test = QPushButton("⚡ Testar Conexão de Sessão")
        btn_test.setStyleSheet(
            """
            QPushButton {
                background-color: #27272A;
                color: #A1A1AA;
                border-radius: 6px;
                padding: 8px 14px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3F3F46;
                color: #FFFFFF;
            }
        """
        )

        h_actions.addWidget(btn_sync)
        h_actions.addWidget(btn_test)
        h_actions.addStretch()

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_desc)
        layout.addLayout(h_actions)

        return card

    def _create_history_card(self) -> QFrame:
        """Cria o card com a tabela de capturas recentes desta plataforma."""
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

        lbl_title = QLabel("📦 Mídias Recentes Capturadas neste Conector")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 15px; font-weight: bold;")

        table = QTableWidget(3, 4)
        table.setHorizontalHeaderLabels(["Título / Nome do Arquivo", "Qualidade / Formato", "Tamanho Est.", "Ação"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        table.verticalHeader().setVisible(False)
        table.setMinimumHeight(150)

        table.setStyleSheet(
            """
            QTableWidget {
                background-color: #0E0F12;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 8px;
                gridline-color: #18181B;
            }
            QHeaderView::section {
                background-color: #18181B;
                color: #A1A1AA;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """
        )

        demo_data = [
            (f"Vídeo de Exemplo {self.config['name']} #01", "1080p (MP4/HLS)", "450 MB"),
            (f"Material Complementar {self.config['name']} #02", "720p (MP4)", "120 MB"),
            (f"Transmissão Gravada {self.config['name']} #03", "4K Ultra HD", "1.2 GB"),
        ]

        for row, (name, qual, size) in enumerate(demo_data):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(qual))
            table.setItem(row, 2, QTableWidgetItem(size))

            btn_dl = QPushButton("⬇️ Baixar")
            btn_dl.setStyleSheet(
                """
                QPushButton {
                    background-color: #6366F1;
                    color: #FFFFFF;
                    border-radius: 4px;
                    padding: 4px 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4F46E5;
                }
            """
            )
            table.setCellWidget(row, 3, btn_dl)

        layout.addWidget(lbl_title)
        layout.addWidget(table)

        return card