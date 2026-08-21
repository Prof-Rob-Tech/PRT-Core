"""
===========================================================
PRT Labs - UI / Updates Page
Class: UpdatesPage
Description: Tela de Atualizações adaptativa a temas do PRT Nexus
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QCheckBox, QComboBox, QScrollArea
)


class BaseCard(QFrame):
    """Card container genérico adaptável aos temas Claro e Escuro."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("updateCard")
        self.setStyleSheet("""
            QFrame#updateCard {
                background-color: rgba(128, 128, 128, 0.05);
                border: 1px solid rgba(128, 128, 128, 0.18);
                border-radius: 8px;
                padding: 10px;
            }
        """)


class UpdatesPage(QWidget):
    """Página de Atualizações adaptativa aos temas do PRT Nexus."""

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setObjectName("updatesPage")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(14)

        # 1. Cabeçalho
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        title = QLabel("🔄 Central de Atualizações")
        title.setStyleSheet("font-size: 18px; font-weight: bold; border: none;")

        subtitle = QLabel("Mantenha o PRT NEXUS e seus motores de extração sempre atualizados para garantir compatibilidade.")
        subtitle.setStyleSheet("font-size: 12px; opacity: 0.65; border: none;")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)

        # 2. Card de Versão do App
        card_version = BaseCard()
        v_layout = QHBoxLayout(card_version)
        v_layout.setContentsMargins(12, 12, 12, 12)

        v_info = QVBoxLayout()
        v_info.setSpacing(4)
        lbl_app_ver = QLabel("PRT NEXUS v0.1.0-alpha")
        lbl_app_ver.setStyleSheet("font-size: 16px; font-weight: bold; border: none;")

        lbl_status = QLabel("🟢 O seu aplicativo está atualizado na versão mais recente.")
        lbl_status.setStyleSheet("font-size: 12px; color: #10B981; font-weight: 500; border: none;")

        v_info.addWidget(lbl_app_ver)
        v_info.addWidget(lbl_status)

        btn_check = QPushButton("🔍 Verificar Atualizações")
        btn_check.setFixedHeight(36)
        btn_check.setCursor(Qt.PointingHandCursor)
        btn_check.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: #FFFFFF;
                font-weight: 600;
                border-radius: 6px;
                padding: 0 16px;
                border: none;
            }
            QPushButton:hover { background-color: #1D4ED8; }
        """)

        v_layout.addLayout(v_info)
        v_layout.addStretch()
        v_layout.addWidget(btn_check)
        content_layout.addWidget(card_version)

        # 3. Motores & Componentes
        sec_engines = QLabel("⚙️ MOTORES & COMPONENTES DE DOWNLOAD")
        sec_engines.setStyleSheet("font-size: 11px; font-weight: bold; opacity: 0.65; border: none;")
        content_layout.addWidget(sec_engines)

        card_engines = BaseCard()
        eng_layout = QVBoxLayout(card_engines)
        eng_layout.setSpacing(10)

        engines = [
            ("Core Extractor (yt-dlp)", "Versão: 2026.08.01"),
            ("Media Converter (FFmpeg)", "Versão: n6.1.1"),
            ("Browser Engine (Chromium Core)", "Versão: v126.0"),
        ]

        for name, ver in engines:
            row = QHBoxLayout()
            lbl_n = QLabel(name)
            lbl_n.setStyleSheet("font-weight: bold; font-size: 13px; border: none;")
            lbl_v = QLabel(ver)
            lbl_v.setStyleSheet("font-size: 11px; opacity: 0.6; margin-left: 8px; border: none;")

            badge = QLabel("• Atualizado")
            badge.setStyleSheet("color: #10B981; font-weight: 600; font-size: 12px; border: none;")

            btn_update_eng = QPushButton("Atualizar Engine")
            btn_update_eng.setFixedHeight(28)
            btn_update_eng.setCursor(Qt.PointingHandCursor)
            btn_update_eng.setStyleSheet("""
                QPushButton {
                    background-color: rgba(128, 128, 128, 0.12);
                    border: 1px solid rgba(128, 128, 128, 0.25);
                    border-radius: 5px;
                    padding: 0 10px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: rgba(128, 128, 128, 0.22);
                }
            """)

            row.addWidget(lbl_n)
            row.addWidget(lbl_v)
            row.addStretch()
            row.addWidget(badge)
            row.addWidget(btn_update_eng)
            eng_layout.addLayout(row)

        content_layout.addWidget(card_engines)

        # 4. Preferências de Atualização
        sec_prefs = QLabel("⚙️ PREFERÊNCIAS DE ATUALIZAÇÃO")
        sec_prefs.setStyleSheet("font-size: 11px; font-weight: bold; opacity: 0.65; border: none;")
        content_layout.addWidget(sec_prefs)

        card_prefs = BaseCard()
        pref_layout = QVBoxLayout(card_prefs)
        pref_layout.setSpacing(10)

        chk_auto = QCheckBox("Verificar atualizações automaticamente ao iniciar o sistema")
        chk_auto.setChecked(True)
        chk_auto.setStyleSheet("font-size: 12px; border: none;")

        channel_box = QHBoxLayout()
        lbl_chan = QLabel("Canal de Lançamento:")
        lbl_chan.setStyleSheet("font-size: 12px; border: none;")

        combo_chan = QComboBox()
        combo_chan.setFixedHeight(30)
        combo_chan.addItems(["Estável (Recomendado)", "Beta", "Desenvolvedor (Nightly)"])
        combo_chan.setStyleSheet("""
            QComboBox {
                background-color: rgba(128, 128, 128, 0.08);
                border: 1px solid rgba(128, 128, 128, 0.25);
                border-radius: 5px;
                padding: 2px 8px;
            }
        """)

        channel_box.addWidget(lbl_chan)
        channel_box.addWidget(combo_chan)
        channel_box.addStretch()

        pref_layout.addWidget(chk_auto)
        pref_layout.addLayout(channel_box)
        content_layout.addWidget(card_prefs)

        # 5. Histórico (Changelog)
        sec_changelog = QLabel("📜 HISTÓRICO DE ATUALIZAÇÕES (CHANGELOG)")
        sec_changelog.setStyleSheet("font-size: 11px; font-weight: bold; opacity: 0.65; border: none;")
        content_layout.addWidget(sec_changelog)

        changelogs = [
            ("v0.1.0-alpha", "13/08/2026", [
                "✨ Lançamento da nova UI do Gerenciador de Plugins.",
                "🐛 Correção no fechamento para a bandeja do sistema (Tray Icon).",
                "🎨 Suporte a múltiplos temas (Dark, Light, Cyber).",
                "🌐 Conectores integrados para Kiwify, Hotmart, Vimeo e YouTube."
            ]),
            ("v0.0.9-alpha", "01/08/2026", [
                "🚀 Mapeamento e captura HLS para Panda Video.",
                "⚙️ Sistema de download em segundo plano reestruturado.",
                "🔒 Melhorias na validação de licenças."
            ])
        ]

        for ver, date_str, items in changelogs:
            card_log = BaseCard()
            log_layout = QVBoxLayout(card_log)
            log_layout.setSpacing(6)

            h_box = QHBoxLayout()
            lbl_ver = QLabel(ver)
            lbl_ver.setStyleSheet("font-weight: bold; font-size: 13px; border: none;")

            lbl_date = QLabel(date_str)
            lbl_date.setStyleSheet("font-size: 11px; opacity: 0.6; border: none;")

            h_box.addWidget(lbl_ver)
            h_box.addWidget(lbl_date)
            h_box.addStretch()

            log_layout.addLayout(h_box)

            for item in items:
                lbl_item = QLabel(item)
                lbl_item.setStyleSheet("font-size: 12px; opacity: 0.85; margin-left: 6px; border: none;")
                log_layout.addWidget(lbl_item)

            content_layout.addWidget(card_log)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)