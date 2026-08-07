"""
===========================================================
PRT Labs - UI / Browser Page
Class: BrowserPage

Description:
    Tela do Navegador Integrado do PRT NEXUS com barra de
    endereço, controles de navegação, botão de análise de 
    módulos e painel de captura de vídeos em tempo real.
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
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from ui.pages.base_page import BasePage
from ui.dialogs.course_mapper_dialog import CourseMapperDialog


class BrowserPage(BasePage):
    """Página do Navegador Integrado com painel de captura de mídias."""

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # 1. Topo - Barra de Controle do Navegador
        layout.addWidget(self._create_top_bar())

        # 2. Divisor Central (Área da Web + Painel do Sniffer/Fila)
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(4)
        splitter.setStyleSheet("QSplitter::handle { background-color: #27272A; }")

        # 2.1 Viewport Web Placeholder (Onde rodará o WebEngine)
        web_placeholder = QFrame()
        web_placeholder.setStyleSheet(
            """
            QFrame {
                background-color: #0E0F12;
                border: 1px solid #27272A;
                border-radius: 8px;
            }
        """
        )
        web_layout = QVBoxLayout(web_placeholder)
        web_layout.setAlignment(Qt.AlignCenter)

        lbl_web_info = QLabel("🌐 Área do Navegador Integrado\n(O conteúdo da aula/plataforma carregará aqui)")
        lbl_web_info.setAlignment(Qt.AlignCenter)
        lbl_web_info.setStyleSheet("color: #71717A; font-size: 16px; font-weight: 500;")
        web_layout.addWidget(lbl_web_info)

        splitter.addWidget(web_placeholder)

        # 2.2 Painel Inferior: Mídias Detectadas & Módulos
        splitter.addWidget(self._create_sniffer_panel())

        # Proporção inicial: 65% Web, 35% Painel Sniffer
        splitter.setSizes([500, 250])

        layout.addWidget(splitter)

    def _create_top_bar(self) -> QFrame:
        """Cria a barra superior de navegação estilo Google Chrome / STREAB."""
        bar = QFrame()
        bar.setStyleSheet(
            """
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 8px;
            }
        """
        )
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Botões de Navegação
        btn_back = QPushButton("◄")
        btn_forward = QPushButton("►")
        btn_reload = QPushButton("🔄")

        for btn in (btn_back, btn_forward, btn_reload):
            btn.setFixedSize(32, 32)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #27272A;
                    color: #FFFFFF;
                    border-radius: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3F3F46;
                }
            """
            )

        layout.addWidget(btn_back)
        layout.addWidget(btn_forward)
        layout.addWidget(btn_reload)

        # Campo de URL
        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText("Cole o link do curso ou navegue até a aula...")
        self.txt_url.setStyleSheet(
            """
            QLineEdit {
                background-color: #0E0F12;
                color: #FFFFFF;
                border: 1px solid #3F3F46;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #6366F1;
            }
        """
        )
        layout.addWidget(self.txt_url, stretch=1)

        # Botão de Ação Especial: Analisar Módulos do Curso
        btn_scan_modules = QPushButton("⚡ Mapear Curso / Módulos")
        btn_scan_modules.setStyleSheet(
            """
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
        """
        )
        btn_scan_modules.clicked.connect(self._open_course_mapper)
        layout.addWidget(btn_scan_modules)

        return bar

    def _open_course_mapper(self) -> None:
        """Abre o modal interativo para selecionar módulos e aulas em lote."""
        dialog = CourseMapperDialog(self)
        if dialog.exec():
            print("[PRT NEXUS] Aulas do curso adicionadas com sucesso à fila de downloads!")

    def _create_sniffer_panel(self) -> QFrame:
        """Cria o painel inferior de detecção automática de vídeos e fila."""
        panel = QFrame()
        panel.setStyleSheet(
            """
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 8px;
            }
        """
        )
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        top_layout = QHBoxLayout()
        lbl_title = QLabel("📡 Detecção de Mídias em Tempo Real")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 14px; font-weight: bold;")

        btn_add_queue = QPushButton("+ Adicionar Selecionados à Fila")
        btn_add_queue.setStyleSheet(
            """
            QPushButton {
                background-color: #22C55E;
                color: #FFFFFF;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #16A34A;
            }
        """
        )

        top_layout.addWidget(lbl_title)
        top_layout.addStretch()
        top_layout.addWidget(btn_add_queue)
        layout.addLayout(top_layout)

        table = QTableWidget(0, 4)
        table.setHorizontalHeaderLabels(["Módulo / Aula", "Tipo / Player", "Qualidade", "Ação"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        table.setStyleSheet(
            """
            QTableWidget {
                background-color: #0E0F12;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 6px;
                gridline-color: #27272A;
            }
            QHeaderView::section {
                background-color: #18181B;
                color: #A1A1AA;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
        """
        )

        demo_data = [
            ("Módulo 01 - Aula 01: Apresentação do Curso", "Vimeo / HLS", "1080p (Alta)"),
            ("Módulo 01 - Aula 02: Instalando as Ferramentas", "Panda Video", "720p (Média)"),
            ("Módulo 02 - Aula 01: Criando a Primeira Estrutura", "M3U8 Stream", "1080p (Alta)"),
        ]

        for row, (aula, tipo, qual) in enumerate(demo_data):
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(aula))
            table.setItem(row, 1, QTableWidgetItem(tipo))
            table.setItem(row, 2, QTableWidgetItem(qual))

            btn_download = QPushButton("Baixar")
            btn_download.setStyleSheet(
                "background-color: #6366F1; color: white; border-radius: 4px; padding: 4px 8px;"
            )
            table.setCellWidget(row, 3, btn_download)

        layout.addWidget(table)
        return panel