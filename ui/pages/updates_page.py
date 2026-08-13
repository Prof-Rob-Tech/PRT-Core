"""
===========================================================
PRT Labs - UI / Pages
Class: UpdatesPage

Description:
    Página de Gerenciamento de Atualizações do PRT NEXUS,
    motores de extração (yt-dlp/ffmpeg) e Changelog.
===========================================================
"""

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

CHANGELOG_DATA = [
    {
        "version": "v0.1.0-alpha",
        "date": "13/08/2026",
        "tag": "Atual",
        "changes": [
            "✨ Lançamento da nova UI do Gerenciador de Plugins.",
            "🐛 Correção no fechamento para a bandeja do sistema (Tray Icon).",
            "⚡ Suporte a múltiplos temas (Dark, Light, Cyber).",
            "🌐 Conectores integrados para Kiwify, Hotmart, Vimeo e YouTube.",
        ],
    },
    {
        "version": "v0.0.9-alpha",
        "date": "01/08/2026",
        "tag": "Anterior",
        "changes": [
            "🚀 Mapeamento e captura HLS para Panda Video.",
            "🛠️ Sistema de download em segundo plano reestruturado.",
            "🔒 Melhorias na validação de licenças.",
        ],
    },
]

ENGINES_DATA = [
    {
        "id": "ytdlp",
        "name": "Core Extractor (yt-dlp)",
        "version": "2026.08.01",
        "status": "● Atualizado",
    },
    {
        "id": "ffmpeg",
        "name": "Media Converter (FFmpeg)",
        "version": "n6.1.1",
        "status": "● Atualizado",
    },
    {
        "id": "chromium",
        "name": "Browser Engine (Chromium Core)",
        "version": "v126.0",
        "status": "● Atualizado",
    },
]


class UpdatesPage(QWidget):
    """Página de Atualizações do PRT NEXUS."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # --- ÁREA COM SCROLL ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical {
                background-color: #09090B; width: 8px; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #27272A; border-radius: 4px;
            }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(0, 0, 10, 0)
        content_layout.setSpacing(20)

        # --- CABEÇALHO DA PÁGINA ---
        header_layout = QVBoxLayout()
        header_layout.setSpacing(6)

        title_layout = QHBoxLayout()
        title_icon = QLabel("🔄")
        title_icon.setStyleSheet("font-size: 22px;")
        title_lbl = QLabel("Central de Atualizações")
        title_lbl.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #FFFFFF;"
        )

        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_lbl)
        title_layout.addStretch()

        subtitle_lbl = QLabel(
            "Mantenha o PRT NEXUS e seus motores de extração sempre atualizados para garantir compatibilidade."
        )
        subtitle_lbl.setStyleSheet("font-size: 13px; color: #71717A;")

        header_layout.addLayout(title_layout)
        header_layout.addWidget(subtitle_lbl)
        content_layout.addLayout(header_layout)

        # --- HERO CARD (STATUS PRINCIPAL) ---
        self.hero_card = QFrame()
        self.hero_card.setStyleSheet("""
            QFrame {
                background: QLinearGradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #121215, stop: 1 #181824);
                border: 1px solid #27272A;
                border-radius: 12px;
            }
        """)
        hero_layout = QVBoxLayout(self.hero_card)
        hero_layout.setContentsMargins(20, 20, 20, 20)
        hero_layout.setSpacing(14)

        top_hero = QHBoxLayout()

        status_box = QVBoxLayout()
        status_box.setSpacing(4)

        self.lbl_app_version = QLabel("PRT NEXUS v0.1.0-alpha")
        self.lbl_app_version.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #FFFFFF;"
        )

        self.lbl_status_msg = QLabel(
            "● O seu aplicativo está atualizado na versão mais recente."
        )
        self.lbl_status_msg.setStyleSheet(
            "font-size: 13px; color: #22C55E; font-weight: 500;"
        )

        status_box.addWidget(self.lbl_app_version)
        status_box.addWidget(self.lbl_status_msg)
        top_hero.addLayout(status_box)

        top_hero.addStretch()

        self.btn_check_updates = QPushButton("🔍 Verificar Atualizações")
        self.btn_check_updates.setCursor(Qt.PointingHandCursor)
        self.btn_check_updates.setStyleSheet("""
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
            QPushButton:disabled {
                background-color: #3F3F46;
                color: #71717A;
            }
        """)
        self.btn_check_updates.clicked.connect(self._simulate_check_updates)
        top_hero.addWidget(self.btn_check_updates)

        hero_layout.addLayout(top_hero)

        # Barra de Progresso (Invisível por padrão)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #27272A;
                border-radius: 3px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #6366F1;
                border-radius: 3px;
            }
        """)
        self.progress_bar.hide()
        hero_layout.addWidget(self.progress_bar)

        content_layout.addWidget(self.hero_card)

        # --- SEÇÃO DE MOTORES E COMPONENTES ---
        engines_title = QLabel("⚙️ Motores & Componentes de Download")
        engines_title.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #8E8E93; text-transform: uppercase;"
        )
        content_layout.addWidget(engines_title)

        engines_card = QFrame()
        engines_card.setStyleSheet("""
            QFrame {
                background-color: #121215;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
        """)
        engines_layout = QVBoxLayout(engines_card)
        engines_layout.setContentsMargins(16, 12, 16, 12)
        engines_layout.setSpacing(10)

        for eng in ENGINES_DATA:
            row = QHBoxLayout()
            row.setContentsMargins(4, 6, 4, 6)

            eng_name = QLabel(eng["name"])
            eng_name.setStyleSheet(
                "font-size: 13px; font-weight: bold; color: #FFFFFF;"
            )

            eng_ver = QLabel(f"Versão: {eng['version']}")
            eng_ver.setStyleSheet("font-size: 12px; color: #71717A;")

            status_pill = QLabel(eng["status"])
            status_pill.setStyleSheet("""
                background-color: rgba(34, 197, 94, 0.1);
                color: #22C55E;
                border: 1px solid rgba(34, 197, 94, 0.2);
                border-radius: 10px;
                padding: 3px 8px;
                font-size: 11px;
                font-weight: bold;
            """)

            btn_update_engine = QPushButton("Atualizar Engine")
            btn_update_engine.setCursor(Qt.PointingHandCursor)
            btn_update_engine.setStyleSheet("""
                QPushButton {
                    background-color: #18181B;
                    color: #D4D4D8;
                    border: 1px solid #3F3F46;
                    border-radius: 6px;
                    padding: 5px 12px;
                    font-size: 11px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #27272A;
                    color: #FFFFFF;
                    border-color: #6366F1;
                }
            """)

            row.addWidget(eng_name)
            row.addWidget(eng_ver)
            row.addStretch()
            row.addWidget(status_pill)
            row.addWidget(btn_update_engine)

            engines_layout.addLayout(row)

            # Divisor simples entre itens
            if eng != ENGINES_DATA[-1]:
                sep = QFrame()
                sep.setFrameShape(QFrame.HLine)
                sep.setStyleSheet("background-color: #1F1F23; border: none;")
                sep.setFixedHeight(1)
                engines_layout.addWidget(sep)

        content_layout.addWidget(engines_card)

        # --- PREFERÊNCIAS DE ATUALIZAÇÃO ---
        pref_title = QLabel("🎛️ Preferências de Atualização")
        pref_title.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #8E8E93; text-transform: uppercase;"
        )
        content_layout.addWidget(pref_title)

        pref_card = QFrame()
        pref_card.setStyleSheet("""
            QFrame {
                background-color: #121215;
                border: 1px solid #27272A;
                border-radius: 10px;
            }
        """)
        pref_layout = QVBoxLayout(pref_card)
        pref_layout.setContentsMargins(16, 16, 16, 16)
        pref_layout.setSpacing(12)

        chk_auto = QCheckBox(
            "Verificar atualizações automaticamente ao iniciar o sistema"
        )
        chk_auto.setChecked(True)
        chk_auto.setStyleSheet("font-size: 13px; color: #E4E4E7;")

        channel_layout = QHBoxLayout()
        channel_lbl = QLabel("Canal de Lançamento:")
        channel_lbl.setStyleSheet("font-size: 13px; color: #A1A1AA;")

        channel_combo = QComboBox()
        channel_combo.addItems(
            ["Estável (Recomendado)", "Beta / Preview (Recursos antecipados)"]
        )
        channel_combo.setStyleSheet("""
            QComboBox {
                background-color: #18181B;
                color: #FFFFFF;
                border: 1px solid #3F3F46;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
            }
        """)

        channel_layout.addWidget(channel_lbl)
        channel_layout.addWidget(channel_combo)
        channel_layout.addStretch()

        pref_layout.addWidget(chk_auto)
        pref_layout.addLayout(channel_layout)

        content_layout.addWidget(pref_card)

        # --- HISTÓRICO DE VERSÕES (CHANGELOG) ---
        changelog_title = QLabel("📜 Histórico de Atualizações (Changelog)")
        changelog_title.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #8E8E93; text-transform: uppercase;"
        )
        content_layout.addWidget(changelog_title)

        for item in CHANGELOG_DATA:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #121215;
                    border: 1px solid #27272A;
                    border-radius: 10px;
                }
            """)
            c_layout = QVBoxLayout(card)
            c_layout.setContentsMargins(16, 14, 16, 14)
            c_layout.setSpacing(8)

            head_row = QHBoxLayout()
            v_title = QLabel(item["version"])
            v_title.setStyleSheet(
                "font-size: 14px; font-weight: bold; color: #FFFFFF;"
            )

            v_date = QLabel(item["date"])
            v_date.setStyleSheet("font-size: 12px; color: #71717A;")

            head_row.addWidget(v_title)
            head_row.addWidget(v_date)
            head_row.addStretch()

            c_layout.addLayout(head_row)

            for change in item["changes"]:
                lbl_change = QLabel(change)
                lbl_change.setStyleSheet("font-size: 12px; color: #A1A1AA;")
                c_layout.addWidget(lbl_change)

            content_layout.addWidget(card)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

    def _simulate_check_updates(self):
        """Simulação visual de busca por atualizações."""
        self.btn_check_updates.setEnabled(False)
        self.btn_check_updates.setText("Buscando...")
        self.progress_bar.setValue(0)
        self.progress_bar.show()

        self.timer_val = 0

        def update_progress():
            self.timer_val += 20
            self.progress_bar.setValue(self.timer_val)
            if self.timer_val >= 100:
                self.timer.stop()
                self.progress_bar.hide()
                self.btn_check_updates.setEnabled(True)
                self.btn_check_updates.setText("🔍 Verificar Atualizações")
                self.lbl_status_msg.setText(
                    "● PRT NEXUS já está na versão mais recente disponível."
                )

        self.timer = QTimer(self)
        self.timer.timeout.connect(update_progress)
        self.timer.start(150)