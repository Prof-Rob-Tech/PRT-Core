"""
===========================================================
PRT Labs - UI / Settings Page
Class: SettingsPage
Description: Tela de Configurações adaptativa a temas do PRT Nexus
===========================================================
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QCheckBox, QScrollArea
)


class BaseCard(QFrame):
    """Card container adaptável aos temas Claro e Escuro."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsCard")
        self.setStyleSheet("""
            QFrame#settingsCard {
                background-color: rgba(128, 128, 128, 0.05);
                border: 1px solid rgba(128, 128, 128, 0.18);
                border-radius: 8px;
                padding: 12px;
            }
        """)


class SettingsPage(QWidget):
    """Página de Configurações do Sistema adaptativa aos temas do PRT Nexus."""

    theme_changed = Signal(str)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setObjectName("settingsPage")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(16)

        # 1. Cabeçalho
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        title = QLabel("⚙️ Configurações do Sistema")
        title.setStyleSheet("font-size: 18px; font-weight: bold; border: none;")

        header_layout.addWidget(title)
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

        # 2. Seção Aparência
        sec_appearance = QLabel("APARÊNCIA E PERSONALIZAÇÃO")
        sec_appearance.setStyleSheet("font-size: 11px; font-weight: bold; opacity: 0.85; border: none;")
        content_layout.addWidget(sec_appearance)

        card_theme = BaseCard()
        theme_layout = QHBoxLayout(card_theme)
        theme_layout.setSpacing(12)

        themes = [
            ("🍌 Tema Escuro\n(Slate Dark)", "dark"),
            ("☀️ Tema Claro\n(Clean White)", "light"),
            ("⚡ Nexus Cyber\n(Neon Vivid)", "cyber"),
        ]

        self.theme_btns = []
        for btn_text, theme_id in themes:
            btn = QPushButton(btn_text)
            btn.setFixedHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(128, 128, 128, 0.08);
                    border: 1px solid rgba(128, 128, 128, 0.25);
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QPushButton:hover {
                    border: 1px solid #2563EB;
                }
            """)
            theme_layout.addWidget(btn, 1)
            self.theme_btns.append((btn, theme_id))

        content_layout.addWidget(card_theme)

        # 3. Seção Comportamento
        sec_behavior = QLabel("COMPORTAMENTO DO APLICATIVO")
        sec_behavior.setStyleSheet("font-size: 11px; font-weight: bold; opacity: 0.85; border: none;")
        content_layout.addWidget(sec_behavior)

        card_behavior = BaseCard()
        beh_layout = QVBoxLayout(card_behavior)
        beh_layout.setSpacing(10)

        chk_style = "QCheckBox { font-size: 12px; font-weight: 500; border: none; gridline-color: transparent; }"

        chk_startup = QCheckBox("Iniciar junto com o Windows")
        chk_startup.setStyleSheet(chk_style)

        chk_tray = QCheckBox("Minimizar para a bandeja ao fechar (Tray Icon)")
        chk_tray.setChecked(True)
        chk_tray.setStyleSheet(chk_style)

        chk_notifications = QCheckBox("Exibir notificações do sistema")
        chk_notifications.setChecked(True)
        chk_notifications.setStyleSheet(chk_style)

        beh_layout.addWidget(chk_startup)
        beh_layout.addWidget(chk_tray)
        beh_layout.addWidget(chk_notifications)

        content_layout.addWidget(card_behavior)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)