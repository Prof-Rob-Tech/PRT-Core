"""
===========================================================
PRT Labs - UI / Pages
Class: DashboardPage
Description: Dashboard Principal do PRT NEXUS adaptável a temas.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class DashboardPage(QWidget):
    """Página Dashboard / Início do PRT NEXUS."""

    def __init__(self, parent=None, on_navigate=None) -> None:
        super().__init__(parent)
        self.on_navigate_callback = on_navigate
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
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        # ------------------------------------------------------------------
        # 1. Cabeçalho
        # ------------------------------------------------------------------
        title_layout = QVBoxLayout()
        title_layout.setSpacing(6)

        lbl_title = QLabel("Dashboard PRT Nexus")
        lbl_title.setStyleSheet("font-size: 24px; font-weight: bold;")

        # Subtítulo com tamanho aumentado para 15px
        lbl_subtitle = QLabel("Central de download, extração de mídias e gestão de conectores.")
        lbl_subtitle.setStyleSheet("color: #B0B0BB; font-size: 15px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        layout.addLayout(title_layout)

        # ------------------------------------------------------------------
        # 2. Cards de Status (com bloco de cor separado)
        # ------------------------------------------------------------------
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(14)

        stats = [
            ("Conectores", "8 Módulos Prontos", "#00E676"),
            ("Downloads Ativos", "0 em andamento", "#6366F1"),
            ("Mídias Salvas", "0 arquivos", "#FF9800"),
            ("Sistema Core", "100% Operacional", "#00F0FF"),
        ]

        for title, value, border_color in stats:
            card = QFrame()
            card.setObjectName("statCardFrame")
            card.setStyleSheet("""
                QFrame#statCardFrame {
                    background-color: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 10px;
                }
                QFrame#statCardFrame:hover {
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(255, 255, 255, 0.15);
                }
            """)

            card_h_layout = QHBoxLayout(card)
            card_h_layout.setContentsMargins(0, 0, 0, 0)
            card_h_layout.setSpacing(0)

            # Barra de cor lateral sem artefatos visuais
            color_bar = QFrame()
            color_bar.setFixedWidth(14)
            color_bar.setStyleSheet(f"""
                background-color: {border_color};
                border-top-left-radius: 9px;
                border-bottom-left-radius: 9px;
                border: none;
            """)
            card_h_layout.addWidget(color_bar)

            # Conteúdo
            content_widget = QWidget()
            content_widget.setStyleSheet("background: transparent; border: none;")
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(16, 14, 16, 14)
            content_layout.setSpacing(6)

            lbl_t = QLabel(title)
            lbl_t.setStyleSheet("color: #C0C0CB; font-size: 13px; font-weight: bold; text-transform: uppercase;")

            lbl_v = QLabel(value)
            lbl_v.setStyleSheet("font-size: 17px; font-weight: bold;")

            content_layout.addWidget(lbl_t)
            content_layout.addWidget(lbl_v)

            card_h_layout.addWidget(content_widget, 1)
            stats_layout.addWidget(card)

        layout.addLayout(stats_layout)

        # ------------------------------------------------------------------
        # 3. Seção Conectores
        # ------------------------------------------------------------------
        lbl_sec = QLabel("Atalhos Rápidos de Conectores")
        lbl_sec.setStyleSheet("font-size: 17px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(lbl_sec)

        grid = QGridLayout()
        grid.setSpacing(14)

        connectors = [
            ("Navegador Web", "Navegar e extrair URLs direto de sites", "navegador"),
            ("Downloads", "Ver gerenciador e histórico de downloads", "downloads"),
            ("YouTube", "Download de vídeos, playlists e áudio", "conn_youtube"),
            ("TikTok", "Extrair vídeos e Reels sem marca d'água", "conn_tiktok"),
            ("Kiwify", "Acessar conteúdos da plataforma Kiwify", "conn_kiwify"),
            ("Hotmart", "Acessar áreas de membros da Hotmart", "conn_hotmart"),
            ("Google Drive", "Baixar arquivos e pastas do Drive", "conn_gdrive"),
            ("Universo Técnico", "Extrair aulas do Universo Técnico", "conn_universo"),
        ]

        card_style = """
            QFrame#connectorCard {
                background-color: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.07);
                border-radius: 10px;
            }
            QFrame#connectorCard:hover {
                border: 1px solid rgba(0, 240, 255, 0.35);
                background-color: rgba(255, 255, 255, 0.04);
            }
        """

        btn_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 6px;
                padding: 7px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #00F0FF;
                color: #000000;
                border: 1px solid #00F0FF;
            }
        """

        row, col = 0, 0
        for name, desc, route in connectors:
            card = QFrame()
            card.setObjectName("connectorCard")
            card.setStyleSheet(card_style)

            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(16, 16, 16, 16)

            lbl_n = QLabel(name)
            lbl_n.setStyleSheet("font-size: 14px; font-weight: bold;")

            lbl_d = QLabel(desc)
            lbl_d.setStyleSheet("color: #A0A0AB; font-size: 12px;")
            lbl_d.setWordWrap(True)

            btn = QPushButton("Acessar Módulo →")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(btn_style)
            btn.clicked.connect(lambda _, r=route: self._navigate(r))

            c_layout.addWidget(lbl_n)
            c_layout.addWidget(lbl_d)
            c_layout.addSpacing(10)
            c_layout.addWidget(btn)

            grid.addWidget(card, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        layout.addLayout(grid)
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _navigate(self, route: str) -> None:
        if callable(self.on_navigate_callback):
            self.on_navigate_callback(route)